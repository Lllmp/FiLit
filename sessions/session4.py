import streamlit as st
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
from styles import apply_session_goals_styling
from collections import Counter

def run():
    """
    Session 4: Jobs Around the Neighborhood
    
    Objectives:
    - Identify the jobs people do
    - Analyze their own skills to determine ways they can support family members
    """
    st.header("👩‍🏫 Session 4: Jobs in Our Community")
    
    # Session overview
    goals = [
        "Learn about different jobs people do in Grimes",
        "Discover the skills needed for different jobs",
        "Explore jobs you might want to do when you grow up"
    ]

    # Apply styled session goals
    apply_session_goals_styling(goals)
    
    # Jobs in our community
    st.subheader("👨‍👩‍👧‍👦 Jobs Help Families and Communities")
    
    st.markdown("""
    <div class="fun-box">
        <h3>Why Jobs Are Important</h3>
        <p>Jobs help in two important ways:</p>
        <ol>
            <li>Jobs help people earn money for their families</li>
            <li>Jobs provide goods and services that the community needs</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Jobs in Grimes
    st.subheader("🏙️ Jobs in Grimes, Iowa")
    
    # Job categories - cached for performance
    @st.cache_data
    def load_job_categories():
        return {
            "Healthcare": ["Doctor", "Nurse", "Dentist", "Pharmacist", "Veterinarian"],
            "Education": ["Teacher", "Principal", "Librarian", "School Counselor", "Coach"],
            "Business": ["Store Owner", "Manager", "Bank Teller", "Accountant", "Salesperson"],
            "Food Service": ["Chef", "Baker", "Server", "Grocery Store Worker", "Farmer"],
            "Public Service": ["Police Officer", "Firefighter", "Mail Carrier", "Mayor", "Park Ranger"],
            "Building & Fixing": ["Construction Worker", "Electrician", "Plumber", "Car Mechanic", "Carpenter"]
        }
    
    job_categories = load_job_categories()
    
    # Select job category
    job_category = st.selectbox("Choose a job category to explore:", list(job_categories.keys()), key="job_category")
    
    # Define appropriate emojis for each job
    @st.cache_data
    def get_job_icons():
        return {
            "Doctor": "👨‍⚕️", "Nurse": "👩‍⚕️", "Dentist": "🦷", "Pharmacist": "💊", "Veterinarian": "🐶",
            "Teacher": "👨‍🏫", "Principal": "👩‍💼", "Librarian": "📚", "School Counselor": "🧠", "Coach": "🏆",
            "Store Owner": "🏪", "Manager": "📋", "Bank Teller": "🏦", "Accountant": "🧮", "Salesperson": "🛍️",
            "Chef": "👨‍🍳", "Baker": "🍞", "Server": "🍽️", "Grocery Store Worker": "🛒", "Farmer": "🚜",
            "Police Officer": "👮‍♀️", "Firefighter": "👨‍🚒", "Mail Carrier": "📬", "Mayor": "🏛️", "Park Ranger": "🌲",
            "Construction Worker": "👷‍♂️", "Electrician": "⚡", "Plumber": "🔧", "Car Mechanic": "🔧", "Carpenter": "🪚"
        }
    
    job_icons = get_job_icons()
    
    # Display jobs with proper formatting
    selected_jobs = job_categories[job_category]
    
    # Fixed job card display
    st.markdown('<div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-top: 20px;">', unsafe_allow_html=True)
    
    for job in selected_jobs:
        emoji = job_icons.get(job, "💼")
        
        st.markdown(f"""
        <div style="text-align: center; width: 150px; margin-bottom: 20px; background-color: rgba(255,255,255,0.1); 
                    border-radius: 15px; padding: 20px; transition: all 0.3s ease;">
            <div style="font-size: 40px;">{emoji}</div>
            <h4 style="color: #FF5C8D; margin: 10px 0;">{job}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Job exploration activity
    st.subheader("🔍 Explore a Job")
    
    # Job details - cached for performance
    @st.cache_data
    def get_job_details():
        return {
            "Teacher": {
                "what_they_do": "Teachers help students learn important subjects like reading, math, science, and more. They plan lessons, grade assignments, and help students understand new things.",
                "skills_needed": ["Patience", "Communication", "Knowledge", "Organization", "Creativity"],
                "tools_used": ["Books", "Computers", "Whiteboards", "Art Supplies", "Educational Games"],
                "where_they_work": ["Schools", "Classrooms", "Sometimes outdoors for activities"],
                "how_they_help": "Teachers help children learn the skills they need for their future. They inspire students and help them discover their talents and interests.",
                "icon": "👨‍🏫"
            },
            "Doctor": {
                "what_they_do": "Doctors help people stay healthy and treat them when they're sick or injured. They examine patients, diagnose problems, and prescribe medicine.",
                "skills_needed": ["Medical Knowledge", "Problem Solving", "Communication", "Attention to Detail", "Compassion"],
                "tools_used": ["Stethoscope", "Medical Equipment", "Computers", "Medicine", "X-ray Machines"],
                "where_they_work": ["Hospitals", "Clinics", "Doctor's Offices"],
                "how_they_help": "Doctors keep people healthy and save lives. They help people feel better when they're sick and teach them how to stay healthy.",
                "icon": "👨‍⚕️"
            },
            "Firefighter": {
                "what_they_do": "Firefighters protect people, animals, and buildings from fires. They also help during emergencies like car accidents or natural disasters.",
                "skills_needed": ["Bravery", "Physical Strength", "Quick Thinking", "Teamwork", "First Aid Knowledge"],
                "tools_used": ["Fire Trucks", "Water Hoses", "Ladders", "Protective Gear", "Rescue Equipment"],
                "where_they_work": ["Fire Stations", "Emergency Scenes", "In the community for education"],
                "how_they_help": "Firefighters save lives and protect property. They also teach people about fire safety to prevent fires from happening.",
                "icon": "👨‍🚒"
            },
            "Chef": {
                "what_they_do": "Chefs create and cook delicious meals for people. They plan menus, prepare ingredients, cook food, and make sure everything tastes good.",
                "skills_needed": ["Cooking Knowledge", "Creativity", "Time Management", "Cleanliness", "Tasting Ability"],
                "tools_used": ["Knives", "Pots & Pans", "Ovens", "Recipe Books", "Measuring Tools"],
                "where_they_work": ["Restaurants", "Hotels", "Schools", "Hospitals", "Catering Companies"],
                "how_they_help": "Chefs feed people and make special moments more enjoyable with delicious food. They create recipes and introduce people to new flavors.",
                "icon": "👨‍🍳"
            },
            "Police Officer": {
                "what_they_do": "Police officers keep people safe and enforce laws. They patrol areas, respond to emergencies, investigate crimes, and help people in trouble.",
                "skills_needed": ["Bravery", "Communication", "Problem Solving", "Fairness", "Physical Fitness"],
                "tools_used": ["Police Car", "Radio", "Computer", "Uniform", "Safety Equipment"],
                "where_they_work": ["Police Stations", "In patrol cars", "Throughout the community"],
                "how_they_help": "Police officers protect people and make sure everyone follows the rules. They help when there are emergencies and teach people about safety.",
                "icon": "👮‍♀️"
            }
        }
    
    job_details = get_job_details()
    
    # Select a job to explore
    selected_job = st.selectbox("Choose a job to learn more about:", list(job_details.keys()), key="selected_job")
    
    # Display job details
    try:
        job = job_details[selected_job]
        
        # Create a nicer card layout
        st.markdown("""
        <style>
        .job-details-card {
            background-color: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
        }
        .job-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .job-icon {
            font-size: 48px;
            margin-right: 20px;
        }
        .job-section {
            margin-bottom: 15px;
        }
        .job-section-title {
            font-weight: bold;
            margin-bottom: 8px;
            color: #4EA5FF;
        }
        .badge-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }
        .badge {
            background-color: #448AFF;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 14px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Job card with icon and title
        st.markdown(f"""
        <div class="job-details-card">
            <div class="job-header">
                <div class="job-icon">{job["icon"]}</div>
                <h3>{selected_job}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # What they do section
        st.markdown(f"""
            <div class="job-section">
                <div class="job-section-title">What they do:</div>
                <p>{job["what_they_do"]}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Skills needed section
        st.markdown(f"""
            <div class="job-section">
                <div class="job-section-title">Skills needed:</div>
                <div class="badge-container">
                    {''.join([f'<span class="badge">{skill}</span>' for skill in job["skills_needed"]])}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Tools they use section
        tools_list = ''.join([f"<li>{tool}</li>" for tool in job["tools_used"]])
        st.markdown(f"""
            <div class="job-section">
                <div class="job-section-title">Tools they use:</div>
                <ul>
                    {tools_list}
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        # Where they work section
        st.markdown(f"""
            <div class="job-section">
                <div class="job-section-title">Where they work:</div>
                <p>{", ".join(job["where_they_work"])}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # How they help section
        st.markdown(f"""
            <div class="job-section">
                <div class="job-section-title">How they help the community:</div>
                <p>{job["how_they_help"]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mark activity as completed if they've explored a job
        if st.button("I've learned about this job!", type="primary"):
            if mark_activity_complete(f"explored_job_{selected_job}"):
                award_coins(5, f"Learning about what {selected_job}s do")
                update_progress("session4", 15)
                
    except Exception as e:
        st.error(f"Error displaying job details: {e}")
        st.info("Please try selecting a different job or refresh the page.")
    
    # Career interests
    st.subheader("🔮 What Job Would You Like?")
    
    st.markdown("""
    <div class="fun-box">
        <h3>Jobs I Might Like</h3>
        <p>Think about jobs you might want to do when you grow up!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Career interest quiz
    st.markdown("### Take a Fun Career Quiz!")
    
    # Quiz questions
    q1 = st.radio(
        "What do you like to do most?",
        ["Help people", "Make or build things", "Solve problems", "Create art or stories", "Work with animals"],
        key="career_q1"
    )
    
    q2 = st.radio(
        "Where would you like to work?",
        ["Inside a building", "Outside in nature", "In different places each day", "At a school", "In a restaurant or store"],
        key="career_q2"
    )
    
    q3 = st.radio(
        "What school subject do you like best?",
        ["Math", "Science", "Reading", "Art", "Physical Education"],
        key="career_q3"
    )
    
    # Career recommendations based on quiz
    if st.button("Find Jobs I Might Like!", type="primary"):
        # Simple mapping of answers to job recommendations
        recommendations = []
        
        # Question 1 mapping
        if q1 == "Help people":
            recommendations.extend(["Doctor", "Nurse", "Teacher", "Police Officer"])
        elif q1 == "Make or build things":
            recommendations.extend(["Construction Worker", "Engineer", "Carpenter", "Chef"])
        elif q1 == "Solve problems":
            recommendations.extend(["Scientist", "Detective", "Computer Programmer", "Engineer"])
        elif q1 == "Create art or stories":
            recommendations.extend(["Artist", "Writer", "Musician", "Graphic Designer"])
        elif q1 == "Work with animals":
            recommendations.extend(["Veterinarian", "Zookeeper", "Marine Biologist", "Pet Groomer"])
        
        # Question 2 mapping (add weight to previous recommendations)
        if q2 == "Inside a building":
            recommendations.extend(["Teacher", "Office Worker", "Librarian", "Chef"])
        elif q2 == "Outside in nature":
            recommendations.extend(["Park Ranger", "Landscaper", "Farmer", "Environmental Scientist"])
        elif q2 == "In different places each day":
            recommendations.extend(["Delivery Driver", "Travel Writer", "Construction Worker", "Sales Representative"])
        elif q2 == "At a school":
            recommendations.extend(["Teacher", "Principal", "School Counselor", "Coach"])
        elif q2 == "In a restaurant or store":
            recommendations.extend(["Chef", "Server", "Store Manager", "Baker"])
        
        # Question 3 mapping (add weight to previous recommendations)
        if q3 == "Math":
            recommendations.extend(["Accountant", "Engineer", "Banker", "Mathematician"])
        elif q3 == "Science":
            recommendations.extend(["Scientist", "Doctor", "Veterinarian", "Chemist"])
        elif q3 == "Reading":
            recommendations.extend(["Writer", "Lawyer", "Librarian", "Teacher"])
        elif q3 == "Art":
            recommendations.extend(["Artist", "Designer", "Architect", "Photographer"])
        elif q3 == "Physical Education":
            recommendations.extend(["Athlete", "Fitness Trainer", "Coach", "Physical Therapist"])
        
        # Count frequency of each job to find top matches
        job_counts = Counter(recommendations)
        top_jobs = job_counts.most_common(3)
        
        # Display results
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 15px; margin-top: 20px; text-align: center;">
            <h3>Jobs You Might Like!</h3>
            <p>Based on your answers, here are some jobs you might enjoy when you grow up:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display top 3 job recommendations with improved styling
        job_cols = st.columns(3)
        for i, (job, count) in enumerate(top_jobs):
            # Get appropriate icon for job
            job_icon = job_icons.get(job, "💼")  # Use the job_icons dictionary we defined earlier
            
            with job_cols[i]:
                st.markdown(f"""
                <div style="background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; 
                             text-align: center; margin-bottom: 15px;">
                    <div style="font-size: 48px; margin-bottom: 15px;">{job_icon}</div>
                    <h3 style="margin-top: 0; color: #FF5C8D;">{job}</h3>
                    <p>This job matches your interests!</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Award achievement if completed
        if mark_activity_complete("career_quiz"):
            award_coins(10, "Discovering jobs that match your interests")
            update_progress("session4", 40)
            award_achievement("🔮", "Future Planner", "You're exploring careers that match your interests!")
    
    # Skills activity
    st.subheader("🌟 Skills I Already Have")
    
    st.markdown("""
    <div class="fun-box">
        <h3>Everyone Has Special Skills!</h3>
        <p>Skills are things you're good at. You already have many skills that can help you with different jobs!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Skill categories
    skill_categories = {
        "Helping Skills": ["Being kind", "Listening", "Sharing", "Helping friends", "Taking care of pets"],
        "Creative Skills": ["Drawing", "Singing", "Dancing", "Building with blocks", "Making up stories"],
        "Learning Skills": ["Reading", "Counting", "Remembering things", "Asking questions", "Learning new games"],
        "Physical Skills": ["Running", "Jumping", "Throwing", "Catching", "Balancing"],
        "Social Skills": ["Making friends", "Taking turns", "Working in a group", "Following rules", "Leading activities"]
    }
    
    # Create a checkbox grid for skills
    st.markdown("### Check the skills you already have:")
    
    # Initialize session state for tracking skills
    if 'my_skills' not in st.session_state:
        st.session_state.my_skills = []
    
    # Loop through skill categories
    for category, skills in skill_categories.items():
        st.markdown(f"#### {category}")
        
        # Create two columns for each category
        skill_cols = st.columns(2)
        for i, skill in enumerate(skills):
            with skill_cols[i % 2]:
                # Check if skill is already selected
                is_selected = skill in st.session_state.my_skills
                
                if st.checkbox(skill, value=is_selected, key=f"skill_{skill}"):
                    # Add to skills list if not already there
                    if skill not in st.session_state.my_skills:
                        st.session_state.my_skills.append(skill)
                else:
                    # Remove from skills list if it was there
                    if skill in st.session_state.my_skills:
                        st.session_state.my_skills.remove(skill)
    
    # Display selected skills
    if st.session_state.my_skills:
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; margin-top: 20px;">
            <h3>Your Amazing Skills!</h3>
            <p>You selected {len(st.session_state.my_skills)} skills that you already have:</p>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
                {" ".join([f'<span class="badge badge-green">{skill}</span>' for skill in st.session_state.my_skills])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a skill certificate button
        if st.button("Create My Skills Certificate"):
            # Get student name from session state
            student_name = st.session_state.get("student_name", "___________________")
            
            st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 20px; border: 8px dashed #FFDE59; 
                        text-align: center; margin-top: 30px; position: relative; box-shadow: 0 10px 20px rgba(0,0,0,0.2);">
                <h2 style="color: #448AFF; margin-bottom: 30px;">Certificate of Amazing Skills</h2>
                <p style="font-style: italic; margin-bottom: 20px;">This certifies that</p>
                <div style="border-bottom: 2px solid #FF80AB; margin: 10px auto 30px auto; width: 80%; padding-bottom: 5px;">
                    <h3 style="color: #FF5C8D;">{student_name}</h3>
                </div>
                <p>has the following special skills:</p>
                <div style="margin: 20px 0; text-align: left; columns: 2; column-gap: 20px; padding: 0 20px;">
                    {" ".join([f"<p>✓ {skill}</p>" for skill in st.session_state.my_skills])}
                </div>
                <div style="margin-top: 40px;">
                    <p style="font-weight: bold;">Mr. Stumberg's 1st Grade Class</p>
                    <p>{datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                <div style="position: absolute; top: -15px; right: -15px; background-color: #4CAF50; color: white; 
                            border-radius: 50%; width: 80px; height: 80px; display: flex; align-items: center; 
                            justify-content: center; font-size: 40px; border: 5px solid white;">🌟</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Award achievement for creating certificate
            if mark_activity_complete("skills_certificate"):
                award_coins(10, "Creating your skills certificate")
                update_progress("session4", 30)
    
    # Knowledge check
    with st.expander("✅ Check Your Learning"):
        st.markdown("### Review what you've learned about jobs")
        
        # First question
        q1 = st.radio(
            "Why are jobs important?",
            ["They help people earn money and provide goods and services", 
            "They are only for adults", 
            "They are only important in big cities", 
            "Jobs are not important"],
            index=None,
            key="learning_q1"
        )
        
        if q1 == "They help people earn money and provide goods and services":
            st.success("Correct! Jobs help people earn money for their families and provide important goods and services for the community.")
            if mark_activity_complete("session4_q1"):
                award_coins(5, "Understanding why jobs are important")
                update_progress("session4", 15)
        elif q1 is not None:
            st.error("That's not quite right. Think about how jobs help families and communities.")
        
        # Second question
        q2 = st.radio(
            "What are skills?",
            ["Things you have to buy", 
            "Things you're good at", 
            "Only things adults can do", 
            "Things that aren't important"],
            index=None,
            key="learning_q2"
        )
        
        if q2 == "Things you're good at":
            st.success("Correct! Skills are things you're good at, and everyone has different skills.")
            if mark_activity_complete("session4_q2"):
                award_coins(5, "Understanding what skills are")
                update_progress("session4", 15)
                
                # Award achievement if both questions correct
                if is_activity_completed("session4_q1") and is_activity_completed("career_quiz"):
                    award_achievement("👩‍🏫", "Job Explorer", "You understand jobs, skills, and career options!")
        elif q2 is not None:
            st.error("That's not quite right. Think about what makes you special and helpful.")