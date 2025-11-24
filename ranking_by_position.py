import streamlit as st

from data_loader import load_players, load_setters


def show_ranking_by_position():
    """Display rankings based on player positions"""

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Setter", "Outside Hitter", "Middle Blocker", "Opposite", "Libero"]
    )

    with tab1:
        df_players = load_players()
        df_players = df_players[df_players["Position"] == "S"]
        df = load_setters().copy()
        df = df.merge(
            df_players[["Name", "Team", "Position"]], on=["Name", "Team"], how="left"
        )

        st.subheader("Top Setters")
        st.text("To compare the players, we use the following algorithm:\n")

