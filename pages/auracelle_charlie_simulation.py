import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import plotly.graph_objects as go

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Auracelle Charlie – Simulation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# Header & Instructions
# -------------------------------
st.title("🌐 Auracelle Charlie – Policy Simulation")

with st.expander("📘 Instructions", expanded=False):
    st.markdown("""
    1️⃣ **Login**: Ensure you're logged in via the Captive Page.

    2️⃣ **Select Policy**: Use the sidebar or simulation controls to choose an AI governance policy.

    3️⃣ **Simulation**: Run the simulation and observe network dynamics and RL adaptation.

    4️⃣ **Visuals**: Interact with the influence graph and geopolitical overlays.

    5️⃣ **Analyze Results**: Use the PageRank table and hover-tooltips to inspect actor influence.

    6️⃣ **Iterate**: Adjust policies or agents and re-run to see comparative outcomes.
    """)

# -------------------------------
# Dummy Policy Placeholder
# -------------------------------
st.subheader("🔎 Assess a Policy")
st.info("Policy selection logic will go here. Choose a policy from the sidebar or dropdown.")

# -------------------------------
# Dummy Graph (NetworkX + Plotly)
# -------------------------------
G = nx.karate_club_graph()
pos = nx.spring_layout(G, seed=42)
pr = nx.pagerank(G)

node_x = []
node_y = []
node_text = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(f"Node {node}<br>PageRank: {pr[node]:.3f}")

edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color="#888"),
    hoverinfo="none",
    mode="lines"))

fig.add_trace(go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    textposition="top center",
    hovertext=node_text,
    hoverinfo="text",
    marker=dict(
        showscale=True,
        colorscale="YlGnBu",
        color=[pr[n] for n in G.nodes()],
        size=20,
        colorbar=dict(thickness=15, title="PageRank", xanchor="left", titleside="right")
    )
))

fig.update_layout(
    title="Influence Network Graph (Karate Club Example)",
    title_x=0.5,
    showlegend=False,
    margin=dict(l=40, r=40, t=60, b=30),
    height=600,
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Dummy Data Table
# -------------------------------
st.subheader("📊 Influence Table")

df = pd.DataFrame({
    "Node": list(pr.keys()),
    "PageRank": list(pr.values())
}).sort_values(by="PageRank", ascending=False)

st.dataframe(df, use_container_width=True)
