import streamlit as st
import pandas as pd
import altair as alt

AUTOMATION_HOURS = 10
AUTOMATION_COST = 400

# Set page title
st.set_page_config(page_title="AI Automation Benefits", layout="wide")

tab1, tab2 = st.tabs(["Time and Cost Savings", "Developer Hours Adjustment"])
# Add sliders for user input
st.sidebar.header("Adjust Parameters")
base_hours = st.sidebar.slider(
    "**Hours of calls per month**", min_value=30, max_value=200, value=50, step=10
)
hourly_rate = st.sidebar.slider(
    "**Hourly rate (€)**", min_value=40, max_value=80, value=40, step=5
)

# Create data
months = list(range(1, 13))
time_data = pd.DataFrame(
    {
        "Month": months,
        "Without AI (hours)": [base_hours * m for m in months],
        "With AI (hours)": [AUTOMATION_HOURS * m for m in months],
    }
)

cost_data = pd.DataFrame(
    {
        "Month": months,
        "Without AI (€)": [base_hours * hourly_rate * m for m in months],
        "With AI (€)": [AUTOMATION_COST * m for m in months],  # Fixed this line
    }
)

# Melt the dataframes for Altair
time_data_melted = pd.melt(
    time_data, id_vars=["Month"], var_name="Scenario", value_name="Hours"
)
cost_data_melted = pd.melt(
    cost_data, id_vars=["Month"], var_name="Scenario", value_name="Cost"
)

# Create time chart
time_chart = (
    alt.Chart(time_data_melted)
    .mark_line(point=True)
    .encode(
        x=alt.X("Month:O", title="Month", sort=None),
        y=alt.Y(
            "Hours:Q",
            title="Cumulative Time (hours)",
            scale=alt.Scale(domain=[0, max(time_data_melted["Hours"]) * 1.1]),
        ),
        color=alt.Color(
            "Scenario:N",
            scale=alt.Scale(
                domain=["Without AI (hours)", "With AI (hours)"], range=["red", "green"]
            ),
        ),
        tooltip=["Month", "Scenario", "Hours"],
    )
    .properties(width=500, height=300, title="Cumulative Time Over 12 Months")
    .interactive()
)

# Create cost chart
cost_chart = (
    alt.Chart(cost_data_melted)
    .mark_line(point=True)
    .encode(
        x=alt.X("Month:O", title="Month", sort=None),
        y=alt.Y(
            "Cost:Q",
            title="Cumulative Cost (€)",
            scale=alt.Scale(domain=[0, max(cost_data_melted["Cost"]) * 1.1]),
        ),
        color=alt.Color(
            "Scenario:N",
            scale=alt.Scale(
                domain=["Without AI (€)", "With AI (€)"], range=["red", "green"]
            ),
        ),
        tooltip=["Month", "Scenario", "Cost"],
    )
    .properties(width=500, height=300, title="Cumulative Cost Over 12 Months")
    .interactive()
)

# Combine charts with annotations
final_time_chart = time_chart
final_cost_chart = cost_chart

dev_hourly_rate = 30
base_dev_hours = 53
base_monthly_fee = 2000
cost_range = list(range(1000, 2001, 100))  # From 1000 to 2000 in steps of 100

dev_hours_data = pd.DataFrame(
    {
        "Monthly Cost (€)": cost_range,
        "Developer Hours": [
            base_dev_hours - ((base_monthly_fee - cost) / dev_hourly_rate)
            for cost in cost_range
        ],
    }
)

# Create new developer hours chart
dev_hours_chart = (
    alt.Chart(dev_hours_data)
    .mark_line(point=True)
    .encode(
        x=alt.X("Monthly Cost (€):Q", title="Monthly Cost (€)"),
        y=alt.Y("Developer Hours:Q", title="Developer Hours per Month"),
        tooltip=["Monthly Cost (€)", "Developer Hours"],
    )
    .properties(width=600, height=400, title="Developer Hours vs Monthly Cost")
    .interactive()
)

with tab1:  # Time and Cost Savings
    # Streamlit app
    st.title("📞 Tanss 2 KI")

    st.write(
        f"""
    In dieser Ansicht vergleichen wir die Zeit- und Kostenersparnis, wenn die zweite Person, die bei den Anrufen zuhören muss, durch KI ersetzt wird.
    """
    )
    st.divider()
    # Display charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(final_time_chart, use_container_width=True)
    with col2:
        st.altair_chart(final_cost_chart, use_container_width=True)

    # Create tables for Time and Cost Savings
    time_savings_data = {
        "Scenario": ["Assistent", "Wartungstunden", "Ersparnis"],
        "Variables": [
            f"{base_hours} hours/month",
            f"{AUTOMATION_HOURS} hours/month",
            f"{base_hours - AUTOMATION_HOURS} hours/month",
        ],
        "Time (hours)": [
            base_hours * 12,
            AUTOMATION_HOURS * 12,
            (base_hours - AUTOMATION_HOURS) * 12,
        ],
    }
    time_savings_df = pd.DataFrame(time_savings_data)

    cost_savings_data = {
        "Scenario": ["Assistent", "Wartungstunden", "Ersparnis"],
        "Variables": [
            f"€{base_hours * hourly_rate}/month",
            f"€{AUTOMATION_COST}/month",
            f"€{(base_hours * hourly_rate) - AUTOMATION_COST}/month",
        ],
        "Cost (€)": [
            base_hours * hourly_rate * 12,
            AUTOMATION_COST * 12,
            (base_hours * hourly_rate * 12) - (AUTOMATION_COST * 12),
        ],
    }
    cost_savings_df = pd.DataFrame(cost_savings_data)

    # Display tables
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Time Savings")
        st.write("Anrufstunden über 12 Monate:")
        st.table(time_savings_df.style.format({"Time (hours)": "{:,.0f}"}))

    with col2:
        st.subheader("Cost Savings")
        st.write("Kostenüberschuss über 12 Monate:")
        st.table(cost_savings_df.style.format({"Cost (€)": "{:,.0f}"}))

with tab2:
    st.title("🧑‍💻 Developer Hours Adjustment")
    st.write("Use the slider to adjust the monthly fee reduction.")
    monthly_fee_reduction = tab2.slider(
        "**Monthly fee reduction (€)**", min_value=0, max_value=1000, value=0, step=100
    )
    current_fee_line = (
        alt.Chart(pd.DataFrame({"x": [base_monthly_fee - monthly_fee_reduction]}))
        .mark_rule(color="red", strokeDash=[12, 6])
        .encode(x="x:Q")
    )
    final_dev_hours_chart = dev_hours_chart + current_fee_line

    col1, col2 = st.columns([2, 1], gap="medium")

    # Create a DataFrame for the current adjustment
    with col1:
        current_adjustment_data = pd.DataFrame(
            {
                "Metric": [
                    "Monthly fee reduction",
                    "Current monthly fee",
                    "Available developer hours",
                ],
                "Value": [
                    f"€{monthly_fee_reduction}",
                    f"€{base_monthly_fee - monthly_fee_reduction}",
                    f"{base_dev_hours - (monthly_fee_reduction / dev_hourly_rate):.2f}",
                ],
            }
        )
        st.altair_chart(final_dev_hours_chart, use_container_width=True)
    with col2:
        st.subheader("Current Adjustment")
        st.table(current_adjustment_data.set_index("Metric"))
