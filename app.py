import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import random
from utils.gemini_analysis import (
    analyze_text, 
    get_severity_color, 
    get_score_color, 
    get_category_icon,
    create_annotated_text_html
)
from utils.file_processor import process_uploaded_file
from data.quiz_examples import QUIZ_EXAMPLES, COMPARISON_EXAMPLES

# Load environment variables
load_dotenv()

# Configure Gemini API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="Digital Literacy Assistant",
    page_icon="🛡️",
    layout="wide"
)

# Initialize session state for quiz
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = False
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_selections' not in st.session_state:
    st.session_state.quiz_selections = []
if 'quiz_revealed' not in st.session_state:
    st.session_state.quiz_revealed = False
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quizzes_taken' not in st.session_state:
    st.session_state.quizzes_taken = 0

# Custom CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
    }
    .quiz-phrase {
        display: inline-block;
        padding: 8px 12px;
        margin: 4px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s;
        background-color: #2d2d2d;
        border: 2px solid #444;
    }
    .quiz-phrase:hover {
        background-color: #3d3d3d;
        border-color: #666;
    }
    .quiz-phrase.selected {
        background-color: #ff4444;
        border-color: #ff6666;
        color: white;
        font-weight: bold;
    }
    .quiz-phrase.correct {
        background-color: #44ff44;
        border-color: #66ff66;
        color: #000;
        font-weight: bold;
    }
    .quiz-phrase.missed {
        background-color: #ffaa44;
        border-color: #ffbb66;
        color: #000;
        font-weight: bold;
    }
    .comparison-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid;
    }
    .suspicious-box {
        background-color: #2d1a1a;
        border-color: #ff4444;
    }
    .legitimate-box {
        background-color: #1a2d1a;
        border-color: #44ff44;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🛡️ Digital Literacy Assistant")
st.markdown("""
Welcome! This tool helps you identify scams, misinformation, and manipulation tactics in text messages, emails, and social media posts.
Paste any suspicious text below or upload a file to analyze it.
""")

# Sidebar for navigation
with st.sidebar:
    st.header("📚 Navigation")
    page = st.radio(
        "Choose a section:",
        ["🔍 Analyze Text", "📖 Learn More"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This tool uses Google Gemini AI to detect:
    - 🎣 Phishing attempts
    - 💰 Financial scams
    - 🗞️ Misinformation
    - 🧠 Emotional manipulation
    - ⚠️ Urgency tactics
    """)
    
    # Show quiz stats if any quizzes taken
    if st.session_state.quizzes_taken > 0:
        st.markdown("---")
        st.markdown("### 🎯 Your Progress")
        accuracy = (st.session_state.quiz_score / st.session_state.quizzes_taken) * 100
        st.metric("Quizzes Completed", st.session_state.quizzes_taken)
        st.metric("Average Score", f"{accuracy:.0f}%")

# Main content area
if page == "🔍 Analyze Text":
    st.header("Analyze Your Text")
    
    # Add tabs for different input methods
    input_tab1, input_tab2 = st.tabs(["📝 Type/Paste Text", "📎 Upload File"])
    
    user_text = None
    
    # Tab 1: Text Input
    with input_tab1:
        user_text = st.text_area(
            "Paste the message, email, or post you want to analyze:",
            height=200,
            placeholder="Example: 'URGENT! Your account will be suspended unless you click this link immediately...'"
        )
    
    # Tab 2: File Upload
    with input_tab2:
        st.markdown("### Upload a file to analyze")
        st.info("📌 **Supported formats:** PDF, DOCX, TXT, PNG, JPG, JPEG")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
            help="Upload a document or image containing text you want to analyze"
        )
        
        if uploaded_file is not None:
            with st.spinner(f"📄 Extracting text from {uploaded_file.name}..."):
                try:
                    extracted_text = process_uploaded_file(uploaded_file)
                    
                    if extracted_text:
                        user_text = extracted_text
                        st.success(f"✅ Successfully extracted {len(extracted_text)} characters from {uploaded_file.name}")
                        
                        # Show preview
                        with st.expander("👁️ Preview extracted text"):
                            st.text_area("Extracted content:", extracted_text, height=200, disabled=True)
                    else:
                        st.warning("⚠️ No text found in the file. Please try a different file.")
                        user_text = None
                        
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
                    user_text = None
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    # Clear functionality
    if clear_button:
        st.rerun()
    
    # Analysis section
    if analyze_button:
        if user_text and user_text.strip():
            st.markdown("---")
            
            with st.spinner("🤖 Analyzing text with Google Gemini AI..."):
                result = analyze_text(user_text)
            
            if result["success"]:
                data = result["data"]
                
                # ========== OVERALL SCORE (Always Visible) ==========
                overall_score = data["overall_confidence_score"]
                score_emoji = get_score_color(overall_score)
                
                st.markdown(f"## {score_emoji} Overall Risk Score: {overall_score}/100")
                st.progress(overall_score / 100)
                
                # Overall Assessment
                if data["is_safe"]:
                    st.success(f"✅ {data['overall_assessment']}")
                else:
                    st.error(f"⚠️ {data['overall_assessment']}")
                
                # Recommendation (Always visible)
                st.info(f"💡 **Recommendation:** {data['recommendation']}")
                
                st.markdown("---")
                
                # ========== CATEGORY BREAKDOWN (Always Visible) ==========
                st.subheader("📊 Category Breakdown")
                
                cols = st.columns(5)
                categories = data["category_scores"]
                
                for idx, (category, score) in enumerate(categories.items()):
                    with cols[idx]:
                        icon = get_category_icon(category)
                        score_emoji = get_score_color(score)
                        category_name = category.replace("_", " ").title()
                        
                        st.markdown(f"### {icon} {category_name}")
                        st.markdown(f"### {score_emoji} {score}/100")
                        st.progress(score / 100)
                
                st.markdown("---")
                
                # ========== TABBED DETAILED ANALYSIS ==========
                st.subheader("🔍 Detailed Analysis")
                
                # Determine if message is suspicious or safe
                is_suspicious = overall_score >= 50
                
                # Create tabs with dynamic labels
                if is_suspicious:
                    tab1, tab2, tab3 = st.tabs([
                        "📝 Annotated Text",
                        "🚩 Warning Signs",
                        "⚠️ Suspicious Phrases"
                    ])
                else:
                    tab1, tab2, tab3 = st.tabs([
                        "📝 Annotated Text",
                        "✅ Safety Indicators",
                        "ℹ️ Analysis Details"
                    ])
                
                # TAB 1: Annotated Text
                with tab1:
                    st.markdown("*Suspicious phrases are highlighted in red. Hover over them for details.*")
                    
                    if data["suspicious_phrases"]:
                        html_content = create_annotated_text_html(user_text, data["suspicious_phrases"])
                        st.markdown(html_content, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #444; font-size: 16px; line-height: 1.8;'>
                        {user_text}
                        </div>
                        """, unsafe_allow_html=True)
                        st.info("✅ No specific suspicious phrases detected in this text.")
                
                # TAB 2: Red Flags or Safety Features
                with tab2:
                    if is_suspicious and data["red_flags"]:
                        st.markdown("### 🚩 Warning Signs Detected")
                        for flag in data["red_flags"]:
                            severity_emoji = get_severity_color(flag["severity"])
                            with st.expander(f"{severity_emoji} {flag['flag']} ({flag['severity'].upper()})"):
                                st.write(flag["explanation"])
                    elif not is_suspicious and data["red_flags"]:
                        st.markdown("### ✅ Why This Message Appears Legitimate")
                        st.info("While some caution flags were detected, the overall message appears relatively safe based on the following analysis:")
                        for flag in data["red_flags"]:
                            severity_emoji = get_severity_color(flag["severity"])
                            with st.expander(f"{severity_emoji} {flag['flag']} (Caution: {flag['severity'].upper()})"):
                                st.write(flag["explanation"])
                    else:
                        st.success("✅ No major warning signs detected in this message.")
                        st.markdown("""
                        This message appears to be legitimate based on:
                        - No urgent pressure tactics
                        - No requests for sensitive information
                        - No suspicious links or attachments
                        - Professional tone and formatting
                        
                        However, always verify sender identity through official channels if uncertain.
                        """)
                
                # TAB 3: Suspicious Phrases or Details
                with tab3:
                    if data["suspicious_phrases"]:
                        st.markdown("### 🔍 Phrase Analysis")
                        st.markdown("*These phrases were highlighted in the annotated text above.*")
                        
                        for idx, phrase_data in enumerate(data["suspicious_phrases"], 1):
                            with st.expander(f"⚠️ Phrase {idx}: \"{phrase_data['phrase']}\""):
                                st.markdown(f"**Why it raised a flag:**")
                                st.write(phrase_data['reason'])
                    else:
                        st.markdown("### ℹ️ Analysis Summary")
                        st.info("No specific suspicious phrases were detected. The message uses generally acceptable language and tone.")
                        
                        # Show what made it safe
                        if not is_suspicious:
                            st.markdown("""
                            **Positive indicators:**
                            - Clear, specific communication
                            - No pressure or urgency
                            - Professional language
                            - No requests for sensitive data
                            """)
                
            else:
                st.error(f"❌ Analysis failed: {result['error']}")
                if "raw_response" in result:
                    with st.expander("Show raw response"):
                        st.code(result["raw_response"])
        else:
            st.warning("⚠️ Please enter some text or upload a file to analyze!")

elif page == "📖 Learn More":
    st.header("📚 Digital Literacy Education")
    
    # Create tabs for learning sections
    learn_tab1, learn_tab2, learn_tab3 = st.tabs([
        "🚩 Red Flags Guide",
        "🎯 Interactive Quiz",
        "🔄 Spot the Difference"
    ])
    
    # TAB 1: Red Flags Guide
    with learn_tab1:
        st.markdown("""
        ### 🎯 What is Digital Literacy?
        
        Digital literacy is the ability to identify trustworthy information online and protect yourself from:
        - **Scams and fraud** - Fake offers, lottery scams, romance scams
        - **Misinformation and fake news** - False claims, manipulated facts
        - **Phishing attempts** - Fake emails/messages stealing your info
        - **Social engineering tactics** - Psychological manipulation
        
        ### 🚩 Common Red Flags to Watch For:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### ⚠️ Urgency Tactics
            - "Act now or lose this opportunity!"
            - "Your account will be suspended immediately!"
            - Creates panic to make you act without thinking
            
            #### 💰 Too Good to Be True
            - "Make $10,000 in one week!"
            - "You've won a prize you didn't enter!"
            - If it sounds impossible, it probably is
            
            #### 🎣 Requests for Personal Info
            - Asking for passwords, PIN codes, SSN
            - Legitimate companies never ask via email/text
            """)
        
        with col2:
            st.markdown("""
            #### 🔗 Suspicious Links
            - Misspelled URLs (g00gle.com vs google.com)
            - Shortened links hiding destination
            - Always hover before clicking!
            
            #### 😱 Emotional Manipulation
            - Fear: "Your loved one is in danger!"
            - Greed: "Limited time offer!"
            - Trust: "I'm from your bank..."
            
            #### 🏛️ Authority Impersonation
            - Claims to be from government/bank
            - Uses official-looking logos
            - Check sender email carefully
            """)
        
        st.markdown("---")
        st.markdown("""
        ### ✅ How to Stay Safe:
        
        1. **Verify before you trust** - Check sources independently
        2. **Don't click suspicious links** - Type URLs directly
        3. **Enable 2FA** - Two-factor authentication adds security
        4. **Trust your instincts** - If something feels off, it probably is
        5. **Use this tool** - Analyze suspicious messages before responding
        
        ### 📞 Report Scams:
        
        - **FTC:** https://reportfraud.ftc.gov
        - **FBI IC3:** https://www.ic3.gov
        - **Your email provider:** Mark as spam/phishing
        """)
    
    # TAB 2: Interactive Quiz
    with learn_tab2:
        st.markdown("## 🎯 Test Your Scam Detection Skills!")
        st.markdown("Can you identify the suspicious phrases in these real-world examples?")
        
        if not st.session_state.quiz_mode:
            st.info("💡 **How it works:** Read the message below and click on phrases you think are suspicious. When you're done, reveal the answer to see how you did!")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🎮 Start Quiz", type="primary", use_container_width=True):
                    st.session_state.quiz_mode = True
                    st.session_state.current_quiz = random.choice(QUIZ_EXAMPLES)
                    st.session_state.quiz_selections = []
                    st.session_state.quiz_revealed = False
                    st.rerun()
        
        else:
            quiz = st.session_state.current_quiz
            
            # Display quiz category and difficulty
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### 📂 Category: {quiz['category']}")
            with col2:
                risk_color = "🔴" if quiz['risk_score'] >= 80 else "🟡" if quiz['risk_score'] >= 50 else "🟢"
                st.markdown(f"### {risk_color} Risk Level: {quiz['risk_score']}/100")
            
            st.markdown("---")
            
            # Display the text with clickable phrases
            st.markdown("### 📝 Message to Analyze:")
            st.markdown("*Click on words or phrases you think are suspicious:*")
            
            # Split text into words for clicking
            words = quiz['text'].split()
            
            if not st.session_state.quiz_revealed:
                # Interactive mode - let user click
                cols_per_row = 6
                word_index = 0
                
                while word_index < len(words):
                    cols = st.columns(cols_per_row)
                    for col in cols:
                        if word_index < len(words):
                            with col:
                                word = words[word_index]
                                # Check if this word is part of a selected phrase
                                is_selected = any(word.lower() in phrase.lower() for phrase in st.session_state.quiz_selections)
                                
                                button_type = "primary" if is_selected else "secondary"
                                if st.button(word, key=f"word_{word_index}", use_container_width=True):
                                    # Try to match with suspicious phrases
                                    matched = False
                                    for sp in quiz['suspicious_phrases']:
                                        if word.lower() in sp['phrase'].lower():
                                            phrase = sp['phrase']
                                            if phrase in st.session_state.quiz_selections:
                                                st.session_state.quiz_selections.remove(phrase)
                                            else:
                                                st.session_state.quiz_selections.append(phrase)
                                            matched = True
                                            break
                                    
                                    if not matched:
                                        # If not part of suspicious phrase, add the word itself
                                        if word in st.session_state.quiz_selections:
                                            st.session_state.quiz_selections.remove(word)
                                        else:
                                            st.session_state.quiz_selections.append(word)
                                    
                                    st.rerun()
                            word_index += 1
                        else:
                            break
                
                st.markdown("---")
                
                # Show selected phrases
                if st.session_state.quiz_selections:
                    st.markdown("### ✅ Your Selections:")
                    for selection in st.session_state.quiz_selections:
                        st.markdown(f"- {selection}")
                
                # Reveal button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("🎯 Reveal Answer", type="primary", use_container_width=True):
                        st.session_state.quiz_revealed = True
                        
                        # Calculate score
                        correct_phrases = [sp['phrase'] for sp in quiz['suspicious_phrases']]
                        correct_count = sum(1 for sel in st.session_state.quiz_selections if any(sel.lower() in cp.lower() or cp.lower() in sel.lower() for cp in correct_phrases))
                        total_possible = len(correct_phrases)
                        score_percent = (correct_count / total_possible * 100) if total_possible > 0 else 0
                        
                        st.session_state.quiz_score += score_percent
                        st.session_state.quizzes_taken += 1
                        
                        st.rerun()
            
            else:
                # Revealed mode - show answers
                st.markdown("### 🎯 Answer Revealed!")
                
                # Calculate and show score
                correct_phrases = [sp['phrase'] for sp in quiz['suspicious_phrases']]
                correct_count = sum(1 for sel in st.session_state.quiz_selections if any(sel.lower() in cp.lower() or cp.lower() in sel.lower() for cp in correct_phrases))
                total_possible = len(correct_phrases)
                score_percent = (correct_count / total_possible * 100) if total_possible > 0 else 0
                
                if score_percent >= 80:
                    st.success(f"🌟 Excellent! You identified {correct_count}/{total_possible} suspicious phrases ({score_percent:.0f}%)")
                elif score_percent >= 50:
                    st.info(f"👍 Good job! You identified {correct_count}/{total_possible} suspicious phrases ({score_percent:.0f}%)")
                else:
                    st.warning(f"📚 Keep learning! You identified {correct_count}/{total_possible} suspicious phrases ({score_percent:.0f}%)")
                
                # Show all suspicious phrases with explanations
                st.markdown("### 🚩 All Suspicious Phrases:")
                for idx, sp in enumerate(quiz['suspicious_phrases'], 1):
                    was_selected = any(sp['phrase'].lower() in sel.lower() or sel.lower() in sp['phrase'].lower() for sel in st.session_state.quiz_selections)
                    icon = "✅" if was_selected else "❌"
                    
                    with st.expander(f"{icon} {idx}. \"{sp['phrase']}\""):
                        st.markdown(f"**Why it's suspicious:**")
                        st.write(sp['reason'])
                
                # Next quiz button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("🔄 Try Another Quiz", type="primary", use_container_width=True):
                        st.session_state.current_quiz = random.choice(QUIZ_EXAMPLES)
                        st.session_state.quiz_selections = []
                        st.session_state.quiz_revealed = False
                        st.rerun()
                
                # Exit quiz button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("🏁 Exit Quiz", use_container_width=True):
                        st.session_state.quiz_mode = False
                        st.rerun()
    
    # TAB 3: Spot the Difference
    with learn_tab3:
        st.markdown("## 🔄 Spot the Difference")
        st.markdown("Compare suspicious messages with their legitimate counterparts. Learn what makes communication trustworthy!")
        
        # Select comparison example
        comparison = st.selectbox(
            "Choose a scenario:",
            range(len(COMPARISON_EXAMPLES)),
            format_func=lambda x: f"{COMPARISON_EXAMPLES[x]['category']}"
        )
        
        example = COMPARISON_EXAMPLES[comparison]
        
        st.markdown("---")
        
        # Show both versions side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ❌ Suspicious Version")
            st.markdown(f"""
            <div class='comparison-box suspicious-box'>
                {example['suspicious']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ✅ Legitimate Version")
            st.markdown(f"""
            <div class='comparison-box legitimate-box'>
                {example['legitimate']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Show detailed differences
        st.markdown("### 🔍 Key Differences Explained:")
        
        for idx, diff in enumerate(example['differences'], 1):
            with st.expander(f"📌 Difference {idx}: {diff['point']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**❌ Suspicious:**")
                    st.error(diff['suspicious_detail'])
                
                with col2:
                    st.markdown("**✅ Legitimate:**")
                    st.success(diff['legitimate_detail'])
        
        # Takeaway
        st.markdown("---")
        st.info("""
        💡 **Key Takeaway:** Legitimate organizations communicate professionally, give you time to verify, 
        provide official contact methods, and never pressure you into immediate action. If you're unsure, 
        always contact the organization directly using contact information from their official website.
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>🛡️ Digital Literacy Assistant | Powered by Google Gemini AI</p>
    <p>Built for Hack-o-Verse Hackathon 2026</p>
</div>
""", unsafe_allow_html=True)


