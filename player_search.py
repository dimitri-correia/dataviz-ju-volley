import pandas as pd
import streamlit as st

DATASET_PATH = "dataset_vnl_men_2024"

# Define stat categories and their corresponding CSV files
STAT_CATEGORIES = {
    "⚔️ Attack Stats": "Attackers.csv",
    "🛡️ Block Stats": "Blockers.csv",
    "🤿 Dig Stats": "Diggers.csv",
    "📥 Receive Stats": "Receivers.csv",
    "🎯 Scoring Stats": "Scorers.csv",
    "🏐 Serve Stats": "Servers.csv",
    "🤝 Setter Stats": "Setters.csv"
}


def show_player_search():
    """Display player search functionality with all related data"""
    players_df = pd.read_csv(f"{DATASET_PATH}/Players.csv")
    player_list = sorted(players_df['Name'].unique().tolist())
    
    selected_player = st.selectbox(
        "Select a player:",
        options=[""] + player_list,
        index=0,
        placeholder="Type to search for a player..."
    )
    
    if not selected_player:
        return
    
    player_info = players_df[players_df['Name'] == selected_player].iloc[0]
    
    st.markdown("---")
    st.subheader(f"📋 {selected_player}'s Profile")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Team", player_info['Team'])
    col2.metric("Position", player_info['Position'])
    col3.metric("Height", f"{player_info['Height']} cm")
    col4.metric("Birth Year", int(player_info['Birth_Year']))
    
    st.markdown("---")
    
    # Display stats from each category
    has_stats = False
    for category_name, filename in STAT_CATEGORIES.items():
        df = pd.read_csv(f"{DATASET_PATH}/{filename}")
        player_data = df[df['Name'] == selected_player]
        
        if player_data.empty:
            continue
        
        has_stats = True
        st.subheader(category_name)
        
        stats = {k: v for k, v in player_data.iloc[0].to_dict().items() if k not in ['Name', 'Team']}
        
        cols = st.columns(min(4, len(stats)))
        for idx, (stat_name, stat_value) in enumerate(stats.items()):
            formatted = f"{stat_value:.2f}" if isinstance(stat_value, float) else str(stat_value)
            cols[idx % len(cols)].metric(stat_name.replace('_', ' '), formatted)
        
        st.markdown("---")
    
    if not has_stats:
        st.info("No performance statistics available for this player in the dataset.")
