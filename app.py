import streamlit as st
from ranking_by_action import show_ranking_by_action
from ranking_by_position import show_ranking_by_position
from player_search import show_player_search
from country_search import show_country_search

st.title("Dataviz - VNL Men 2024")

# Main tabs to choose ranking type
tab1, tab2, tab3, tab4 = st.tabs(["Ranking by action", "Ranking by position", "Player Search", "Country Search"])

with tab1:
    show_ranking_by_action()

with tab2:
    show_ranking_by_position()

with tab3:
    show_player_search()

with tab4:
    show_country_search()
