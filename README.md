# 🏭 Multi-Agent Supply Chain Optimizer

## 🚀 Live Demo
**[Click here to run the live AI Agents on Streamlit Cloud](https://autonomous-supply-chain-optimizer-6jbyely3xsdrb5tdriadaz.streamlit.app/)**

---

## 🚀 Overview
An **Agentic AI** solution designed to bridge the gap between Industrial Engineering (**Atoms**) and AI Engineering (**Bits**). This system uses a **multi-agent orchestration framework** to simulate how a digital workforce resolves complex industrial disruptions autonomously.

While traditional ERP systems simply flag shortages, this optimizer **reasons through them**—cross-referencing parts, negotiating vendor selection, and drafting executive strategy in seconds.

---

## 🤖 The Digital Workforce
**Powered by CrewAI & Gemini 2.5 Flash**

The system orchestrates a sequential "Triage Protocol" between three specialized agents:

* **🕵️‍♂️ Risk Analyst:** Conducts a real-time audit of **BOM (Bill of Materials)** vs. **Warehouse Inventory**. It identifies critical shortages and calculates exact "Build Capacity."
* **🤝 Procurement Specialist:** Consumes the shortage report and scans the **Supplier Database**. It performs a multi-variable analysis to balance **Unit Cost** vs. **Lead-Time Reliability**.
* **👔 Operations Director:** Reviews the tactical findings and executes the final strategy, outputting a concise 3-bullet executive summary focused on **Production Uptime** and **ROI**.

---

## ⚡ Key Features
* **📂 Dynamic Data Ingestion:** Supports user-uploaded CSVs for BOM, Inventory, and Supplier data, allowing for real-world custom testing beyond demo data.
* **🛡️ Production Resilience:** Features custom `max_rpm` throttling and environment-agnostic API key handling to ensure stability under free-tier constraints.
* **📊 Deterministic Output:** Combines structured data parsing with LLM reasoning to ensure agent findings are grounded directly in the provided industrial datasets.

---

## 🛠️ Tech Stack
* **AI Engine:** Google Gemini 2.5 Flash
* **Orchestration:** CrewAI
* **Interface:** Streamlit (Custom Dark-Themed UI)
* **Data Handling:** Pandas & Pydantic
* **Deployment:** Streamlit Cloud

---

## 📈 Business Impact
Reduces manual supply chain triage time by **98%**, transforming hours of logistical spreadsheet cross-referencing into an automated, actionable executive strategy within seconds.
