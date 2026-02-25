import streamlit as st
import pandas as pd
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 1. PAGE SETUP & STYLE ---
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

# --- 2. SECRETS & AUTH ---
if "GEMINI_API_KEY" not in os.environ and "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ GEMINI_API_KEY not found. Please add it to the 'Advanced' secrets tab in Streamlit Cloud.")
    st.stop()

if "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# --- 3. HEADER SECTION ---
col_title, col_stats = st.columns([4, 2])
with col_title:
    st.title("🏭 Multi-Agent Supply Chain Optimizer")
    st.write("Autonomous AI workforce for real-time disruption resolution and procurement strategy.")

with col_stats:
    m1, m2 = st.columns(2)
    m1.metric("Engine", "CrewAI + Gemini")
    m2.metric("Status", "Agentic Flow")

st.divider()

# --- 4. DATA INGESTION ---
if 'df_bom' not in st.session_state: st.session_state.df_bom = None
if 'df_inventory' not in st.session_state: st.session_state.df_inventory = None
if 'df_suppliers' not in st.session_state: st.session_state.df_suppliers = None

st.sidebar.header("Data Ingestion")
data_mode = st.sidebar.radio("Select Data Source:", ["Use Demo Data", "Upload Custom CSVs"])

if data_mode == "Upload Custom CSVs":
    st.sidebar.markdown("### Upload your files:")
    bom_file = st.sidebar.file_uploader("1. Upload BOM (Bill of Materials)", type=["csv"])
    inv_file = st.sidebar.file_uploader("2. Upload Inventory", type=["csv"])
    sup_file = st.sidebar.file_uploader("3. Upload Suppliers", type=["csv"])

    if bom_file and inv_file and sup_file:
        try:
            st.session_state.df_bom = pd.read_csv(bom_file)
            st.session_state.df_inventory = pd.read_csv(inv_file)
            st.session_state.df_suppliers = pd.read_csv(sup_file)
            st.sidebar.success("All custom data loaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error reading custom files: {e}")
    else:
        st.sidebar.warning("Please upload all 3 CSV files to proceed.")
        st.session_state.df_bom = None
        st.session_state.df_inventory = None
        st.session_state.df_suppliers = None
else:
    try:
        st.session_state.df_bom = pd.read_csv("bom.csv")
        st.session_state.df_inventory = pd.read_csv("inventory.csv")
        st.session_state.df_suppliers = pd.read_csv("suppliers.csv")
        st.sidebar.success("Demo data loaded!")
    except Exception as e:
        st.sidebar.error(f"Error loading demo files: {e}. Ensure bom.csv, inventory.csv, and suppliers.csv exist.")
        st.session_state.df_bom = None

# --- 5. DATA DISPLAY & EXECUTION ---
if st.session_state.df_bom is not None:
    
    df_bom = st.session_state.df_bom
    df_inventory = st.session_state.df_inventory
    df_suppliers = st.session_state.df_suppliers

    st.subheader("📊 Real-Time Factory Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.expander("📝 Bill of Materials (BOM)", expanded=True):
            st.dataframe(df_bom, hide_index=True, use_container_width=True)
    with col2:
        with st.expander("📦 Warehouse Inventory", expanded=True):
            st.dataframe(df_inventory, hide_index=True, use_container_width=True)
    with col3:
        with st.expander("🌍 Supplier Network", expanded=True):
            st.dataframe(df_suppliers, hide_index=True, use_container_width=True)

    st.divider()

    if st.button("🚨 INITIALIZE AI TRIAGE PROTOCOL"):
        
        with st.status("🤖 Orchestrating AI Agent Team...", expanded=True) as status:
            
            # Use Langchain wrapper to explicitly route to 1.5-flash and avoid the 404 SDK error
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
            
            bom_md = df_bom.to_markdown(index=False)
            inv_md = df_inventory.to_markdown(index=False)
            sup_md = df_suppliers.to_markdown(index=False)
            
            st.write("🕵️‍♂️ risk_analyst.join_session()")
            risk_analyst = Agent(
                role="Supply Chain Risk Analyst",
                goal="Identify immediate inventory shortages and production risks.",
                backstory="You are a veteran supply chain analyst at a heavy-duty pump manufacturing plant. You excel at finding critical bottlenecks.",
                llm=llm
            )

            st.write("🤝 procurement_specialist.join_session()")
            procurement_specialist = Agent(
                role="Procurement Specialist",
                goal="Find the most cost-effective and timely supplier for critically low parts.",
                backstory="You are a shrewd negotiator. You scan the supplier network to find the best balance of speed and cost.",
                llm=llm
            )

            st.write("👔 operations_director.join_session()")
            operations_director = Agent(
                role="Operations Director",
                goal="Review supply chain crises and make final executive decisions.",
                backstory="You prioritize keeping the assembly line moving and maximizing ROI.",
                llm=llm
            )

            task_1 = Task(
                description=f"Analyze BOM:\n{bom_md}\nand Inventory:\n{inv_md}\nIdentify the part shortage and calculate build capacity for 'Centrifugal Pump'.",
                expected_output="A report identifying the specific part shortage and the exact number of final products that can be built.",
                agent=risk_analyst
            )

            task_2 = Task(
                description=f"Based on the Analyst's report, look at the Supplier Database:\n{sup_md}\nRecommend the best vendor to resolve this specific crisis immediately.",
                expected_output="A comparison of the available suppliers for the missing part with a firm recommendation.",
                agent=procurement_specialist
            )

            task_3 = Task(
                description="Summarize the findings for the CEO. Highlight the Crisis, the Chosen Solution, and the Financial/Time Impact.",
                expected_output="A concise 3-bullet-point executive summary.",
                agent=operations_director
            )

            factory_crew = Crew(
                agents=[risk_analyst, procurement_specialist, operations_director],
                tasks=[task_1, task_2, task_3],
                process=Process.sequential
            )

            st.write("🚀 Running Multi-Agent Reasoning Pipeline...")
            final_result = factory_crew.kickoff()
            status.update(label="✅ Crisis Resolution Complete", state="complete", expanded=False)

        # --- 6. AGENT REPORT CARDS ---
        st.markdown("## 📑 Resolution Strategy Logs")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="agent-card">
                <h3 style="color: #00ffa2; margin-top:0;">🕵️‍♂️ Risk Analyst</h3>
                {task_1.output.raw}
            </div>""", unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""<div class="agent-card">
                <h3 style="color: #00ffa2; margin-top:0;">🤝 Procurement Spec</h3>
                {task_2.output.raw}
            </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div class="agent-card">
            <h3 style="color: #00ffa2; margin-top:0;">👔 Operations Director Summary</h3>
            {task_3.output.raw}
        </div>""", unsafe_allow_html=True)

        st.balloons()
else:
    st.info("👈 Please select a data source from the sidebar to begin.")
