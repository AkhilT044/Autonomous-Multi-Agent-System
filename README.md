
# 🤖 AI Hedge Fund Manager (Autonomous Multi-Agent System)

## 🛠️ Tools & Technologies Used



![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini%201.5%20Flash-8E75B2?logo=google&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code%20(Colab)-007ACC?logo=visual-studio-code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)

---

**A professional-grade Multi-Agent System that acts as an autonomous financial analyst.** This project orchestrates a team of AI Agents—a Technical Analyst, a News Journalist, and a Chief Investment Officer (Supervisor)—to analyze real-time stock market data and generate investment decisions.

## 🔴 LIVE DEMO
### 👉 [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://multi-agent-stock-analysis-system-ib22heed3d7ht3xdxsjwuz.streamlit.app/)
*(Note: The app supports BYOK (Bring Your Own Key) for security. If you don't have a key, it runs in Simulation Mode to demonstrate functionality.)*

### YouTube link of Project Explanation 👉 [![YouTube](https://img.shields.io/badge/YouTube-Project%20Explanation-red?logo=youtube)](https://www.youtube.com/watch?v=Wdd1GY8IwZU)

---

## 🧠 The Architecture (How it Works)

This system is not just a chatbot. It is an **Agentic Workflow** built on the **"Boardroom Pattern"**:

### 1. The Workforce (Specialist Agents)
Instead of one general AI doing everything, we split the logic into specialized roles to prevent hallucinations and increase accuracy.

* **📊 Agent A: The Quantitative Analyst ("The Quant")**
    * **Role:** Mathematics & Trends.
    * **Tools:** Fetches raw price data via `yfinance` (Open, Close, Moving Averages).
    * **Logic:** Analyzes volatility, percentage changes, and price momentum. It effectively ignores news to remain objective.
* **📰 Agent B: The Financial Journalist ("The Sentiment Scout")**
    * **Role:** Sentiment & Context.
    * **Tools:** Fetches live news headlines via `yfinance`.
    * **Logic:** Reads headlines to determine market mood (Fear vs. Greed). It effectively ignores charts to focus on the narrative.

### 2. The Supervisor (Decision Maker)
* **👔 Agent C: The Chief Investment Officer (CIO)**
    * **Role:** Synthesis & Final Decision.
    * **Mechanism:** Uses **A2A (Agent-to-Agent) Communication**. The CIO receives the conflicting reports from the Quant and the Journalist.
    * **Logic:** "If Technicals say BUY but News says PENDING LAWSUIT, override to HOLD." It applies high-level reasoning to resolve conflicts.

### 3. Fault Tolerance (Crash-Proofing)
* **Simulation Fallback:** If the Google Gemini API hits a rate limit (429 Error), the system automatically switches to a "Simulation Mode," generating mock data to ensure the application UI never crashes during a presentation.

---

## 🛠️ Tech Stack

* **Brain:** `google-genai` (Gemini 1.5 Flash) - Chosen for high speed and low latency.
* **Frontend:** `Streamlit` - For a responsive, interactive web dashboard.
* **Data Feed:** `yfinance` - Real-time stock market data and news.
* **Orchestration:** Custom Python Agent Classes (State Management & Retry Logic).
* **Notifications:** `smtplib` - Real-time email alert system using Gmail SMTP.

---

## 🛡️ Security & Reliability Features

We designed this agent with specific safeguards for competition environments and scalability.

### 1. The "Bring Your Own Key" (BYOK) Architecture
Instead of hardcoding our API credentials, the app requires users to input their own Google Gemini API Key.
* **Why?** To prevent quota exhaustion during public demos and ensure security best practices.
* **How:** The key is stored temporarily in the session state and is never saved to a database.

### 2. The "Simulation Mode" (Fault Tolerance)
We implemented a robust fallback mechanism to handle the Google Gemini Free Tier limits (`429 Too Many Requests`).
* **The Problem:** In a hackathon demo, if 10 judges click "Analyze" simultaneously, the API quota will crash the app.
* **Our Solution:** If the API fails, the agent automatically switches to **Simulation Mode**. It generates a pre-scripted "Mock Decision" to ensure the UI flow (Charts → Analysis → Email) completes successfully without an error screen.
* **User Feedback:** A warning banner `⚠️ API busy, using simulation data` appears so the user knows exactly what is happening.

### 3. The Email Alert System (Privacy-First)
The agent features a dual-mode notification system for "Buy/Sell" signals.
* **Mode A (Visual Simulation - Default):** Uses `st.toast` popup notifications to simulate an alert being sent.
    * *Reasoning:* To protect user privacy and avoid triggering Gmail's anti-spam blockers during repeated testing.
* **Mode B (Real SMTP - Configurable):** The backend supports full SMTP integration (`smtplib`).
    * *How to Enable:* Users can open the sidebar expander **"🔐 Email Config"** and enter their own Gmail App Password to enable real-world emailing. This proves the backend logic is fully functional while keeping the default experience safe.

---
## 🔮 Future Roadmap

We have architected this system to scale from a single-user demo to a production SaaS platform.

* [ ] **Automated Cron Jobs (The "Watchdog" Feature):**
    * *Current State:* User clicks to run.
    * *Future State:* Deploy via **GitHub Actions** or **AWS Lambda** to auto-run every morning at 9:00 AM EST. The agent will proactively email users *only* when a critical "Strong Buy/Sell" signal is detected.

* [ ] **Portfolio Memory (SQL Database):**
    * *Current State:* Stateless analysis.
    * *Future State:* Integrate **PostgreSQL (Supabase)** to store user portfolios. The agent will calculate actual P&L (Profit & Loss) and remember previous recommendations to track its own accuracy over time.

* [ ] **Multi-Ticker Analysis (S&P 500 Scanner):**
    * *Current State:* Analyzes one specific ticker deeply.
    * *Future State:* Implement **Python Asyncio** to scan 500+ tickers in parallel, filtering for high-RSI opportunities and presenting the "Top 3 Picks of the Day" automatically.



---

## 📂 Project Structure

```bash
AI-Hedge-Fund/
├── capstone.ipynb        # experimenting the process and logics before the main application
├── app.py                # The Main Application (Logic + UI)
├── requirements.txt      # Dependencies for Cloud Deployment
└── README.md             # Documentation

---

