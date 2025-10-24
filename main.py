# EA SPORTS FC 25 PLAYER
import streamlit as st
import os
import pandas as pd
import plotly.express as px


st.set_page_config(
     page_title='EA SPORTS FC 25 PLAYER DASHBOARD',
     page_icon="static/EA.jpeg",
     layout="wide"
)

@st.cache_data
def load_data():
     df = pd.read_csv("data/EA_FC25_Player_Data.csv")
     # clean column names (in case they may contain spaces)
     df.columns = [c.strip().title() for c in df.columns]
     return df

df = load_data()

# --- SIDEBAR ---

st.sidebar.title('Filters')   
st.sidebar.markdown("Use filters below to explore player data")

leagues = st.sidebar.multiselect("Select League(s)", sorted(df['League'].dropna().unique()))
positions = st.sidebar.multiselect("Select position(s)", sorted(df['Position'].dropna().unique()))
clubs = st.sidebar.multiselect("Select Club(s)", sorted(df['Team'].dropna().unique()))

# --- FILTER DATA ---
filtered_df = df.drop(df.columns[[0, 1]], axis=1).copy()

if leagues:
     filtered_df = filtered_df[filtered_df["League"].isin(leagues)]
if positions:
     filtered_df = filtered_df[filtered_df["Position"].isin(positions)]
if clubs:
     filtered_df = filtered_df[filtered_df["Team"].isin(clubs)]

st.header("EA SPORTS FC 25 Player Performance Dashboard")

# --- SUMMARY METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Players", f"{len(filtered_df)}")
col2.metric("Avg Overall", round(filtered_df['Ovr'].mean(), 2) if "Ovr" in filtered_df else "N/A")
mean_age = filtered_df['Age'].mean() if "Age" in filtered_df.columns else None
col3.metric("Avg Age", round(mean_age) if mean_age and not pd.isna(mean_age) else "N/A")


# --- PLAYER TABLE ---
st.markdown("### Player List")
st.dataframe(
     filtered_df,
     use_container_width=True
)

st.subheader("Top 10 Players by Overall Rating")
top_players = filtered_df.nlargest(10, "Ovr")
fig1 = px.bar(
     top_players,
     x="Ovr",
     y="Name",
     color="Team",
     text="Ovr",
     orientation="h", 
     title="Top 10 Overall Players", 
)

# Hide the x-axis
fig1.update_layout(
    xaxis=dict(
        showticklabels=False, 
        title="Overall",
    )
)


# tooltip
fig1.update_traces(
     textposition="outside",
     hovertemplate=(
          "<b>%{y}</b><br>"           
          "Overall: %{x}<br>"         
          "Team: %{customdata[0]}<br>" 
          "Age: %{customdata[1]}<extra></extra><br>"
     ),
     customdata=top_players[["Team", "Age"]],
)
st.plotly_chart(fig1, use_container_width=True)


# Rating Distribution
st.subheader("Distribution of Overall Ratings")
fig2 = px.histogram(
     filtered_df,
     x="Ovr",
     nbins=20,
     title="Overall Rating Distribution")


fig2.update_layout(
    xaxis=dict(
        showticklabels=True,  
        title="Overall",       
    )
)
st.plotly_chart(fig2, use_container_width=True)


# Nationality Ratings
st.subheader("Average Overall Ratings by Nationality (Top 10)")
nat_df = (
     filtered_df.groupby("Nation")["Ovr"]
     .mean()
     .round()
     .sort_values(ascending=False)
     .head(10)
     .reset_index()
)
fig3 = px.bar(nat_df, x="Nation", y="Ovr", color="Nation", text="Ovr")
fig3.update_traces(textposition="outside")
st.plotly_chart(fig3, use_container_width=True)


# --- PLAYER COMPARISON ---
st.markdown("---")
st.markdown("## ⚔️ Player Comparison")

colA, colB = st.columns(2)
with colA:
    p1 = st.selectbox("Select Player 1", sorted(filtered_df["Name"].unique()))
with colB:
    p2 = st.selectbox("Select Player 2", sorted(filtered_df["Name"].unique()), index=1 if len(filtered_df) > 1 else 0)
    
player1 = filtered_df[filtered_df["Name"] == p1].iloc[0]
player2 = filtered_df[filtered_df["Name"] == p2].iloc[0]

attributes = ["Pac", "Pas", "Dri", "Def", "Phy"]
compare_df = pd.DataFrame({
    "Attribute": attributes,
    p1: [player1[attr] if attr in player1 else 0 for attr in attributes],
    p2: [player2[attr] if attr in player2 else 0 for attr in attributes],
})

fig4 = px.line_polar(
    compare_df.melt(id_vars=["Attribute"], var_name="Player", value_name="Score"),
    r="Score",
    theta="Attribute",
    color="Player",
    line_close=True,  # Don't connect the last to the first point
    title=f"{p1} vs {p2} — Attribute Comparison",
    color_discrete_sequence=["#1f77b4", "#d62728"]
)

fig4.update_traces(line=dict(width=2), marker=dict(size=6), fill='toself', opacity=0.4)
st.plotly_chart(fig4, use_container_width=True)
st.dataframe(compare_df)