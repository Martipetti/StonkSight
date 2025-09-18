import streamlit as st
import yfinance as yf
from models.lstm import Lstm

st.set_page_config(
    page_title='Stonk Sight'
)

if "data_frame" not in st.session_state:
    st.session_state.data_frame = None

if "my_instance" not in st.session_state:
    st.session_state.my_instance = Lstm()

def search(stock):
    if not stock:
        st.warning("Please enter a stock symbol.")
        return
    try:
        ticker = yf.Ticker(stock)
        st.session_state.data_frame = ticker.history(period="1y")[['Close']]
    except Exception as e:
        st.error("❌ Could not retrieve data. Please check the stock symbol and try again.")

st.title("📊 Stonk Sight")

col1, col2 = st.columns([4, 1])

with col1:
    stock = st.text_input(
        'Search your favorite stocks:',
        placeholder='Search for stocks...',
        max_chars=50,
        label_visibility="collapsed"
    )

with col2:
    st.button("🔍", on_click=search, args=(stock,))

if st.session_state.data_frame is not None:
    data = st.session_state.data_frame
    if data.empty:
        st.warning("No data found for the given stock symbol.")
    else:
        st.line_chart(data=data, use_container_width=True)
        if st.button('Predict', on_click=lambda: None):
            with st.spinner('Predicting...'):
                features, target = st.session_state.my_instance.preprocess(data)
                predictions, stats = st.session_state.my_instance.build_train_predict(features, target)
                st.subheader("Prediction Results")
                st.write("Predictions:")
                st.write(predictions)
                st.write("Statistics:")
                st.json(stats)
