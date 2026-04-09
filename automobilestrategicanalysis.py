#run cmd: python -m streamlit run "infosys strategic analysis.py" 
import streamlit as st
import pandas as pd
import yfinance as yf
import requests
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Strategic Intelligence Dashboard", layout="wide")

st.markdown("<h1 style='text-align:center;'>🚗 Strategic Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### Real-Time Automobile Industry Analysis & Decision Support")

# ---------------- COMPANY DATA ----------------
companies = {
    "Tesla": "TSLA",
    "Mercedes": "MBG.DE",
    "Ferrari": "RACE",
    "Porsche": "P911.DE",
    "BMW": "BMW.DE"
}

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")
company_name = st.sidebar.selectbox("Select Company", list(companies.keys()))
ticker = companies[company_name]

# ---------------- STOCK DATA ----------------
data = yf.download(ticker, period="6mo")

latest_price = round(data["Close"].iloc[-1], 2)
prev_price = round(data["Close"].iloc[-2], 2)
change = round(latest_price - prev_price, 2)

# ---------------- KPI DASHBOARD ----------------
col1, col2, col3 = st.columns(3)
col1.metric("Company", company_name)
col2.metric("Stock Price", f"${latest_price}")
col3.metric("Daily Change", f"{change}")

# ---------------- STOCK CHART ----------------
st.subheader("📈 Stock Price Trend")
st.line_chart(data["Close"])

# ---------------- SIMPLE SENTIMENT FUNCTION ----------------
def analyze_sentiment(text):
    text = text.lower()
    if any(word in text for word in ["growth", "profit", "record", "increase", "success"]):
        return "Positive"
    elif any(word in text for word in ["loss", "decline", "drop", "fall", "crisis"]):
        return "Negative"
    else:
        return "Neutral"

# ---------------- NEWS API ----------------
st.subheader("📰 Industry News & Sentiment")

API_KEY = "9c99c15f-233a-4e84-88a6-226c2ad7e5d6"   

url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={API_KEY}"

response = requests.get(url)
data_news = response.json()

articles = data_news.get("articles", [])[:5]

positive = 0
negative = 0
neutral = 0

for article in articles:
    title = article.get("title", "No Title")
    sentiment = analyze_sentiment(title)

    if sentiment == "Positive":
        positive += 1
    elif sentiment == "Negative":
        negative += 1
    else:
        neutral += 1

    st.markdown(f"### 📰 {title}")
    st.write(f"**Sentiment:** {sentiment}")
    st.write("---")

# ---------------- SENTIMENT CHART ----------------
st.subheader("📊 Sentiment Overview")

df_sent = pd.DataFrame({
    "Sentiment": ["Positive", "Negative", "Neutral"],
    "Count": [positive, negative, neutral]
})

st.bar_chart(df_sent.set_index("Sentiment"))

# ---------------- CUSTOMER INSIGHTS ----------------
st.subheader("😊 Customer Satisfaction Trend")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
values = [random.randint(60, 90) for _ in range(6)]

df_growth = pd.DataFrame({
    "Month": months,
    "Customer Index": values
})

st.line_chart(df_growth.set_index("Month"))

# ---------------- COMPANY COMPARISON ----------------
st.subheader("🏆 Company Comparison (Avg Stock Price)")

comparison = {}

for name, tick in companies.items():
    temp = yf.download(tick, period="1mo")
    comparison[name] = temp["Close"].mean()

df_compare = pd.DataFrame(list(comparison.items()), columns=["Company", "Avg Price"])
st.bar_chart(df_compare.set_index("Company"))

# ---------------- AI STRATEGY ----------------
st.subheader("🤖 Strategic Insight")

if positive > negative:
    st.success(f"{company_name} shows strong positive sentiment. Recommended: Expansion & Investment.")
elif negative > positive:
    st.error(f"{company_name} shows negative sentiment. Recommended: Risk Control & Improvement.")
else:
    st.info(f"{company_name} is stable. Monitor market trends.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("💡 Antigravity Approach: Dynamic real-time intelligence replacing traditional static analysis.")