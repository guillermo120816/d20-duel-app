import streamlit as st
import random

# --- Configuration and Initialization ---

# Use wide layout for better spacing on all devices
st.set_page_config(layout="wide") 
st.title("D20 Duel: High Roll Wins 🏆")
st.write("Two players roll a 20-sided die. Highest number wins the round!")

# Initialize Session State (Crucial for game memory)
if 'player1_roll' not in st.session_state:
    st.session_state.player1_roll = None
if 'player2_roll' not in st.session_state:
    st.session_state.player2_roll = None
if 'winner' not in st.session_state:
    st.session_state.winner = ""
if 'rolls_done' not in st.session_state:
    st.session_state.rolls_done = 0 
if 'p1_wins' not in st.session_state:
    st.session_state.p1_wins = 0      
if 'p2_wins' not in st.session_state:
    st.session_state.p2_wins = 0      


# --- Game Logic Functions ---

def roll_dice(player_num):
    """Generates a random number between 1 and 20 for a player."""
    if st.session_state.rolls_done < 2:
        roll = random.randint(1, 20)
        
        # Store the result in the session state
        if player_num == 1:
            st.session_state.player1_roll = roll
        elif player_num == 2:
            st.session_state.player2_roll = roll
        
        # Increment the roll counter
        st.session_state.rolls_done += 1

def check_winner():
    """Compares the rolls, sets the winner state, and updates the score."""
    p1 = st.session_state.player1_roll
    p2 = st.session_state.player2_roll
    
    if p1 is not None and p2 is not None:
        if p1 > p2:
            st.session_state.winner = "Player 1 Wins!"
            st.session_state.p1_wins += 1 
        elif p2 > p1:
            st.session_state.winner = "Player 2 Wins!"
            st.session_state.p2_wins += 1 
        else:
            st.session_state.winner = "It's a Tie!"
    else:
        st.session_state.winner = ""

def reset_round():
    """Clears roll and winner state to start a new round, preserving win totals."""
    st.session_state.player1_roll = None
    st.session_state.player2_roll = None
    st.session_state.winner = ""
    st.session_state.rolls_done = 0

# --- UI Display ---

# Display Running Score Tally
st.subheader("Current Tally:")
score_col1, score_col2, score_col3 = st.columns(3)

score_col1.metric("P1 Wins", st.session_state.p1_wins)
score_col2.metric("P2 Wins", st.session_state.p2_wins)
score_col3.metric("Rounds", st.session_state.p1_wins + st.session_state.p2_wins)

st.write("---")

# --- Player Roll Area ---

col1, col2 = st.columns(2)

with col1:
    st.header("Player 1")
    
    # Disable button if Player 1 has already rolled
    disable_p1 = st.session_state.player1_roll is not None 
    st.button("Roll D20", key="p1_button", on_click=roll_dice, args=(1,), disabled=disable_p1)
    
    # Display the current roll
    if st.session_state.player1_roll is not None:
        st.metric(label="Your Roll", value=str(st.session_state.player1_roll))
    else:
        st.info("Awaiting Roll...")

with col2:
    st.header("Player 2")
    
    # Disable button if Player 2 has already rolled OR if P1 hasn't rolled yet
    disable_p2 = st.session_state.player2_roll is not None or st.session_state.rolls_done == 0
    st.button("Roll D20", key="p2_button", on_click=roll_dice, args=(2,), disabled=disable_p2)
    
    # Display the current roll
    if st.session_state.player2_roll is not None:
        st.metric(label="Your Roll", value=str(st.session_state.player2_roll))
    else:
        st.info("Awaiting Roll...")


# --- Winner Announcement and Reset Button (Updated Arrangement) ---

st.write("---")

# Check if both players have rolled (rolls_done == 2)
if st.session_state.rolls_done == 2:
    
    # 1. Run the winner check logic
    check_winner()

    # 2. Display the result
    st.subheader("Results:")
    
    # Check for winner and display appropriate message
    if st.session_state.winner.endswith("Wins!"):
        st.balloons()
        st.success(f"🥳 {st.session_state.winner}!")
    elif st.session_state.winner.endswith("Tie!"):
        st.warning(f"🤝 {st.session_state.winner}")
        
    # 3. Display the reset button in a centered column
    # We use a 3-column arrangement to push the button to the middle
    col_l, col_c, col_r = st.columns([1, 2, 1])
    
    with col_c:
        # The new, centered button. Since it is the only element in the wider middle column, it looks centered.
        st.button("Start New Round", on_click=reset_round, use_container_width=True)

st.caption("Tip: To reset the entire game score, refresh the page.")
