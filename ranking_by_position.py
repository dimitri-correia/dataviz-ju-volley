import pandas as pd
import streamlit as st

DATASET_PATH = "dataset_vnl_men_2024"


def show_ranking_by_position():
    """Display rankings based on player positions"""
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Setter", "Outside Hitter", "Middle Blocker", "Opposite", "Libero"]
    )

    with tab1:
        df_players = pd.read_csv(f"{DATASET_PATH}/Players.csv")
        df_players = df_players[df_players['Position'] == 'S']
        df = pd.read_csv(f"{DATASET_PATH}/Setters.csv")
        df = df.merge(df_players[['Name', 'Team', 'Position']], on=['Name', 'Team'], how='left')

        st.subheader("Top Setters")
        st.text("To compare the players, we use the following algorithm:\n")

