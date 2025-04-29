# Mr. Stumberg's 1st Grade Financial Literacy Adventure

An interactive Streamlit application designed to teach financial literacy concepts to 1st grade students in an engaging, age-appropriate way. This educational tool aligns with the JA Our Families curriculum and supports Iowa Core standards for financial literacy.

## 🌟 Features

The app features five interactive learning sessions:

### 👪 Session 1: All Kinds of Families
- Learn how families are alike and different
- Discover how families work together
- Explore how families help the community

### 🛒 Session 2: Money for Needs and Wants
- Distinguish between needs and wants
- Learn why families need to earn money
- Practice making spending decisions

### 🏪 Session 3: Businesses Around the Neighborhood
- Discover local businesses in Grimes, Iowa
- Learn about goods vs. services
- Meet entrepreneurs in the community

### 👩‍🏫 Session 4: Jobs in Our Community
- Explore different types of jobs
- Learn how jobs help families and communities
- Discover future career possibilities

### 🚀 Session 5: Create Your Own Business
- Design a personal business based on interests
- Create a business name with adjustable creativity
- Design a business advertisement

## 🧩 Educational Elements

The app incorporates several educational strategies:

- **Interactive Learning**: Students actively engage with content through games, quizzes, and creative activities
- **Visual Learning**: Colorful visuals, emoji symbols, and child-friendly design elements
- **Reward System**: Students earn virtual coins for completing activities
- **Achievement Badges**: Special accomplishments unlock achievement badges
- **Progress Tracking**: Visual progress indicators for each session

## 🖥️ Technical Features

- **Modular Design**: Each session is contained in its own file for easy maintenance
- **Session State Management**: Reliable state tracking across the application
- **Responsive UI**: Kid-friendly interface that works on various devices
- **OpenAI Integration**: Optional AI-generated business names for enhanced creativity
- **Customizable Design Elements**: Students can personalize their business designs

## 📋 Installation & Setup

1. Clone this repository
```bash
git clone https://github.com/yourusername/financial-literacy-app.git
cd financial-literacy-app

Create a virtual environment

bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install required packages

bashpip install -r requirements.txt

Run the application

bashstreamlit run main.py
📁 Project Structure
FinancialLiteracyApp/
├── main.py                 # Main application entry point
├── utils.py                # Utility functions
├── styles.py               # CSS styles
├── sessions/
│   ├── __init__.py         # Package initialization
│   ├── session1.py         # All Kinds of Families
│   ├── session2.py         # Money for Needs and Wants
│   ├── session3.py         # Businesses All Around the Neighborhood
│   ├── session4.py         # Jobs Around the Neighborhood
│   └── session5.py         # A New Business
└── requirements.txt        # Package dependencies

🙏 Acknowledgments

Developed for Mr. Stumberg's 1st Grade Class at Grimes Elementary
Based on Junior Achievement's "JA Our Families" curriculum
Created with Streamlit and Python
Optional AI features powered by OpenAI

📚 Curriculum Alignment
This app aligns with the JA Our Families curriculum and supports the following Iowa Core standards for financial literacy:

Developing understanding of financial goals
Distinguishing between needs and wants
Recognizing how financial choices affect individuals and communities
Understanding entrepreneurship and career opportunities