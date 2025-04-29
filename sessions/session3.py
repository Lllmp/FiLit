import streamlit as st
from utils import (
    award_coins, 
    award_achievement, 
    update_progress, 
    mark_activity_complete, 
    is_activity_completed,
    create_quiz_question,  # Add this import to all session files
    safe_rerun  # Use this instead of st.experimental_rerun
)
from styles import apply_session_goals_styling


def run():
    """
    Session 3: Businesses All Around the Neighborhood
    
    Objectives:
    - Define entrepreneur, goods and services
    - Interpret map symbols
    - Identify the goods and services businesses provide
    """
    st.header("🏪 Session 3: Businesses Around Grimes")
    
    # Session overview

    # List of goals for this session
    goals = [
        "Learn about businesses in Grimes, Iowa<",
        "Understand what goods and services are",
        "Discover how entrepreneurs start businesses"
    ]

    # Apply styled session goals
    apply_session_goals_styling(goals)
    
    # Key vocabulary for this section
    st.subheader("📝 Important Words to Know")
    
    vocab_col1, vocab_col2, vocab_col3 = st.columns(3)
    
    with vocab_col1:
        st.markdown("""
        <div class="vocabulary-card">
            <h4>Business</h4>
            <p>A place that sells goods or services to make money.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with vocab_col2:
        st.markdown("""
        <div class="vocabulary-card">
            <h4>Goods</h4>
            <p>Things that businesses make or sell, like toys, food, or clothes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with vocab_col3:
        st.markdown("""
        <div class="vocabulary-card">
            <h4>Services</h4>
            <p>Help or work that businesses do for people, like cutting hair, fixing cars, or teaching.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Entrepreneur definition
    st.markdown("""
    <div class="vocabulary-card">
        <h4>Entrepreneur</h4>
        <p>A person who starts a business. Entrepreneurs come up with new ideas and work hard to make their businesses successful.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grimes business map - Interactive
    st.subheader("🗺️ Businesses in Grimes, Iowa")
    
    st.markdown("""
    <div class="fun-box">
        <h3>Explore Businesses in Grimes!</h3>
        <p>Click on businesses to learn what they do.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Local Grimes businesses data - expanded with more details and categories
    grimes_businesses = [
        {
            "name": "Fareway", 
            "type": "Grocery Store", 
            "category": "Goods", 
            "description": "A grocery store that sells food, drinks, and household items to families in Grimes.",
            "location": "351 Gateway Dr, Grimes, IA",
            "icon": "🛒"
        },
        {
            "name": "Awakening Coffee", 
            "type": "Coffee Shop", 
            "category": "Goods & Services", 
            "description": "A coffee shop that serves coffee drinks, tea, and pastries. People can relax and meet friends there.",
            "location": "310 SE Main St, Grimes, IA",
            "icon": "☕"
        },
        {
            "name": "Mustang Sports Cards", 
            "type": "Sports Cards & Collectibles", 
            "category": "Goods", 
            "description": "A store that sells sports cards, collectibles, and memorabilia to sports fans of all ages.",
            "location": "1461 SE Meadowlark Cir #1, Grimes, IA",
            "icon": "🏀"
        },
        {
            "name": "Al's Dairy Freeze", 
            "type": "Ice Cream Shop", 
            "category": "Goods", 
            "description": "An ice cream shop that serves ice cream cones, sundaes, and other frozen treats to the community.",
            "location": "500 S Gear St, West Burlington, IA",
            "icon": "🍦"
        },
        {
            "name": "The Grimes Public Library", 
            "type": "Library", 
            "category": "Services", 
            "description": "A place where people can borrow books, use computers, and join fun activities for children and adults.",
            "location": "Grimes Public Library, Grimes, IA",
            "icon": "📚"
        },
        {
            "name": "Dallas Center-Grimes Schools", 
            "type": "School", 
            "category": "Services", 
            "description": "Schools where children learn important subjects, make friends, and prepare for their future.",
            "location": "2405 W 1st St, Grimes, IA",
            "icon": "🏫"
        },
        {
            "name": "Edward Jones - Financial Advisor", 
            "type": "Financial Services", 
            "category": "Services", 
            "description": "A business that helps people save money, plan for retirement, and manage their finances.",
            "location": "102 SE Jacob St, Grimes, IA",
            "icon": "💰"
        },
        {
            "name": "Waterfront Seafood Market", 
            "type": "Seafood Market & Restaurant", 
            "category": "Goods & Services", 
            "description": "A place where people can buy fresh seafood or eat seafood dishes in the restaurant.",
            "location": "2414 SE Grimes Blvd, Grimes, IA",
            "icon": "🐟"
        }
    ]
    
    # Initialize the selected business in session state if not already there
    if 'selected_business_idx' not in st.session_state:
        st.session_state.selected_business_idx = None
    
    # Business directory - Display all businesses as cards
    business_cols = st.columns(4)
    for i, business in enumerate(grimes_businesses):
        with business_cols[i % 4]:
            # Determine badge color
            if business["category"] == "Goods":
                badge_class = "badge-blue"
            elif business["category"] == "Services":
                badge_class = "badge-green"
            else:
                badge_class = "badge-yellow"
            
            st.markdown(f"""
            <div class="card">
                <div style="font-size: 32px; text-align: center; margin-bottom: 10px;">{business["icon"]}</div>
                <h4 style="margin-top: 0; text-align: center;">{business["name"]}</h4>
                <span class="badge {badge_class}">{business["category"]}</span>
                <p style="font-size: 14px; margin-top: 5px;">{business["type"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Button to learn more
            if st.button(f"Learn More", key=f"business_{i}"):
                st.session_state.selected_business_idx = i
                # Mark activity as completed
                if mark_activity_complete("explored_business"):
                    award_coins(2, "Learning about a local business")
                    update_progress("session3", 10)
    
    # Display selected business details
    if st.session_state.selected_business_idx is not None:
        business = grimes_businesses[st.session_state.selected_business_idx]
        
        # Determine badge class for the selected business
        if business["category"] == "Goods":
            badge_class = "badge-blue"
        elif business["category"] == "Services":
            badge_class = "badge-green"
        else:
            badge_class = "badge-yellow"
        
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; margin-top: 20px; animation: fadeIn 0.5s ease-in-out;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 48px; margin-right: 20px;">{business["icon"]}</div>
                <div>
                    <h2 style="margin: 0;">{business["name"]}</h2>
                    <p style="margin: 5px 0 0 0;">{business["type"]}</p>
                </div>
            </div>
            
            <div style="margin: 20px 0;">
                <span class="badge {badge_class}">{business["category"]}</span>
                <p style="margin-top: 10px;">{business["description"]}</p>
                <p><strong>Location:</strong> {business["location"]}</p>
            </div>
            
            <div style="margin-top: 20px;">
                <h4>What People Get Here:</h4>
                <ul>
                    {f"<li>Products to buy</li>" if "Goods" in business["category"] else ""}
                    {f"<li>Help from workers</li>" if "Services" in business["category"] else ""}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Button to go back to the directory
        if st.button("Back to Directory"):
            st.session_state.selected_business_idx = None
            st.rerun()
    
    # Goods vs Services Activity
    st.subheader("🛍️ Goods vs. Services Game")
    
    st.markdown("""
    <div class="fun-box">
        <h3>Can You Tell the Difference?</h3>
        <p>Some businesses sell goods (things you can touch) and some provide services (help or work they do).<br>Can you tell which is which?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Goods vs Services examples
    examples = [
        {"item": "Haircut", "answer": "Service", "icon": "✂️"},
        {"item": "Pizza", "answer": "Good", "icon": "🍕"},
        {"item": "Car Wash", "answer": "Service", "icon": "🚗"},
        {"item": "Book", "answer": "Good", "icon": "📕"},
        {"item": "Doctor Visit", "answer": "Service", "icon": "👨‍⚕️"},
        {"item": "Toy", "answer": "Good", "icon": "🧸"},
        {"item": "Music Lesson", "answer": "Service", "icon": "🎵"},
        {"item": "Ice Cream Cone", "answer": "Good", "icon": "🍦"}
    ]
    
    # Initialize answers if they don't exist
    if 'goods_services_answers' not in st.session_state:
        st.session_state.goods_services_answers = {}
    
    # Check if all questions have been answered
    all_answered = len(st.session_state.goods_services_answers) == len(examples)
    
    # Column layout for questions
    if not all_answered:
        q_cols = st.columns(2)
        for i, example in enumerate(examples):
            item = example["item"]
            # Skip if already answered
            if item in st.session_state.goods_services_answers:
                continue
                
            with q_cols[i % 2]:
                st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 10px;">{example["icon"]}</div>
                    <h4>{item}</h4>
                    <p>Is this a good or a service?</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Good", key=f"good_{item}"):
                        st.session_state.goods_services_answers[item] = "Good"
                        st.rerun()
                with col2:
                    if st.button("Service", key=f"service_{item}"):
                        st.session_state.goods_services_answers[item] = "Service"
                        st.rerun()
    
    # Display results if all questions answered
    if all_answered:
        # Count correct answers
        correct = 0
        for example in examples:
            item = example["item"]
            if item in st.session_state.goods_services_answers and st.session_state.goods_services_answers[item] == example["answer"]:
                correct += 1
        
        # Display results
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; text-align: center; margin-top: 20px;">
            <h3>Your Score: {correct}/{len(examples)}</h3>
            <p>You got {correct} out of {len(examples)} items correct!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display answers
        st.markdown("### Let's review the answers:")
        
        review_cols = st.columns(4)
        for i, example in enumerate(examples):
            with review_cols[i % 4]:
                item = example["item"]
                user_answer = st.session_state.goods_services_answers.get(item, "")
                correct_answer = example["answer"]
                is_correct = user_answer == correct_answer
                
                st.markdown(f"""
                <div style="background-color: {'#e6ffe6' if is_correct else '#ffe6e6'}; padding: 15px; border-radius: 10px; margin-bottom: 15px; text-align: center;">
                    <div style="font-size: 24px; margin-bottom: 5px;">{example["icon"]}</div>
                    <h4 style="margin: 5px 0;">{item}</h4>
                    <p style="margin: 5px 0;">Your answer: <strong>{user_answer}</strong></p>
                    <p style="margin: 5px 0;">Correct answer: <strong>{correct_answer}</strong></p>
                    <div style="font-size: 24px; margin-top: 5px;">
                        {"✅" if is_correct else "❌"}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Award coins if not already awarded
        if mark_activity_complete("goods_services_game"):
            coins_earned = correct * 2
            award_coins(coins_earned, f"Getting {correct} answers correct in the Goods vs. Services game")
            
            # Update progress
            update_progress("session3", 40)
            
            # Award achievement if they did well
            if correct >= 6:
                award_achievement("🛍️", "Business Basics Pro", "You know the difference between goods and services!")
        
        # Play again button
        if st.button("Play Again"):
            st.session_state.goods_services_answers = {}
            st.rerun()
    
    # Entrepreneur spotlight
    st.subheader("👨‍💼 Entrepreneur Spotlight")
    
    st.markdown("""
    <div class="fun-box">
        <h3>Meet Local Entrepreneurs!</h3>
        <p>These people started businesses right here in Grimes!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple profiles of made-up entrepreneurs
    entrepreneurs = [
        {
            "name": "Ms. Johnson",
            "business": "Awakening Coffee",
            "story": "Ms. Johnson loved making coffee for her friends. She started Awakening Coffee so everyone in Grimes could enjoy her delicious drinks!",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWAQMAAABrSHpRAAAABlBMVEXh4eH///8Z1D2NAAAA+ElEQVRIx+2UsQ3DMAwEqcVL0AGcRvBQXsIDuFGK9JAhkq1Twp8YiQCd+5fPv5NZnrk5K0+xANnmXPFo6IJzfcWsnIwjA4USVwplGcPJIiaFihMXzkJJoSLHhdJCjaOQm0qoJngVysxMoQJwFup0e//aPbqMQtkKhdO+7FVhvoTBs77IwBJXKFgVRQbWlUUGluBCJUrBLcGFCqyLwiwZd6HqQq0LlUMlPK3hKpTlZmEDZeEolHFZEKVgYaHgQK0LVRcqL5QFkxJX8r6oOKHiQvlkm4uKE1RcWBcVlm+hhMvCQvlkm7OtY5ZQlMLxkIMKZaFOReWZp5gUWcwH0kXWoDQvN3MAAAAASUVORK5CYII="
        },
        {
            "name": "Mr. Rodriguez",
            "business": "Mustang Sports Cards",
            "story": "Mr. Rodriguez collected sports cards as a kid. Now he runs a shop where people can find rare cards and share their love of sports!",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWAQMAAABrSHpRAAAABlBMVEXh4eH///8Z1D2NAAAA+ElEQVRIx+2UvQ3EIAyFsRgFA7AUKRBDMEC6AqVjiExww0vXJMrPkc+5NtKT5c/m+XeyyzN3Z+0pliBbnCs+TV1wrm/YKifjyEChxJVCWcZwsohJoeLEhbNQUqjIcaG0UOOo5KYSahpeC2VmplABOAt1ur1/7R5dRqFshcJpX/baMF9iPOuLHFjiCg1WR5GDdWWRgyW4UIlScEtwowKr4jBLxl2otqHODZVDJzyt4WqUZYvCBsriKJRxWxClYGGj4EAdG6ptqLpRFkxKXMn7puIEFTfWRYflWyhhtTBTPtnhbOuYJRSl2OqII7JRpiJ7gUWRxXwAXWQNSrMZ7z8AAAAASUVORK5CYII="
        }
    ]
    
    # Display entrepreneurs
    entre_cols = st.columns(2)
    for i, entrepreneur in enumerate(entrepreneurs):
        with entre_cols[i]:
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; align-items: center;">
                    <img src="{entrepreneur['image']}" style="width: 80px; height: 80px; border-radius: 50%; margin-right: 15px;">
                    <div>
                        <h4 style="margin: 0;">{entrepreneur['name']}</h4>
                        <p style="margin: 5px 0 0 0;">Owner of {entrepreneur['business']}</p>
                    </div>
                </div>
                <p style="margin-top: 15px;">{entrepreneur['story']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Learn About {entrepreneur['name']}", key=f"entrepreneur_{i}"):
                if mark_activity_complete(f"entrepreneur_{i}"):
                    award_coins(3, f"Learning about {entrepreneur['name']}'s business journey")
                    update_progress("session3", 5)
    
    # Steps to become an entrepreneur
    st.markdown("""
    <div style="background-color: white; padding: 20px; border-radius: 15px; margin-top: 20px;">
        <h3 style="text-align: center;">How to Become an Entrepreneur</h3>
        
        <div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-top: 20px;">
            <div style="text-align: center; width: 150px; margin-bottom: 20px;">
                <div style="font-size: 40px;">💡</div>
                <h4>1. Have an Idea</h4>
                <p>Think of something people need or want</p>
            </div>
            <div style="text-align: center; width: 150px; margin-bottom: 20px;">
                <div style="font-size: 40px;">📝</div>
                <h4>2. Make a Plan</h4>
                <p>Plan how your business will work</p>
            </div>
            <div style="text-align: center; width: 150px; margin-bottom: 20px;">
                <div style="font-size: 40px;">💵</div>
                <h4>3. Get Money</h4>
                <p>Find money to start your business</p>
            </div>
            <div style="text-align: center; width: 150px; margin-bottom: 20px;">
                <div style="font-size: 40px;">🚀</div>
                <h4>4. Start Working</h4>
                <p>Open your business and work hard</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Knowledge check
    with st.expander("✅ Check Your Learning"):
        st.markdown("### Review what you've learned about businesses")
        
        q1 = st.radio(
            "What is an entrepreneur?",
            ["Someone who rides a bus", "Someone who starts a business", "Someone who reads books", "Someone who plays sports"],
            index=None
        )
        
        if q1 == "Someone who starts a business":
            st.success("Correct! An entrepreneur is someone who starts a business.")
            if mark_activity_complete("session3_q1"):
                award_coins(5, "Understanding what an entrepreneur is")
                update_progress("session3", 20)
        elif q1 != "":
            st.error("That's not quite right. Think about the people who start businesses.")
        
        q2 = st.radio(
            "Which of these is an example of a service?",
            ["A toy", "A sandwich", "A shoe", "A haircut"],
            index=None
        )
        
        if q2 == "A haircut":
            st.success("Correct! A haircut is a service because someone is doing work for you.")
            if mark_activity_complete("session3_q2"):
                award_coins(5, "Identifying services correctly")
                update_progress("session3", 20)
                
                # Award achievement if both questions correct
                if is_activity_completed("session3_q1") and is_activity_completed("goods_services_game"):
                    award_achievement("🏪", "Business Expert", "You understand businesses, goods, services, and entrepreneurs!")