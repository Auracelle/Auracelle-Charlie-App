import streamlit as st

st.set_page_config(page_title="Auracelle Charlie | Login", layout="wide", initial_sidebar_state="collapsed")
st.title("🔐 Captive Page Login: Auracelle Charlie")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    st.markdown("#### 📌 Purpose of the Sandbox")
    st.info("This sandbox allows stakeholders to simulate AI governance policy decisions across nations, corporations, and civil society groups.\n\n"
            "Your role is to act as a representative decision-maker and engage with others based on your country's strategic position, constraints, and policy objectives.")

    submit = st.form_submit_button("Login")

def _go_to_sim():
    st.switch_page("pages/auracelle_charlie_simulation.py")

if submit:
    if password == "charlie2025":
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
        st.query_params.update({"logged_in": "true"})
        _go_to_sim()
    else:
        st.error("Incorrect password. Access denied.")
        st.stop()

if st.session_state.get("authenticated", False):
    _go_to_sim()
