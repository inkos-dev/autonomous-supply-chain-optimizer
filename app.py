import streamlit as st
import pandas as pd
import os
from crewai import Agent, Task, Crew, Process

st.set_page_config(page_title="INKOS | Supply Chain AI", page_icon="🏭", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; } 
    div[data-testid="stMetric"] { background-color: #1f2937; border: 1px solid #374151; padding: 15px; border-radius: 10px; }
    .stButton>button { 
        background-color: #00ffa2; 
        color: #000000; 
        border-radius: 8px; 
        border: none; 
        font-weight: bold; 
        width: 100%; 
        height: 50px; 
        font-size: 18px;
    }
    .agent-card { 
        background-color: #1f2937; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #00ffa2; 
        margin-bottom: 20px; 
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

if "GEMINI_API_KEY" not in os.environ and "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ API Key not found.")
    st.stop()

key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = key
os.environ["GEMINI_API_KEY"] = key

col_title, col_stats = st.columns([4, 2])
with col_title:
    st.title("🏭 Multi-Agent Supply Chain Optimizer")
    st.write("Autonomous AI workforce for real-time factory disruption resolution.")

with col_stats:
    m1, m2 = st.columns(2)
    m1.metric("Engine", "Gemini 2.5 Flash")
    m2.metric("Status", "Agentic Flow")

st.divider()

if 'df_bom' not in st.session_state: st.session_state.df_bom = None
if 'df_inventory' not in st.session_state: st.session_state.df_inventory = None
if 'df_suppliers' not in st.session_state: st.session_state.df_suppliers = None

st.sidebar.header("Data Ingestion")
data_mode = st.sidebar.radio("Select Data Source:", ["Use Demo Data", "Upload Custom CSVs"])

if data_mode == "Upload Custom CSVs":
    bom_file = st.sidebar.file_uploader("1. BOM", type=["csv"])
    inv_file = st.sidebar.file_uploader("2. Inventory", type=["csv"])
    sup_file = st.sidebar.file_uploader("3. Suppliers", type=["csv"])

    if bom_file and inv_file and sup_file:
        try:
            st.session_state.df_bom = pd.read_csv(bom_file)
            st.session_state.df_inventory = pd.read_csv(inv_file)
            st.session_state.df_suppliers = pd.read_csv(sup_file)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")
else:
    try:
        st.session_state.df_bom = pd.read_csv("bom.csv")
        st.session_state.df_inventory = pd.read_csv("inventory.csv")
        st.session_state.df_suppliers = pd.read_csv("suppliers.csv")
    except Exception:
        st.session_state.df_bom = None

if st.session_state.df_bom is not None:
    df_bom = st.session_state.df_bom
    df_inventory = st.session_state.df_inventory
    df_suppliers = st.session_state.df_suppliers

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.expander("📝 BOM", expanded=True):
            st.dataframe(df_bom, hide_index=True, width='stretch')
    with col2:
        with st.expander("📦 Inventory", expanded=True):
            st.dataframe(df_inventory, hide_index=True, width='stretch')
    with col3:
        with st.expander("🌍 Suppliers", expanded=True):
            st.dataframe(df_suppliers, hide_index=True, width='stretch')

    st.divider()

    if st.button("🚨 INITIALIZE AI TRIAGE PROTOCOL"):
        with st.status("🤖 Orchestrating Agents...", expanded=True) as status:
            bom_md = df_bom.to_markdown(index=False)
            inv_md = df_inventory.to_markdown(index=False)
            sup_md = df_suppliers.to_markdown(index=False)

            # Using the exact 2.5 Flash ID used in your other tools
            model_id = "gemini/gemini-2.5-flash"

            risk_analyst = Agent(
                role="Risk Analyst",
                goal="Identify part shortages and build capacity.",
                backstory="Veteran analyst. Expert at finding critical bottlenecks.",
                llm=model_id,
                allow_delegation=False
            )

            procurement_specialist = Agent(
                role="Procurement Specialist",
                goal="Find the best vendor to resolve shortages.",
                backstory="Shrewd negotiator focusing on speed and cost.",
                llm=model_id,
                allow_delegation=False
            )

            operations_director = Agent(
                role="Operations Director",
                goal="Make final executive decisions on the crisis.",
                backstory="Prioritizes assembly line uptime and ROI.",
                llm=model_id,
                allow_delegation=False
            )

            task_1 = Task(
                description=f"Analyze BOM and Inventory:\n{bom_md}\n{inv_md}\nIdentify build capacity.",
                expected_output="Shortage report.",
                agent=risk_analyst
            )

            task_2 = Task(
                description=f"Review Suppliers:\n{sup_md}\nSelect best vendor for shortages.",
                expected_output="Vendor recommendation.",
                agent=procurement_specialist
            )

            task_3 = Task(
                description="Summarize for CEO.",
                expected_output="3-bullet executive summary.",
                agent=operations_director
            )

            factory_crew = Crew(
                agents=[risk_analyst, procurement_specialist, operations_director],
                tasks=[task_1, task_2, task_3],
                process=Process.sequential,
                max_rpm=2  # CRITICAL: Keeps agents from hitting the rate limit immediately
            )

            final_result = factory_crew.kickoff()
            status.update(label="✅ Strategy Compiled", state="complete", expanded=False)

        st.markdown("## 📑 Resolution Strategy Logs")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="agent-card"><h3>🕵️‍♂️ Risk Analyst</h3>{task_1.output.raw}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="agent-card"><h3>🤝 Procurement</h3>{task_2.output.raw}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agent-card"><h3>👔 Executive Summary</h3>{task_3.output.raw}</div>', unsafe_allow_html=True)
        st.balloons()
else:
    st.info("👈 Please select a data source from the sidebar to begin.")
