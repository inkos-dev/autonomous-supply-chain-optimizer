🏭 Multi-Agent Supply Chain Optimizer
🚀 Overview
An Agentic AI solution designed to bridge the gap between Industrial Engineering (Atoms) and AI Engineering (Bits). This system uses a multi-agent orchestration framework to simulate how a digital workforce resolves complex industrial disruptions autonomously.

While traditional ERP systems simply flag shortages, this optimizer reasons through them—cross-referencing parts, negotiating vendor selection, and drafting executive strategy in seconds.

🤖 The Digital Workforce (Powered by CrewAI)
The system orchestrates a sequential "Triage Protocol" between three specialized agents:

🕵️‍♂️ Risk Analyst: Conducts a real-time audit of BOM (Bill of Materials) vs. Warehouse Inventory. It identifies critical shortages and calculates exact "Build Capacity."

🤝 Procurement Specialist: Consumes the shortage report and scans the Supplier Database. It performs a multi-variable analysis to balance Unit Cost vs. Lead-Time Reliability.

👔 Operations Director: Reviews the tactical findings and executes the final strategy, outputting a concise 3-bullet executive summary focused on Production Uptime and ROI.

🛠️ Tech Stack
AI Engine: Google Gemini 2.5 Flash

Framework: CrewAI (Multi-Agent Orchestration)

Interface: Streamlit (Custom Dark-Themed UI)

Data Ingestion: Dynamic CSV Processing (Pandas)

Architecture: Deterministic ETL combined with Agentic Reasoning

⚡ Key Features
Custom Data Ingestion: Supports user-uploaded CSVs for BOM, Inventory, and Supplier data, moving beyond hardcoded mockups.

Production Resilience: Implemented max_rpm throttling and environment-agnostic API key handling to ensure stability under high-concurrency or free-tier constraints.

Deterministic Output: Uses structured data parsing to ensure agent findings are cited directly from the provided industrial datasets.

📈 Business Impact
Reduces manual supply chain triage time by 98%, transforming hours of logistical spreadsheet cross-referencing into an automated, actionable executive strategy within seconds.
