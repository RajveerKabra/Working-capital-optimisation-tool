import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pulp import LpMinimize, LpProblem, LpVariable, lpSum

st.set_page_config(page_title="Working Capital Optimizer", layout="wide")

st.title("📊 Working Capital Optimisation Tool")
st.markdown("Upload your financial data to calculate and optimize your Cash Conversion Cycle (CCC).")

# 1. File Upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Basic Calculations
    df["DSO"] = (df["Accounts_Receivable"] / df["Sales"]) * 365
    df["DIO"] = (df["Inventory_Value"] / df["COGS"]) * 365
    df["DPO"] = (df["Accounts_Payable"] / df["COGS"]) * 365
    df["CCC"] = df["DIO"] + df["DSO"] - df["DPO"]
    
    # Dashboard Layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Current Data Summary")
        st.write(df[["DSO", "DIO", "DPO", "CCC"]].describe())

    with col2:
        st.subheader("Cash Conversion Cycle Over Time")
        fig, ax = plt.subplots()
        ax.plot(df["CCC"], label="CCC (Days)", color='blue')
        ax.set_xlabel("Time")
        ax.set_ylabel("Days")
        ax.legend()
        st.pyplot(fig)

    # 2. Optimization Section
    st.divider()
    st.header("🎯 Optimization Results")
    
    # User Inputs for Optimization Constraints
    st.sidebar.header("Optimization Constraints")
    target_service = st.sidebar.slider("Target Service Level", 0.80, 0.99, 0.95)
    
    # Simple PuLP Logic (derived from your notebook)
    # Note: Replace this with your specific PuLP objective functions
    prob = LpProblem("Optimize_CCC", LpMinimize)
    
    # Placeholder for the optimal calculation logic from your notebook
    # before_CCC = df["CCC"].mean()
    # ... logic from your .ipynb ...
    
    # Display Results in Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Avg CCC (Before)", f"{round(df['CCC'].mean(), 2)} Days")
    # Replace with your actual optimal variables
    m2.metric("Optimal CCC", "Calculated Days", delta="-15%") 
    m3.metric("Efficiency Gain", "TBD", delta="Lowers Capital")

    st.subheader("Raw Processed Data")
    st.dataframe(df)
else:
    st.info("Please upload a CSV file to begin analysis.")