import streamlit as st
import pandas as pd
import plotly.express as px

from predictor import predict_winner
from data_loader import load_experiment

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="A/B Test Outcome Predictor",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# Header
# ---------------------------------------------------

st.title("📊 A/B Test Outcome Predictor")
st.write(
    "Predict the winner of an A/B experiment using Bayesian Inference."
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.header("Experiment Settings")

experiment = st.sidebar.selectbox(
    "Select Experiment",
    list(range(1, 13))
)

percentage = st.sidebar.slider(
    "Percentage of Data Used",
    10,
    100,
    40,
    10
)

predict = st.sidebar.button("Predict Winner")

# ---------------------------------------------------
# Summary Cards
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Experiments", "12")

with col2:
    st.metric("Prediction Model", "Bayesian")

with col3:
    st.metric("Data Used", f"{percentage}%")

# ---------------------------------------------------
# Prediction Section
# ---------------------------------------------------

if predict:

    df = load_experiment(experiment)

    winner, probability = predict_winner(
        experiment,
        percentage / 100
    )

    group_A = df[df["group"] == "A"]
    group_B = df[df["group"] == "B"]

    rate_A = group_A["converted"].mean() * 100
    rate_B = group_B["converted"].mean() * 100

    conversions_A = int(group_A["converted"].sum())
    conversions_B = int(group_B["converted"].sum())

    st.success("Prediction Completed Successfully!")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Predicted Winner",
            winner
        )

    with c2:
        st.metric(
            "Probability (B > A)",
            f"{probability:.4f}"
        )

    if winner == "Undecided":
        st.warning("Recommendation: Collect More Data")
    else:
        st.success("Recommendation: Stop Experiment Early")

    # ---------------------------------------------
    # Conversion Metrics
    # ---------------------------------------------

    st.subheader("Conversion Rates")

    m1, m2 = st.columns(2)

    with m1:
        st.metric(
            "Group A",
            f"{rate_A:.2f}%"
        )

    with m2:
        st.metric(
            "Group B",
            f"{rate_B:.2f}%"
        )

    # ---------------------------------------------
    # Charts
    # ---------------------------------------------

    left, right = st.columns(2)

    with left:

        bar_df = pd.DataFrame({
            "Group": ["A", "B"],
            "Conversion Rate": [rate_A, rate_B]
        })

        fig1 = px.bar(
            bar_df,
            x="Group",
            y="Conversion Rate",
            text="Conversion Rate",
            title="Conversion Rate Comparison"
        )

        fig1.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with right:

        pie_df = pd.DataFrame({
            "Group": ["A", "B"],
            "Conversions": [conversions_A, conversions_B]
        })

        fig2 = px.pie(
            pie_df,
            names="Group",
            values="Conversions",
            title="Conversion Share"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # ---------------------------------------------
    # Dataset Preview
    # ---------------------------------------------

    st.subheader("Experiment Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    # ---------------------------------------------
    # Download CSV
    # ---------------------------------------------

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Download Experiment CSV",
        data=csv,
        file_name=f"experiment_{experiment}.csv",
        mime="text/csv"
    )