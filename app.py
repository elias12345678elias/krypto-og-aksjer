{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import yfinance as yf\
import matplotlib.pyplot as plt\
import requests\
\
def get_fundamental_data(ticker):\
    # Sjekk om det er en krypto eller aksje\
    if ticker.isalpha() and not ticker.endswith(".OL") and len(ticker) <= 5:\
        ticker += ".OL"\
    \
    stock = yf.Ticker(ticker)\
    info = stock.info\
    \
    data = \{\
        "Selskap": info.get("longName", "N/A"),\
        "Markedsverdi": f"\{info.get('marketCap', 'N/A'):,\}" if info.get('marketCap') else "N/A",\
        "P/E-forhold": info.get("trailingPE", "N/A"),\
        "EPS (Inntjening per aksje)": info.get("trailingEps", "N/A"),\
        "Gjeldsgrad (Debt-to-Equity)": info.get("debtToEquity", "N/A"),\
        "ROE (Return on Equity)": info.get("returnOnEquity", "N/A"),\
        "Inntektsvekst": info.get("revenueGrowth", "N/A"),\
        "Utbytteavkastning": info.get("dividendYield", "N/A"),\
        "Beta (Volatilitet)": info.get("beta", "N/A"),\
    \}\
    return data, stock\
\
def get_crypto_data(ticker):\
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=\{ticker.lower()\}&vs_currencies=usd&include_market_cap=true&include_24hr_change=true"\
    response = requests.get(url)\
    if response.status_code == 200:\
        data = response.json().get(ticker.lower(), \{\})\
        return \{\
            "Pris (USD)": data.get("usd", "N/A"),\
            "Markedsverdi": data.get("usd_market_cap", "N/A"),\
            "24t endring (%)": data.get("usd_24h_change", "N/A"),\
        \}\
    return None\
\
def evaluate_stock(data):\
    pe = data.get("P/E-forhold")\
    roe = data.get("ROE (Return on Equity)")\
    debt = data.get("Gjeldsgrad (Debt-to-Equity)")\
    growth = data.get("Inntektsvekst")\
    dividend = data.get("Utbytteavkastning")\
    \
    rating = "N\'f8ytral"\
    \
    if pe != "N/A" and pe < 20 and roe != "N/A" and roe > 15 and debt != "N/A" and debt < 1.5:\
        rating = "Sterk Kj\'f8p"\
    elif pe != "N/A" and pe > 30:\
        rating = "Overpriset"\
    elif growth != "N/A" and growth < 0:\
        rating = "Risiko \'96 Inntektsnedgang"\
    elif dividend != "N/A" and dividend > 0.05:\
        rating = "Bra utbytteaksje"\
    \
    return rating\
\
def plot_stock_chart(stock):\
    hist = stock.history(period="6mo")\
    if hist.empty:\
        st.warning("Ingen prisdata tilgjengelig for denne aksjen.")\
        return\
    \
    fig, ax = plt.subplots()\
    ax.plot(hist.index, hist["Close"], label="Lukkekurs", color="blue")\
    ax.set_title("\uc0\u55357 \u56521  Aksjekurs siste 6 m\'e5neder")\
    ax.set_xlabel("Dato")\
    ax.set_ylabel("Pris")\
    ax.legend()\
    st.pyplot(fig)\
\
# Streamlit UI\
st.set_page_config(page_title="Fundamental Analyse", layout="centered")\
st.title("\uc0\u55357 \u56520  Fundamental og Krypto Analyse Bot")\
\
ticker = st.text_input("Skriv inn aksjesymbol eller kryptonavn (f.eks. AAPL for Apple, BTC for Bitcoin):")\
\
if ticker:\
    try:\
        if ticker.upper() in ["BTC", "ETH", "ADA", "XRP", "DOGE"]:  # Legg til flere kryptoer her\
            crypto_data = get_crypto_data(ticker.lower())\
            if crypto_data:\
                st.subheader("\uc0\u55357 \u56522  Analyse av kryptovaluta:")\
                st.json(crypto_data)\
            else:\
                st.error("Kunne ikke hente kryptodata.")\
        else:\
            data, stock = get_fundamental_data(ticker)\
            rating = evaluate_stock(data)\
            \
            st.subheader("\uc0\u55357 \u56522  Analyse av aksjen:")\
            st.json(data)\
            \
            st.subheader("\uc0\u55357 \u56520  Vurdering:")\
            st.success(f"Denne aksjen vurderes som: \{rating\}")\
            \
            st.subheader("\uc0\u55357 \u56521  Aksjekursutvikling:")\
            plot_stock_chart(stock)\
    except Exception as e:\
        st.error(f"Noe gikk galt: \{e\}")\
\
st.markdown("---")\
st.caption("Laget med \uc0\u10084 \u65039  av din personlige AI-assistent")\
\
}