import streamlit as st
import pandas as pd
import altair as alt

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


# Add information about AI saving an extra person
st.sidebar.markdown(
    "**Note:** <br> AI automation saves the need for an extra person.",
    unsafe_allow_html=True,
)

# Create data
months = list(range(1, 13))
time_data = pd.DataFrame(
    {
        "Month": months,
        "Without AI (hours)": [base_hours * 2 * m for m in months],
        "With AI (hours)": [base_hours * m for m in months],
    }
)

cost_data = pd.DataFrame(
    {
        "Month": months,
        "Without AI (€)": [base_hours * hourly_rate * 2 * m for m in months],
        "With AI (€)": [base_hours * hourly_rate * m for m in months],
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

cost_annotation = (
    alt.Chart(pd.DataFrame({"x": [6], "y": [max(cost_data_melted["Cost"]) * 0.9]}))
    .mark_text(
        text=f"Cost calculation: Hours x €{hourly_rate}/hour",
        align="left",
        baseline="middle",
        fontSize=12,
        color="black",
    )
    .encode(x="x:O", y="y:Q")
)

# Combine charts with annotations
final_time_chart = time_chart
final_cost_chart = cost_chart + cost_annotation

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
    These charts show the time and cost savings from using AI automation for call summarization over 12 months.
    """
    )
    # Display charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(final_time_chart, use_container_width=True)
    with col2:
        st.altair_chart(final_cost_chart, use_container_width=True)

    # Create tables for Time and Cost Savings
    time_savings_data = {
        "Scenario": ["Without AI", "With AI", "Total Savings"],
        "Variables": [f"{base_hours} hours", "10 hours", f"{base_hours - 10} hours"],
        "Time (hours)": [base_hours * 2 * 12, base_hours * 12, base_hours * 12],
    }
    time_savings_df = pd.DataFrame(time_savings_data)

    cost_savings_data = {
        "Scenario": ["Without AI", "With AI", "Total Savings"],
        "Variables": [
            f"€{hourly_rate}/hour",
            "€400/month",
            f"€{hourly_rate * base_hours - 400}/month",
        ],
        "Cost (€)": [
            base_hours * hourly_rate * 2 * 12,
            base_hours * hourly_rate * 12,
            base_hours * hourly_rate * 12,
        ],
    }
    cost_savings_df = pd.DataFrame(cost_savings_data)

    # Display tables
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Time Savings")
        st.write("Cumulative time over 12 months:")
        st.table(time_savings_df.style.format({"Time (hours)": "{:,.0f}"}))

    with col2:
        st.subheader("Cost Savings")
        st.write("Cumulative cost over 12 months:")
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
