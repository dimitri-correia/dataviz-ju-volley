import pandas as pd
import plotly.express as px
import streamlit as st

def show_ranking_by_action():
    """
    Display rankings based on volleyball actions (Attack, Block, Service)
    """
    st.header("Classement par action")
    
    # Load players data for position filtering
    df_players = pd.read_csv("dataset_vnl_men_2024/Players.csv", encoding='latin-1')
    
    # Action selection with tabs
    tab1, tab2, tab3 = st.tabs(["Attack", "Block", "Service"])
    
    with tab1:
        df = pd.read_csv("dataset_vnl_men_2024/Attackers.csv", encoding='latin-1')
        st.subheader("Top Attackers")
        df = df.merge(df_players[['Name', 'Team', 'Position']], on=['Name', 'Team'], how='left')
        df = df[df['Position'].isin(['MB', 'O', 'OH'])]
        df = df.drop(columns=['Att_Attack', 'MAvg_Attack'], errors='ignore')
        
        # Interactive visualization options
        st.subheader("Interactive Visualization")
        numeric_cols = df.select_dtypes(include="number").columns
        
        if len(numeric_cols) > 0:
            # User selects the metric for X-axis, Y-axis is always player name
            metric = st.selectbox("Select Metric", numeric_cols, key="attack_metric")
            
            # Sort by the selected metric and take top players
            df_sorted = df.sort_values(by=metric, ascending=False).head(20)
            
            # Create horizontal bar chart
            fig = px.bar(
                df_sorted, 
                x=metric, 
                y='Name', 
                orientation='h',
                title=f"Attack - Top 20 Players by {metric}",
                hover_data=df_sorted.columns,
                labels={'Name': 'Player'},
                height=max(400, len(df_sorted) * 25)  # Dynamic height to show all names
            )
            
            # Reverse the Y-axis so highest values are at the top
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Display the data
        st.dataframe(df)
    
    with tab2:
        df = pd.read_csv("dataset_vnl_men_2024/Blockers.csv", encoding='latin-1')
        st.subheader("Top Blockers")
        df = df.merge(df_players[['Name', 'Team', 'Position']], on=['Name', 'Team'], how='left')
        df = df[df['Position'].isin(['MB', 'O', 'OH', 'S'])]
        df = df.drop(columns=['Att_Block', 'MAvg_Block', 'Rebounds'], errors='ignore')
        
        # Interactive visualization options
        st.subheader("Interactive Visualization")
        numeric_cols = df.select_dtypes(include="number").columns
        
        if len(numeric_cols) > 0:
            # User selects the metric for X-axis, Y-axis is always player name
            metric = st.selectbox("Select Metric", numeric_cols, key="block_metric")
            
            # Sort by the selected metric and take top players
            df_sorted = df.sort_values(by=metric, ascending=False).head(20)
            
            # Create horizontal bar chart
            fig = px.bar(
                df_sorted, 
                x=metric, 
                y='Name', 
                orientation='h',
                title=f"Block - Top 20 Players by {metric}",
                hover_data=df_sorted.columns,
                labels={'Name': 'Player'},
                height=max(400, len(df_sorted) * 25)  # Dynamic height to show all names
            )
            
            # Reverse the Y-axis so highest values are at the top
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Display the data
        st.dataframe(df)
    
    with tab3:
        df = pd.read_csv("dataset_vnl_men_2024/Servers.csv", encoding='latin-1')
        st.subheader("Top Servers")
        df = df.merge(df_players[['Name', 'Team', 'Position']], on=['Name', 'Team'], how='left')
        df = df[df['Position'].isin(['L']) == False]
        df = df.drop(columns=['Att_Serve', 'MAvg_Serve'], errors='ignore')
        
        # Interactive visualization options
        st.subheader("Interactive Visualization")
        numeric_cols = df.select_dtypes(include="number").columns
        
        if len(numeric_cols) > 0:
            # User selects the metric for X-axis, Y-axis is always player name
            metric = st.selectbox("Select Metric", numeric_cols, key="service_metric")
            
            # Sort by the selected metric and take top players
            df_sorted = df.sort_values(by=metric, ascending=False).head(20)
            
            # Create horizontal bar chart
            fig = px.bar(
                df_sorted, 
                x=metric, 
                y='Name', 
                orientation='h',
                title=f"Service - Top 20 Players by {metric}",
                hover_data=df_sorted.columns,
                labels={'Name': 'Player'},
                height=max(400, len(df_sorted) * 25)  # Dynamic height to show all names
            )
            
            # Reverse the Y-axis so highest values are at the top
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Display the data
        st.dataframe(df)