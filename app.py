import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

from database import create_tables, add_default_admin, save_analysis, get_history
from detector import analyze_text
from login import login_page
from pdf_generator import generate_pdf
from articles import articles
from legal_resources import resources

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Discrimination Portal",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------------
# DATABASE SETUP
# -----------------------------------

create_tables()
add_default_admin()

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------------
# LOGIN PAGE
# -----------------------------------

if not st.session_state.logged_in:
    login_page()
    st.stop()

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🛡️ AI Portal")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Analysis History",
        "Articles",
        "Legal Resources"
    ]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# -----------------------------------
# DASHBOARD
# -----------------------------------

if menu == "Dashboard":

    st.title("🛡️ AI-Based Discrimination Detection Portal")

    current_time = datetime.now()

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"📅 Date : {current_time.strftime('%d-%m-%Y')}"
        )

    with col2:
        st.info(
            f"⏰ Time : {current_time.strftime('%H:%M:%S')}"
        )

    st.markdown("---")

    st.subheader("✍️ Text Analysis")

    user_text = st.text_area(
        "Enter Tamil or English Text",
        height=180
    )

    if st.button("🔍 Analyze Text"):

        if user_text.strip() == "":
            st.warning("Please enter text.")

        else:

            result = analyze_text(user_text)

            severity = result["severity"]

            st.subheader("📊 Analysis Result")

            if severity >= 75:
                st.error(result["result"])
            elif severity >= 40:
                st.warning(result["result"])
            else:
                st.success(result["result"])

            st.info(result["alert"])

            st.progress(severity)

            st.metric(
                "Severity Score",
                f"{severity}%"
            )

            st.write("### 🔑 Detected Keywords")

            if result["words"]:
                st.write(result["words"])
            else:
                st.write("No warning keywords detected.")

            st.write("### 😊 Sentiment Score")
            st.write(round(result["sentiment"], 2))

            save_analysis(
                user_text,
                result["result"],
                severity,
                str(datetime.now())
            )

            pdf_file = "report.pdf"

            generate_pdf(
                pdf_file,
                user_text,
                result["result"],
                severity
            )

            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=file,
                    file_name="report.pdf",
                    mime="application/pdf"
                )

# -----------------------------------
# ANALYSIS HISTORY
# -----------------------------------

elif menu == "Analysis History":

    st.title("📜 Analysis History")

    rows = get_history()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "ID",
                "Text",
                "Result",
                "Severity",
                "Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader("📊 Severity Distribution")

        fig = px.histogram(
            df,
            x="Severity",
            nbins=10,
            title="Severity Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        risk_counts = (
            df["Result"]
            .value_counts()
            .reset_index()
        )

        risk_counts.columns = [
            "Risk Level",
            "Count"
        ]

        pie_fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="Count",
            title="Risk Category Distribution"
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

    else:
        st.warning("No analysis history found.")

# -----------------------------------
# ARTICLES
# -----------------------------------

elif menu == "Articles":

    st.title("📚 Awareness Articles")

    for article in articles:
        with st.expander(article["title"]):
            st.write(article["content"])

# -----------------------------------
# LEGAL RESOURCES
# -----------------------------------

elif menu == "Legal Resources":

    st.title("⚖️ Legal Resources")

    st.info(
        "Resources provided for awareness and guidance."
    )

    st.subheader("📚 Awareness Resources")

    for item in resources:
        st.write("✅", item)

    st.markdown("---")

    st.subheader("🆘 Emergency Support")

    st.markdown("""
### 📞 Helplines

- Emergency Service : 112
- Police : 100
- Women Helpline : 181

### 📧 Support Email

support@aidiscriminationportal.com

### 🌐 Useful Resources

- https://www.india.gov.in
- https://cybercrime.gov.in
- https://nhrc.nic.in

### 📋 Recommended Actions

1. Save screenshots or evidence.
2. Report harmful content to moderators.
3. Contact authorities when required.
4. Seek support from trusted organizations.
""")

    st.markdown("---")

    st.subheader("📩 Report Concern")

    name = st.text_input("Your Name")

    issue = st.text_area(
        "Describe your concern"
    )

    if st.button("Submit Report"):

        if name and issue:
            st.success(
                "Report submitted successfully."
            )
        else:
            st.warning(
                "Please fill all fields."
            )