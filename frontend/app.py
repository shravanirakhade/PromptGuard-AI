"""
PromptGuard AI - Professional Dashboard
"""

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="PromptGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
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

.section-title {
    color: #172554;
    font-size: 23px;
    font-weight: 700;
}

div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
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

    st.markdown(
        '<div class="section-title">🚀 Test Your Prompt</div>',
        unsafe_allow_html=True
    )

    prompt = st.text_area(
        "Enter your prompt",
        placeholder="Example: Explain Machine Learning with examples...",
        height=150
    )

    keywords = st.text_input(
        "Expected keywords",
        placeholder="Example: Machine Learning, AI, Data"
    )

    if st.button("🚀 Run Prompt Test", use_container_width=True):

        if not prompt.strip():

            st.warning("Please enter a prompt before testing.")

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

                    st.success("Prompt testing completed successfully!")

                    st.divider()

                    st.markdown(
                        '<div class="section-title">📋 Test Results</div>',
                        unsafe_allow_html=True
                    )

                    evaluation = result["evaluation"]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
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

                    with st.expander("Original Prompt", expanded=True):
                        st.write(result["original_prompt"])

                    with st.expander("Improved Prompt", expanded=True):
                        st.info(result["improved_prompt"])

                    with st.expander("Generated Response", expanded=True):
                        st.write(result["ai_response"])

                    st.subheader("Evaluation Feedback")

                    for item in evaluation["feedback"]:
                        st.write("✔️", item)

                    st.caption(
                        "Note: The current response generator uses "
                        "a local demonstration response."
                    )

                else:

                    st.error(f"Backend Error: {response.text}")

            except requests.exceptions.RequestException:

                st.error(
                    "Cannot connect to the backend. "
                    "Please make sure the FastAPI server is running."
                )


# ---------------- TESTING HISTORY ----------------

elif page == "Testing History":

    st.title("📊 Testing History")

    st.write("View your previously tested prompts.")

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

                            st.write("Original Prompt:", record[1])

                            st.write("Improved Prompt:", record[2])

                            st.write("Response:", record[3])

                            st.write("Score:", record[4])

                            st.write("Status:", record[5])

                            st.write("Date:", record[6])

                else:

                    st.info("No testing history available yet.")

            else:

                st.error("Unable to retrieve testing history.")

        except requests.exceptions.RequestException:

            st.error("Backend connection failed.")


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
    - Local demonstration response generation
    - Response quality evaluation
    - Expected keyword matching
    - PASS/FAIL testing results
    - SQLite testing history
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
        "are planned as future enhancements."
    )