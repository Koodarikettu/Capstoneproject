import streamlit as st
from generative_model import perform_swot_analysis


#käynnistyy konsolista komennolla, riippuen tiedoston nimestä  "streamlit run app.py"
st.title("Financial report summarizer")

with st.form("my_form"):
    st.subheader("Upload a financial report in pdf or text")
    col1, col2 = st.columns(2)
    with col1:
        pdf_report = st.file_uploader("Upload a financial report", type=("pdf"))
    with col2:
        report = st.text_input("Enter financial report in text:")

    st.subheader("Selecet the type of summarization")
    
    summarization_type = st.selectbox("Select the type of summarization", ["SWOT", "PESTEL"])

    submitted = st.form_submit_button("Submit")


def swot_analysis(data):
    st.title("SWOT-analysis")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Strenghts (S)")
        for item in data.strengths:
            st.write(f"- {item}")

        st.subheader("Opportunities (O)")
        for item in data.opportunities:
            st.write(f"- {item}")

    with col4:
        st.subheader("Weaknesses (W)")
        for item in data.weaknesses:
            st.write(f"- {item}")

        st.subheader("Threats (T)")
        for item in data.threats:
            st.write(f"- {item}")
    return


def pestel_analysis(data):
    st.title("SWOT-analysis")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Strenghts (S)")
        for item in data.strengths:
            st.write(f"- {item}")

        st.subheader("Opportunities (O)")
        for item in data.opportunities:
            st.write(f"- {item}")

    with col4:
        st.subheader("Weaknesses (W)")
        for item in data.weaknesses:
            st.write(f"- {item}")

        st.subheader("Threats (T)")
        for item in data.threats:
            st.write(f"- {item}")
    return


if pdf_report or report:
    if pdf_report:
        report = pdf_report
    st.balloons()
    analysis = perform_swot_analysis(report)
    swot_analysis(analysis)

