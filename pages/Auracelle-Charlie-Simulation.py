# ✅ Auracelle Charlie — Two-Page (Login → Simulation)
# Version 2 (fixed): initializes session_state['round'] and includes 'Assess Policy' popover.

!pip install -q pyngrok streamlit networkx matplotlib numpy pandas torch plotly


import os, time, subprocess
from pyngrok import ngrok
from IPython.display import display, HTML

!pkill -f streamlit || true
!pkill -f ngrok || true
try:
    ngrok.disconnect("http://localhost:8501")
except Exception:
    pass
try:
    ngrok.kill()
except Exception:
    pass

ngrok.set_auth_token("2vmh7uE9lpuOWrldBNSV68hJKH7_4Ukd3XG92jWofsVoZALiJ")
os.makedirs("pages", exist_ok=True)


app_py_content = r'''import streamlit as st

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
'''
with open('app.py','w') as f:
    f.write(app_py_content)


simulation_py_content = r'''import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Auracelle Charlie | Simulation", layout="wide", initial_sidebar_state="collapsed")

# Gate
if not st.session_state.get("authenticated", False):
    st.warning("Please log in first.")
    st.switch_page("app.py")

st.title("AI Governance Policy Wargame: A Multi-Agent Simulation Sandbox")
st.header("Auracelle Charlie: Intelligence Map+ Edition 🚀")

# Instructions
instructions_title = "**How to Use the Sandbox**"
instructions_lines = [
    "**Step 1: Login & Redirect** - Use your credentials on the Captive Page. You will be redirected here after success.",
    "**Step 2: Select Countries & Roles** - Choose Country A and Country B. Assign a role to each (e.g., Governance, MilitaryAI, DataPrivacy).",
    "**Step 3: Pick a Policy Scenario** - Scenarios (AI Diffusion Rule, Data Privacy Act 118th, EU AI Act, NATO Article 5) adjust dynamics via a Lessons Learned factor.",
    "**Step 4: Review Positions** - Compare GDP, Influence, and Policy Position. Propose a new policy position for your country.",
    "**Step 5: Alignment & Response** - The Alignment Score shows convergence; the app suggests likely opponent behavior.",
    "**Step 6: Advance Rounds** - Use Next Simulation Round to iterate; Q-learning updates behavior each round.",
    "**Step 7: Influence Network** - See edge weights and intelligence levels; weights change with learning and alignment.",
    "**Step 8: Geo Map** - Hover for details; Dubai is mapped to UAE; NATO is highlighted near Brussels.",
    "**Step 9: PageRank Table** - Quickly see relative influence of the selected actors.",
    "**Step 10: Tips** - Try different roles/policies, then compare alignment and influence shifts across rounds."
]
instructions_text = instructions_title + "\n\n" + "\n\n".join(instructions_lines)
with st.expander("📘 Instructions", expanded=False):
    st.markdown(instructions_text)

# Init session state (fix)
if "round" not in st.session_state:
    st.session_state["round"] = 1
if "q_table" not in st.session_state:
    st.session_state["q_table"] = {}
if "edge_memory" not in st.session_state:
    st.session_state["edge_memory"] = {}

# Policy selection + Clickable Assess Policy
policy_options = [
    "Interim Final Rule on Artificial Intelligence Diffusion",
    "Data Privacy Act 118th",
    "The European Union AI Act",
    "NATO Article 5"
]
selected_policy = st.selectbox("Select Policy Scenario", policy_options)

policy_explanations = {
    policy_options[0]: "This aims to control how advanced AI is shared, focusing on security and limiting risks.",
    policy_options[1]: "A privacy-focused law requiring strong safeguards for personal and sensitive data.",
    policy_options[2]: "Comprehensive regulation to ensure AI is safe, transparent, and respects human rights.",
    policy_options[3]: "A collective defense principle applied to cyber and AI-related threats."
}
with st.popover("🔎 Assess Policy"):
    st.markdown(f"**{selected_policy}**\n\n{policy_explanations[selected_policy]}")

lessons_learned_factor = {
    policy_options[0]: 0.8,
    policy_options[1]: 0.9,
    policy_options[2]: 1.0,
    policy_options[3]: 0.95
}[selected_policy]

# Entities
country_options = ["Dubai", "United Kingdom", "United States", "Japan", "China", "Brazil", "India", "NATO"]
default_data = {
    "Dubai": {"gdp": 0.5, "influence": 0.7, "position": "Moderate regulatory stance"},
    "United Kingdom": {"gdp": 3.2, "influence": 0.85, "position": "Supports EU-style data protection"},
    "United States": {"gdp": 21.0, "influence": 0.95, "position": "Favors innovation over regulation"},
    "Japan": {"gdp": 5.1, "influence": 0.88, "position": "Pro-regulation for trust"},
    "China": {"gdp": 17.7, "influence": 0.93, "position": "Strict state-driven AI governance"},
    "Brazil": {"gdp": 2.0, "influence": 0.75, "position": "Leaning toward EU-style regulation"},
    "India": {"gdp": 3.7, "influence": 0.82, "position": "Strategic tech balancing, privacy-preserving innovation"},
    "NATO": {"gdp": 25.0, "influence": 0.97, "position": "Collective security & data interoperability"}
}

selected_country_a = st.selectbox("Select Country A", country_options, index=0)
selected_country_b = st.selectbox("Select Country B", country_options, index=1)

# Roles
st.subheader("🧩 Assign Roles to Each Country")
role_tags = ["Governance","MilitaryAI","DataPrivacy","ExportControl","Diplomacy","StandardSetting","Surveillance","Trade","TechAlliance"]
role_country_a = st.selectbox(f"Select Role for {selected_country_a}", role_tags, key="role_country_a")
role_country_b = st.selectbox(f"Select Role for {selected_country_b}", role_tags, key="role_country_b")
st.write(f"🛡️ **{selected_country_a}** is acting as: `{role_country_a}`")
st.write(f"🛡️ **{selected_country_b}** is acting as: `{role_country_b}`")

player_country = st.selectbox("🎖️ You are representing:", country_options, index=0)
opponent_country = selected_country_b if player_country == selected_country_a else selected_country_a

# Country A vs Country B comparison
st.subheader("🆚 Policy Position Comparison: Country A vs Country B")
st.table({
    "Aspect": ["GDP (Trillion USD)", "Influence", "AI Policy Position"],
    selected_country_a: [default_data[selected_country_a]["gdp"], default_data[selected_country_a]["influence"], default_data[selected_country_a]["position"]],
    selected_country_b: [default_data[selected_country_b]["gdp"], default_data[selected_country_b]["influence"], default_data[selected_country_b]["position"]]
})

player_new_position = st.text_input("📜 Propose a New Policy Position for Your Country", value=default_data[player_country]["position"])
alignment_score = 1.0 if player_new_position == default_data[opponent_country]["position"] else 0.0
st.metric("🤝 Negotiation Alignment Score", f"{alignment_score * 100:.0f}%")
opponent_adjustment = "Maintain Position" if alignment_score == 1.0 else "May adjust toward player stance"
st.write(f"🧠 Opponent likely response: **{opponent_adjustment}**")

st.subheader(f"🕑 Current Simulation Round: {st.session_state['round']}")
if st.button("▶️ Next Simulation Round"):
    st.session_state["round"] += 1

# Minimal Q-Learning stub
q_table = st.session_state["q_table"]
actions = ["adjust toward A", "adjust toward B", "maintain"]
state = (default_data[selected_country_a]["position"], default_data[selected_country_b]["position"])
if state not in q_table:
    q_table[state] = {a: 0 for a in actions}
action = max(q_table[state], key=q_table[state].get)
position_a = default_data[selected_country_a]["position"]
position_b = default_data[selected_country_b]["position"]
if action == "adjust toward A":
    position_b = position_a
elif action == "adjust toward B":
    position_a = position_b
def get_reward(a,b):
    return (1 if a==b else -1) * lessons_learned_factor
reward = get_reward(position_a, position_a)
q_table[state][action] += 0.1 * (reward + 0.9 * max(q_table[state].values()) - q_table[state][action])

influence_a = default_data[selected_country_a]["influence"]
influence_b = default_data[selected_country_b]["influence"]
gdp_a = default_data[selected_country_a]["gdp"]
gdp_b = default_data[selected_country_b]["gdp"]
alignment_factor = 1.0 if position_a == position_b else 0.5
intelligence_a = influence_a * alignment_factor
intelligence_b = influence_b * alignment_factor

edge_memory = st.session_state["edge_memory"]
edge_key = (selected_country_a, selected_country_b)
if edge_key not in edge_memory:
    edge_memory[edge_key] = 0.5
learning_factor = q_table[state][action] / (max(q_table[state].values()) + 1e-6) if max(q_table[state].values()) != 0 else 0.5
edge_weight_dynamic = round(learning_factor * (influence_a + influence_b) / 2, 2)
edge_memory[edge_key] = edge_weight_dynamic

# Influence network graph
label_a = f"{selected_country_a}\nGDP: {gdp_a}T\nInfluence: {influence_a}"
label_b = f"{selected_country_b}\nGDP: {gdp_b}T\nInfluence: {influence_b}"
G = nx.DiGraph()
G.add_node(label_a, gdp=gdp_a, influence=influence_a, intelligence=intelligence_a)
G.add_node(label_b, gdp=gdp_b, influence=influence_b, intelligence=intelligence_b)
G.add_edge(label_a, label_b, weight=edge_weight_dynamic)

pagerank_scores = nx.pagerank(G, personalization={label_a: influence_a, label_b: influence_b})
tab1, tab2 = st.tabs(["🕸️ Influence Network Graph", "🗺️ Interactive Geo Map"])
with tab1:
    st.subheader("🌐 AI Governance Intelligence Influence Map")
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    node_colors = []
    for n in G.nodes():
        intel = G.nodes[n]["intelligence"]
        node_colors.append("blue" if intel>=0.9 else ("green" if intel>=0.75 else ("yellow" if intel>=0.5 else "red")))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=3000, font_size=10, font_weight="bold", ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"Weight: {v:.2f}" for k,v in nx.get_edge_attributes(G,"weight").items()}, font_color="purple", ax=ax)
    st.pyplot(fig)
    st.subheader("📊 Influence Propagation (PageRank)")
    st.dataframe(pd.DataFrame({"Country":[selected_country_a,selected_country_b],"PageRank Score":[pagerank_scores[label_a],pagerank_scores[label_b]]}))

with tab2:
    st.subheader("🗺️ Intelligence Map+: Hover for Geopolitics")
    to_iso3 = {"United States":"USA","United Kingdom":"GBR","Japan":"JPN","China":"CHN","Brazil":"BRA","India":"IND","Dubai":"ARE"}
    rows = []
    for k,v in default_data.items():
        if k == "NATO" or k not in to_iso3:
            continue
        role = role_country_a if k == selected_country_a else (role_country_b if k == selected_country_b else "—")
        rows.append({"entity":k,"iso3":to_iso3[k],"gdp_trillion":v["gdp"],"influence":v["influence"],"position":v["position"],"role":role,"policy":selected_policy})
    geo_df = pd.DataFrame(rows)
    fig_geo = px.choropleth(geo_df, locations="iso3", color="influence", color_continuous_scale="Viridis", range_color=(0.5,1.0), hover_name="entity", hover_data={"iso3":False,"gdp_trillion":True,"influence":True,"position":True,"role":True,"policy":True}, projection="natural earth", title="") if not geo_df.empty else go.Figure()
    nato = "NATO"
    nato_hover = (f"<b>{nato}</b><br>"
                  f"GDP (combined): {default_data[nato]['gdp']}T<br>"
                  f"Influence: {default_data[nato]['influence']}<br>"
                  f"Position: {default_data[nato]['position']}<br>"
                  f"Policy: {selected_policy}")
    fig_geo.add_trace(go.Scattergeo(lon=[4.3517], lat=[50.8503], mode="markers+text", text=["NATO"], textposition="top center", marker=dict(size=10, symbol="diamond"), hovertemplate=nato_hover))

    def iso_to_centroid(iso):
        return {"USA":(-98.5795,39.8283),"GBR":(-3.435973,55.378051),"JPN":(138.2529,36.2048),"CHN":(104.1954,35.8617),"BRA":(-51.9253,-14.2350),"IND":(78.9629,20.5937),"ARE":(54.3773,23.4241)}.get(iso,(0,0))

    for sel in [selected_country_a, selected_country_b]:
        if sel in to_iso3:
            lon, lat = iso_to_centroid(to_iso3[sel])
            fig_geo.add_trace(go.Scattergeo(lon=[lon], lat=[lat], mode="markers", marker=dict(size=12), hovertemplate=(f"<b>{sel}</b><br>" f"Role: {role_country_a if sel==selected_country_a else role_country_b}" "<extra></extra>")))

    fig_geo.update_layout(margin=dict(l=0,r=0,t=0,b=0), coloraxis_colorbar=dict(title="Influence"), geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"))
    st.plotly_chart(fig_geo, use_container_width=True)
'''
with open('pages/auracelle_charlie_simulation.py','w') as f:
    f.write(simulation_py_content)


streamlit_process = subprocess.Popen(["streamlit","run","app.py","--server.port","8501","--server.address","0.0.0.0"])
time.sleep(5)
public_url = "https://auracelle-charlie-app.azurewebsites.net"
print(f"🔗 Your app is live at: {public_url}")
from IPython.display import HTML, display
display(HTML(f'<a href="{public_url}" target="_blank">🔗 Open Auracelle Charlie (Login → Simulation)</a>'))
