import openai
import os
import random
import streamlit as st


def initialize_session_state():
    """Initialize all session state variables needed for the app"""
    # Progress tracking
    if 'progress' not in st.session_state:
        st.session_state.progress = {
            'session1': 0,
            'session2': 0,
            'session3': 0,
            'session4': 0,
            'session5': 0
        }
    
    # Coin tracking
    if 'total_coins' not in st.session_state:
        st.session_state.total_coins = 0
    
    # Achievements
    if 'achievements' not in st.session_state:
        st.session_state.achievements = []
    
    # Completed activities
    if 'completed_activities' not in st.session_state:
        st.session_state.completed_activities = []
    
    # Session 5 specific state
    if 'business_ideas' not in st.session_state:
        st.session_state.business_ideas = []
    
    if 'selected_business' not in st.session_state:
        st.session_state.selected_business = ""
    
    if 'business_names' not in st.session_state:
        st.session_state.business_names = []
    
    if 'selected_business_name' not in st.session_state:
        st.session_state.selected_business_name = ""
    
    if 'business_colors' not in st.session_state:
        st.session_state.business_colors = []
    
    if 'business_symbol' not in st.session_state:
        st.session_state.business_symbol = ""

def award_coins(amount, reason=None):
    """Award coins to the student with an optional reason"""
    st.session_state.total_coins += amount
    if reason:
        st.success(f"🎉 You earned {amount} coins: {reason}")

def award_achievement(icon, title, description):
    """Award a new achievement to the student"""
    if title not in [a['title'] for a in st.session_state.achievements]:
        st.session_state.achievements.append({
            'icon': icon,
            'title': title,
            'description': description
        })
        st.balloons()
        st.success(f"🏆 New Achievement: {title}")

def update_progress(session_key, percentage):
    """Update the progress for a specific session"""
    st.session_state.progress[session_key] = min(100, st.session_state.progress[session_key] + percentage)

def mark_activity_complete(activity_key):
    """Mark an activity as completed if not already done"""
    if activity_key not in st.session_state.completed_activities:
        st.session_state.completed_activities.append(activity_key)
        return True
    return False

def is_activity_completed(activity_key):
    """Check if an activity has been completed"""
    return activity_key in st.session_state.completed_activities

def get_random_element(items_list, seed=None):
    """Get a random element from a list, optionally with a seed for consistency"""
    import random
    if seed is not None:
        random.seed(seed)
    return random.choice(items_list)

def get_emoji_for_category(category, seed=None):
    """Generate a consistent emoji for a category"""
    category_emojis = {
        "business": ["🏢", "🏪", "🛒", "🏦", "🏫", "🏭"],
        "money": ["💰", "💵", "💸", "🪙", "💲", "🤑"],
        "family": ["👨‍👩‍👧‍👦", "👨‍👩‍👧", "👩‍👦", "👨‍👧‍👦", "👨‍👧", "👩‍👧‍👦"],
        "jobs": ["👨‍🏫", "👩‍🔧", "👩‍🚒", "👨‍🍳", "👩‍⚕️", "👨‍🌾"],
        "needs": ["🏠", "🍎", "💧", "👕", "🧸"],
        "wants": ["🎮", "🍦", "🎠", "📱", "🚲"]
    }
    
    default_category = "business"
    emoji_list = category_emojis.get(category.lower(), category_emojis[default_category])
    return get_random_element(emoji_list, seed)


def safe_rerun():
    """Safely rerun the app, handling deprecated functions"""
    try:
        # Use the new non-experimental rerun
        st.rerun()
    except Exception as e:
        # Fallback if there's any issue
        st.warning(f"Please refresh the page to continue. Error: {e}")
            

def create_simple_color_selector(key_prefix="color"):
    """
    Create a simplified visual color selector using Streamlit columns
    Returns: The selected color name and hex value
    
    Parameters:
        key_prefix: Prefix for the button keys to avoid conflicts when using multiple selectors
    """
    # Define colors with kid-friendly names, hex values and emojis
    colors = {
        "Red": {"hex": "#FF5252", "emoji": "🔴"},
        "Blue": {"hex": "#448AFF", "emoji": "🔵"},
        "Green": {"hex": "#4CAF50", "emoji": "🟢"},
        "Yellow": {"hex": "#FFEB3B", "emoji": "🟡"},
        "Purple": {"hex": "#9C27B0", "emoji": "🟣"},
        "Pink": {"hex": "#FF80AB", "emoji": "💗"},
        "Orange": {"hex": "#FF9800", "emoji": "🟠"},
        "Teal": {"hex": "#009688", "emoji": "🌊"},
        "Light Blue": {"hex": "#03A9F4", "emoji": "💧"},
        "Lime": {"hex": "#CDDC39", "emoji": "🍏"}
    }
    
    # Initialize session state for selected color if not exists
    if f"{key_prefix}_name" not in st.session_state:
        st.session_state[f"{key_prefix}_name"] = "Blue"  # Default
        st.session_state[f"{key_prefix}_hex"] = "#448AFF"  # Default hex
    
    # Create a grid of color options using columns
    st.write("Click to select a color:")
    
    # Create 5 columns for the first row of colors
    cols1 = st.columns(5)
    # Create 5 columns for the second row of colors
    cols2 = st.columns(5)
    
    # Combine the columns into a single list for easier iteration
    all_cols = cols1 + cols2
    
    # Display color options as buttons
    for i, (color_name, color_info) in enumerate(colors.items()):
        with all_cols[i]:
            # Create a button with the color emoji
            if st.button(
                color_info["emoji"], 
                key=f"{key_prefix}_{color_name.lower().replace(' ', '_')}",
                help=f"Select {color_name}"
            ):
                # Update the session state with the selected color
                st.session_state[f"{key_prefix}_name"] = color_name
                st.session_state[f"{key_prefix}_hex"] = color_info["hex"]
                # Force a rerun to update the display
                st.rerun()
    
    # Display the currently selected color
    selected_color = st.session_state[f"{key_prefix}_name"]
    selected_hex = st.session_state[f"{key_prefix}_hex"]
    selected_emoji = colors[selected_color]["emoji"]
    
    st.markdown(f"""
    <div style="margin-top: 10px; padding: 10px; border-radius: 10px; background-color: {selected_hex}; 
                text-align: center; color: white; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">
        Selected: {selected_emoji} {selected_color}
    </div>
    """, unsafe_allow_html=True)
    
    # Return the selected color name and hex value
    return selected_color, selected_hex
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


def create_simple_color_selector(key_prefix="color"):
    """
    Create a simplified visual color selector using Streamlit columns
    Returns: The selected color name and hex value
    
    Parameters:
        key_prefix: Prefix for the button keys to avoid conflicts when using multiple selectors
    """
    # Define colors with kid-friendly names, hex values and emojis
    colors = {
        "Red": {"hex": "#FF5252", "emoji": "🔴"},
        "Blue": {"hex": "#448AFF", "emoji": "🔵"},
        "Green": {"hex": "#4CAF50", "emoji": "🟢"},
        "Yellow": {"hex": "#FFEB3B", "emoji": "🟡"},
        "Purple": {"hex": "#9C27B0", "emoji": "🟣"},
        "Pink": {"hex": "#FF80AB", "emoji": "💗"},
        "Orange": {"hex": "#FF9800", "emoji": "🟠"},
        "Teal": {"hex": "#009688", "emoji": "🌊"},
        "Light Blue": {"hex": "#03A9F4", "emoji": "💧"},
        "Lime": {"hex": "#CDDC39", "emoji": "🍏"}
    }
    
    # Initialize session state for selected color if not exists
    if f"{key_prefix}_name" not in st.session_state:
        st.session_state[f"{key_prefix}_name"] = "Blue"  # Default
        st.session_state[f"{key_prefix}_hex"] = "#448AFF"  # Default hex
    
    # Create a grid of color options using columns
    st.write("Click to select a color:")
    
    # Create 5 columns for the first row of colors
    cols1 = st.columns(5)
    # Create 5 columns for the second row of colors
    cols2 = st.columns(5)
    
    # Combine the columns into a single list for easier iteration
    all_cols = cols1 + cols2
    
    # Display color options as buttons
    for i, (color_name, color_info) in enumerate(colors.items()):
        with all_cols[i]:
            # Create a button with the color emoji
            if st.button(
                color_info["emoji"], 
                key=f"{key_prefix}_{color_name.lower().replace(' ', '_')}",
                help=f"Select {color_name}"
            ):
                # Update the session state with the selected color
                st.session_state[f"{key_prefix}_name"] = color_name
                st.session_state[f"{key_prefix}_hex"] = color_info["hex"]
                # Force a rerun to update the display
                st.rerun()
    
    # Display the currently selected color
    selected_color = st.session_state[f"{key_prefix}_name"]
    selected_hex = st.session_state[f"{key_prefix}_hex"]
    selected_emoji = colors[selected_color]["emoji"]
    
    st.markdown(f"""
    <div style="margin-top: 10px; padding: 10px; border-radius: 10px; background-color: {selected_hex}; 
                text-align: center; color: white; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">
        Selected: {selected_emoji} {selected_color}
    </div>
    """, unsafe_allow_html=True)
    
    # Return the selected color name and hex value
    return selected_color, selected_hex

def create_visual_color_selector(key_prefix="color"):
    """
    Create a visual color selector using Streamlit's native components
    
    Parameters:
        key_prefix: Unique prefix for widget keys to avoid conflicts
        
    Returns:
        tuple: (selected_color_name, selected_color_hex)
    """
    # Define colors with kid-friendly names and hex values
    colors = {
        "Red": {"hex": "#FF5252", "emoji": "🔴"},
        "Blue": {"hex": "#448AFF", "emoji": "🔵"},
        "Green": {"hex": "#4CAF50", "emoji": "🟢"},
        "Yellow": {"hex": "#FFEB3B", "emoji": "🟡"},
        "Purple": {"hex": "#9C27B0", "emoji": "🟣"},
        "Pink": {"hex": "#FF80AB", "emoji": "💗"},
        "Orange": {"hex": "#FF9800", "emoji": "🟠"},
        "Teal": {"hex": "#009688", "emoji": "🌊"},
        "Light Blue": {"hex": "#03A9F4", "emoji": "💧"},
        "Lime": {"hex": "#CDDC39", "emoji": "🍏"}
    }
    
    # Initialize session state for selected color if not exists
    if f"{key_prefix}_name" not in st.session_state:
        st.session_state[f"{key_prefix}_name"] = "Blue"  # Default
        st.session_state[f"{key_prefix}_hex"] = "#448AFF"  # Default hex
    
    # Display color options as a grid
    st.write("Click to select a color:")
    
    # First row of colors (5 colors)
    cols1 = st.columns(5)
    colors_list = list(colors.items())
    
    # Display first 5 colors
    for i in range(5):
        color_name, color_info = colors_list[i]
        with cols1[i]:
            # Create unique key for each button
            unique_key = f"{key_prefix}_btn_{color_name.lower().replace(' ', '_')}"
            if st.button(
                color_info["emoji"], 
                key=unique_key,
                help=f"Select {color_name}"
            ):
                # Update session state
                st.session_state[f"{key_prefix}_name"] = color_name
                st.session_state[f"{key_prefix}_hex"] = color_info["hex"]
                st.rerun()
    
    # Second row of colors (5 colors)
    cols2 = st.columns(5)
    
    # Display next 5 colors
    for i in range(5, 10):
        color_name, color_info = colors_list[i]
        with cols2[i-5]:
            # Create unique key for each button
            unique_key = f"{key_prefix}_btn_{color_name.lower().replace(' ', '_')}"
            if st.button(
                color_info["emoji"], 
                key=unique_key,
                help=f"Select {color_name}"
            ):
                # Update session state
                st.session_state[f"{key_prefix}_name"] = color_name
                st.session_state[f"{key_prefix}_hex"] = color_info["hex"]
                st.rerun()
    
    # Display the currently selected color
    selected_color = st.session_state[f"{key_prefix}_name"]
    selected_hex = st.session_state[f"{key_prefix}_hex"]
    selected_emoji = colors[selected_color]["emoji"]
    
    # Display selected color with background matching the color
    st.markdown(f"""
    <div style="margin-top: 10px; padding: 10px; border-radius: 10px; background-color: {selected_hex}; 
                text-align: center; color: white; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">
        Selected: {selected_emoji} {selected_color}
    </div>
    """, unsafe_allow_html=True)
    
    # Return the selected color name and hex value
    return selected_color, selected_hex


def create_business_advertisement(business_name, business_type, tagline, contact, symbol, color1, color2):
    """
    Create a properly rendered business advertisement
    
    This function ensures proper HTML rendering without showing raw HTML code
    
    Parameters:
        business_name: The name of the business
        business_type: Type of business (e.g., Pet Sitting Helper)
        tagline: Slogan for the business
        contact: Contact information
        symbol: Emoji symbol for the business
        color1: Primary color hex code
        color2: Secondary color hex code
    """
    # Use st.markdown with properly escaped HTML
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color1}, {color2}); 
                border-radius: 20px; padding: 0; overflow: hidden; 
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);">
        
        <div style="background-color: rgba(255, 255, 255, 0.95); 
                    margin: 15px; padding: 30px; border-radius: 15px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1); text-align: center;">
            
            <div style="font-size: 64px; margin-bottom: 20px;">{symbol}</div>
            
            <h2 style="color: #333; font-size: 28px; margin-bottom: 10px; 
                       font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;">
                {business_name}
            </h2>
            
            <p style="font-style: italic; color: #555; margin: 15px 0; font-size: 18px;">
                "{tagline}"
            </p>
            
            <div style="margin: 25px 0; background-color: rgba(240, 240, 240, 0.7);
                        padding: 15px; border-radius: 10px;">
                <p style="font-weight: bold; margin: 0 0 5px 0;">What We Offer:</p>
                <p style="margin: 0;">{business_type}</p>
            </div>
            
            <div style="background-color: {color1}; color: white; 
                        padding: 10px 20px; border-radius: 10px; 
                        display: inline-block; font-weight: bold;">
                Contact: {contact}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_business_names(business_type, student_name, creativity_level, count=5):
    """
    Generate business names using OpenAI or fallback to built-in algorithm
    
    Parameters:
        business_type: Type of business (e.g., "Pet Sitting Helper")
        student_name: The student's first name
        creativity_level: How creative names should be (1-5)
        count: Number of names to generate
        
    Returns:
        list: Generated business names
    """
    # Try to use OpenAI if API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            openai.api_key = api_key
            
            # Create the prompt for OpenAI
            prompt = f"""Create {count} business names for a {business_type} business run by a 1st grade student named {student_name}.

Creativity level: {creativity_level}/5 (where 1 is simple, 5 is super creative and fun)

Guidelines:
- Include "{student_name}'s" in some of the names
- Keep names simple enough for a 1st grader to read and understand
- Make names fun, positive, and kid-appropriate
- The higher the creativity level, the more playful and imaginative the names should be
- Avoid any negative or scary themes

Format as a simple list with just the business names (no numbering or explanations).
"""
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7 + (creativity_level * 0.1)  # Increase randomness with creativity
            )
            
            # Extract the names from response
            content = response.choices[0].message["content"].strip()
            names = [name.strip().strip('*-•123456789.').strip() for name in content.split('\n')]
            names = [name for name in names if name]  # Remove any empty strings
            
            # Return generated names or fall back if none were generated
            if names:
                return names[:count]  # Return the requested number of names
        
        except Exception as e:
            # If OpenAI fails, use the fallback method
            st.warning(f"Using built-in name generator instead of AI. (Error: {type(e).__name__})")
    
    # Fallback method if OpenAI isn't available or fails
    # Define creativity levels with more creative adjectives and suffixes
    adjectives = {
        1: ["Super", "Great", "Good", "Smart", "Helpful"],
        2: ["Amazing", "Awesome", "Fantastic", "Brilliant", "Wonderful"],
        3: ["Spectacular", "Terrific", "Magnificent", "Marvelous", "Extraordinary"],
        4: ["Stupendous", "Colossal", "Phenomenal", "Mind-Blowing", "Ultra"],
        5: ["Absolutely Incredible", "Totally Outrageous", "Ridiculously Amazing", 
            "Extraordinarily Fantastic", "Unbelievably Awesome"]
    }
    
    business_suffix = {
        1: ["Service", "Helper", "Company", "Business", "Team"],
        2: ["Experts", "Specialists", "Pros", "Stars", "Champions"],
        3: ["Wizards", "Heroes", "Masters", "Legends", "Squad"],
        4: ["Extraordinaires", "Superstars", "Dynamos", "Sensations", "Wonders"],
        5: ["Magnificent Marvels", "Spectacular Specialists", "Dynamic Dynamos", 
            "Fantastic Phenoms", "Tremendous Titans"]
    }
    
    # Generate names based on patterns
    names = []
    
    # Extract keywords from business type
    business_keywords = business_type.lower().split()
    
    # Formula 1: [Student's Name]'s [Business Type]
    names.append(f"{student_name}'s {business_type}")
    
    # Formula 2: [Student's Name]'s [Adjective] [Business Type]
    adj = random.choice(adjectives[min(creativity_level, 5)])
    names.append(f"{student_name}'s {adj} {business_type}")
    
    # Formula 3: [Student's Name]'s [Adjective] [Keyword] [Suffix]
    # Generate remaining names
    for _ in range(count - 2):
        adj = random.choice(adjectives[min(creativity_level, 5)])
        keyword = random.choice(business_keywords) if business_keywords else business_type
        suffix = random.choice(business_suffix[min(creativity_level, 5)])
        
        # Capitalize the keyword
        keyword = keyword.capitalize()
        
        names.append(f"{student_name}'s {adj} {keyword} {suffix}")
    
    return names

# Example usage in Session 5:
def display_business_name_generator(business_type, student_name):
    """Display the business name generator UI component"""
    
    st.subheader("✨ Create a Business Name")
    
    st.markdown(f"""
    <div class="fun-box">
        <h3>You selected: {business_type}</h3>
        <p>Now let's create a fun name for your business!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Creativity level slider (renamed from "silliness")
    creativity = st.slider(
        "How creative do you want your business name to be?",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Simple, 5 = Super Creative!"
    )
    
    # Generate names button
    if st.button("Generate Business Names", key="generate_business_names_btn"):
        if student_name:
            # Generate names using our function
            business_names = generate_business_names(
                business_type,
                student_name,
                creativity
            )
            
            # Store in session state
            st.session_state.business_names = business_names
            st.success("Business names created! Pick your favorite below.")
        else:
            st.error("Please enter your name first!")
    
    # Display generated business names
    if "business_names" in st.session_state and st.session_state.business_names:
        st.markdown("<h4>Pick your favorite business name:</h4>", unsafe_allow_html=True)
        
        for i, name in enumerate(st.session_state.business_names):
            st.markdown(f"""
            <div class="business-name-option" style="background-color: #f8f9fa; padding: 15px; 
                          border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #FFB400;">
                <h4 style="margin: 0;">{name}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Unique key for each button
            if st.button(f"Choose This Name", key=f"select_name_{i}_{hash(name)}"):
                st.session_state.selected_business_name = name
                # Award coins logic would go here
                st.success(f"You picked: {name}!")
                # Force a rerun to move to next step
                st.rerun()
                
def create_symbol_selector(key_prefix="symbol"):
    """Create a visual emoji symbol selector for business advertisements"""
    symbols = [
        {"emoji": "⭐", "description": "Star - for special quality"},
        {"emoji": "🌟", "description": "Sparkle - for something amazing"},
        {"emoji": "🔆", "description": "Bright - for happiness"},
        # Add more symbols...
    ]
    
    # Initialize session state
    if f"{key_prefix}_value" not in st.session_state:
        st.session_state[f"{key_prefix}_value"] = "⭐"
    
    # Create symbol grid with 3 columns
    st.write("Choose a symbol for your business:")
    
    for i in range(0, len(symbols), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(symbols):
                symbol = symbols[i+j]
                with cols[j]:
                    if st.button(symbol["emoji"], 
                               key=f"{key_prefix}_btn_{i+j}",
                               help=symbol["description"]):
                        st.session_state[f"{key_prefix}_value"] = symbol["emoji"]
                        st.rerun()
    
    # Return selected symbol
    return st.session_state[f"{key_prefix}_value"]

def create_quiz_question(question, options, correct_answer, correct_message, 
                       incorrect_message, activity_key, coins=5, 
                       reason=None, progress=10):
    """Create a quiz question with proper answer handling"""
    # Create unique session state keys
    answer_key = f"{activity_key}_answer"
    answered_key = f"{activity_key}_answered"
    
    # Initialize session state
    if answer_key not in st.session_state:
        st.session_state[answer_key] = None
    if answered_key not in st.session_state:
        st.session_state[answered_key] = False
    
    # Display question with no default selection
    answer = st.radio(question, options, index=None, key=f"radio_{activity_key}")
    
    # Update session state when answered
    if answer is not None:
        st.session_state[answer_key] = answer
    
    # Add check button
    if st.button("Check Answer", key=f"check_{activity_key}"):
        st.session_state[answered_key] = True
    
    # Only show feedback after submission
    if st.session_state[answered_key]:
        if st.session_state[answer_key] == correct_answer:
            st.success(correct_message)
            # Use try-except to handle any potential errors
            try:
                if mark_activity_complete(activity_key):
                    award_coins(coins, reason)
                    update_progress(activity_key.split("_")[0], progress)
            except Exception as e:
                st.error(f"Error processing correct answer: {e}")
        elif st.session_state[answer_key] is None:
            st.warning("Please select an answer first!")
        else:
            st.error(incorrect_message)
    
    # Prevent recursion by not calling st.write() directly
    st.markdown("&nbsp;", unsafe_allow_html=True)