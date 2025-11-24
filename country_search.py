import pandas as pd
import streamlit as st
import os

def show_country_search():
    """Display country search functionality with all related data"""
    
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
    
    # Get list of all countries
    country_list = sorted(players_df['Team'].unique().tolist())
    
    st.subheader("🌍 Country Search")
    
    # Search box for country
    selected_country = st.selectbox(
        "Select a country:",
        options=[""] + country_list,
        index=0,
        placeholder="Type to search for a country..."
    )
    
    if selected_country:
        # Get all players from the selected country
        country_players = players_df[players_df['Team'] == selected_country]
        
        st.markdown("---")
        st.subheader(f"🏐 {selected_country} Team Overview")
        
        # Display team statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Players", len(country_players))
        with col2:
            avg_height = country_players['Height'].mean()
            st.metric("Average Height", f"{avg_height:.1f} cm")
        with col3:
            avg_age = 2024 - country_players['Birth_Year'].mean()
            st.metric("Average Age", f"{avg_age:.1f}")
        
        st.markdown("---")
        
        # Display players by position
        st.subheader("👥 Squad by Position")
        positions = country_players['Position'].value_counts()
        
        for position, count in positions.items():
            position_players = country_players[country_players['Position'] == position]
            with st.expander(f"{position} ({count} players)"):
                for _, player in position_players.iterrows():
                    age = 2024 - player['Birth_Year']
                    st.write(f"**{player['Name']}** - {player['Height']} cm - Age: {int(age)}")
        
        st.markdown("---")
        
        # Display team performance statistics by category
        st.subheader("📊 Team Performance Statistics")
        
        categories = {
            "⚔️ Attack": attackers_df,
            "🛡️ Block": blockers_df,
            "🤿 Dig": diggers_df,
            "📥 Receive": receivers_df,
            "🎯 Scoring": scorers_df,
            "🏐 Serve": servers_df,
            "🤝 Setter": setters_df
        }
        
        for category_name, df in categories.items():
            # Get players from this country who have stats in this category
            country_stats = df[df['Team'] == selected_country]
            
            if not country_stats.empty:
                with st.expander(f"{category_name} ({len(country_stats)} players)"):
                    # Sort by the first numeric column (usually points or a key metric)
                    numeric_cols = country_stats.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        sort_col = numeric_cols[0]
                        country_stats = country_stats.sort_values(by=sort_col, ascending=False)
                    
                    # Display as a dataframe
                    st.dataframe(
                        country_stats,
                        use_container_width=True,
                        hide_index=True
                    )
