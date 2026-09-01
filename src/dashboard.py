import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------
# CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Benin Sales Analytics",
    page_icon="🇧🇯",
    layout="wide"
)


# -----------------------------
# CHARGEMENT DES DONNÉES
# -----------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/ventes.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    df["Chiffre_Affaires"] = (
        df["Quantite"] * df["Prix"]
    )

    return df


df = load_data()

# -----------------------------
# FILTRES
# -----------------------------

st.sidebar.header("🎛️ Filtres")

villes = ["Toutes"] + sorted(df["Ville"].unique().tolist())

produits = ["Tous"] + sorted(df["Produit"].unique().tolist())

ville_selectionnee = st.sidebar.selectbox(
    "Choisir une ville",
    villes
)

produit_selectionne = st.sidebar.selectbox(
    "Choisir un produit",
    produits
)


# Filtrer les données

df_filtre = df.copy()

if ville_selectionnee != "Toutes":
    df_filtre = df_filtre[
        df_filtre["Ville"] == ville_selectionnee
    ]

if produit_selectionne != "Tous":
    df_filtre = df_filtre[
        df_filtre["Produit"] == produit_selectionne
    ]


# -----------------------------
# TITRE
# -----------------------------

st.title("🇧🇯 Benin Sales Analytics")

st.markdown(
    "### Dashboard d'analyse des ventes"
)


# -----------------------------
# KPI
# -----------------------------

ca_total = df_filtre["Chiffre_Affaires"].sum()
quantite_total = df_filtre["Quantite"].sum()
panier_moyen = df_filtre["Chiffre_Affaires"].mean()

produit_top = (
    df_filtre.groupby("Produit")["Chiffre_Affaires"]
    .sum()
    .idxmax()
)

ville_top = (
    df_filtre.groupby("Ville")["Chiffre_Affaires"]
    .sum()
    .idxmax()
)


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "CA total",
        f"{ca_total:,.0f} FCFA"
    )


with col2:
    st.metric(
        "Unités vendues",
        f"{quantite_total}"
    )


with col3:
    st.metric(
        "CA moyen / vente",
        f"{panier_moyen:,.0f} FCFA"
    )


with col4:
    st.metric(
        "Produit n°1",
        produit_top
    )


# -----------------------------
# CA PAR PRODUIT
# -----------------------------

st.subheader("📦 Chiffre d'affaires par produit")

ca_produit = (
    df_filtre.groupby("Produit")["Chiffre_Affaires"]
    .sum()
    .reset_index()
)

fig_produit = px.bar(
    ca_produit,
    x="Produit",
    y="Chiffre_Affaires",
    title="CA par produit"
)

st.plotly_chart(
    fig_produit,
    use_container_width=True
)


# -----------------------------
# CA PAR VILLE
# -----------------------------

st.subheader("🏙️ Chiffre d'affaires par ville")

ca_ville = (
    df_filtre.groupby("Ville")["Chiffre_Affaires"]
    .sum()
    .reset_index()
)

fig_ville = px.bar(
    ca_ville,
    x="Ville",
    y="Chiffre_Affaires",
    title="CA par ville"
)

st.plotly_chart(
    fig_ville,
    use_container_width=True
)