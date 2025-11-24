import pandas as pd
import streamlit as st
import os

def show_player_search():
    """Display player search functionality with all related data"""
    
    # Load all datasets
    dataset_path = "dataset_vnl_men_2024"
    
    players_df = pd.read_csv(os.path.join(dataset_path, "Players.csv"))
    attackers_df = pd.read_csv(os.path.join(dataset_path, "Attackers.csv"))
    blockers_df = pd.read_csv(os.path.join(dataset_path, "Blockers.csv"))
    diggers_df = pd.read_csv(os.path.join(dataset_path, "Diggers.csv"))
    receivers_df = pd.read_csv(os.path.join(dataset_path, "Receivers.csv"))
    scorers_df = pd.read_csv(os.path.join(dataset_path, "Scorers.csv"))
    servers_df = pd.read_csv(os.path.join(dataset_path, "Servers.csv"))
    setters_df = pd.read_csv(os.path.join(dataset_path, "Setters.csv"))
    
    # Get list of all players
    player_list = sorted(players_df['Name'].unique().tolist())
    
    st.subheader("🔍 Player Search")
    
    # Search box with autocomplete
    selected_player = st.selectbox(
        "Select a player:",
        options=[""] + player_list,
        index=0,
        placeholder="Type to search for a player..."
    )
    
    if selected_player:
        # Display player basic info
        player_info = players_df[players_df['Name'] == selected_player].iloc[0]
        
        st.markdown("---")
        st.subheader(f"📋 {selected_player}'s Profile")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Team", player_info['Team'])
        with col2:
            st.metric("Position", player_info['Position'])
        with col3:
            st.metric("Height", f"{player_info['Height']} cm")
        with col4:
            st.metric("Birth Year", int(player_info['Birth_Year']))
        
        st.markdown("---")
        
        # Check and display stats from each category
        categories = {
            "⚔️ Attack Stats": attackers_df,
            "🛡️ Block Stats": blockers_df,
            "🤿 Dig Stats": diggers_df,
            "📥 Receive Stats": receivers_df,
            "🎯 Scoring Stats": scorers_df,
            "🏐 Serve Stats": servers_df,
            "🤝 Setter Stats": setters_df
        }
        
        for category_name, df in categories.items():
            player_data = df[df['Name'] == selected_player]
            
            if not player_data.empty:
                st.subheader(category_name)
                
                # Display as columns for better readability
                player_stats = player_data.iloc[0].to_dict()
                
                # Remove Name and Team from stats display
                stats_to_show = {k: v for k, v in player_stats.items() if k not in ['Name', 'Team']}
                
                # Create columns dynamically based on number of stats
                num_stats = len(stats_to_show)
                num_cols = min(4, num_stats)
                
                if num_cols > 0:
                    cols = st.columns(num_cols)
                    for idx, (stat_name, stat_value) in enumerate(stats_to_show.items()):
                        with cols[idx % num_cols]:
                            # Format the value
                            if isinstance(stat_value, float):
                                formatted_value = f"{stat_value:.2f}"
                            else:
                                formatted_value = str(stat_value)
                            st.metric(stat_name.replace('_', ' '), formatted_value)
                
                st.markdown("---")
        
        # Check if player has no stats in any category
        has_stats = any(not df[df['Name'] == selected_player].empty for df in categories.values())
        if not has_stats:
            st.info("No performance statistics available for this player in the dataset.")
