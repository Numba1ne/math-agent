import streamlit as st
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Import agent initialization from main.py
from main import initialize_agent

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Math Agent - Secondary School Exam Prep",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stChatMessage {
        padding: 1rem;
    }
    .math-example {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_agent():
    """Get initialized agent with caching."""
    try:
        agent_executor, system_message, api_status = initialize_agent()
        return agent_executor, system_message, f"✅ {api_status}"
    except ValueError as e:
        st.error(f"❌ {str(e)}")
        st.stop()
        return None, None, None

def main():
    # Initialize agent
    agent_executor, system_message, api_status = get_agent()
    
    # Header
    st.markdown('<h1 class="main-header">📐 Math Agent</h1>', unsafe_allow_html=True)
    st.markdown("### Your Comprehensive Secondary School Math Assistant for Exam Preparation")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.info(api_status)
        
        st.header("📚 Math Topics Covered")
        st.markdown("""
        - **📐 Algebra**: Equations, factoring, expanding
        - **📏 Geometry**: Areas, volumes, Pythagorean theorem
        - **📊 Trigonometry**: sin, cos, tan, inverses
        - **📈 Statistics**: Mean, median, mode, standard deviation
        - **🔢 Sequences**: Arithmetic & geometric
        - **📉 Logarithms**: All types
        - **➕ Basic Math**: Arithmetic, percentages, ratios
        """)
        
        st.header("💡 Example Questions")
        examples = [
            "Solve 2*x + 5 = 13",
            "Find the area of a circle with radius 5",
            "Calculate sin(30)",
            "What is the mean of [10, 20, 30, 40, 50]?",
            "Solve quadratic equation: a=1, b=-5, c=6",
            "Find the 10th term of arithmetic sequence: first=5, difference=3",
        ]
        
        for example in examples:
            if st.button(f"📝 {example}", key=example, use_container_width=True):
                st.session_state.example_question = example
        
        st.header("⚙️ Settings")
        if st.button("🔄 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hello! I'm your Math AI assistant. I can help you with algebra, geometry, trigonometry, statistics, sequences, logarithms, and more!\n\nAsk me any math question, and I'll solve it step-by-step to help you prepare for your exams."
            }
        ]
    
    # Handle example question from sidebar
    if "example_question" in st.session_state:
        user_question = st.session_state.example_question
        del st.session_state.example_question
    else:
        user_question = None
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me a math question...") or user_question:
        if user_question:
            prompt = user_question
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Create messages with system instruction
                messages = [
                    system_message,
                    HumanMessage(content=prompt)
                ]
                
                # Stream the response
                for chunk in agent_executor.stream({"messages": messages}):
                    if "agent" in chunk and "messages" in chunk["agent"]:
                        for message in chunk["agent"]["messages"]:
                            if hasattr(message, 'content') and message.content:
                                full_response += message.content
                                message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                error_message = f"❌ Error: {str(e)}\n\nPlease try again with a different question."
                message_placeholder.error(error_message)
                full_response = error_message
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()

