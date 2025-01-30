import streamlit as st
import random
import json

# Simulate a career database for enhanced features
career_database = {
    "Software Engineer": {
        "description": "Design and develop software applications.",
        "salary_range": "$70,000 - $120,000",
        "skills_required": ["Programming", "Problem-solving", "Teamwork"],
        "growth_rate": "High"
    },
    "Graphic Designer": {
        "description": "Create visual concepts, using computer software.",
        "salary_range": "$40,000 - $80,000",
        "skills_required": ["Designing", "Creativity", "Communication"],
        "growth_rate": "Moderate"
    },
    "Nurse": {
        "description": "Provide medical care and treatment to patients.",
        "salary_range": "$50,000 - $90,000",
        "skills_required": ["Healthcare", "Communication", "Problem-solving"],
        "growth_rate": "High"
    },
    # Add more careers similarly...
}

# Function to generate career recommendations based on interests and skills
def get_career_recommendations(interests, skills):
    # Define career options for each interest/skill combination
    career_options = {
        "Technology": ["Software Engineer", "Data Scientist", "Web Developer"],
        "Arts": ["Graphic Designer", "Artist", "Art Director"],
        "Healthcare": ["Healthcare Professional", "Nurse", "Physician"],
        "Business": ["Marketing Manager", "Business Analyst", "Sales Executive"],
        "Engineering": ["Mechanical Engineer", "Electrical Engineer", "Civil Engineer"],
        "Education": ["Teacher", "Education Consultant", "School Administrator"],
        "Design": ["UI/UX Designer", "Graphic Designer", "Product Designer"]
    }
    
    # Create an empty list to store recommended careers
    recommendations = []
    
    # Check the interests and suggest careers based on them
    for interest in interests:
        if interest in career_options:
            recommendations.extend(career_options[interest])
    
    # Remove duplicates (if any)
    recommendations = list(set(recommendations))
    
    # Return recommendations
    return recommendations

# Streamlit App UI
st.title("AI Career Compass")

# Introduction Section
st.header("Welcome to Your Future!")
st.write("""
    AI Career Compass is your personalized platform to help you discover your skills, interests, and potential career paths.
    Explore your passions, assess your abilities, and take control of your future career decisions.
""")

# User Profile Section
st.sidebar.header("User Profile")
user_name = st.sidebar.text_input("Enter your name:")
if user_name:
    st.sidebar.write(f"Hello, {user_name}!")
else:
    st.sidebar.write("Please enter your name to start exploring.")

# Button to Start Exploring
if 'exploring' not in st.session_state:
    st.session_state['exploring'] = False

# Career Quiz: Simple personality-based quiz
def career_quiz():
    questions = [
        {"question": "Do you enjoy solving complex problems?", "answer": "yes", "careers": ["Software Engineer", "Data Scientist"]},
        {"question": "Do you have a creative streak?", "answer": "yes", "careers": ["Graphic Designer", "Artist"]},
        {"question": "Are you passionate about helping people?", "answer": "yes", "careers": ["Nurse", "Healthcare Professional"]},
        {"question": "Do you like working with technology?", "answer": "yes", "careers": ["Web Developer", "Data Scientist"]},
        # Add more questions here...
    ]
    
    quiz_answers = []
    for q in questions:
        user_answer = st.radio(q["question"], ["yes", "no"])
        if user_answer == "yes":
            quiz_answers.append(q["careers"])

    recommended_careers = list(set([career for sublist in quiz_answers for career in sublist]))
    return recommended_careers

# Show career quiz when button is clicked
if not st.session_state['exploring']:
    if st.button("Start Exploring"):
        st.session_state['exploring'] = True

# If the user has clicked "Start Exploring", show the selection fields
if st.session_state['exploring']:
    st.subheader("How It Works")
    st.write("""
        Through self-assessment tools and interactive quizzes, you'll be able to explore various career options based on your preferences and strengths.
        Our AI-driven recommendations will provide insights into suitable career paths.
    """)

    # Self-Assessment Questionnaire for Interests and Skills
    interests = st.multiselect(
        "What fields are you interested in?",
        ["Technology", "Arts", "Healthcare", "Business", "Engineering", "Education", "Design"],
        key="interests"
    )
    
    skills = st.multiselect(
        "Which skills do you have?",
        ["Programming", "Writing", "Designing", "Communication", "Problem-solving", "Teamwork", "Leadership"],
        key="skills"
    )

    # Display selected inputs
    if interests:
        st.write(f"Your selected interests: {', '.join(interests)}")
    if skills:
        st.write(f"Your selected skills: {', '.join(skills)}")

    # Button to Get Career Recommendations
    if st.button("Get Career Recommendations"):
        if interests and skills:
            # Call the function to get career recommendations
            recommendations = get_career_recommendations(interests, skills)
            
            if recommendations:
                st.subheader("Your Potential Career Paths:")
                for career in recommendations:
                    st.write(f"- {career}")
                    
                    # Show more career details from the database
                    if career in career_database:
                        st.write(f"**Description:** {career_database[career]['description']}")
                        st.write(f"**Salary Range:** {career_database[career]['salary_range']}")
                        st.write(f"**Growth Rate:** {career_database[career]['growth_rate']}")
                        st.write(f"**Skills Required:** {', '.join(career_database[career]['skills_required'])}")
            else:
                st.warning("No career recommendations found based on your interests and skills.")
        else:
            st.warning("Please select at least one interest and one skill.")
    
    # Career Quiz Section
    if st.button("Take Career Quiz"):
        st.subheader("Career Quiz: Find Your Perfect Match!")
        recommended_careers = career_quiz()
        if recommended_careers:
            st.write("Based on your quiz responses, we recommend the following careers:")
            for career in recommended_careers:
                st.write(f"- {career}")
        else:
            st.warning("No career matches found. Try answering more questions.")

# Allow users to download their results
if st.button("Download My Career Report"):
    if interests and skills:
        # Prepare the data for download
        report = {
            "name": user_name,
            "interests": interests,
            "skills": skills,
            "recommendations": get_career_recommendations(interests, skills)
        }
        # Save to a file (JSON format here)
        with open("career_report.json", "w") as f:
            json.dump(report, f)
        st.write("Your report has been saved. You can download it from the following link:")
        st.download_button("Download Report", data=open("career_report.json", "rb"), file_name="career_report.json")
