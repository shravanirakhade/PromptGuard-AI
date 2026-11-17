"""
PromptGuard AI - Frontend Application
"""

import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# Page configuration
st.set_page_config(
    page_title="PromptGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# Application heading
st.title("🛡️ PromptGuard AI")
st.subheader("Intelligent AI Prompt Testing & Evaluation Platform")

st.write(
    "Test your prompts, evaluate responses, "
    "and maintain your testing history."
)

st.divider()

# Prompt input
st.header("Test Your Prompt")

prompt = st.text_area(
    "Enter your prompt:",
    placeholder="Example: Explain Python programming..."
)

keywords = st.text_input(
    "Expected keywords (comma separated):",
    placeholder="Python, programming, AI"
)

# Test button
if st.button("🚀 Test My Prompt"):

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

                st.success("Prompt testing completed!")

                st.subheader("Original Prompt")
                st.write(result["original_prompt"])

                st.subheader("Improved Prompt")
                st.info(result["improved_prompt"])

                st.subheader("AI Response")
                st.write(result["ai_response"])

                st.subheader("Evaluation Results")

                evaluation = result["evaluation"]

                col1, col2 = st.columns(2)

                col1.metric(
                    "Quality Score",
                    f'{evaluation["score"]}/100'
                )

                col2.metric(
                    "Test Status",
                    evaluation["status"]
                )

                for item in evaluation["feedback"]:
                    st.write("•", item)

            else:
                st.error(f"Backend Error: {response.text}")

        except requests.exceptions.RequestException as error:
            st.error(f"Cannot connect to backend: {error}")


# Testing history
st.divider()
st.header("📊 Prompt Testing History")

if st.button("View Testing History"):

    try:
        history_response = requests.get(
            f"{API_URL}/history",
            timeout=10
        )

        if history_response.status_code == 200:

            history_data = history_response.json()

            st.write(
                "Total tests:",
                history_data["total_records"]
            )

            for record in history_data["history"]:

                with st.expander(f"Test #{record[0]} - {record[5]}"):

                    st.write("Original Prompt:", record[1])
                    st.write("Improved Prompt:", record[2])
                    st.write("Response:", record[3])
                    st.write("Score:", record[4])
                    st.write("Status:", record[5])
                    st.write("Date:", record[6])

        else:
            st.error("Unable to retrieve testing history.")

    except requests.exceptions.RequestException as error:
        st.error(f"Backend connection failed: {error}")