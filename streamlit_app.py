import streamlit as st
import requests
import re

# Replace this with your deployed API endpoint URL
API_URL = "https://<your-render-domain>/process"

st.title("Web Research Report Generator")

# User input for query
query = st.text_input("Enter your query (include 'scrape' or 'crawl'):")

if st.button("Generate Report"):
    if not query:
        st.warning("Please enter a query before generating the report.")
    else:
        with st.spinner("Generating report..."):
            try:
                resp = requests.post(API_URL, json={"message": query})
                resp.raise_for_status()
            except requests.RequestException as e:
                st.error(f"API request failed: {e}")
            else:
                data = resp.json()
                report = data.get("report", "")
                if not report:
                    st.write("No report content returned from the API.")
                else:
                    # Split into sections by the dashed separator lines
                    sections = re.split(r"\n─+\n", report)
                    # Display the introductory block
                    st.markdown(sections[0])

                    # Clean up trailing TERMINATE marker if present
                    sections[-1] = sections[-1].replace("TERMINATE", "").strip()

                    # Render each named section
                    for sec in sections[1:]:
                        if ":\n" in sec:
                            title, body = sec.split(":\n", 1)
                        else:
                            title, body = "", sec
                        st.subheader(title)
                        st.markdown(body)

# Instructions on running
st.sidebar.markdown("---")
st.sidebar.info("Run this app with `streamlit run streamlit_app.py`.\n\nBe sure to set `API_URL` to your FastAPI endpoint.")
