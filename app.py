import streamlit as st
from exa_py import Exa

# UI Configuration
st.set_page_config(page_title="AI Search Engine", page_icon="🔍")

# Initialize Exa from Secrets
try:
    api_key = st.secrets["EXA_API_KEY"]
    exa = Exa(api_key=api_key)
except KeyError:
    st.error("Missing EXA_API_KEY in secrets.toml. Please check your setup!")
    st.stop()

# Initializing history state

if "history" not in st.session_state:
    st.session_state.history = []


# Sidebar for simple settings 
with st.sidebar:
    st.title("Search Options")
    num_results = st.slider("Number of results", 1, 10, 5)
    st.info("API Key is securely loaded from secrets.")

# Main UI
st.title("🚀 My Custom AI Search")
st.markdown("Enter a query to search the web using **neural embeddings**.")

query = st.text_input("What are you looking for?", placeholder="e.g., Best cafes in Kochi")
if query:
    if query not in st.session_state.history:
        st.session_state.history.insert(0,query)

    with st.spinner("Searching the neural web..."):
        
        response = exa.search(
            query, 
            num_results=num_results, 
            type="magic"  
        )
        
        # 5. Displaying Results
        st.subheader(f"Top {len(response.results)} Results:")
        for result in response.results:
            with st.container():
                st.markdown(f"### [{result.title}]({result.url})")
                
                if result.score is not None:
                    score_pct = round(result.score * 100, 2)
                    st.write(f"**Relevance Score:** {score_pct}%")
                else:
                    st.write("**Relevance Score:** N/A")
                st.divider()