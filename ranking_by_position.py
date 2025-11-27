import pandas as pd
import plotly.express as px
import streamlit as st

from data_loader import (
    load_attackers,
    load_blockers,
    load_diggers,
    load_players,
    load_receivers,
    load_servers,
    load_setters,
)


def calculate_efficiency(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Calculate efficiency as a ratio, handling division by zero."""
    return (numerator / denominator.replace(0, float("nan"))) * 100


def display_efficiency_chart(df: pd.DataFrame, position_name: str):
    """Display a horizontal bar chart of player efficiencies."""
    if df.empty:
        st.info(f"No data available for {position_name}.")
        return

    # Sort by overall efficiency and get top 20
    df_sorted = df.sort_values(by="Overall Efficiency", ascending=False).head(20)

    fig = px.bar(
        df_sorted,
        x="Overall Efficiency",
        y="Name",
        orientation="h",
        title=f"{position_name} - Top 20 Players by Overall Efficiency",
        hover_data=df_sorted.columns,
        labels={"Name": "Player"},
        height=max(400, len(df_sorted) * 25),
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, hide_index=True)


def get_setter_efficiency(df_players: pd.DataFrame) -> pd.DataFrame:
    """Calculate efficiency metrics for Setters.

    Metrics:
    - Setting efficiency: successful sets / total sets
    - Service efficiency: aces / total serves
    - Dig efficiency: successful digs / total digs
    """
    setters = df_players[df_players["Position"] == "S"][["Name", "Team"]].copy()

    df_set = load_setters()
    df_serve = load_servers()
    df_dig = load_diggers()

    df = setters.merge(df_set[["Name", "Team", "Sf_Set", "Tot_Set"]], on=["Name", "Team"], how="left")
    df = df.merge(df_serve[["Name", "Team", "ServePoints", "TotalServeMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_dig[["Name", "Team", "Sf_Dig", "T_Dig"]], on=["Name", "Team"], how="left")

    df["Setting Efficiency"] = calculate_efficiency(df["Sf_Set"], df["Tot_Set"])
    df["Service Efficiency"] = calculate_efficiency(df["ServePoints"], df["TotalServeMade"])
    df["Dig Efficiency"] = calculate_efficiency(df["Sf_Dig"], df["T_Dig"])

    df["Overall Efficiency"] = df[["Setting Efficiency", "Service Efficiency", "Dig Efficiency"]].mean(axis=1)

    return df[["Name", "Team", "Setting Efficiency", "Service Efficiency", "Dig Efficiency", "Overall Efficiency"]].dropna(subset=["Overall Efficiency"])


def get_outside_hitter_efficiency(df_players: pd.DataFrame) -> pd.DataFrame:
    """Calculate efficiency metrics for Outside Hitters.

    Metrics:
    - Service efficiency: aces / total serves
    - Attack success: successful attacks / total attacks
    - Block efficiency: successful blocks / total blocks
    - Reception efficiency: successful receptions / total receptions
    - Dig efficiency: successful digs / total digs
    """
    outside_hitters = df_players[df_players["Position"] == "OH"][["Name", "Team"]].copy()

    df_serve = load_servers()
    df_attack = load_attackers()
    df_block = load_blockers()
    df_receive = load_receivers()
    df_dig = load_diggers()

    df = outside_hitters.merge(df_serve[["Name", "Team", "ServePoints", "TotalServeMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_attack[["Name", "Team", "AttackPoints", "TotalAttackMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_block[["Name", "Team", "BlockPoints", "TotalBlockMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_receive[["Name", "Team", "Sf_Receive", "Tot_Receive"]], on=["Name", "Team"], how="left")
    df = df.merge(df_dig[["Name", "Team", "Sf_Dig", "T_Dig"]], on=["Name", "Team"], how="left")

    df["Service Efficiency"] = calculate_efficiency(df["ServePoints"], df["TotalServeMade"])
    df["Attack Success"] = calculate_efficiency(df["AttackPoints"], df["TotalAttackMade"])
    df["Block Efficiency"] = calculate_efficiency(df["BlockPoints"], df["TotalBlockMade"])
    df["Reception Efficiency"] = calculate_efficiency(df["Sf_Receive"], df["Tot_Receive"])
    df["Dig Efficiency"] = calculate_efficiency(df["Sf_Dig"], df["T_Dig"])

    df["Overall Efficiency"] = df[["Service Efficiency", "Attack Success", "Block Efficiency", "Reception Efficiency", "Dig Efficiency"]].mean(axis=1)

    return df[["Name", "Team", "Service Efficiency", "Attack Success", "Block Efficiency", "Reception Efficiency", "Dig Efficiency", "Overall Efficiency"]].dropna(subset=["Overall Efficiency"])


def get_opposite_efficiency(df_players: pd.DataFrame) -> pd.DataFrame:
    """Calculate efficiency metrics for Opposite players.

    Metrics:
    - Service efficiency: aces / total serves
    - Attack success: successful attacks / total attacks
    - Block efficiency: successful blocks / total blocks
    - Dig efficiency: successful digs / total digs
    """
    opposites = df_players[df_players["Position"] == "O"][["Name", "Team"]].copy()

    df_serve = load_servers()
    df_attack = load_attackers()
    df_block = load_blockers()
    df_dig = load_diggers()

    df = opposites.merge(df_serve[["Name", "Team", "ServePoints", "TotalServeMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_attack[["Name", "Team", "AttackPoints", "TotalAttackMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_block[["Name", "Team", "BlockPoints", "TotalBlockMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_dig[["Name", "Team", "Sf_Dig", "T_Dig"]], on=["Name", "Team"], how="left")

    df["Service Efficiency"] = calculate_efficiency(df["ServePoints"], df["TotalServeMade"])
    df["Attack Success"] = calculate_efficiency(df["AttackPoints"], df["TotalAttackMade"])
    df["Block Efficiency"] = calculate_efficiency(df["BlockPoints"], df["TotalBlockMade"])
    df["Dig Efficiency"] = calculate_efficiency(df["Sf_Dig"], df["T_Dig"])

    df["Overall Efficiency"] = df[["Service Efficiency", "Attack Success", "Block Efficiency", "Dig Efficiency"]].mean(axis=1)

    return df[["Name", "Team", "Service Efficiency", "Attack Success", "Block Efficiency", "Dig Efficiency", "Overall Efficiency"]].dropna(subset=["Overall Efficiency"])


def get_middle_blocker_efficiency(df_players: pd.DataFrame) -> pd.DataFrame:
    """Calculate efficiency metrics for Middle Blockers.

    Metrics:
    - Service efficiency: aces / total serves
    - Attack success: successful attacks / total attacks
    - Block efficiency: successful blocks / total blocks
    - Dig efficiency: successful digs / total digs
    """
    middle_blockers = df_players[df_players["Position"] == "MB"][["Name", "Team"]].copy()

    df_serve = load_servers()
    df_attack = load_attackers()
    df_block = load_blockers()
    df_dig = load_diggers()

    df = middle_blockers.merge(df_serve[["Name", "Team", "ServePoints", "TotalServeMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_attack[["Name", "Team", "AttackPoints", "TotalAttackMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_block[["Name", "Team", "BlockPoints", "TotalBlockMade"]], on=["Name", "Team"], how="left")
    df = df.merge(df_dig[["Name", "Team", "Sf_Dig", "T_Dig"]], on=["Name", "Team"], how="left")

    df["Service Efficiency"] = calculate_efficiency(df["ServePoints"], df["TotalServeMade"])
    df["Attack Success"] = calculate_efficiency(df["AttackPoints"], df["TotalAttackMade"])
    df["Block Efficiency"] = calculate_efficiency(df["BlockPoints"], df["TotalBlockMade"])
    df["Dig Efficiency"] = calculate_efficiency(df["Sf_Dig"], df["T_Dig"])

    df["Overall Efficiency"] = df[["Service Efficiency", "Attack Success", "Block Efficiency", "Dig Efficiency"]].mean(axis=1)

    return df[["Name", "Team", "Service Efficiency", "Attack Success", "Block Efficiency", "Dig Efficiency", "Overall Efficiency"]].dropna(subset=["Overall Efficiency"])


def get_libero_efficiency(df_players: pd.DataFrame) -> pd.DataFrame:
    """Calculate efficiency metrics for Liberos.

    Metrics:
    - Reception efficiency: successful receptions / total receptions
    - Dig efficiency: successful digs / total digs
    - Setting efficiency: successful sets / total sets
    """
    liberos = df_players[df_players["Position"] == "L"][["Name", "Team"]].copy()

    df_receive = load_receivers()
    df_dig = load_diggers()
    df_set = load_setters()

    df = liberos.merge(df_receive[["Name", "Team", "Sf_Receive", "Tot_Receive"]], on=["Name", "Team"], how="left")
    df = df.merge(df_dig[["Name", "Team", "Sf_Dig", "T_Dig"]], on=["Name", "Team"], how="left")
    df = df.merge(df_set[["Name", "Team", "Sf_Set", "Tot_Set"]], on=["Name", "Team"], how="left")

    df["Reception Efficiency"] = calculate_efficiency(df["Sf_Receive"], df["Tot_Receive"])
    df["Dig Efficiency"] = calculate_efficiency(df["Sf_Dig"], df["T_Dig"])
    df["Setting Efficiency"] = calculate_efficiency(df["Sf_Set"], df["Tot_Set"])

    df["Overall Efficiency"] = df[["Reception Efficiency", "Dig Efficiency", "Setting Efficiency"]].mean(axis=1)

    return df[["Name", "Team", "Reception Efficiency", "Dig Efficiency", "Setting Efficiency", "Overall Efficiency"]].dropna(subset=["Overall Efficiency"])


def show_ranking_by_position():
    """Display rankings based on player positions"""

    df_players = load_players()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Setter", "Outside Hitter", "Middle Blocker", "Opposite", "Libero"]
    )

    with tab1:
        st.subheader("Top Setters")
        st.text(
            "Efficiency metrics used:\n"
            "• Setting efficiency: successful sets / total sets\n"
            "• Service efficiency: aces / total serves\n"
            "• Dig efficiency: successful digs / total digs"
        )
        df = get_setter_efficiency(df_players)
        display_efficiency_chart(df, "Setter")

    with tab2:
        st.subheader("Top Outside Hitters")
        st.text(
            "Efficiency metrics used:\n"
            "• Service efficiency: aces / total serves\n"
            "• Attack success: successful attacks / total attacks\n"
            "• Block efficiency: successful blocks / total blocks\n"
            "• Reception efficiency: successful receptions / total receptions\n"
            "• Dig efficiency: successful digs / total digs"
        )
        df = get_outside_hitter_efficiency(df_players)
        display_efficiency_chart(df, "Outside Hitter")

    with tab3:
        st.subheader("Top Middle Blockers")
        st.text(
            "Efficiency metrics used:\n"
            "• Service efficiency: aces / total serves\n"
            "• Attack success: successful attacks / total attacks\n"
            "• Block efficiency: successful blocks / total blocks\n"
            "• Dig efficiency: successful digs / total digs"
        )
        df = get_middle_blocker_efficiency(df_players)
        display_efficiency_chart(df, "Middle Blocker")

    with tab4:
        st.subheader("Top Opposites")
        st.text(
            "Efficiency metrics used:\n"
            "• Service efficiency: aces / total serves\n"
            "• Attack success: successful attacks / total attacks\n"
            "• Block efficiency: successful blocks / total blocks\n"
            "• Dig efficiency: successful digs / total digs"
        )
        df = get_opposite_efficiency(df_players)
        display_efficiency_chart(df, "Opposite")

    with tab5:
        st.subheader("Top Liberos")
        st.text(
            "Efficiency metrics used:\n"
            "• Reception efficiency: successful receptions / total receptions\n"
            "• Dig efficiency: successful digs / total digs\n"
            "• Setting efficiency: successful sets / total sets"
        )
        df = get_libero_efficiency(df_players)
        display_efficiency_chart(df, "Libero")

