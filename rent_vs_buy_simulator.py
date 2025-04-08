# rent_vs_buy_simulator.py
# Streamlit App: Rent vs. Buy Calculator (Canada)
# To run: streamlit run rent_vs_buy_simulator.py

import streamlit as st
import matplotlib.pyplot as plt

st.title("🏠 Rent vs. Buy Simulator (Canada)")
st.write("Compare your long-term net worth between renting and buying a home in Canada.")

# --- Sidebar: User Inputs ---
st.sidebar.header("Adjust Your Scenario")

home_price = st.sidebar.number_input("Home Price ($)", value=668000)
mortgage_rate = st.sidebar.slider("Mortgage Rate (%)", 0.5, 10.0, 5.5)
down_payment_percent = st.sidebar.slider("Down Payment (%)", 5, 50, 20)
years = st.sidebar.slider("Mortgage Term (Years)", 5, 40, 30)
home_appreciation = st.sidebar.slider("Home Appreciation (%/yr)", 0.0, 10.0, 2.5)

monthly_rent = st.sidebar.number_input("Monthly Rent ($)", value=2100)
rent_inflation = st.sidebar.slider("Rent Inflation (%/yr)", 0.0, 10.0, 4.0)
investment_return = st.sidebar.slider("Investment Return (%/yr)", 0.0, 15.0, 6.0)
property_tax = st.sidebar.slider("Property Tax (% of value)", 0.0, 3.0, 0.8)
maintenance_cost = st.sidebar.slider("Maintenance (% of value)", 0.0, 5.0, 1.5)

# --- Core Calculation ---
def simulate_rent_vs_buy():
    dp = home_price * down_payment_percent / 100
    loan = home_price - dp
    months = years * 12
    r_monthly = mortgage_rate / 100 / 12
    monthly_payment = loan * (r_monthly * (1 + r_monthly) ** months) / ((1 + r_monthly) ** months - 1)

    home_value = home_price
    rent = monthly_rent
    equity = dp
    savings = dp

    buy_net = []
    rent_net = []

    for _ in range(years):
        home_value *= 1 + home_appreciation / 100
        annual_payment = monthly_payment * 12
        annual_tax = home_value * property_tax / 100
        annual_maintenance = home_value * maintenance_cost / 100
        equity += annual_payment - (annual_tax + annual_maintenance)

        rent *= 1 + rent_inflation / 100
        annual_rent = rent * 12
        investable = annual_payment - annual_rent
        if investable > 0:
            savings *= 1 + investment_return / 100
            savings += investable
        else:
            savings *= 1 + investment_return / 100

        buy_net.append(equity + home_value)
        rent_net.append(savings)

    return buy_net, rent_net

# --- Run Simulation ---
buy_vals, rent_vals = simulate_rent_vs_buy()

# --- Plot Results ---
st.subheader("📈 Net Worth Over Time")
fig, ax = plt.subplots()
ax.plot(range(1, years + 1), buy_vals, label="Buying")
ax.plot(range(1, years + 1), rent_vals, label="Renting")
ax.set_xlabel("Years")
ax.set_ylabel("Net Worth ($)")
ax.set_title("Rent vs. Buy: Net Worth Projection")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# --- Summary ---
final_buy = buy_vals[-1]
final_rent = rent_vals[-1]

st.subheader("📊 Final Summary")
st.write(f"After {years} years:")
st.write(f"🏠 Buying Net Worth: ${final_buy:,.2f}")
st.write(f"🏡 Renting Net Worth: ${final_rent:,.2f}")

if final_buy > final_rent:
    st.success("Buying appears to result in a higher net worth over time.")
elif final_rent > final_buy:
    st.warning("Renting and investing the difference may be more profitable.")
else:
    st.info("Renting and buying result in similar financial outcomes.")
