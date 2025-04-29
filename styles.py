import streamlit as st

def apply_styles():
    """Apply optimized styles with better contrast and visual appeal for 1st graders"""
    
    # Enhanced color palette with better contrast
    PRIMARY_COLOR = "#4EA5FF"       # Brighter blue - better contrast on dark background
    SECONDARY_COLOR = "#FF6B8B"     # Brighter pink - better legibility
    ACCENT_COLOR = "#22E5AF"        # Brighter teal - stands out better
    ACCENT_COLOR_2 = "#FFDE59"      # Brighter yellow - higher contrast
    NEUTRAL_COLOR = "#F8F9FA"       # Light background
    TEXT_COLOR = "#FFFFFF"          # White text for dark background
    TEXT_COLOR_DARK = "#1A1B25"     # Near-black text for light backgrounds
    DARK_BG = "#14151F"             # Darker background
    
    # Apply custom CSS
    st.markdown(f"""
    <style>
        /* Base styling for dark mode */
        .main {{
            color: {TEXT_COLOR};
            background-color: {DARK_BG};
        }}
        
        /* Main header styling */
        header {{
            visibility: hidden;
        }}
        
        /* Clear streamlit default padding */
        .block-container {{
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        
        /* Main title styling */
        h1, h2, .main-title {{
            color: {PRIMARY_COLOR} !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
            font-weight: 700;
            font-size: 2.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            letter-spacing: 1px;
        }}
        
        /* Section header styling */
        h3, h4, h5, h6, .section-title {{
            color: {SECONDARY_COLOR} !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
            font-weight: 600;
            font-size: 1.8rem;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        }}
        
        /* Standard text styling */
        p, li, label, .text {{
            color: {TEXT_COLOR};
            font-size: 1.1rem;
            line-height: 1.5;
        }}
        
        /* Session goals box */
        .session-goals {{
            background-color: {NEUTRAL_COLOR};
            color: {TEXT_COLOR_DARK};
            padding: 25px;
            border-radius: 20px;
            border: 4px solid {PRIMARY_COLOR};
            margin: 20px 0;
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }}
        
        .session-goals h3 {{
            color: {PRIMARY_COLOR} !important;
            font-weight: bold;
            font-size: 1.8rem;
            text-shadow: none;
        }}
        
        .session-goals p, .session-goals li {{
            color: {TEXT_COLOR_DARK};
        }}
        
        /* Fun boxes for activities */
        .fun-box {{
            background-color: rgba(78, 165, 255, 0.15);
            border: 3px solid {PRIMARY_COLOR};
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .fun-box::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 8px;
            background: linear-gradient(90deg, {PRIMARY_COLOR}, {SECONDARY_COLOR}, {ACCENT_COLOR}, {ACCENT_COLOR_2});
            animation: rainbowSlide 3s linear infinite;
        }}
        
        /* Business idea cards */
        .business-idea-card {{
            background-color: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            margin-bottom: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 3px solid {ACCENT_COLOR};
        }}
        
        .business-idea-card:hover {{
            transform: translateY(-5px) scale(1.03);
            box-shadow: 0 12px 20px rgba(0,0,0,0.25);
            border-color: {SECONDARY_COLOR};
            background-color: rgba(255,255,255,0.15);
        }}
        
        /* Money bank styling */
        .money-bank {{
            background-color: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .money-counter {{
            font-size: 28px;
            font-weight: bold;
            color: {ACCENT_COLOR_2};
            background-color: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 15px;
            border: 3px dashed {ACCENT_COLOR_2};
            display: inline-block;
            animation: pulse 2s infinite;
        }}
        
        /* Badge styling */
        .badge {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            margin-right: 8px;
            margin-bottom: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        
        .badge-blue {{
            background-color: {PRIMARY_COLOR};
            color: white;
        }}
        
        .badge-green {{
            background-color: {ACCENT_COLOR};
            color: white;
        }}
        
        .badge-yellow {{
            background-color: {ACCENT_COLOR_2};
            color: #333;
        }}
        
        .badge-pink {{
            background-color: {SECONDARY_COLOR};
            color: white;
        }}
        
        /* Business advertisement styling */
        .business-ad {{
            background: linear-gradient(135deg, var(--color1), var(--color2)); 
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 12px 20px rgba(0,0,0,0.3);
        }}
        
        .business-ad-content {{
            background-color: rgba(255,255,255,0.9);
            color: #333;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }}
        
        .business-ad-symbol {{
            font-size: 64px;
            margin-bottom: 20px;
            filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
        }}
        
        .business-ad-title {{
            color: var(--color1) !important;
            font-size: 2.2rem;
            font-weight: bold;
            margin: 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}
        
        .business-ad-tagline {{
            font-style: italic;
            margin: 15px 0;
            font-size: 18px;
            color: var(--color2);
        }}
        
        .business-ad-description {{
            margin: 20px 0;
            font-weight: bold;
        }}
        
        .business-ad-contact {{
            background-color: var(--color1);
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            display: inline-block;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        /* Jobs section styling */
        .job-card {{
            background-color: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .job-card:hover {{
            transform: translateY(-5px);
            background-color: rgba(255,255,255,0.15);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        }}
        
        .job-icon {{
            font-size: 40px;
            margin-bottom: 10px;
        }}
        
        .job-title {{
            color: {SECONDARY_COLOR} !important;
            font-weight: bold;
            font-size: 1.2rem;
            margin: 10px 0;
        }}
        
        /* Certificate styling */
        .certificate {{
            background-color: #f8f8ff;
            color: #333;
            padding: 40px;
            border-radius: 20px;
            border: 8px dashed {ACCENT_COLOR_2};
            text-align: center;
            margin-top: 30px;
            position: relative;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }}
        
        .certificate h2 {{
            color: {PRIMARY_COLOR} !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        
        .certificate h3 {{
            color: {SECONDARY_COLOR} !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        
        /* Button styling */
        .stButton>button {{
            background-color: {ACCENT_COLOR};
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 15px;
            padding: 12px 24px;
            border: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            background-color: {PRIMARY_COLOR};
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            transform: translateY(-3px);
        }}
        
        /* Input fields styling */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea {{
            border-radius: 15px;
            border: 3px solid {PRIMARY_COLOR};
            font-size: 16px;
            padding: 10px 15px;
            background-color: rgba(255,255,255,0.1);
            color: {TEXT_COLOR};
        }}
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {{
            background-color: rgba(255,255,255,0.15);
            border-color: {SECONDARY_COLOR};
            box-shadow: 0 0 0 2px rgba(255, 107, 139, 0.3);
        }}
        
        /* Select boxes styling */
        .stSelectbox>div>div {{
            background-color: rgba(255,255,255,0.1);
            border: 3px solid {ACCENT_COLOR};
            border-radius: 15px;
            color: {TEXT_COLOR};
        }}
        
        .stSelectbox>div>div:hover {{
            border-color: {SECONDARY_COLOR};
        }}
        
        /* Animation definitions */
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        @keyframes rainbowSlide {{
            0% {{ background-position: 0% 50%; }}
            100% {{ background-position: 100% 50%; }}
        }}
        
        /* Progress bar styling */
        .progress-container {{
            background-color: rgba(255,255,255,0.1);
            border-radius: 15px;
            margin: 15px 0;
            height: 25px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .progress-bar {{
            background: linear-gradient(90deg, {ACCENT_COLOR}, {PRIMARY_COLOR});
            height: 25px;
            border-radius: 15px;
            text-align: center;
            color: white;
            font-weight: bold;
            line-height: 25px;
            position: relative;
            overflow: hidden;
        }}
        
        .progress-bar::after {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                rgba(255,255,255,0) 0%,
                rgba(255,255,255,0.4) 50%,
                rgba(255,255,255,0) 100%
            );
            animation: shimmer 2s infinite linear;
        }}
        
        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        /* Sidebar customization */
        .sidebar .sidebar-content {{
            background-color: {DARK_BG};
        }}
        
        /* Activity tracking */
        .achievement {{
            display: flex;
            align-items: center;
            background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.1));
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-left: 5px solid {ACCENT_COLOR_2};
            transition: all 0.3s ease;
        }}
        
        .achievement:hover {{
            transform: translateX(5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.15));
        }}
        
        .achievement-icon {{
            font-size: 28px;
            margin-right: 15px;
            animation: bounce 2s infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
    </style>
    """, unsafe_allow_html=True)

def apply_business_ad_styling(color1, color2, business_name, tagline, description, contact, symbol):
    """
    Create a properly styled business advertisement with the provided details
    This function ensures HTML is properly rendered instead of showing as code
    """
    st.markdown(f"""
    <h3 style="text-align: center;">Your Business Advertisement</h3>
    
    <div class="business-ad" style="--color1: {color1}; --color2: {color2};">
        <div class="business-ad-content">
            <div class="business-ad-symbol">{symbol}</div>
            <h2 class="business-ad-title">{business_name}</h2>
            <p class="business-ad-tagline">"{tagline}"</p>
            
            <div class="business-ad-description">
                <p><strong>What We Offer:</strong></p>
                <p>{description}</p>
            </div>
            
            <div class="business-ad-contact">
                Contact: {contact}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def apply_job_card_styling(job_list, job_icons):
    """Create properly styled job cards for the job section"""
    st.markdown('<div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-top: 20px;">', unsafe_allow_html=True)
    
    for job in job_list:
        emoji = job_icons.get(job, "💼")
        st.markdown(f"""
        <div class="job-card">
            <div class="job-icon">{emoji}</div>
            <h4 class="job-title">{job}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def apply_session_goals_styling(goals_list):
    """Create properly styled session goals box"""
    goals_html = "".join([f"<li>{goal}</li>" for goal in goals_list])
    
    st.markdown(f"""
    <div class="session-goals">
        <h3>Session Goals</h3>
        <p>In this session, you will:</p>
        <ul>
            {goals_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)
    

def apply_color_selector_styles():
    """Add CSS for the visual color selector"""
    st.markdown("""
    <style>
        /* Color selection grid */
        .color-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }
        
        .color-option {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        }
        
        .color-option:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 10px rgba(0,0,0,0.2);
        }
        
        .color-option.selected {
            transform: scale(1.15);
            box-shadow: 0 0 0 4px white, 0 6px 15px rgba(0,0,0,0.3);
        }
        
        /* Color name tooltip */
        .color-option .tooltip {
            position: absolute;
            background-color: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            bottom: -30px;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
            white-space: nowrap;
        }
        
        .color-option:hover .tooltip {
            opacity: 1;
        }
    </style>
    """, unsafe_allow_html=True)

