import plotly.express as px
import streamlit as st

from data_loader import load_attackers, load_blockers, load_players, load_servers


def display_action_ranking(df, action_name, metric_key):
    """Display ranking visualization for a specific action"""
    
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        st.dataframe(df)
        return
    
    metric = st.selectbox("Select Metric", numeric_cols, key=metric_key)
    df_sorted = df.sort_values(by=metric, ascending=False).head(20)
    
    fig = px.bar(
        df_sorted, 
        x=metric, 
        y='Name', 
        orientation='h',
        title=f"{action_name} - Top 20 Players by {metric}",
        hover_data=df_sorted.columns,
        labels={'Name': 'Player'},
        height=max(400, len(df_sorted) * 25)
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
    
    st.plotly_chart(fig, width='stretch')
    st.dataframe(df)


def show_ranking_by_action():
    """Display rankings based on volleyball actions (Attack, Block, Service)"""

    df_players = load_players()

    tab1, tab2, tab3 = st.tabs(["Attack", "Block", "Service"])

    with tab1:
        df = load_attackers().copy()
        df = df.merge(df_players[['Name', 'Team', 'Position']], on=['Name', 'Team'], how='left')
        df = df[df['Position'].isin(['MB', 'O', 'OH'])]
        df = df.drop(columns=['Att_Attack', 'MAvg_Attack'], errors='ignore')
        display_action_ranking(df, "Attackers", "attack_metric")

    with tab2:
        df = load_blockers().copy()
        df = df.merge(df_players[['Name', 'Team', 'Position']], on=['Name', 'Team'], how='left')
        df = df[df['Position'].isin(['MB', 'O', 'OH', 'S'])]
        df = df.drop(columns=['Att_Block', 'MAvg_Block', 'Rebounds'], errors='ignore')
        display_action_ranking(df, "Blockers", "block_metric")

    with tab3:
        df = load_servers().copy()
        df = df.merge(df_players[['Name', 'Team', 'Position']], on=['Name', 'Team'], how='left')
        df = df[~df['Position'].isin(['L'])]
        df = df.drop(columns=['Att_Serve', 'MAvg_Serve'], errors='ignore')
        display_action_ranking(df, "Servers", "service_metric")