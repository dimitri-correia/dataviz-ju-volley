import pandas as pd
import streamlit as st

DATASET_PATH = "dataset_vnl_men_2024"

# Define stat categories and their corresponding CSV files
STAT_CATEGORIES = {
    "⚔️ Attack": "Attackers.csv",
    "🛡️ Block": "Blockers.csv",
    "🤿 Dig": "Diggers.csv",
    "📥 Receive": "Receivers.csv",
    "🎯 Scoring": "Scorers.csv",
    "🏐 Serve": "Servers.csv",
    "🤝 Setter": "Setters.csv"
}


def show_country_search():
    """Display country search functionality with all related data"""
    players_df = pd.read_csv(f"{DATASET_PATH}/Players.csv")
    country_list = sorted(players_df['Team'].unique().tolist())
    
    st.subheader("🌍 Country Search")
    
    selected_country = st.selectbox(
        "Select a country:",
        options=[""] + country_list,
        index=0,
        placeholder="Type to search for a country..."
    )
    
    if not selected_country:
        return
    
    country_players = players_df[players_df['Team'] == selected_country]
    
    st.markdown("---")
    st.subheader(f"🏐 {selected_country} Team Overview")
    
    # Team statistics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Players", len(country_players))
    col2.metric("Average Height", f"{country_players['Height'].mean():.1f} cm")
    col3.metric("Average Age", f"{2024 - country_players['Birth_Year'].mean():.1f}")
    
    st.markdown("---")
    
    # Players by position
    st.subheader("👥 Squad by Position")
    for position, count in country_players['Position'].value_counts().items():
        position_players = country_players[country_players['Position'] == position]
        with st.expander(f"{position} ({count} players)"):
            for _, player in position_players.iterrows():
                age = 2024 - player['Birth_Year']
                st.write(f"**{player['Name']}** - {player['Height']} cm - Age: {int(age)}")
    
    st.markdown("---")
    
    # Team performance by category
    st.subheader("📊 Team Performance Statistics")
    for category_name, filename in STAT_CATEGORIES.items():
        df = pd.read_csv(f"{DATASET_PATH}/{filename}")
        country_stats = df[df['Team'] == selected_country]
        
        if country_stats.empty:
            continue
        
        with st.expander(f"{category_name} ({len(country_stats)} players)"):
            numeric_cols = country_stats.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                country_stats = country_stats.sort_values(by=numeric_cols[0], ascending=False)
            st.dataframe(country_stats, use_container_width=True, hide_index=True)
