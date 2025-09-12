import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import plotly.graph_objects as go
from collections import defaultdict

st.set_page_config(page_title="Auracelle Charlie", layout="wide", initial_sidebar_state="collapsed")

# 🧠 AI Governance Policy Wargame: A Multi-Agent Simulation Sandbox
st.title("🧠 AI Governance Policy Wargame: A Multi-Agent Simulation Sandbox")
st.markdown("### 🌍 Auracelle Charlie: Intelligence Map+ Edition 🚀")

# ------------------ Instructions ------------------
with st.expander("📘 Instructions"):
    st.markdown("""
    - Select a policy and country to simulate its effect.
    - The influence graph and geopolitical map will update accordingly.
    - Click 🔎 **Assess a Policy** to view policy implications.
    - PageRank determines stakeholder influence.
    - More features coming soon (data ingress, multi-agent reinforcement learning).
    """)

# ------------------ Popover ------------------
st.popover("🔎 Assess a Policy")
st.markdown("""
Click this to view how a selected policy affects the global network.
Use the dropdowns below to begin.
""")

# ------------------ Policy & Country Selection ------------------
policy_options = ["Data Localization Mandate", "AI Ethics Treaty", "Open Source AI Ban"]
country_list = ["Dubai", "UK", "US", "Japan", "China", "Brazil", "India", "NATO"]
selected_policy = st.selectbox("Select a Policy", policy_options)
selected_country = st.selectbox("Select a Country", country_list)

# ------------------ Build Network Graph ------------------
G = nx.DiGraph()
nodes = ["Dubai", "UK", "US", "Japan", "China", "Brazil", "India", "NATO"]
edges = [("US", "UK"), ("US", "Japan"), ("UK", "Dubai"), ("Japan", "India"),
         ("China", "Brazil"), ("NATO", "US"), ("NATO", "UK"), ("NATO", "Dubai")]
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# ------------------ Compute Influence ------------------
pr = nx.pagerank(G)
pr_df = pd.DataFrame(pr.items(), columns=["Node", "PageRank"]).sort_values(by="PageRank", ascending=False)
st.subheader("📊 Influence Rankings (PageRank)")
st.dataframe(pr_df, use_container_width=True)

# ------------------ Visualization Tabs ------------------
tabs = st.tabs(["🇺 Network Graph", "🌐 Geopolitical Map"])

with tabs[0]:
    fig, ax = plt.subplots(figsize=(8,6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10, ax=ax)
    st.pyplot(fig)

with tabs[1]:
    geo_map = go.Figure()
    lat_lon_map = {
        "Dubai": (25.276987, 55.296249),
        "UK": (55.3781, -3.4360),
        "US": (37.0902, -95.7129),
        "Japan": (36.2048, 138.2529),
        "China": (35.8617, 104.1954),
        "Brazil": (-14.2350, -51.9253),
        "India": (20.5937, 78.9629),
        "NATO": (50.8503, 4.3517)  # Brussels
    }
    for node in G.nodes:
        lat, lon = lat_lon_map[node]
        geo_map.add_trace(go.Scattergeo(
            lon=[lon],
            lat=[lat],
            text=node,
            mode='markers+text',
            marker=dict(size=10),
            name=node
        ))
    geo_map.update_geos(projection_type="natural earth")
    geo_map.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(geo_map, use_container_width=True)

# ------------------ Q-Learning Placeholder ------------------
st.subheader("🧪 AI Simulation Notes")
st.markdown("""
Future editions will allow agents (countries, NGOs, firms) to learn policy strategies via reinforcement learning. This placeholder represents early Q-learning adaptation.

```
Q(s, a) ← Q(s, a) + α [R + γ max Q(s', a') - Q(s, a)]
```

Where:
- `s` = current state
- `a` = action taken (e.g., policy enactment)
- `R` = reward (e.g., regional influence gain)
- `γ` = discount factor

""")

# ------------------ End ------------------
st.caption("Auracelle Charlie © 2025 | Streamlit Version | Maintained by Grace-Alice Evans")
