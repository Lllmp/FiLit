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
    st.header("👪 Session 1: All Kinds of Families")

    goals = [
        "Learn how families are alike and different",
        "Discover how families work together",
        "Explore how families help the community"
    ]
    apply_session_goals_styling(goals)

    st.subheader("🏠 Families in Our Community")
    family_col1, family_col2 = st.columns([3, 2])

    with family_col1:
        st.markdown("""
        <div class="fun-box">
            <h3>Family Members Help Each Other</h3>
            <p>Families come in all shapes and sizes! In each family, people have different jobs to help each other.</p>
        </div>
        """, unsafe_allow_html=True)

        family_roles = {
            "Parents/Guardians": ["Work to earn money", "Cook meals", "Help with homework", "Take care of the home"],
            "Children": ["Help with chores", "Learn at school", "Help younger siblings", "Keep their rooms clean"],
            "Grandparents": ["Share wisdom", "Help with childcare", "Tell family stories", "Teach traditions"],
            "Everyone": ["Be kind to each other", "Help neighbors", "Save money", "Support the community"]
        }

        selected_role = st.selectbox("Select a family member:", list(family_roles.keys()))
        st.markdown(f"""
        <div class="card">
            <h4>How {selected_role} Help Their Family:</h4>
            <ul>
                {"".join([f"<li>{task}</li>" for task in family_roles[selected_role]])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with family_col2:
        st.markdown("<h4>Draw Your Family</h4>", unsafe_allow_html=True)
        st.markdown("(Pretend this is a drawing area)")
        family_members = st.text_input("Who is in your family?", placeholder="Example: Mom, Dad, brother, sister, me")

        if family_members:
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 10px; border: 2px dashed #FF5C8D;">
                <p style="margin: 0;">My Family: {family_members}</p>
            </div>
            """, unsafe_allow_html=True)
            if mark_activity_complete("family_members_input"):
                award_coins(2, "Sharing about your family")
                update_progress("session1", 10)

    st.subheader("💰 How Families and Money Work Together")
    st.markdown("""
    <div class="fun-box">
        <h3>Families and the Economy</h3>
        <p>Families are an important part of the economy! The economy is how people make, buy, and sell things.</p>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 20px;">
            <div style="text-align: center; width: 150px;"><div style="font-size: 40px;">💼</div><p><b>Work</b><br>Family members work at jobs</p></div>
            <div style="text-align: center; width: 150px;"><div style="font-size: 40px;">💵</div><p><b>Earn</b><br>They earn money from jobs</p></div>
            <div style="text-align: center; width: 150px;"><div style="font-size: 40px;">🛒</div><p><b>Spend</b><br>They buy things they need</p></div>
            <div style="text-align: center; width: 150px;"><div style="font-size: 40px;">🏦</div><p><b>Save</b><br>They save money for later</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 💸 Family Money Flow Activity")
    money_earned = st.slider("How much money does your family earn in a week?", 10, 100, 50, 5)
    st.markdown("#### How would your family spend this money?")

    spend_home = st.slider("Home (rent or house payment)", 0, money_earned, money_earned // 3)
    remaining = money_earned - spend_home
    spend_food = st.slider("Food for the family", 0, remaining, remaining // 3)
    remaining -= spend_food
    spend_transportation = st.slider("Transportation (car, bus, gas)", 0, remaining, remaining // 3)
    remaining -= spend_transportation
    spend_fun = st.slider("Fun activities", 0, remaining, remaining // 4)
    remaining -= spend_fun
    spend_savings = remaining

    total = money_earned
    home_percent = int((spend_home / total) * 100)
    food_percent = int((spend_food / total) * 100)
    transport_percent = int((spend_transportation / total) * 100)
    fun_percent = int((spend_fun / total) * 100)
    savings_percent = int((spend_savings / total) * 100)

    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 15px; margin-top: 20px;">
        <h4 style="text-align: center;">Your Family Budget</h4>
        <div style="display: flex; margin-bottom: 15px;">
            <div style="background-color: #4361EE; width: {home_percent}%; height: 30px; color: white;">Home</div>
            <div style="background-color: #FF5C8D; width: {food_percent}%; height: 30px; color: white;">Food</div>
            <div style="background-color: #06D6A0; width: {transport_percent}%; height: 30px; color: white;">Transport</div>
            <div style="background-color: #FFD166; width: {fun_percent}%; height: 30px; color: #212529;">Fun</div>
            <div style="background-color: #20B2AA; width: {savings_percent}%; height: 30px; color: white;">Savings</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Submit My Family Budget"):
        if mark_activity_complete("family_budget_activity"):
            award_coins(5, "Creating your family budget")
            update_progress("session1", 30)
            st.success("Great job planning your family budget! Notice how families need to spend money on needs first, then wants, and also save some money for later.")

    st.subheader("🏘️ Families in Grimes")
    st.markdown("""
    <div class="fun-box">
        <h3>Families Help Our Community</h3>
        <p>Families in Grimes help make our community better in many ways!</p>
    </div>
    """, unsafe_allow_html=True)

    family_contributions = [
        {"title": "Shopping at Local Stores", "description": "When families shop at stores in Grimes, they help store owners earn money to support their families.", "icon": "🛍️"},
        {"title": "Working at Local Jobs", "description": "Family members work at businesses, schools, and other places in Grimes to help our community.", "icon": "💼"},
        {"title": "Helping Neighbors", "description": "Families in Grimes help each other when someone needs assistance.", "icon": "🤝"},
        {"title": "Supporting Schools", "description": "Families support schools like Mr. Stumberg's class by helping with homework and school events.", "icon": "🏫"},
        {"title": "Keeping Grimes Clean", "description": "Families help keep parks, streets, and public places in Grimes clean and beautiful.", "icon": "🌳"}
    ]

    contrib_cols = st.columns(3)
    for i, contribution in enumerate(family_contributions):
        with contrib_cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <div style="font-size: 32px; text-align: center;">{contribution['icon']}</div>
                <h4 style="text-align: center;">{contribution['title']}</h4>
                <p>{contribution['description']}</p>
            </div>
            """, unsafe_allow_html=True)

    # ✅ UPDATED Knowledge Checks using create_quiz_question()
    with st.expander("✅ Check Your Learning"):
        st.markdown("### Review what you've learned")
        create_quiz_question(
            question="What is one way families help the economy?",
            options=["They play games together", "They work at jobs and earn money", "They ride bikes", "They sleep at night"],
            correct_answer="They work at jobs and earn money",
            correct_message="Correct! When family members work at jobs, they earn money that they can use to buy things they need and want.",
            incorrect_message="Not quite. Think about how families get money to buy things.",
            activity_key="session1_q1",
            coins=5,
            reason="Answering correctly about families and the economy",
            progress=25
        )

    with st.expander("✅ Check Your Learning"):
        st.markdown("### Review what you've learned about families and community")
        create_quiz_question(
            question="How do families in Grimes help the community?",
            options=["By sleeping all day", "By moving to a different city", "By shopping at local stores and working at local jobs", "By never leaving their homes"],
            correct_answer="By shopping at local stores and working at local jobs",
            correct_message="Correct! When families shop and work locally, they help the Grimes community thrive.",
            incorrect_message="Not quite. Think about what makes a community stronger.",
            activity_key="session1_q2",
            coins=5,
            reason="Answering correctly about families in the community",
            progress=25
        )

        # Award achievement if both questions complete
        if is_activity_completed("session1_q1") and is_activity_completed("session1_q2"):
            award_achievement("👪", "Family Expert", "You understand how families work together and help the community!")

    # Final session completion check
    if is_activity_completed("family_members_input") and \
       is_activity_completed("family_budget_activity") and \
       is_activity_completed("session1_q1") and \
       is_activity_completed("session1_q2"):
        st.session_state.progress["session1"] = 100
