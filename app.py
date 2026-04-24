import streamlit as st
import PyPDF2
import google.generativeai as genai
import re

#  1. CONFIGURATION & STYLING 
def setup_page():
    st.set_page_config(page_title="Policy AI Adapter", layout="wide")
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #ffffff; }
        
        /*1. HEADER CONTAINER WITH RADIAL GRADIENT BACKGROUND */
        .title-container {
            display: flex; 
            flex-direction: column; 
            align-items: center;
            justify-content: center; 
            text-align: center; 
            padding: 40px 0; /* Increased padding for better gradient visibility */
            width: 100%;
            background: radial-gradient(circle at center, rgba(31, 119, 180, 0.15) 0%, transparent 70%);
        }

        .title-row { display: flex; align-items: center; justify-content: center; gap: 20px; }

        /*2. UNIFORM CARD STYLING WITH SHINING BLUE BORDER */
        .policy-card {
            background-color: #161b22;
            border: 3px solid #1f77b4; 
            border-radius: 12px;
            padding: 20px;
            height: 160px; 
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 0 15px rgba(31, 119, 180, 0.4); 
            margin-bottom: 10px;
        }

        .card-caption { font-size: 0.85rem; color: #8899ac; margin-bottom: 5px; }
        .card-value { font-size: 1.2rem; font-weight: 600; color: white; line-height: 1.3; }
        .card-footer { font-size: 0.8rem; color: #1f77b4; margin-top: auto; }

        }
                
        /* 3.FIXED SIDEBAR FOOTER */
        .sidebar-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0b0e14;
            padding: 15px;
            text-align: center;
            border-top: 1px solid #1f77b4;
            z-index: 999;
        }
        .status-dot {
            height: 10px; width: 10px;
            background-color: #0ec417;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
            box-shadow: 0 0 8px #0ec417;
        }
        [data-testid="stMetric"] { display: none; }
        
        
        .stPopover > button {
            background-color: transparent !important;
            border: 1px solid #1f77b4 !important;
            color: #1f77b4 !important;
            font-size: 0.8rem !important;
            margin-top: -5px;
        }
        </style>

        <div class="title-container">
            <div class="title-row">
                <img src="https://cdn-icons-png.flaticon.com/128/8878/8878120.png" width="60">
                <h1 style="font-size: 55px; margin: 0; padding: 0; color: white; border: none; background: none;">PolicySense AI</h1>
            </div>
            <p style="font-size: 18px; color: #a0a0a0; margin-top: 10px;">
                Strategic Intelligence System for Policy Summarization & Scenario Adaptation
            </p>
        </div>
        """, unsafe_allow_html=True)

# 2. AI & DATA CORE 
GEMINI_API_KEY =   # Replace with your actual API key

def get_working_model():
    if not GEMINI_API_KEY:
        st.sidebar.error("⚠️ API Key is missing!")
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        safe_config = {"temperature": 0, "top_p": 1, "top_k": 1, "max_output_tokens": 4096}
        selected_model = next((m for m in available_models if 'gemini-1.5-flash' in m), 
                              available_models[0] if available_models else None)
        if selected_model:
            return genai.GenerativeModel(model_name=selected_model, generation_config=safe_config)
        return None
    except Exception as e:
        st.sidebar.error(f"Gemini Init Error: {e}")
        return None
    
# 3. Preprocessing function to clean and structure extracted text for better AI understanding

def preprocess_policy_text(text):
    # 1. Remove multiple newlines and extra spaces (Noise Reduction)
    text = re.sub(r'\s+', ' ', text)
    # 2. Remove common PDF 'artifacts' (e.g., "Page 1 of 10")
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
    # 3. Remove standalone special characters that don't add meaning
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


def extract_text(file):
    try:
        reader = PyPDF2.PdfReader(file)
        # Extract text from the first 25 pages
        raw_text = "".join([page.extract_text() or "" for page in reader.pages[:25]])
        # APPLY PREPROCESSING (Crucial for Assignment Requirement)
        clean_text = preprocess_policy_text(raw_text)
        
        return clean_text
    except Exception as e:
        st.error(f"PDF Error: {e}")
        return ""

def generate_ai(model, prompt, context):
    if not model: return "AI Model not initialized."
    try:
        full_prompt = f"""
        You are a Professional Policy Intelligence Specialist.
        Instruction: {prompt}
        Base your response ONLY on the following document context:
        {context[:15000]}
        """
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Generation Error: {e}"


# 4. UPDATED SIDEBAR SECTION 

with st.sidebar:
    # Custom Sidebar Styling
    st.markdown("""
        <style>
        /* Sidebar background and text */
        [data-testid="stSidebar"] {
            background-color: #0b0e14;
            border-right: 1px solid #1f77b4;
        }
        
        /* Styling the Upload Box */
        [data-testid="stFileUploader"] {
            background-color: #161b22;
            border: 1px solid 
            border-radius: 10px;
            padding: 10px;
        }      

        /* Sidebar Button Styling */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            border: 1px solid #1f77b4;
            background-color: transparent;
            color: white;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1f77b4;
            box-shadow: 0 0 10px rgba(31, 119, 180, 0.6);
            border: 1px solid white;
        }
        </style>
             
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: white; font-size: 22px;'>System Panel </h2>", unsafe_allow_html=True)
    st.divider()  ## Control Title

    st.markdown("<p style='color: #8899ac; font-weight: bold; margin-bottom: 5px;'>Upload Policy Document</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")  #Upload Section
    
    if uploaded_file:
        st.success(f"{uploaded_file.name}")

        # FIXED ONLINE BAR AT BOTTOM
        st.markdown("""
        </style>
            <div class="sidebar-footer">
                <span class="status-dot"></span>
                <span style="color: white; font-size: 12px; font-family: sans-serif;">
                   POLICY ADVISOR |SYSTEM ONLINE
                </span>
            </div>
        </style>
        """, unsafe_allow_html=True)

# 5. MAIN APPLICATION 
def main():
    setup_page()
    model = get_working_model()

# MAIN CONTENT SECTION
    if uploaded_file:
        if 'pdf_content' not in st.session_state:
            with st.spinner("Extracting & Preprocessing content..."):
                st.session_state['pdf_content'] = extract_text(uploaded_file)
                st.toast("NLP Preprocessing Complete!", icon="✅")
                st.session_state['summary'] = ""
                st.session_state['custom_output'] = ""

                snippet = st.session_state['pdf_content'][:5000]
                st.session_state['policy_name'] = generate_ai(model, "Extract the full official title of this document (max 10 words).", snippet)
                st.session_state['horizon'] = generate_ai(model, "What is the time period or year of this policy? (e.g., 2021-2030). Answer in 1-3 words.", snippet)
                st.session_state['key_stat'] = generate_ai(model, "Identify one primary quantitative target or the main focus of this policy in 2 words (e.g. '80% Reduction' or 'Safety Standards').", snippet)
                
# METRIC CARDS
        st.divider()
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            display_name = st.session_state['policy_name']
            short_name = (display_name[:30] + '...') if len(display_name) > 30 else display_name
            st.markdown(f"""
                <div class="policy-card">
                    <div>
                        <div class="card-caption">Document Title</div>
                        <div class="card-value">{short_name}</div>
                    </div>
                    <div class="card-footer">↑ Source Identified</div>
                </div>
            """, unsafe_allow_html=True)
            with st.popover("Show Full Title"):
                st.write(st.session_state['policy_name'])

        with col_m2:
            st.markdown(f"""
                <div class="policy-card">
                    <div>
                        <div class="card-caption">Time Horizon</div>
                        <div class="card-value">{st.session_state['horizon']}</div>
                    </div>
                    <div class="card-footer">↑ Active Period</div>
                </div>
            """, unsafe_allow_html=True)

        with col_m3:
            st.markdown(f"""
                <div class="policy-card">
                    <div>
                        <div class="card-caption">Primary Focus</div>
                        <div class="card-value">{st.session_state['key_stat']}</div>
                    </div>
                    <div class="card-footer">↑ AI Detected</div>
                </div>
            """, unsafe_allow_html=True)

        st.divider()

# ANALYSIS PANELS
        left_panel, right_panel = st.columns(2, gap="large")
        with left_panel:
            st.subheader("Policy Summary:")
            if st.button("Generate Executive Summary"):
                with st.spinner("Analyzing..."):
                 summary_prompt = "Provide a detailed summary of main goals and Key strategies and overall direction."
                 st.session_state['summary'] = generate_ai(model, summary_prompt, st.session_state['pdf_content'])
            if st.session_state['summary']:
                    st.markdown(f"""
            <div style="
                background-color: #161b22; 
                border: 1px solid #1f77b4; 
                border-radius: 10px; 
                padding: 20px; 
                color: #ffffff;
                line-height: 1.6;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            ">
                {st.session_state['summary']}
            </div>
        """, unsafe_allow_html=True)
            

        with right_panel:
            # Everything below this must be indented by 4 more spaces
            st.subheader("Scenario Adaptation Chatbot")
           
            # Initialize Chat History
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Chat Display Container
            chat_container = st.container(height=400)

            # Show History
            for message in st.session_state.messages:
                icon = "👤" if message["role"] == "user" else "🤖"
                with chat_container.chat_message(message["role"], avatar=icon):
                    st.markdown(message["content"])

            # Chat Input
            if prompt := st.chat_input("Ex: How does this affect the general public?"):
                with chat_container.chat_message("user", avatar="👤"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                with chat_container.chat_message("assistant"):
                    with st.spinner("Analyzing scenario..."):
                        # Combine summary and prompt for better context
                        context = f"Policy Summary: {st.session_state['summary']}"
                        response = generate_ai(model, f"Scenario: {prompt}", context)
                        st.markdown(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                
# 6. EXPORT SECTION
        if st.session_state['summary'] or st.session_state['custom_output']:
            st.divider()
            report_content = f"POLICY ANALYSIS REPORT\nGenerated by PolicySense AI\n{'-'*50}\n" \
                             f"DOCUMENT: {uploaded_file.name}\nPERIOD: {st.session_state['horizon']}\n" \
                             f"FOCUS: {st.session_state['key_stat']}\n\n1. EXECUTIVE SUMMARY\n{st.session_state['summary']}\n\n" \
                                f"2. SCENARIO ANALYSIS\n" + "\n".join([f"{i+1}. {m['content']}" for i, m in enumerate(st.session_state.messages) if m["role"] == "assistant"])
            
            _, col_d2, _ = st.columns([1, 1, 1])
            with col_d2:
                st.download_button(
                    label="Download Full Analysis (TXT)",
                    data=report_content,
                    file_name=f"PolicySense_Analysis_{uploaded_file.name.split('.')[0]}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    else:
        st.write("---")
        st.info("Please upload a policy document in the sidebar to begin analysis.")
if __name__ == "__main__":
    main()
