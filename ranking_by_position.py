import pandas as pd
import streamlit as st

DATASET_PATH = "dataset_vnl_men_2024"


def show_ranking_by_position():
    """Display rankings based on player positions"""
    st.header("Classement par position")
    
    position = st.selectbox(
        "Choisir une position",
        ["Setter", "Outside Hitter", "Middle Blocker", "Opposite", "Libero"]
    )
    
    st.info(f"Classement pour la position: {position}")
    st.warning("⚠️ L'algorithme de classement par position sera implémenté prochainement.")
    
    st.markdown("""
    ### À venir:
    - Algorithme de notation par position
    - Critères spécifiques pour chaque poste
    - Visualisations adaptées
    
    ### Positions disponibles:
    - **Setter**: Passeur
    - **Outside Hitter**: Attaquant de pointe
    - **Middle Blocker**: Central
    - **Opposite**: Attaquant opposé
    - **Libero**: Libéro
    """)
    
    st.subheader("Aperçu des joueurs")
    df_players = pd.read_csv(f"{DATASET_PATH}/Players.csv")
    st.dataframe(df_players.head(10))
