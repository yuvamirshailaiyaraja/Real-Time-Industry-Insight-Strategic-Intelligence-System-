import streamlit as st
import requests
import pandas as pd

# Page Config
st.set_page_config(page_title="Strategic Intelligence Dashboard", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>📊 Strategic Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Real-Time Market Monitoring & Decision Support System</h4>", unsafe_allow_html=True)

st.write("---")

# Sidebar
st.sidebar.header("⚙️ Controls")
industry = st.sidebar.selectbox("📌 Select Industry Sector", ["business", "technology", "health"])

# API KEY
API_KEY = "pub_e1d3576f63084cf7878c79bef3b7d555"

# Fetch News
url = f"https://newsapi.org/v2/top-headlines?category={industry}&language=en&apiKey={API_KEY}"

articles = []

try:
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])
except:
    st.warning("⚠️ Live data unavailable. Switching to demo dataset.")

# Backup Data
if not articles:
    articles = [
        {"title": "Global markets show strong growth and profit increase"},
        {"title": "Economic slowdown leads to decline in investments"},
        {"title": "Tech companies introduce innovative AI solutions"},
        {"title": "Startup ecosystem sees massive funding success"},
        {"title": "Healthcare sector faces operational challenges"}
    ]

# Sentiment Analysis
def analyze_sentiment(text):
    text = text.lower()
    if any(word in text for word in ["growth", "profit", "success", "increase"]):
        return "Positive"
    elif any(word in text for word in ["decline", "loss", "slowdown", "drop"]):
        return "Negative"
    return "Neutral"

# Strategy Generator
def generate_strategy(sentiment):
    if sentiment == "Positive":
        return "📈 Expansion Recommended"
    elif sentiment == "Negative":
        return "⚠️ Risk Mitigation Required"
    return "🔍 Monitor & Evaluate"

# Process Data
sentiment_count = {"Positive": 0, "Negative": 0, "Neutral": 0}
processed_data = []

for article in articles[:10]:
    title = article.get("title", "No Title")
    sentiment = analyze_sentiment(title)
    strategy = generate_strategy(sentiment)

    sentiment_count[sentiment] += 1

    processed_data.append({
        "Title": title,
        "Sentiment": sentiment,
        "Strategy": strategy
    })

df = pd.DataFrame(processed_data)

# KPI Section
st.subheader("📌 Key Market Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Signals", len(df))
col2.metric("Positive Signals", sentiment_count["Positive"])
col3.metric("Negative Signals", sentiment_count["Negative"])
col4.metric("Neutral Signals", sentiment_count["Neutral"])

st.write("---")

# Main Layout
col_left, col_right = st.columns([2, 1])

# Left: News Insights
with col_left:
    st.subheader("📰 Market Intelligence Feed")

    for _, row in df.iterrows():
        with st.container():
            st.markdown(f"### {row['Title']}")
            st.write(f"**Sentiment:** {row['Sentiment']}")
            st.write(f"**Strategic Insight:** {row['Strategy']}")
            st.write("---")

# Right: Charts & Insights
with col_right:
    st.subheader("📊 Sentiment Distribution")

    chart_df = pd.DataFrame(
        list(sentiment_count.items()),
        columns=["Sentiment", "Count"]
    )
    st.bar_chart(chart_df.set_index("Sentiment"))

    st.subheader("🤖 AI Strategic Summary")

    if sentiment_count["Positive"] > sentiment_count["Negative"]:
        st.success("Market momentum is strong. Expansion and investment opportunities are favorable.")
    elif sentiment_count["Negative"] > sentiment_count["Positive"]:
        st.error("Market shows instability. Focus on risk management and cost control.")
    else:
        st.info("Market is balanced. Strategic monitoring is recommended.")

# Footer
st.write("---")
st.caption("⚡ Powered by Real-Time Data Analytics | Strategic Intelligence System") 

#run cmd : python -m streamlit run app.py