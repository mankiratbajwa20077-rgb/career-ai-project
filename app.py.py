import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 2rem auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    h1 {
        color: #667eea;
        font-weight: 700;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #764ba2;
        font-weight: 600;
    }
    
    h3 {
        color: #667eea;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        transition: all 0.3s;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox, .stSlider {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE INIT ============
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

# ============ CAREER DATABASE ============
career_data = [
    ["Science", "Engineering", "Software Engineer", "₹6–20 LPA", "IITs, NITs, IIITs", "AI, Cloud, Cybersecurity", "High", "Bachelor's in CS/IT"],
    ["Science", "Engineering", "Data Scientist", "₹8–25 LPA", "IIT, ISI, IISc", "AI & Big Data", "Very High", "Master's in Data Science"],
    ["Science", "Engineering", "AI Engineer", "₹10–30 LPA", "IIT, IISc", "Generative AI", "Very High", "Bachelor's + AI Specialization"],
    ["Science", "Medical", "Doctor", "₹8–40 LPA", "AIIMS, MAMC", "Healthcare innovation", "High", "MBBS + MD/MS"],
    ["Science", "Medical", "Biotechnologist", "₹4–12 LPA", "IISc, JNU", "Bio-AI", "Medium", "B.Tech/M.Tech in Biotech"],
    ["Science", "Medical", "Pharmacist", "₹4–10 LPA", "Jamia, Manipal", "Pharma R&D", "Medium", "B.Pharm/PharmD"],
    ["Science", "Research", "Scientist", "₹8–20 LPA", "IISc, DRDO", "Space & AI", "High", "PhD in Sciences"],
    ["Science", "Design", "Architect", "₹5–15 LPA", "SPA, CEPT", "Smart cities", "Medium", "B.Arch"],
    ["Science", "Tech", "Cybersecurity Analyst", "₹6–18 LPA", "IIIT, IIT", "Digital security", "Very High", "Bachelor's in CS + Certifications"],
    ["Science", "Tech", "Game Developer", "₹5–20 LPA", "Private institutes", "Gaming & VR", "High", "Bachelor's in CS/Game Design"],
    ["Commerce", "Finance", "Chartered Accountant", "₹8–30 LPA", "ICAI", "Global finance", "High", "CA Certification"],
    ["Commerce", "Finance", "Investment Banker", "₹10–40 LPA", "IIMs", "FinTech", "High", "MBA in Finance"],
    ["Commerce", "Management", "Business Analyst", "₹6–18 LPA", "IIM, ISB", "Data-driven biz", "High", "MBA/Analytics degree"],
    ["Commerce", "Management", "Marketing Manager", "₹6–20 LPA", "IIMs", "Digital marketing", "High", "MBA in Marketing"],
    ["Commerce", "Management", "HR Manager", "₹5–15 LPA", "TISS, IIM", "People analytics", "Medium", "MBA in HR"],
    ["Commerce", "Economics", "Economist", "₹7–22 LPA", "ISI, DSE", "Policy analytics", "Medium", "Master's in Economics"],
    ["Commerce", "Law", "Corporate Lawyer", "₹8–25 LPA", "NLUs", "Startup law", "High", "LLB + LLM"],
    ["Commerce", "Finance", "Financial Planner", "₹5–15 LPA", "Private institutes", "Wealth tech", "Medium", "CFP Certification"],
    ["Commerce", "Tech", "FinTech Specialist", "₹8–25 LPA", "IIM, IIT", "Digital payments", "Very High", "MBA/B.Tech combo"],
    ["Commerce", "Entrepreneurship", "Startup Founder", "Variable", "Any", "Startup India", "High", "Any + Business Acumen"],
    ["Arts", "Media", "Journalist", "₹4–12 LPA", "IIMC", "Digital media", "Medium", "Bachelor's in Journalism"],
    ["Arts", "Media", "Content Creator", "₹3–20 LPA", "Any", "Creator economy", "High", "Any + Creative Skills"],
    ["Arts", "Design", "Graphic Designer", "₹4–15 LPA", "NIFT, NID", "Brand design", "High", "Bachelor's in Design"],
    ["Arts", "Design", "UI/UX Designer", "₹6–18 LPA", "Private institutes", "Product design", "Very High", "Design degree + UX Course"],
    ["Arts", "Psychology", "Psychologist", "₹5–20 LPA", "DU, TISS", "Mental health", "High", "Master's in Psychology"],
    ["Arts", "Education", "Teacher", "₹4–12 LPA", "B.Ed Colleges", "EdTech", "Medium", "B.Ed/M.Ed"],
    ["Arts", "Law", "Civil Lawyer", "₹5–15 LPA", "NLUs", "Judicial services", "Medium", "LLB"],
    ["Arts", "Public Service", "IAS/IPS", "₹10–20 LPA", "UPSC", "Governance", "Medium", "Any degree + UPSC"],
    ["Arts", "Social Work", "NGO Specialist", "₹4–10 LPA", "TISS", "Social impact", "Medium", "MSW"],
    ["Arts", "Languages", "Foreign Language Expert", "₹5–18 LPA", "JNU", "Global business", "High", "Language degree"],
    ["Any", "Tech", "Product Manager", "₹10–35 LPA", "IIM, ISB", "Tech leadership", "Very High", "MBA or B.Tech + Experience"],
    ["Any", "Tech", "AI Product Designer", "₹8–25 LPA", "Private institutes", "Human-AI", "Very High", "Design + Tech background"],
    ["Any", "Analytics", "Data Analyst", "₹5–15 LPA", "IIT, DU", "Business intelligence", "Very High", "Any + Analytics course"],
    ["Any", "Sustainability", "Climate Analyst", "₹6–18 LPA", "TERI", "Green economy", "High", "Environmental Science degree"],
    ["Any", "Healthcare", "Health Data Analyst", "₹6–20 LPA", "IIT, AIIMS", "Health AI", "High", "Healthcare + Data Science"],
    ["Any", "Cyber Law", "Cyber Law Expert", "₹7–22 LPA", "NLUs", "Digital law", "High", "LLB + Cyber Law specialization"],
    ["Any", "EdTech", "Online Course Creator", "₹5–25 LPA", "Any", "Remote learning", "High", "Subject expertise + Tech"],
    ["Any", "E-Commerce", "E-Commerce Manager", "₹6–18 LPA", "IIMs", "D2C brands", "High", "MBA or relevant experience"],
    ["Any", "AI Ethics", "AI Ethics Officer", "₹8–25 LPA", "Global universities", "Responsible AI", "Medium", "Ethics + Tech background"],
    ["Any", "Space Tech", "Space Analyst", "₹8–22 LPA", "IISc, ISRO", "Private space", "High", "Aerospace Engineering"]
]

df = pd.DataFrame(career_data, columns=[
    "Stream", "Interest", "Career", "Salary", "Top Colleges", "Future Trend", "Demand", "Education"
])

# ============ NAVIGATION ============
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# ============ SIDEBAR ============
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/graduation-cap.png", width=80)
    st.title("🎓 Navigation")
    
    if st.button("🏠 Home", use_container_width=True):
        navigate_to('home')
    
    if st.button("📝 Career Quiz", use_container_width=True):
        navigate_to('quiz')
    
    if st.button("🔍 Career Explorer", use_container_width=True):
        navigate_to('explorer')
    
    if st.button("📊 Analytics", use_container_width=True):
        navigate_to('analytics')
    
    if st.button("🎯 Roadmap", use_container_width=True):
        navigate_to('roadmap')
    
    if st.button("💡 Resources", use_container_width=True):
        navigate_to('resources')
    
    st.markdown("---")
    st.info("**Current Page:** " + st.session_state.page.title())
    
    if st.session_state.user_data:
        st.success(f"👤 {st.session_state.user_data.get('name', 'User')}")

# ============ HOME PAGE ============
def show_home():
    st.title("🎓 AI Career Navigator")
    st.markdown("### Your personalized guide to future-ready careers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>40+</h2>
            <p>Career Paths</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>10+</h2>
            <p>Interest Areas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>100%</h2>
            <p>Personalized</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 👋 Welcome! Let's start your career journey")
    
    with st.form("user_info"):
        name = st.text_input("Your Name", placeholder="Enter your full name")
        age = st.number_input("Your Age", min_value=14, max_value=30, value=17)
        stream = st.selectbox("Current/Intended Stream", ["Science", "Commerce", "Arts", "Undecided"])
        grade = st.selectbox("Current Grade/Level", ["10th", "11th", "12th", "Graduate", "Post-Graduate"])
        
        submitted = st.form_submit_button("🚀 Start Your Journey", use_container_width=True)
        
        if submitted and name:
            st.session_state.user_data = {
                'name': name,
                'age': age,
                'stream': stream,
                'grade': grade,
                'timestamp': datetime.now()
            }
            st.success(f"Welcome aboard, {name}! 🎉")
            st.balloons()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🎯 Why Choose AI Career Navigator?</h3>
            <ul>
                <li>AI-powered recommendations</li>
                <li>Future-ready career insights</li>
                <li>Personalized learning paths</li>
                <li>Industry salary benchmarks</li>
                <li>Top college recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>📈 Featured Trends</h3>
            <ul>
                <li>🤖 AI & Machine Learning</li>
                <li>🌐 FinTech & Blockchain</li>
                <li>🎮 Gaming & Metaverse</li>
                <li>🌱 Sustainability Careers</li>
                <li>💊 Health-Tech Innovation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============ QUIZ PAGE ============
def show_quiz():
    st.title("📝 Career Aptitude Quiz")
    st.markdown("### Discover your strengths and ideal career matches")
    
    if not st.session_state.user_data:
        st.warning("Please complete your profile on the Home page first!")
        return
    
    questions = [
        {
            "q": "What do you enjoy most?",
            "options": ["Solving problems", "Creating content", "Helping people", "Analyzing data"],
            "weights": {"Engineering": [3,0,0,2], "Design": [0,3,0,1], "Psychology": [0,1,3,1], "Analytics": [2,0,0,3]}
        },
        {
            "q": "Your ideal work environment?",
            "options": ["Tech startup", "Hospital/Clinic", "Creative studio", "Corporate office"],
            "weights": {"Tech": [3,0,2,1], "Medical": [0,3,0,1], "Design": [1,0,3,0], "Management": [1,1,0,3]}
        },
        {
            "q": "Which skill do you want to develop?",
            "options": ["Coding", "Communication", "Leadership", "Research"],
            "weights": {"Engineering": [3,0,1,2], "Media": [0,3,2,0], "Management": [0,2,3,1], "Research": [2,0,1,3]}
        },
        {
            "q": "What motivates you most?",
            "options": ["Innovation", "Impact", "Income", "Independence"],
            "weights": {"Tech": [3,1,2,2], "Social Work": [1,3,0,1], "Finance": [1,0,3,2], "Entrepreneurship": [2,1,2,3]}
        },
        {
            "q": "Preferred learning style?",
            "options": ["Hands-on projects", "Reading & theory", "Group discussions", "Visual learning"],
            "weights": {"Engineering": [3,1,1,2], "Research": [1,3,2,1], "Management": [1,2,3,1], "Design": [2,1,1,3]}
        }
    ]
    
    with st.form("quiz_form"):
        answers = []
        for i, item in enumerate(questions):
            st.subheader(f"Q{i+1}. {item['q']}")
            answer = st.radio(f"q{i}", item['options'], key=f"quiz_{i}", label_visibility="collapsed")
            answers.append(answer)
        
        submitted = st.form_submit_button("📊 Get Results", use_container_width=True)
        
        if submitted:
            st.session_state.quiz_answers = answers
            interest_scores = {}
            
            for i, answer in enumerate(answers):
                idx = questions[i]['options'].index(answer)
                for interest, weights in questions[i]['weights'].items():
                    interest_scores[interest] = interest_scores.get(interest, 0) + weights[idx]
            
            top_interests = sorted(interest_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            st.session_state.quiz_score = top_interests
            
            st.success("Quiz completed! 🎉")
            st.markdown("### Your Top Interest Areas:")
            
            for interest, score in top_interests:
                st.markdown(f"**{interest}**: {score} points")
            
            st.info("Check the Career Explorer to see matching careers!")

# ============ EXPLORER PAGE ============
def show_explorer():
    st.title("🔍 Career Explorer")
    st.markdown("### Find your perfect career match")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_stream = st.selectbox("Filter by Stream", ["All"] + list(df["Stream"].unique()))
    
    with col2:
        filter_interest = st.selectbox("Filter by Interest", ["All"] + list(df["Interest"].unique()))
    
    with col3:
        filter_demand = st.selectbox("Filter by Demand", ["All", "Very High", "High", "Medium"])
    
    search = st.text_input("🔎 Search careers...", placeholder="e.g., Software, Doctor, Designer")
    
    filtered_df = df.copy()
    
    if filter_stream != "All":
        filtered_df = filtered_df[(filtered_df["Stream"] == filter_stream) | (filtered_df["Stream"] == "Any")]
    
    if filter_interest != "All":
        filtered_df = filtered_df[filtered_df["Interest"] == filter_interest]
    
    if filter_demand != "All":
        filtered_df = filtered_df[filtered_df["Demand"] == filter_demand]
    
    if search:
        filtered_df = filtered_df[filtered_df["Career"].str.contains(search, case=False)]
    
    st.markdown(f"### Found {len(filtered_df)} matching careers")
    
    for _, row in filtered_df.iterrows():
        with st.expander(f"🎯 {row['Career']} ({row['Stream']} - {row['Interest']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**💰 Salary Range:** {row['Salary']}")
                st.markdown(f"**📈 Demand:** {row['Demand']}")
                st.markdown(f"**🔮 Future Trend:** {row['Future Trend']}")
            
            with col2:
                st.markdown(f"**🎓 Education:** {row['Education']}")
                st.markdown(f"**🏫 Top Colleges:** {row['Top Colleges']}")
            
            if st.button(f"View Roadmap for {row['Career']}", key=f"road_{row['Career']}"):
                st.session_state.selected_career = row['Career']
                navigate_to('roadmap')

# ============ ANALYTICS PAGE ============
def show_analytics():
    st.title("📊 Career Analytics Dashboard")
    st.markdown("### Data-driven insights into career trends")
    
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "💰 Salaries", "🎯 Demand"])
    
    with tab1:
        st.subheader("Careers by Interest Area")
        interest_counts = df.groupby("Interest").size().reset_index(name='count')
        fig1 = px.bar(interest_counts, x='Interest', y='count', 
                     color='count', color_continuous_scale='Viridis',
                     title="Number of Careers per Interest Area")
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        st.subheader("Salary Distribution by Stream")
        salary_data = df.groupby("Stream").size().reset_index(name='count')
        fig2 = px.pie(salary_data, values='count', names='Stream',
                     title="Career Distribution by Stream",
                     hole=0.4, color_discrete_sequence=px.colors.sequential.Purples)
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        st.subheader("Career Demand Analysis")
        demand_counts = df.groupby("Demand").size().reset_index(name='count')
        fig3 = px.funnel(demand_counts, x='count', y='Demand',
                        title="Careers by Demand Level")
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Careers", len(df))
    with col2:
        st.metric("High Demand", len(df[df["Demand"].isin(["High", "Very High"])]))
    with col3:
        st.metric("Interest Areas", df["Interest"].nunique())
    with col4:
        st.metric("Streams", df["Stream"].nunique())

# ============ ROADMAP PAGE ============
def show_roadmap():
    st.title("🎯 Career Roadmap")
    st.markdown("### Your personalized path to success")
    
    selected = st.selectbox("Select a Career", df["Career"].unique())
    career_info = df[df["Career"] == selected].iloc[0]
    
    st.markdown(f"## {career_info['Career']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>📋 Career Overview</h3>
            <p><strong>Stream:</strong> {career_info['Stream']}</p>
            <p><strong>Interest Area:</strong> {career_info['Interest']}</p>
            <p><strong>Salary Range:</strong> {career_info['Salary']}</p>
            <p><strong>Demand:</strong> {career_info['Demand']}</p>
            <p><strong>Future Scope:</strong> {career_info['Future Trend']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card">
            <h3>🎓 Education</h3>
            <p>{career_info['Education']}</p>
            <h3>🏫 Top Colleges</h3>
            <p>{career_info['Top Colleges']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🗺️ Step-by-Step Roadmap")
    
    roadmap_steps = [
        ("📚 Foundation", "Complete required education and build fundamental skills"),
        ("💻 Skills Development", "Learn industry-specific tools and technologies"),
        ("🎯 Internships", "Gain practical experience through internships"),
        ("🏆 Certifications", "Obtain relevant certifications to boost credibility"),
        ("🌐 Networking", "Build professional network and attend industry events"),
        ("💼 Job Applications", "Apply to companies and prepare for interviews"),
        ("🚀 Career Growth", "Continuous learning and climbing the career ladder")
    ]
    
    for i, (title, desc) in enumerate(roadmap_steps, 1):
        st.markdown(f"""
        <div class="card">
            <h4>Step {i}: {title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ============ RESOURCES PAGE ============
def show_resources():
    st.title("💡 Learning Resources")
    st.markdown("### Boost your career preparation")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Courses", "📖 Books", "🎥 Videos", "🔗 Links"])
    
    with tab1:
        st.subheader("Recommended Online Courses")
        courses = [
            ("Coursera", "AI & Machine Learning", "https://www.coursera.org"),
            ("Udemy", "Web Development Bootcamp", "https://www.udemy.com"),
            ("edX", "Data Science Professional", "https://www.edx.org"),
            ("Khan Academy", "Mathematics & Sciences", "https://www.khanacademy.org")
        ]
        
        for platform, course, link in courses:
            st.markdown(f"**{platform}**: {course} - [Visit]({link})")
    
    with tab2:
        st.subheader("Must-Read Career Books")
        books = [
            "Designing Your Life - Bill Burnett",
            "So Good They Can't Ignore You - Cal Newport",
            "The Lean Startup - Eric Ries",
            "Range - David Epstein"
        ]
        
        for book in books:
            st.markdown(f"📖 {book}")
    
    with tab3:
        st.subheader("YouTube Channels")
        channels = [
            "Career Guidance by Experts",
            "Skill Development Tutorials",
            "Interview Preparation",
            "Industry Insights"
        ]
        
        for channel in channels:
            st.markdown(f"🎥 {channel}")
    
    with tab4:
        st.subheader("Useful Websites")
        links = {
            "NEET/JEE Prep": "https://www.nta.ac.in",
            "UPSC Preparation": "https://www.upsc.gov.in",
            "Internship Portal": "https://internshala.com",
            "Job Portal": "https://www.naukri.com"
        }
        
        for name, url in links.items():
            st.markdown(f"🔗 [{name}]({url})")

# ============ PAGE ROUTER ============
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'quiz':
    show_quiz()
elif st.session_state.page == 'explorer':
    show_explorer()
elif st.session_state.page == 'analytics':
    show_analytics()
elif st.session_state.page == 'roadmap':
    show_roadmap()
elif st.session_state.page == 'resources':
    show_resources()

# ============ FOOTER ============
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #667eea;'>
    <p>🌟 AI Career Navigator | Empowering Future Leaders | SDG 4: Quality Education 🌟</p>
    <p>Made with ❤️ for students across India</p>
</div>
""", unsafe_allow_html=True)