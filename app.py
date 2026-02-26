import streamlit as st
import pandas as pd
import os
import time
from crewai import Agent, Task, Crew, Process

st.set_page_config(page_title="INKOS | Supply Chain AI", page_icon="🏭", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; } 
    div[data-testid="stMetric"] { background-color: #1f2937; border: 1px solid #374151; padding: 15px; border-radius: 10px; }
    
    /* Pulse Animation for Metrics */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 162, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 162, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 162, 0); }
    }
    .status-active { border: 2px solid #00ffa2; animation: pulse 2s infinite; }

    .stButton>button { 
        background-color: #00ffa2; 
        color: #000000; 
        border-radius: 8px; 
        border: none; 
        font-weight: bold; 
        width: 100%; 
        height: 50px; 
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00d688;
        box-shadow: 0px 0px 15px #00ffa2;
        transform: translateY(-2px);
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

if 'df_bom' not in st.session_state: st.session_state.df_bom = None
if 'df_inventory' not in st.session_state: st.session_state.df_inventory = None
if 'df_suppliers' not in st.session_state: st.session_state.df_suppliers = None

with st.sidebar:
    st.title("🛰️ System Control")
    
    if st.session_state.df_bom is not None:
        st.success("SIMULATION READY")
        st.info(f"Loaded: {len(st.session_state.df_bom)} Bill of Material Items")
    else:
        st.warning("SYSTEM OFFLINE: Load Data")
        
    st.divider()
    data_mode = st.radio("Select Environment Source:", ["Use Demo Data", "Upload Custom CSVs"])

    if data_mode == "Upload Custom CSVs":
        bom_file = st.sidebar.file_uploader("1. BOM", type=["csv"])
        inv_file = st.sidebar.file_uploader("2. Inventory", type=["csv"])
        sup_file = st.sidebar.file_uploader("3. Suppliers", type=["csv"])

        if bom_file and inv_file and sup_file:
            st.session_state.df_bom = pd.read_csv(bom_file)
            st.session_state.df_inventory = pd.read_csv(inv_file)
            st.session_state.df_suppliers = pd.read_csv(sup_file)
            st.rerun()
    else:
        if st.button("Initialize Synthetic Environment"):
            try:
                st.session_state.df_bom = pd.read_csv("bom.csv")
                st.session_state.df_inventory = pd.read_csv("inventory.csv")
                st.session_state.df_suppliers = pd.read_csv("suppliers.csv")
                st.rerun()
            except:
                st.error("Missing demo CSV files in root directory.")

col_title, col_stats = st.columns([4, 2])
with col_title:
    st.title("🏭 Multi-Agent Supply Chain Optimizer")
    st.write("Autonomous AI workforce for real-time factory disruption resolution.")

with col_stats:
    m1, m2 = st.columns(2)
    m1.metric("Engine", "Gemini 2.5 Flash")
    m2.metric("Status", "Standby" if st.session_state.df_bom is None else "Active")

st.divider()

if st.session_state.df_bom is None:
    st.markdown("""
        <div style="text-align: center; padding: 50px; border: 2px dashed #374151; border-radius: 15px;">
            <h2 style="color: #6b7280;">Awaiting Data Ingestion...</h2>
            <p style="color: #4b5563;">Use the sidebar to load the factory environment.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

df_bom = st.session_state.df_bom
df_inventory = st.session_state.df_inventory
df_suppliers = st.session_state.df_suppliers

st.subheader("📊 Real-Time Simulation Feed")
col1, col2, col3 = st.columns(3)
with col1:
    with st.expander("📝 Bill of Materials", expanded=True):
        st.dataframe(df_bom, hide_index=True, width='stretch')
with col2:
    with st.expander("📦 Inventory Stock", expanded=True):
        st.dataframe(df_inventory, hide_index=True, width='stretch')
with col3:
    with st.expander("🌍 Global Suppliers", expanded=True):
        st.dataframe(df_suppliers, hide_index=True, width='stretch')

st.divider()

if st.button("🚨 INITIALIZE AI TRIAGE PROTOCOL"):
    with st.status("🤖 Orchestrating AI Agent Team...", expanded=True) as status:
        
        bom_md = df_bom.to_markdown(index=False)
        inv_md = df_inventory.to_markdown(index=False)
        sup_md = df_suppliers.to_markdown(index=False)
        
        st.write("🕵️‍♂️ **Analyst joining session...**")
        risk_analyst = Agent(
            role="Risk Analyst",
            goal="Identify part shortages and calculate build capacity.",
            backstory="Veteran analyst. Expert at finding bottlenecks.",
            llm="gemini/gemini-2.5-flash",
            allow_delegation=False
        )

        st.write("🤝 **Specialist joining session...**")
        procurement_specialist = Agent(
            role="Procurement Specialist",
            goal="Find the best vendor to resolve shortages.",
            backstory="Shrewd negotiator focusing on speed and cost.",
            llm="gemini/gemini-2.5-flash",
            allow_delegation=False
        )

        st.write("👔 **Operations Director joining session...**")
        operations_director = Agent(
            role="Operations Director",
            goal="Review findings and issue final executive strategy.",
            backstory="Prioritizes assembly line uptime and ROI.",
            llm="gemini/gemini-2.5-flash",
            allow_delegation=False
        )

        task_1 = Task(
            description=f"Analyze data:\nBOM:\n{bom_md}\nInventory:\n{inv_md}\nIdentify the specific part shortage.",
            expected_output="A report identifying the specific part shortage.",
            agent=risk_analyst
        )

        task_2 = Task(
            description=f"Using the shortage report and supplier data:\n{sup_md}\nPick the best vendor.",
            expected_output="A vendor recommendation.",
            agent=procurement_specialist
        )

        task_3 = Task(
            description="Summarize the crisis and solution in 3 bold bullet points for the CEO.",
            expected_output="A concise executive summary.",
            agent=operations_director
        )

        factory_crew = Crew(
            agents=[risk_analyst, procurement_specialist, operations_director],
            tasks=[task_1, task_2, task_3],
            process=Process.sequential,
            max_rpm=2
        )

        st.write("🚀 **Executing Multi-Agent Reasoning Pipeline...**")
        final_result = factory_crew.kickoff()
        status.update(label="✅ Crisis Resolution Complete", state="complete", expanded=False)

    st.markdown("## 📑 Resolution Strategy Logs")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="agent-card"><h3>🕵️‍♂️ Risk Analyst</h3>{task_1.output.raw}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="agent-card"><h3>🤝 Procurement</h3>{task_2.output.raw}</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="agent-card"><h3>👔 Executive Strategy Summary</h3>{task_3.output.raw}</div>', unsafe_allow_html=True)
    st.balloons()
