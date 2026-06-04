import streamlit as st
from compiler import AICompiler

st.set_page_config(page_title="AI Software Compiler Engine", layout="wide")

st.title("🏗️ AI Software Compiler Engine")
st.write("Converts open-ended specifications into strict, validated, production-grade blueprints.")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Configuration Input")
    api_key = st.text_input("Enter Free Gemini API Key:", type="password")
    
    user_prompt = st.text_area(
        "Describe your application requirements:", 
        value="Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics.",
        height=150
    )
    
    compile_btn = st.button("Compile Application Architecture", type="primary", use_container_width=True)

with col2:
    st.subheader("Compiler Execution Diagnostics")
    
    if compile_btn:
        if not api_key:
            st.error("Please enter your free Gemini API Key first.")
        elif not user_prompt:
            st.error("Please provide an app instruction prompt.")
        else:
            log_container = st.empty()
            
            def update_pipeline_log(message, state="running"):
                with log_container.container():
                    if state == "running":
                        st.info(message)
                    else:
                        st.success(message)
            
            try:
                compiler = AICompiler(api_key=api_key)
                compiled_blueprint = compiler.run_pipeline(user_prompt, update_pipeline_log)
                
                st.subheader("Validated Executable System Schema (JSON)")
                st.json(compiled_blueprint)
            except Exception as e:
                st.error(f"Execution Error: {e}")