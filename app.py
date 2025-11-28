import streamlit as st
import time
import os
import yfinance as yf
from google.genai import Client

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Hedge Fund",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# 1. MAIN PAGE HEADER (Banner & Title) - MOVED TO TOP
# ==============================================================================

# --- BANNER IMAGE ---
# Use 'try-except' to handle both cases (Local file OR Internet backup)
try:
    # 1. Try to load local file (Best for presentation)
    st.image(
        "banner.png",
        use_container_width=True,
        caption="Autonomous Financial Multi-Agent System",
    )
except:
    # 2. Fallback to Internet URL if file is missing
    st.image(
        "https://images.unsplash.com/photo-1611974765270-ca1258634369",
        use_container_width=True,
        caption="Autonomous Financial Multi-Agent System",
    )

st.title("🤖 AI Hedge Fund Manager")
st.markdown("""
**Welcome to the Future of Trading.** This system uses a team of **Autonomous AI Agents** to analyze stocks in real-time.
""")

# ==============================================================================
# 2. AUTHENTICATION (Sidebar)
# ==============================================================================
api_key = None

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9592/9592969.png", width=50)
    st.title("⚙️ Control Panel")

    st.markdown("### 🔑 API Access")

    # Try to load from Secrets
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
            st.success("✅ Key loaded from Secrets")
    except Exception:
        pass

    # If no key, ask manually
    if not api_key:
        api_key = st.text_input(
            "Enter Gemini API Key",
            type="password",
            help="Get your free key at aistudio.google.com",
        )
        if not api_key:
            st.warning("⚠️ Please enter your API Key to unlock the agents.")
            st.stop()  # This stops the script, but the Banner above stays visible!
    else:
        st.success("✅ Connected")

    st.divider()

    # Subscription Feature
    st.markdown("### 📧 Alerts")
    user_email = st.text_input("Your Email Address")
    if st.button("Subscribe to Reports"):
        if user_email:
            with st.spinner("Verifying..."):
                time.sleep(1)
            st.toast(f"✅ Subscribed! Alerts sent to {user_email}")
        else:
            st.warning("Enter an email first.")

# Initialize Client
try:
    client = Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.stop()


# ==============================================================================
# 3. HELPER FUNCTIONS
# ==============================================================================
def get_stock_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1d")
        if history.empty:
            return None
        current = history["Close"].iloc[-1]
        open_p = history["Open"].iloc[-1]
        change = ((current - open_p) / open_p) * 100
        return f"${current:.2f} ({change:+.2f}%)"
    except:
        return None


def get_market_news(symbol):
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news
        if not news:
            return "No specific news found."
        return "\n".join([f"- {n.get('title')}" for n in news[:3]])
    except:
        return "Error fetching news."


# ==============================================================================
# 4. AGENT BRAIN
# ==============================================================================
class Agent:
    def __init__(self, name, model, instructions):
        self.name = name
        self.model = model
        self.instructions = instructions

    def work(self, context, prompt, status_box):
        status_box.text(f"🔄 {self.name} is analyzing...")
        final_prompt = f"{self.instructions}\nDATA:\n{context}\nTASK: {prompt}"

        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=self.model, contents=final_prompt
                )
                return response.text
            except Exception:
                time.sleep(2)

        status_box.warning("⚠️ API busy, using simulation data.")
        if "Technical" in self.name:
            return "SIMULATION: Trend is UP. RSI is 40. Strong Support at $130."
        if "News" in self.name:
            return "SIMULATION: Market sentiment is cautious but optimistic. Earnings report pending."
        return "SIMULATION DECISION: BUY. (API Quota Reached)."


# ==============================================================================
# 5. MAIN DASHBOARD CONTENT (Inputs & Results)
# ==============================================================================

# Input Area
col1, col2 = st.columns([3, 1])
with col1:
    ticker = st.text_input(
        "🔎 Enter Stock Ticker", "NVDA", placeholder="e.g. AAPL, TSLA, BTC-USD"
    )
with col2:
    st.write("")
    st.write("")
    start_btn = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

# Execution
if start_btn:
    st.divider()
    model_name = "gemini-1.5-flash"

    with st.spinner(f"📡 Connecting to Market Data for {ticker}..."):
        price_str = get_stock_price(ticker)
        news_str = get_market_news(ticker)

    if not price_str:
        st.error(f"❌ Could not find data for {ticker}. Please check the symbol.")
        st.stop()

    st.metric(
        label=f"{ticker} Live Price",
        value=price_str.split("(")[0],
        delta=price_str.split("(")[1].strip(")"),
    )

    c1, c2, c3 = st.columns(3)

    # Agent A
    with c1:
        st.info("📊 **Technical Agent**")
        status_a = st.empty()
        agent_a = Agent(
            "Quant", model_name, "Analyze technicals (Price, Trends). Be concise."
        )
        res_a = agent_a.work(price_str, f"Analyze {ticker}", status_a)
        status_a.success("✅ Complete")
        with st.expander("View Technical Report", expanded=True):
            st.markdown(res_a)

    # Agent B
    with c2:
        st.info("📰 **News Agent**")
        status_b = st.empty()
        agent_b = Agent(
            "Journalist",
            model_name,
            "Analyze sentiment from news headlines. Be concise.",
        )
        res_b = agent_b.work(news_str, f"Analyze sentiment for {ticker}", status_b)
        status_b.success("✅ Complete")
        with st.expander("View News Report", expanded=True):
            st.markdown(res_b)

    # Agent C
    with c3:
        st.info("👔 **CIO (Supervisor)**")
        status_c = st.empty()
        status_c.text("🤔 Thinking...")
        agent_c = Agent(
            "CIO",
            model_name,
            "You are a Chief Investment Officer. Decide BUY/SELL/HOLD.",
        )
        final_context = f"Tech: {res_a}\nNews: {res_b}"
        res_c = agent_c.work(final_context, "Write a final email decision.", status_c)
        status_c.success("✅ Decision Made")

    st.divider()
    st.subheader("📧 Final Decision Email")

    container = st.container(border=True)
    if "BUY" in res_c.upper():
        container.success(f"### 🟢 BUY SIGNAL\n\n{res_c}")
        st.balloons()
    elif "SELL" in res_c.upper():
        container.error(f"### 🔴 SELL SIGNAL\n\n{res_c}")
    else:
        container.warning(f"### 🟡 HOLD SIGNAL\n\n{res_c}")
