import streamlit as st
import random
import os
from datetime import datetime
from utils import (
    award_coins, 
    award_achievement, 
    update_progress, 
    mark_activity_complete, 
    is_activity_completed,
    create_quiz_question,  # Add this import to all session files
    safe_rerun  # Use this instead of st.experimental_rerun
)
import openai
from styles import apply_business_ad_styling
from styles import apply_session_goals_styling
from utils import create_symbol_selector





def run():
    """
    Session 5: Create Your Own Business
    
    Objectives:
    - Describe one of the entrepreneurial characteristics: Satisfy a Need or Want
    - Create a business idea based on student interests
    - Design marketing materials for the business
    """
    # Constants for styling - using the app's color scheme
    PRIMARY_COLOR = "#3B4CCA"     # Deeper blue 
    SECONDARY_COLOR = "#EB4971"   # Brighter pink
    ACCENT_COLOR = "#03B980"      # Vibrant teal
    ACCENT_COLOR_2 = "#FFB400"    # Golden yellow
    
    # Configure OpenAI if API key is available
    if 'OPENAI_API_KEY' in os.environ:
        openai.api_key = os.environ['OPENAI_API_KEY']
        use_openai = True
    else:
        use_openai = False
    
    st.header("🚀 Session 5: Create Your Own Business")
    
    # Session overview
    # List of goals for this session
    goals = [
        "Create your very own business idea",
        "Make a fun business name",
        "Design a colorful advertisement for your business"
    ]

    # Apply styled session goals
    apply_session_goals_styling(goals)
    # --------------------------------
    # Step 1: Collect student information
    # --------------------------------
    st.markdown("""
    <div class="step-header">
        <span style="font-size: 24px;">📝</span> Step 1: Tell us about yourself!
    </div>
    """, unsafe_allow_html=True)
    
    # Student information form
    student_col1, student_col2 = st.columns(2)
    
    with student_col1:
        student_name = st.text_input("What's your first name?", key="student_name")
        
        # City selection (limited to Grimes and Dallas Center)
        city = st.selectbox(
            "Where will your business be located?",
            ["Grimes", "Dallas Center"],
            key="city"
        )
    
    with student_col2:
        # Multi-select for student interests
        interests = st.multiselect(
            "What do you like to do? (Choose at least 2 things)",
            [
                "Sports and games", 
                "Reading books",
                "Drawing and art", 
                "Music and dancing",
                "Animals and pets",
                "Helping others",
                "Building things",
                "Math and numbers",
                "Computers and technology",
                "Playing outside",
                "Making new friends",
                "Cooking and food"
            ],
            key="interests"
        )
    
    # --------------------------------
    # Step 2: Generate Business Ideas
    # --------------------------------
    st.markdown("""
    <div class="step-header">
        <span style="font-size: 24px;">💡</span> Step 2: Business Idea Generator
    </div>
    """, unsafe_allow_html=True)
    
    # Business idea database - categorized by interest, city, and timeframe
    business_ideas_db = {
        "Sports and games": {
            "Grimes": {
                "now": [
                    "Sports Equipment Organization Service",
                    "Neighborhood Game Organizer",
                    "Game Rules Explainer",
                    "Sports Card Trading Helper",
                    "Backyard Games Setup"
                ],
                "future": [
                    "Sports Coach or Trainer",
                    "Recreation Center Manager",
                    "Sports Equipment Designer",
                    "Professional Athlete",
                    "Game Developer"
                ]
            },
            "Dallas Center": {
                "now": [
                    "Farm Field Games Organizer",
                    "Outdoor Games Helper",
                    "Sports Equipment Cleaner",
                    "Score Keeper",
                    "Game Setup Helper"
                ],
                "future": [
                    "Rural Sports League Manager",
                    "Farm-based Recreation Coordinator",
                    "Sports Equipment Engineer",
                    "Sports Broadcaster",
                    "Team Manager"
                ]
            }
        },
        "Reading books": {
            "Grimes": {
                "now": [
                    "Book Organization Helper",
                    "Story Time Reader",
                    "Book Recommender",
                    "Reading Buddy Service",
                    "Bookmark Creator"
                ],
                "future": [
                    "Librarian",
                    "Author or Writer",
                    "Book Editor",
                    "Reading Teacher",
                    "Book Store Owner"
                ]
            },
            "Dallas Center": {
                "now": [
                    "Farm Story Reader",
                    "Book Delivery Helper",
                    "Reading Corner Organizer",
                    "Book Swap Organizer",
                    "Library Helper"
                ],
                "future": [
                    "Rural Library Manager",
                    "Country Book Store Owner",
                    "Farm Story Writer",
                    "Book Publisher",
                    "Literature Professor"
                ]
            }
        },
        "Drawing and art": {
            "Grimes": {
                "now": [
                    "Sidewalk Chalk Artist",
                    "Window Decorator",
                    "Birthday Card Creator",
                    "Art Supply Organizer",
                    "Coloring Partner"
                ],
                "future": [
                    "Professional Artist",
                    "Graphic Designer",
                    "Art Teacher",
                    "Museum Curator",
                    "Animator"
                ]
            },
            "Dallas Center": {
                "now": [
                    "Nature Art Collector",
                    "Farm Scene Sketcher",
                    "Countryside Photographer Helper",
                    "Barn Art Decorator",
                    "Country Craft Maker"
                ],
                "future": [
                    "Rural Landscape Artist",
                    "Farm Photographer",
                    "Agricultural Illustrator",
                    "Country Crafts Business Owner",
                    "Art Conservator"
                ]
            }
        },
        "Animals and pets": {
            "Grimes": {
                "now": [
                    "Pet Walking Helper",
                    "Pet Sitting Helper",
                    "Homemade Pet Toy Maker",
                    "Pet Photo Helper",
                    "Pet Treat Baker"
                ],
                "future": [
                    "Veterinarian",
                    "Pet Store Owner",
                    "Animal Trainer",
                    "Wildlife Conservationist",
                    "Animal Nutritionist"
                ]
            },
            "Dallas Center": {
                "now": [
                    "Farm Animal Helper",
                    "Barn Cat Caretaker",
                    "Egg Collector",
                    "Animal Brush Assistant",
                    "Pet Food Helper"
                ],
                "future": [
                    "Farm Veterinarian",
                    "Animal Scientist",
                    "Ranch Manager",
                    "Livestock Specialist",
                    "Agricultural Researcher"
                ]
            }
        }
        # Additional categories would continue in the same format
    }
    
    # Fallback ideas if the database doesn't have matches for the student's interests
    fallback_ideas = {
        "now": [
            "Lemonade Stand",
            "Pet Helper Service",
            "Art Stand",
            "Helpful Neighbor Service",
            "Reading Buddy Service",
            "Craft Creator"
        ],
        "future": [
            "Store Owner",
            "Veterinarian",
            "Artist",
            "Teacher",
            "Chef",
            "Computer Programmer"
        ]
    }
    
    # When interests and city are selected, generate business ideas
    if len(interests) >= 2 and city and st.button("Generate Business Ideas!"):
        # Clear previous ideas
        st.session_state.business_ideas = {"now": [], "future": []}
        
        # Collect ideas based on interests
        for interest in interests:
            if interest in business_ideas_db and city in business_ideas_db[interest]:
                # Add "now" ideas
                if "now" in business_ideas_db[interest][city]:
                    st.session_state.business_ideas["now"].extend(business_ideas_db[interest][city]["now"])
                
                # Add "future" ideas
                if "future" in business_ideas_db[interest][city]:
                    st.session_state.business_ideas["future"].extend(business_ideas_db[interest][city]["future"])
        
        # Use OpenAI to generate additional personalized ideas if available
        if use_openai and len(interests) > 0 and student_name:
            try:
                # Generate current ideas
                now_prompt = f"Generate 2 simple business ideas for a 1st grader named {student_name} who likes {', '.join(interests)}. These should be things a 1st grader could actually do now with adult supervision. Format as a simple list of just the business names. Keep names very short and simple."
                
                now_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": now_prompt}],
                    max_tokens=100,
                    temperature=0.7
                )
                
                # Parse and add AI-generated current ideas
                ai_now_ideas = now_response.choices[0].message.content.strip().split('\n')
                ai_now_ideas = [idea.strip().strip('.-*123456789') for idea in ai_now_ideas]
                ai_now_ideas = [idea for idea in ai_now_ideas if idea and len(idea) < 50]
                
                st.session_state.business_ideas["now"].extend(ai_now_ideas)
                
                # Generate future ideas
                future_prompt = f"Generate 2 career ideas for when a 1st grader named {student_name} grows up, based on their interests in {', '.join(interests)}. Format as a simple list of just the job titles. Keep names very short and simple."
                
                future_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": future_prompt}],
                    max_tokens=100,
                    temperature=0.7
                )
                
                # Parse and add AI-generated future ideas
                ai_future_ideas = future_response.choices[0].message.content.strip().split('\n')
                ai_future_ideas = [idea.strip().strip('.-*123456789') for idea in ai_future_ideas]
                ai_future_ideas = [idea for idea in ai_future_ideas if idea and len(idea) < 50]
                
                st.session_state.business_ideas["future"].extend(ai_future_ideas)
                
            except Exception as e:
                # If OpenAI fails, just continue with our database ideas
                pass
        
        # Ensure we have unique ideas
        if st.session_state.business_ideas["now"]:
            st.session_state.business_ideas["now"] = list(dict.fromkeys(st.session_state.business_ideas["now"]))[:4]
        
        if st.session_state.business_ideas["future"]:
            st.session_state.business_ideas["future"] = list(dict.fromkeys(st.session_state.business_ideas["future"]))[:4]
        
        # If we end up with no ideas, add some generic ones
        if not st.session_state.business_ideas["now"]:
            st.session_state.business_ideas["now"] = random.sample(fallback_ideas["now"], min(4, len(fallback_ideas["now"])))
        
        if not st.session_state.business_ideas["future"]:
            st.session_state.business_ideas["future"] = random.sample(fallback_ideas["future"], min(4, len(fallback_ideas["future"])))
        
        # Award coins for generating ideas
        if mark_activity_complete("business_ideas_generated"):
            update_progress("session5", 20)
            award_coins(5, "Generating awesome business ideas")
        
        # Force a rerun to show the ideas
        st.rerun()

    
    # Display generated business ideas
    if "business_ideas" in st.session_state and st.session_state.business_ideas:
        st.markdown("""
        <div class="fun-box">
            <h3>Your Business Ideas</h3>
            <p>Here are some business ideas just for you! Click on one to select it.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display "You can start now" ideas
        st.markdown("""
        <div class="section-header">
            Things You Can Start Now! ✨
        </div>
        """, unsafe_allow_html=True)
        
        now_cols = st.columns(2)
        for i, idea in enumerate(st.session_state.business_ideas.get("now", [])):
            with now_cols[i % 2]:
                # Generate a consistent emoji for each idea
                idea_seed = hash(idea) % 10
                idea_emojis = ["🚀", "🎯", "🎨", "🐾", "📚", "🎵", "🏆", "🌟", "🔧", "🍎"]
                idea_emoji = idea_emojis[idea_seed]
                
                st.markdown(f"""
                <div class="business-idea-card">
                    <div style="font-size: 32px; margin-bottom: 10px;">{idea_emoji}</div>
                    <h4>{idea}</h4>
                    <span class="badge badge-green">Start Now</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Add selection button
                if st.button(f"Choose This", key=f"select_now_idea_{i}"):
                    st.session_state.selected_business = idea
                    st.session_state.selected_timeframe = "now"
                    st.session_state.business_names = []  # Clear previous names
                    
                    # Feedback to user
                    st.success(f"You selected: {idea}!")
                    
                    # Force a rerun to proceed to next step
                    st.rerun()


        
        # Display "When you grow up" ideas
        st.markdown("""
        <div class="section-header">
            When You Grow Up! 🔮
        </div>
        """, unsafe_allow_html=True)
        
        future_cols = st.columns(2)
        for i, idea in enumerate(st.session_state.business_ideas.get("future", [])):
            with future_cols[i % 2]:
                # Generate a consistent emoji for each idea
                idea_seed = hash(idea) % 10
                idea_emojis = ["🚀", "🔬", "🏥", "🎓", "🏛️", "💻", "🔧", "🛠️", "📱", "🌎"]
                idea_emoji = idea_emojis[idea_seed]
                
                st.markdown(f"""
                <div class="business-idea-card">
                    <div style="font-size: 32px; margin-bottom: 10px;">{idea_emoji}</div>
                    <h4>{idea}</h4>
                    <span class="badge badge-blue">Future Job</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Add selection button
                if st.button(f"Choose This", key=f"select_future_idea_{i}"):
                    st.session_state.selected_business = idea
                    st.session_state.selected_timeframe = "future"
                    st.session_state.business_names = []  # Clear previous names
                    
                    # Feedback to user
                    st.success(f"You selected: {idea}!")
                    
                    # Force a rerun to proceed to next step
                    st.rerun()

    
    # Add manual continue button if needed
    if "selected_business" in st.session_state and st.session_state.selected_business and not st.session_state.get("business_names", []):
        # Show which business was selected
        st.info(f"You selected: {st.session_state.selected_business}")
        
        # Add a backup continue button
        if st.button("Continue to Name Creator", key="continue_to_naming"):
            st.rerun()

    
    # --------------------------------
    # Step 3: Business Name Generator
    # --------------------------------
    if "selected_business" in st.session_state and st.session_state.selected_business:
        st.markdown("""
        <div class="step-header">
            <span style="font-size: 24px;">✨</span> Step 3: Create a Business Name
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="fun-box">
            <h3>You selected: {st.session_state.selected_business}</h3>
            <p>Now let's create a fun name for your business!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Silliness level slider
        silliness = st.slider(
            "How silly do you want your business name to be?",
            min_value=1,
            max_value=5,
            value=3,
            help="1 = Normal, 5 = Super Silly!"
        )
        
        # Generate business names button
        if st.button("Generate Business Names"):
            if student_name:
                # Use OpenAI if available for more creative names
                if use_openai:
                    try:
                        business_type = st.session_state.selected_business
                        timeframe = st.session_state.get("selected_timeframe", "now")
                        
                        # Create a prompt for OpenAI
                        name_prompt = f"""Generate 5 business names for a {business_type} {'business' if timeframe == 'now' else 'career'} for a 1st grader named {student_name}.
                        
                        Silliness level: {silliness}/5 (where 1 is normal, 5 is super silly)
                        
                        Follow these patterns:
                        - Some names should include "{student_name}'s" at the beginning
                        - Make the names fun and catchy
                        - Keep names simple enough for a 1st grader to read
                        - The higher the silliness level, the more creative and fun the names should be
                        
                        Format as a list with just the names, no numbering or explanations."""
                        
                        name_response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": name_prompt}],
                            max_tokens=150,
                            temperature=0.7
                        )
                        
                        # Parse the names
                        names = name_response.choices[0].message.content.strip().split('\n')
                        names = [name.strip().strip('.-*123456789') for name in names]
                        names = [name for name in names if name]
                        
                        if names:
                            st.session_state.business_names = names[:5]  # Limit to 5 names
                        else:
                            # Fallback to our algorithm if parsing fails
                            raise Exception("Failed to parse names")
                            
                    except Exception as e:
                        # Fallback to our algorithm
                        st.session_state.business_names = generate_business_names(
                            st.session_state.selected_business,
                            student_name,
                            silliness
                        )
                else:
                    # Use our algorithm
                    st.session_state.business_names = generate_business_names(
                        st.session_state.selected_business,
                        student_name,
                        silliness
                    )
            else:
                st.error("Please enter your name first!")
                
            # Force a rerun to show the names
            st.rerun()

        
        # Display generated business names
        if "business_names" in st.session_state and st.session_state.business_names:
            st.markdown("<h4>Pick your favorite business name:</h4>", unsafe_allow_html=True)
            
            for i, name in enumerate(st.session_state.business_names):
                st.markdown(f"""
                <div class="business-name-option">
                    <h4 style="margin: 0;">{name}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Choose This Name", key=f"select_name_{i}"):
                    st.session_state.selected_business_name = name
                    
                    # Award coins for naming business
                    if mark_activity_complete("business_named"):
                        update_progress("session5", 20)
                        award_coins(10, "Creating a perfect business name")
                    
                    # Force a rerun to move to next step
                    st.rerun()

    
    # Add manual continue button if needed
    if "selected_business_name" in st.session_state and st.session_state.selected_business_name and not st.session_state.get("business_advertisement", False):
        # Show which name was selected
        st.info(f"You chose the name: {st.session_state.selected_business_name}")
        
        # Add a backup continue button
        if st.button("Continue to Advertisement Designer", key="continue_to_design"):
            st.rerun()

    
    # --------------------------------
    # Step 4: Business Advertisement Designer
    # --------------------------------
    if "selected_business_name" in st.session_state and st.session_state.selected_business_name:
        st.markdown("""
        <div class="step-header">
            <span style="font-size: 24px;">🎨</span> Step 4: Design Your Business Advertisement
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="fun-box">
            <h3>Design an Advertisement for: {st.session_state.selected_business_name}</h3>
            <p>Create a colorful advertisement to tell people about your business!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Available colors with hex codes for 1st graders
        colors_options = {
            "Red": "#FF5252",
            "Blue": "#448AFF",
            "Green": "#4CAF50",
            "Yellow": "#FFEB3B",
            "Purple": "#9C27B0",
            "Pink": "#FF80AB",
            "Orange": "#FF9800",
            "Teal": "#009688",
            "Light Blue": "#03A9F4",
            "Lime": "#CDDC39"
        }
        
        # Available symbols with meaning for businesses
        symbols_options = [
            "⭐ (Star - for special quality)",
            "🌟 (Sparkle - for something amazing)",
            "🔆 (Bright - for happiness)",
            "🎯 (Target - for goals)",
            "🏆 (Trophy - for being the best)",
            "👍 (Thumbs Up - for good service)",
            "🌈 (Rainbow - for variety)",
            "🌱 (Seedling - for growth)",
            "🛠️ (Tools - for building/fixing)",
            "🤝 (Handshake - for helping)",
            "🎨 (Art - for creativity)",
            "📚 (Books - for knowledge)",
            "🧩 (Puzzle - for problem solving)",
            "🔑 (Key - for solutions)",
            "🎁 (Gift - for special offers)"
        ]
        
        # Color and symbol selection
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Choose your main color by clicking on it:")
            color1_name, color1_hex = create_simple_color_selector(key_prefix="primary_color")

            
            # Tagline input below colors
            tagline = st.text_input("Tagline for your business:", 
                                value=st.session_state.get("business_tagline", "The best service in town!"),
                                key="tagline_input")
            st.session_state.business_tagline = tagline
            
        with col2:
            st.write("Choose your second color by clicking on it:")
            color2_name, color2_hex = create_simple_color_selector(key_prefix="secondary_color")

            
            # This new function will return just the emoji symbol
            selected_symbol = create_symbol_selector(key_prefix="business_symbol")
            
            # Contact information
            contact = st.text_input("How can people contact you?", 
                                value=f"Ask for {student_name}",
                                key="contact_input")
            st.session_state.business_contact = contact

        # Then when you create the preview, use the selected_symbol:
        if st.button("Preview My Business Advertisement", key="preview_ad_button"):
            st.session_state.business_colors = [color1_hex, color2_hex]   
            st.session_state.business_symbol = selected_symbol  # Use the selected symbol directly
            st.session_state.business_advertisement = True
    
            # Use st.rerun() instead of st.experimental_rerun() 
            st.rerun()  # This replaces safe_rerun() or st.experimental_rerun()
            
            # Award coins for designing
            if mark_activity_complete("business_ad_designed"):
                update_progress("session5", 20)
                award_coins(10, "Designing your business advertisement")
                
                # Award achievement if all steps completed
                if is_activity_completed("business_ideas_generated") and is_activity_completed("business_named"):
                    award_achievement("🚀", "Young Entrepreneur", "You created your very own business!")
            
            # Force a rerun to show the ad
            st.rerun()
        
        # Display the preview advertisement
        if "business_advertisement" in st.session_state and st.session_state.business_advertisement:
            st.markdown("""
            <h3 style="text-align: center;">Your Business Advertisement</h3>
            """, unsafe_allow_html=True)
            
            # Use the new function to create a properly rendered advertisement
            create_business_advertisement(
                business_name=st.session_state.selected_business_name,
                business_type=st.session_state.selected_business,
                tagline=st.session_state.business_tagline,
                contact=st.session_state.business_contact,
                symbol=st.session_state.business_symbol,
                color1=st.session_state.business_colors[0],
                color2=st.session_state.business_colors[1]
            )
            
            # Business certificate
            st.markdown("""
            <h3 style="text-align: center;">Your Business Certificate</h3>
            """, unsafe_allow_html=True)
            
            # Generate current date
            current_date = datetime.now().strftime("%B %d, %Y")
            
            st.markdown(f"""
            <div class="certificate">
                <h2 style="color: {PRIMARY_COLOR};">Certificate of Business Creation</h2>
                <p style="font-style: italic; margin-bottom: 20px;">This certifies that</p>
                <h3 style="color: {SECONDARY_COLOR};">{student_name}</h3>
                <p>has successfully created a business called</p>
                <h3 style="color: {PRIMARY_COLOR}; margin: 10px 0;">
                    {st.session_state.selected_business_name}
                </h3>
                <div style="font-size: 64px; margin: 20px 0;">{st.session_state.business_symbol}</div>
                <div style="margin-top: 30px;">
                    <p style="font-weight: bold;">Mr. Stumberg's 1st Grade Class</p>
                    <p>{current_date}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Next steps
            st.markdown("""
            <div class="lesson-box" style="margin-top: 30px;">
                <h3>What You've Learned</h3>
                <p>Congratulations! You've learned how to:</p>
                <ul>
                    <li>Come up with a business idea based on what you like to do</li>
                    <li>Create a catchy name for your business</li>
                    <li>Design a colorful advertisement to tell people about your business</li>
                </ul>
                <p>You're on your way to becoming an entrepreneur!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Final knowledge check
            with st.expander("✅ Check Your Learning"):
                st.markdown("### Review what you've learned about creating a business")
                
                q1 = st.radio(
                    "What is an entrepreneur?",
                    ["Someone who plays sports", "Someone who starts a business", "Someone who teaches school", "Someone who drives a bus"]
                )
                
                if q1 == "Someone who starts a business":
                    st.success("Correct! An entrepreneur is someone who starts and runs their own business.")
                    if mark_activity_complete("session5_q1"):
                        award_coins(5, "Understanding entrepreneurs")
                        update_progress("session5", 10)
                elif q1 != "":
                    st.error("That's not quite right. Think about what we just did in this session!")
                
                q2 = st.radio(
                    "Why is it important to think about what you like to do when creating a business?",
                    ["It doesn't matter what you like", "So you can copy someone else's business", "So your business will be fun for you and use your skills", "So you can make a million dollars"],
                    index=None
                )
                
                if q2 == "So your business will be fun for you and use your skills":
                    st.success("Correct! When you build a business around things you enjoy and are good at, you'll have more fun and do a better job!")
                    if mark_activity_complete("session5_q2"):
                        award_coins(5, "Understanding business planning")
                        update_progress("session5", 10)
                        
                        # Award final super achievement if everything is complete
                        if all(x in st.session_state.completed_activities for x in ["business_ideas_generated", "business_named", "business_ad_designed", "session5_q1"]):
                            award_achievement("🌟", "Financial Literacy Master", "You've completed all activities and learned how to create your own business!")
                elif q2 != "":
                    st.error("That's not quite right. Think about why we started with your interests!")
    
    # If no business idea selected yet, show message
    if not st.session_state.get("business_ideas", {}) and not st.session_state.get("selected_business", ""):
        st.info("👆 Fill in your information above and click 'Generate Business Ideas' to get started!")
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
def create_business_advertisement(business_name, business_type, tagline, contact, symbol, color1, color2):
    """
    Create a properly rendered business advertisement
    
    Parameters:
        business_name: The name of the business
        business_type: Type of business (e.g., Pet Sitting Helper)
        tagline: Slogan for the business
        contact: Contact information
        symbol: Emoji symbol for the business
        color1: Primary color hex code
        color2: Secondary color hex code
    """
    # Use st.markdown with properly structured HTML and unsafe_allow_html=True
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
    
def generate_business_names(business_type, student_name, silliness_level, count=5):
    """Generate business names based on student name, business type, and silliness level"""
    # Extract key words from the business type
    business_keywords = business_type.lower().split()
    
    # Lists of adjectives by silliness level
    adjectives = {
        1: ["Super", "Great", "Good", "Smart", "Helpful"],
        2: ["Amazing", "Awesome", "Fantastic", "Brilliant", "Wonderful"],
        3: ["Spectacular", "Terrific", "Magnificent", "Marvelous", "Extraordinary"],
        4: ["Stupendous", "Colossal", "Phenomenal", "Mind-Blowing", "Ultra"],
        5: ["Absolutely Incredible", "Totally Outrageous", "Ridiculously Amazing", 
            "Extraordinarily Fantastic", "Unbelievably Awesome"]
    }
    
    # Lists of business suffix by silliness level
    business_suffix = {
        1: ["Service", "Helper", "Company", "Business", "Team"],
        2: ["Experts", "Specialists", "Pros", "Stars", "Champions"],
        3: ["Wizards", "Heroes", "Masters", "Legends", "Squad"],
        4: ["Extraordinaires", "Superstars", "Dynamos", "Sensations", "Wonders"],
        5: ["Magnificent Marvels", "Spectacular Specialists", "Dynamic Dynamos", 
            "Fantastic Phenoms", "Tremendous Titans"]
    }
    
    names = []
    
    # Formula 1: [Student's Name]'s [Business Type]
    names.append(f"{student_name}'s {business_type}")
    
    # Formula 2: [Student's Name]'s [Adjective] [Business Type]
    adj = random.choice(adjectives[min(silliness_level, 5)])
    names.append(f"{student_name}'s {adj} {business_type}")
    
    # Formula 3: [Adjective] [Keyword from Business] [Suffix]
    for _ in range(count - 2):
        adj = random.choice(adjectives[min(silliness_level, 5)])
        keyword = random.choice(business_keywords) if business_keywords else business_type
        suffix = random.choice(business_suffix[min(silliness_level, 5)])
        
        # Capitalize the keyword
        keyword = keyword.capitalize()
        
        names.append(f"{student_name}'s {adj} {keyword} {suffix}")
    
    return names