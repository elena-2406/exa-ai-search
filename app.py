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
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

    st.divider()
    st.subheader("💡 Guided Search")

    # Category 1: Academic & Research
    with st.expander("🎓 Academia"):
        if st.button("AI Research Papers"):
            st.info("Try: 'Latest advancements in LLM efficiency 2025'")
        if st.button("Quantum Computing"):
            st.info("Try: 'Current state of error correction in quantum computing'")

    # Category 2: Career & Skills
    with st.expander("💼 Career"):
        if st.button("Tech Internships"):
            st.info("Try: 'Summer 2026 SDE internships for BTech students'")
        if st.button("Open Source"):
            st.info("Try: 'Beginner friendly open source projects for Python'")

    # Category 3: Local & Lifestyle
    with st.expander("📍 Local (Kochi)"):
        if st.button("Work Cafes"):
            st.info("Try: 'Best cafes with high speed wifi in Kochi for working'")
        if st.button("Tech Events"):
            st.info("Try: 'Upcoming tech meetups and hackathons in Kerala 2026'")

    st.divider()
    st.subheader("📜 Recent Searches")
    for h in st.session_state.history[:5]:
        st.caption(f"🕒 {h}")
    
    
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