"""Centralized data loading module with caching for optimized performance."""
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
    "🤝 Setter": "Setters.csv",
}


@st.cache_data
def load_players():
    """Load and cache the Players.csv file."""
    return pd.read_csv(f"{DATASET_PATH}/Players.csv")


@st.cache_data
def load_stat_file(filename):
    """Load and cache a stat CSV file."""
    return pd.read_csv(f"{DATASET_PATH}/{filename}")


def load_attackers():
    """Load the Attackers.csv file."""
    return load_stat_file("Attackers.csv")


def load_blockers():
    """Load the Blockers.csv file."""
    return load_stat_file("Blockers.csv")


def load_diggers():
    """Load the Diggers.csv file."""
    return load_stat_file("Diggers.csv")


def load_receivers():
    """Load the Receivers.csv file."""
    return load_stat_file("Receivers.csv")


def load_scorers():
    """Load the Scorers.csv file."""
    return load_stat_file("Scorers.csv")


def load_servers():
    """Load the Servers.csv file."""
    return load_stat_file("Servers.csv")


def load_setters():
    """Load the Setters.csv file."""
    return load_stat_file("Setters.csv")
