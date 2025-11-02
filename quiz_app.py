import streamlit as st
import time

# --- 1. Quiz Data (Hardcoded List of Dictionaries) ---
# All questions and answers are stored here to make the app a single file for easy deployment.
QUIZ_QUESTIONS = [
    {
        "id": "2.7.1",
        "question": "According to Furetank procedures, how should crew access the Safety Management System (SMS) manuals?",
        "options": [
            "Physical copies stored in the bridge office only.",
            "By logging into the vessel's digital system (FMS / DOCMAP).",
            "They are provided as hard copies to each crew member.",
            "By requesting them from the DPA."
        ],
        "answer_index": 1,
        "correct_answer_explanation": "SMS Manuals are digital documents accessed by logging into FMS / DOCMAP on the vessel's system."
    },
    {
        "id": "2.7.2",
        "question": "Who is the Furetank Designated Person Ashore (DPA), and where is their contact information posted?",
        "options": [
            "The Fleet Manager, contact information found in the Crew List document.",
            "Donald Werner, HSQE-Manager, with contact information posted onboard on the homepage and the bridge.",
            "The Master of the vessel, as they are the direct contact person.",
            "The Technical Manager, contact information available only in the Bridge Manual."
        ],
        "answer_index": 1,
        "correct_answer_explanation": "The DPA is Donald Werner, HSQE-Manager, and contact details are posted on the bridge and the ship's homepage."
    },
    {
        "id": "3.5.2",
        "question": "If a SIRE 2.0 inspector asks about training on Life Saving Appliances (LSA) or Fire Fighting Equipment (FFA), what is the most effective response?",
        "options": [
            "Directing the inspector to the training certificates log.",
            "Quoting the relevant section of the SOLAS convention.",
            "Showing the inspector how to operate a piece of equipment (e.g., an EEBD or fire extinguisher).",
            "Stating that training is done quarterly."
        ],
        "answer_index": 2,
        "correct_answer_explanation": "The most effective demonstration of training and familiarity is to physically show the inspector how to operate the equipment (e.g., use an EEBD or a fire extinguisher)."
    },
    {
        "id": "4.4.6_Mobile",
        "question": "During cargo operations on deck, what is the Furetank procedure regarding carrying mobile phones?",
        "options": [
            "Allowed, provided the phone is switched off.",
            "Allowed, but must be in an intrinsically safe casing.",
            "Not allowed to be carried on deck.",
            "Allowed, only if carrying a UHF radio in a holster."
        ],
        "answer_index": 2,
        "correct_answer_explanation": "Mobile phones must not be carried on deck during cargo operations."
    },
    {
        "id": "4.4.6_UHF",
        "question": "How should a crew member carry their UHF radio during cargo operations?",
        "options": [
            "The UHF radio must be carried in a radio holster.",
            "The radio must be secured to a lanyard around the neck.",
            "The UHF radio is carried loosely in a pocket.",
            "It is only carried by the Officer on Watch (OOW)."
        ],
        "answer_index": 0,
        "correct_answer_explanation": "The UHF radio is always carried in a radio holster."
    },
    {
        "id": "5.1.6",
        "question": "What demonstration should be performed for the inspector when asked 'How do you launch the lifeboat?'",
        "options": [
            "Explaining the role of the person in charge only.",
            "Showing the maintenance log of the davits.",
            "Showing the inspector the physical steps of how to launch the lifeboat.",
            "Verbally explaining the sequence of releasing the brake and retrieving the gripes."
        ],
        "answer_index": 2,
        "correct_answer_explanation": "The answer requires demonstrating the launch steps to the inspector."
    },
    {
        "id": "5.1.14",
        "question": "When responding to a 'Man Overboard' incident, where should a crew member verify their specific duty?",
        "options": [
            "In the Bridge Standing Orders.",
            "In the emergency procedures handbook.",
            "On the Man Overboard muster list (PR773).",
            "As directed verbally by the Master."
        ],
        "answer_index": 2,
        "correct_answer_explanation": "The duty is found on the Man Overboard muster list PR773."
    },
    {
        "id": "5.1.15",
        "question": "Where are the Plans and Procedures for Recovery from Water documented?",
        "options": [
            "The vessel's Safety Data Sheets (SDS).",
            "Plans and procedures for recovery from water RP015.",
            "The Medical First Aid Guide (MFAG).",
            "The ISM Code, Part A."
        ],
        "answer_index": 1,
        "correct_answer_explanation": "The procedure is documented in Plans and procedures for recovery from water RP015."
    },
    {
        "id": "5.2.1",
        "question": "When starting the emergency fire pump for an inspector, what two items should be shown to verify the procedure?",
        "options": [
            "The fuel gauge and the oil pressure indicator.",
            "Which buttons to press and the posted instructions.",
            "The main switchboard and the engine RPM counter.",
            "The valve settings on the main fire line and the sea chest."
        ],
        "answer_index": 1,
        "correct_answer_explanation": "Show which buttons to press and the posted instructions for starting the emergency fire pump."
    },
    {
        "id": "5.2.2",
        "question": "Where should a crew member find the information regarding the correct open/close positioning of fire dampers for cargo operations or emergencies?",
        "options": [
            "On a clearly visible list of fire dampers that shows their position and system markings.",
            "The information is relayed verbally by the OOW before operations start.",
            "On the Chief Engineer's whiteboard.",
            "In the engine room training folder."
        ],
        "answer_index": 0,
        "correct_answer_explanation": "A list of fire dampers should clearly show their position and they should be marked with a system for how they should be positioned."
    },
    {
        "id": "5.2.8",
        "question": "What three firefighting systems should be pointed out in the galley for an inspector?",
        "options": [
            "Fixed fire system, portable extinguisher, and ventilation system stopping.",
            "Fire blanket, water hose, and CO2 alarm.",
            "Fixed sprinkler system, fire axe, and emergency lighting.",
            "Powder extinguisher, foam extinguisher, and fire flap."
        ],
        "answer_index": 0,
        "correct_answer_explanation": "The systems are the fixed fire system, portable extinguisher, and ventilation system stopping."
    },
    {
        "id": "5.2.15",
        "question": "When asked about the deck foam system, what three components should the crew member show or describe?",
        "options": [
            "The water pressure pump, the foam proportioner, and the fire main connection.",
            "The foam cannons, how they line up against the manifold, and how to use them.",
            "The foam sample log, the foam concentrate storage level, and the discharge pressure.",
            "The manual activation point, the remote control unit, and the air release valve."
        ],
        "answer_index": 1,
        "correct_answer_explanation": "Show the foam cannons, how you line them up against the manifold, and how you use them."
    },
    {
        "id": "5.2.16",
        "question": "What is the primary purpose of the fire doors in the engine room?",
        "options": [
            "To prevent unauthorized access to the engine room.",
            "To provide extra sound insulation.",
            "To seal off the fire zones.",
            "To prevent the spread of flooding."
        ],
        "answer_index": 2,
        "correct_answer_explanation": "The purpose of fire doors is to seal off the fire zones."
    },
    {
        "id": "5.3.1",
        "question": "During the test of a firefighter's air bottle (SCBA), at what pressure should the low air alarm whistle typically activate?",
        "options": [
            "280 bar.",
            "180 bar.",
            "100 bar.",
            "50 bar."
        ],
        "answer_index": 3,
        "correct_answer_explanation": "The low air alarm whistle should start at 50 bar."
    },
    {
        "id": "5.3.4",
        "question": "What is the sole purpose of the Emergency Escape Breathing Apparatus (EEBD)?",
        "options": [
            "To be used for personal escape from a dangerous area into safety.",
            "To be used for rescue operations in smoky areas.",
            "To replace a failed SCBA set during firefighting.",
            "To provide a continuous air supply for 30 minutes."
        ],
        "answer_index": 0,
        "correct_answer_explanation": "EEBDs are not used for rescue operations, only for personal use during escape of a dangerous area into safety."
    }
]
TOTAL_QUESTIONS = len(QUIZ_QUESTIONS)


# --- 2. Configuration and Initialization ---

st.set_page_config(layout="wide")
st.title("🚢 Furetank SIRE 2.0 Quiz for Ratings")
st.caption("Quiz on Furetank's procedures, documentation, and SIRE 2.0 compliance.")


# Initialize Session State (Crucial for game memory)
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False
if 'user_choice_index' not in st.session_state:
    st.session_state.user_choice_index = -1


# --- 3. Core Logic Functions ---

def check_answer():
    """Checks the user's selected answer against the correct answer and updates state."""
    if st.session_state.user_choice_index == -1:
        st.warning("Please select an answer before submitting.")
        return

    st.session_state.show_explanation = True
    
    current_q_data = QUIZ_QUESTIONS[st.session_state.current_q_index]
    correct_index = current_q_data["answer_index"]
    
    # 1. Check if the answer is correct
    if st.session_state.user_choice_index == correct_index:
        st.session_state.score += 1
        st.session_state.feedback = f"✅ **Correct!**"
    else:
        st.session_state.feedback = f"❌ **Incorrect.**"


def next_question():
    """Advances to the next question or finishes the quiz."""
    # Reset states for the next question
    st.session_state.show_explanation = False
    st.session_state.user_choice_index = -1
    if 'feedback' in st.session_state:
        del st.session_state.feedback # Clear feedback text
    
    # Advance
    st.session_state.current_q_index += 1
    
    if st.session_state.current_q_index >= TOTAL_QUESTIONS:
        st.session_state.quiz_finished = True
    
    # Force Streamlit to re-run the script to display the next state
    st.experimental_rerun()


def restart_quiz():
    """Resets all session state variables to start the quiz over."""
    st.session_state.current_q_index = 0
    st.session_state.score = 0
    st.session_state.quiz_finished = False
    st.session_state.show_explanation = False
    st.session_state.user_choice_index = -1
    if 'feedback' in st.session_state:
        del st.session_state.feedback


# --- 4. UI Layout ---

st.sidebar.metric("Current Score", f"{st.session_state.score} / {TOTAL_QUESTIONS}")
st.sidebar.caption(f"Questions Loaded: {TOTAL_QUESTIONS}")

if st.session_state.quiz_finished:
    # --- Final Score Screen ---
    final_score = st.session_state.score
    
    st.header("Quiz Complete! 🥳")
    st.markdown(f"## Your Final Score: **{final_score} out of {TOTAL_QUESTIONS}**")
    
    if final_score == TOTAL_QUESTIONS:
        st.balloons()
        st.success("Perfect score! You are a Furetank and SIRE 2.0 master.")
    elif final_score >= TOTAL_QUESTIONS * 0.7:
        st.info("Excellent job! A very strong performance.")
    else:
        st.warning("Keep studying! Review the Furetank procedures for a stronger rating.")
        
    st.button("Start New Quiz", on_click=restart_quiz)

else:
    # --- Current Question Screen ---
    q_index = st.session_state.current_q_index
    q_data = QUIZ_QUESTIONS[q_index]
    
    st.header(f"Question {q_index + 1} of {TOTAL_QUESTIONS}")
    st.markdown(f"### {q_data['question']}")
    
    # Use st.radio for options. We use the key to save the selected index directly.
    selected_index = st.radio(
        "Select your answer:",
        options=q_data["options"],
        key="user_choice", 
        disabled=st.session_state.show_explanation,
        index=None
    )

    # Convert the selected option text back to its index for use in state
    if selected_index is not None:
        st.session_state.user_choice_index = q_data["options"].index(selected_index)
    
    
    if not st.session_state.show_explanation:
        # Show Submit button
        submit_disabled = st.session_state.user_choice_index == -1
        st.button(
            "Submit Answer",
            on_click=check_answer,
            disabled=submit_disabled,
            use_container_width=True
        )
    else:
        # Show feedback and explanation after submission
        st.markdown(st.session_state.feedback)
        
        # Display the explanation in an expanding box
        with st.expander("Show Detailed Explanation", expanded=True):
            correct_index = q_data["answer_index"]
            correct_answer = q_data["options"][correct_index]
            
            st.markdown(f"**Correct Answer:** {correct_answer}")
            st.markdown(f"**Reasoning/Procedure:** {q_data['correct_answer_explanation']}")
        
        # Show Next Question button
        st.button(
            "Next Question",
            on_click=next_question,
            use_container_width=True
        )
