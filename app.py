import streamlit as st
from generative_model import perform_swot_analysis

#käynnistyy konsolista komennolla, riippuen tiedoston nimestä  "streamlit run app.py"



st.title("Financial report summarizer")
st.divider()
st.write("Enter your financial report in text")

report = st.text_input("Report:")

st.divider()

if report:
    st.balloons()
    analysis = perform_swot_analysis(report)
    st.write(f"Swot analysis of the report is {analysis}")
