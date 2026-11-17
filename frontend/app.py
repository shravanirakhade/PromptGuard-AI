"""
PromptGuard AI - Advanced Dashboard
"""

import streamlit as st
import requests
import csv
import io

API_URL = "http://127.0.0.1:8000"


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="PromptGuard AI",
    page_icon="🛡️",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #172554;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
}

div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🛡️ PromptGuard AI")

    st.caption("AI Prompt Testing Platform")

    st.divider()

    page = st.radio(
        "Navigation",
        ["Dashboard", "Testing History", "About Project"]
    )

    st.divider()

    st.info(
        "Test prompts, evaluate responses, "
        "and monitor prompt quality."
    )


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">PromptGuard AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Intelligent AI Prompt Testing & Evaluation Platform'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.header("🚀 Test Your Prompt")

    prompt = st.text_area(
        "Enter your prompt",
        placeholder="Example: Explain Machine Learning with examples...",
        height=150
    )

    keywords = st.text_input(
        "Expected keywords",
        placeholder="Machine Learning, AI, Data"
    )

    # ---------------- PROMPT QUALITY ANALYSIS ----------------

    if st.button(
        "🔍 Analyze Prompt Quality",
        use_container_width=True
    ):

        if not prompt.strip():

            st.warning("Please enter a prompt.")

        else:

            try:

                with st.spinner("Analyzing prompt quality..."):

                    response = requests.post(
                        f"{API_URL}/analyze-prompt",
                        json={"prompt": prompt},
                        timeout=15
                    )

                if response.status_code == 200:

                    result = response.json()
                    analysis = result["analysis"]

                    st.success("Prompt analysis completed!")

                    st.divider()

                    st.subheader("📊 Prompt Quality Analysis")

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Prompt Quality Score",
                        f'{analysis["score"]}/100'
                    )

                    with col2:

                        if analysis["status"] == "PASS":

                            st.success("PROMPT PASSED")

                        else:

                            st.warning("NEEDS IMPROVEMENT")

                    st.progress(
                        analysis["score"] / 100
                    )

                    st.write(
                        "Word Count:",
                        analysis["word_count"]
                    )

                    st.subheader("💡 Suggestions")

                    for item in analysis["feedback"]:

                        st.write("•", item)

                else:

                    st.error(
                        f"Backend Error: {response.text}"
                    )

            except requests.exceptions.RequestException:

                st.error(
                    "Unable to connect to backend. "
                    "Please make sure FastAPI is running."
                )

    # ---------------- RUN PROMPT TEST ----------------

    if st.button(
        "🚀 Run Prompt Test",
        use_container_width=True
    ):

        if not prompt.strip():

            st.warning("Please enter a prompt.")

        else:

            keyword_list = [
                word.strip()
                for word in keywords.split(",")
                if word.strip()
            ]

            try:

                with st.spinner("Testing your prompt..."):

                    response = requests.post(
                        f"{API_URL}/test-prompt",
                        json={
                            "prompt": prompt,
                            "expected_keywords": keyword_list
                        },
                        timeout=15
                    )

                if response.status_code == 200:

                    result = response.json()

                    evaluation = result["evaluation"]

                    metrics = evaluation.get("metrics", {})

                    st.success(
                        "Prompt testing completed successfully!"
                    )

                    st.divider()

                    # ---------------- EVALUATION SUMMARY ----------------

                    st.header("📊 Evaluation Summary")

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Quality Score",
                        f'{evaluation["score"]}/100'
                    )

                    with col2:

                        if evaluation["status"] == "PASS":

                            st.success("TEST PASSED")

                        else:

                            st.error("TEST FAILED")

                    st.progress(
                        evaluation["score"] / 100
                    )

                    st.divider()

                    # ---------------- RESPONSE METRICS ----------------

                    st.header("📈 Response Metrics")

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Word Count",
                        metrics.get("word_count", 0)
                    )

                    col2.metric(
                        "Character Count",
                        metrics.get("character_count", 0)
                    )

                    st.divider()

                    # ---------------- KEYWORD ANALYSIS ----------------

                    st.header("🔍 Keyword Analysis")

                    matched = metrics.get(
                        "matched_keywords", []
                    )

                    missing = metrics.get(
                        "missing_keywords", []
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.subheader("✅ Matched Keywords")

                        if matched:

                            for word in matched:

                                st.write(f"• {word}")

                        else:

                            st.info("No matched keywords.")

                    with col2:

                        st.subheader("❌ Missing Keywords")

                        if missing:

                            for word in missing:

                                st.write(f"• {word}")

                        else:

                            st.success("No missing keywords.")

                    st.divider()

                    # ---------------- PROMPT DETAILS ----------------

                    st.header("📝 Prompt Details")

                    with st.expander("Original Prompt"):

                        st.write(result["original_prompt"])

                    with st.expander("Improved Prompt"):

                        st.info(result["improved_prompt"])

                    with st.expander("Generated Response"):

                        st.write(result["ai_response"])

                    # ---------------- EVALUATION FEEDBACK ----------------

                    st.header("💡 Evaluation Feedback")

                    for item in evaluation["feedback"]:

                        st.write("•", item)

                    # ---------------- CSV REPORT DOWNLOAD ----------------

                    st.divider()

                    st.header("📥 Download Evaluation Report")

                    report = io.StringIO()

                    writer = csv.writer(report)

                    writer.writerow([
                        "PromptGuard AI Evaluation Report"
                    ])

                    writer.writerow([
                        "Original Prompt",
                        result["original_prompt"]
                    ])

                    writer.writerow([
                        "Improved Prompt",
                        result["improved_prompt"]
                    ])

                    writer.writerow([
                        "Generated Response",
                        result["ai_response"]
                    ])

                    writer.writerow([
                        "Quality Score",
                        evaluation["score"]
                    ])

                    writer.writerow([
                        "Test Status",
                        evaluation["status"]
                    ])

                    writer.writerow([
                        "Word Count",
                        metrics.get("word_count", 0)
                    ])

                    writer.writerow([
                        "Character Count",
                        metrics.get("character_count", 0)
                    ])

                    writer.writerow([
                        "Matched Keywords",
                        ", ".join(matched)
                    ])

                    writer.writerow([
                        "Missing Keywords",
                        ", ".join(missing)
                    ])

                    writer.writerow([
                        "Evaluation Feedback"
                    ])

                    for item in evaluation["feedback"]:

                        writer.writerow([item])

                    st.download_button(
                        label="📥 Download CSV Report",
                        data="\ufeff" + report.getvalue(),
                        file_name="PromptGuard_Evaluation_Report.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                    st.caption(
                        "Evaluation uses rule-based checks. "
                        "The current response generator is a local demo."
                    )

                else:

                    st.error(
                        f"Backend Error: {response.text}"
                    )

            except requests.exceptions.RequestException:

                st.error(
                    "Cannot connect to backend. "
                    "Please make sure FastAPI is running."
                )


# ---------------- TESTING HISTORY ----------------

elif page == "Testing History":

    st.title("📊 Testing History")

    st.write(
        "View your previously tested prompts."
    )

    if st.button("🔄 Load Testing History"):

        try:

            response = requests.get(
                f"{API_URL}/history",
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()

                st.metric(
                    "Total Tests",
                    data["total_records"]
                )

                if data["history"]:

                    for record in data["history"]:

                        with st.expander(
                            f"Test #{record[0]} - {record[5]}"
                        ):

                            st.write(
                                "Original Prompt:",
                                record[1]
                            )

                            st.write(
                                "Improved Prompt:",
                                record[2]
                            )

                            st.write(
                                "Response:",
                                record[3]
                            )

                            st.write(
                                "Score:",
                                record[4]
                            )

                            st.write(
                                "Status:",
                                record[5]
                            )

                            st.write(
                                "Date:",
                                record[6]
                            )

                else:

                    st.info(
                        "No testing history available."
                    )

            else:

                st.error(
                    "Unable to retrieve history."
                )

        except requests.exceptions.RequestException:

            st.error(
                "Backend connection failed."
            )


# ---------------- ABOUT PROJECT ----------------

elif page == "About Project":

    st.title("ℹ️ About PromptGuard AI")

    st.write(
        "PromptGuard AI is a prompt testing and evaluation "
        "platform developed using Python."
    )

    st.subheader("Key Features")

    st.markdown("""
    - Prompt validation
    - Automatic prompt improvement
    - Prompt quality analysis
    - Local demonstration response generation
    - Response quality evaluation
    - Expected keyword matching
    - Word and character count
    - Missing keyword detection
    - PASS/FAIL testing results
    - SQLite testing history
    - CSV evaluation report download
    """)

    st.subheader("Technology Stack")

    st.markdown("""
    - Python
    - FastAPI
    - Streamlit
    - SQLite
    - Pytest
    - Requests
    """)

    st.info(
        "Real AI model integration and semantic evaluation "
        "are planned future enhancements."
    )