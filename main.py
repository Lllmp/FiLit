import streamlit as st
from datetime import datetime
import os
from sessions import session1, session2, session3, session4, session5
from utils import award_coins, award_achievement, initialize_session_state
from styles import apply_styles


# Set page configuration
st.set_page_config(
    page_title="Mr. Stumberg's Financial Literacy Adventure",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:teacher@grimeselementary.edu',
        'Report a bug': 'mailto:support@grimeselementary.edu',
        'About': 'Created for Mr. Stumberg\'s 1st Grade Financial Literacy Class'
    }
)

# Add caching for assets
@st.cache_resource
def load_css():
    # Custom CSS loading function to improve performance
    from styles import apply_styles
    return apply_styles()

# Call the cached function
load_css()

# Apply CSS styling
apply_styles()

# Initialize session state
initialize_session_state()

# School header with current date
current_date = datetime.now().strftime("%B %d, %Y")
st.markdown(f"""
<div class="school-header">
    <h2 style="margin:0">Mr. Stumberg's 1st Grade Financial Literacy Adventure</h2>
    <p style="margin:5px 0 0 0; color:white;">{current_date}</p>
</div>
""", unsafe_allow_html=True)
    

# Sidebar for navigation and progress tracking
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=Mr.S", width=150)
    
    st.markdown(f"""
    <div style="background-color: white; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="margin-top: 0;">Your Money Bank</h3>
        <div class="money-counter">💰 {st.session_state.total_coins} coins</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress overview
    st.markdown("### Your Learning Journey")
    
    # Show progress for each session
    sessions = [
        {"name": "Session 1: All Kinds of Families", "key": "session1", "emoji": "👪"},
        {"name": "Session 2: Money for Needs and Wants", "key": "session2", "emoji": "🛒"},
        {"name": "Session 3: Businesses Around Grimes", "key": "session3", "emoji": "🏪"},
        {"name": "Session 4: Jobs in Our Community", "key": "session4", "emoji": "👩‍🏫"},
        {"name": "Session 5: Create Your Own Business", "key": "session5", "emoji": "🚀"}
    ]
    
    for session in sessions:
        progress = st.session_state.progress[session["key"]]
        st.markdown(f"""
        <div>
            <p style="margin-bottom: 5px;">{session["emoji"]} {session["name"]}</p>
            <div class="progress-container">
                <div class="progress-bar" style="width:{progress}%">
                    {progress}%
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Achievements section
    if st.session_state.achievements:
        st.markdown("### Your Achievements")
        for achievement in st.session_state.achievements:
            st.markdown(f"""
            <div class="achievement">
                <div class="achievement-icon">{achievement['icon']}</div>
                <div>
                    <strong>{achievement['title']}</strong><br>
                    <small>{achievement['description']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Helper info
    with st.expander("💡 For Parents & Teachers"):
        st.markdown("""
        This app follows the JA Our Families curriculum and Iowa Core standards for financial literacy:
        - Developing financial and career goals
        - Analyzing credit and debt levels
        - Evaluating savings and long-term investments
        
        Each session builds on previous learning with age-appropriate activities.
        """)

# Main content area with tabs for different sessions
sessions_tab = st.tabs([
    "👪 Session 1: All Kinds of Families",
    "🛒 Session 2: Needs & Wants",
    "🏪 Session 3: Businesses",
    "👩‍🏫 Session 4: Jobs",
    "🚀 Session 5: Your Business"
])

# Load each session into its respective tab
with sessions_tab[0]:
    session1.run()

with sessions_tab[1]:
    session2.run()

with sessions_tab[2]:
    session3.run()

with sessions_tab[3]:
    session4.run()

with sessions_tab[4]:
    session5.run()
    
# Add to main.py
try:
    # Initialize session state
    initialize_session_state()
    
    # School header with current date
    current_date = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"""
    <div class="school-header">
        <h2 style="margin:0">Mr. Stumberg's 1st Grade Financial Literacy Adventure</h2>
        <p style="margin:5px 0 0 0; color:white;">{current_date}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Rest of main.py content
    
except Exception as e:
    st.error(f"The app encountered an error: {type(e).__name__}: {e}")
    st.info("Try refreshing the page to continue.")