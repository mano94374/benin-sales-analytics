import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    """Charge les données de ventes."""
    df = pd.read_csv("data/ventes.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    return df

#Fonction de Calcul de chiffre d'affaires
def calculate_sales(df):
    """Calcule le chiffre d'affaires de chaque vente."""

    df["Chiffre_Affaires"] = df["Quantite"] * df["Prix"]

    return df

#Fonction produit

def analyze_products(df):
    """Analyse les ventes par produit."""

    ca_par_produit = df.groupby("Produit")["Chiffre_Affaires"].sum()

    quantite_par_produit = df.groupby("Produit")["Quantite"].sum()

    prix_moyen_par_produit = df.groupby("Produit")["Prix"].mean()

    resume_produits = pd.DataFrame({
        "Quantite_totale": quantite_par_produit,
        "CA_total": ca_par_produit,
        "Prix_moyen": prix_moyen_par_produit
    })

    resume_produits = resume_produits.sort_values(
        by="CA_total",
        ascending=False
    )

    return ca_par_produit, resume_produits

#Analyse des ventes par ville

def analyze_cities(df):
    """Analyse les ventes par ville."""

    ca_par_ville = df.groupby("Ville")["Chiffre_Affaires"].sum()

    return ca_par_ville

#Analyse des ventes par mois


def analyze_months(df):
    """Analyse l'évolution mensuelle du chiffre d'affaires."""

    df["Mois"] = df["Date"].dt.to_period("M")

    ca_par_mois = df.groupby("Mois")["Chiffre_Affaires"].sum()

    return ca_par_mois


#Graphique

def create_charts(ca_par_produit, ca_par_ville, ca_par_mois):
    """Crée et sauvegarde les graphiques."""

    # Graphique 1 : CA par produit
    ca_par_produit.plot(kind="bar")

    plt.title("Chiffre d'affaires par produit")
    plt.xlabel("Produit")
    plt.ylabel("Chiffre d'affaires (FCFA)")

    plt.tight_layout()
    plt.savefig("outputs/charts/ca_par_produit.png")
    plt.close()

    # Graphique 2 : CA par ville
    ca_par_ville.plot(kind="bar")

    plt.title("Chiffre d'affaires par ville")
    plt.xlabel("Ville")
    plt.ylabel("Chiffre d'affaires (FCFA)")

    plt.tight_layout()
    plt.savefig("outputs/charts/ca_par_ville.png")
    plt.close()

    # Graphique 3 : évolution mensuelle
    ca_par_mois.plot(kind="line", marker="o")

    plt.title("Évolution du chiffre d'affaires par mois")
    plt.xlabel("Mois")
    plt.ylabel("Chiffre d'affaires (FCFA)")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig("outputs/charts/ca_par_mois.png")
    plt.close()

    print("\nGraphiques créés avec succès !")

    
def create_quantity_vs_revenue_chart(resume_produits):
    """Compare le volume vendu au chiffre d'affaires par produit."""

    plt.scatter(
        resume_produits["Quantite_totale"],
        resume_produits["CA_total"]
    )

    for produit in resume_produits.index:
        plt.annotate(
            produit,
            (
                resume_produits.loc[produit, "Quantite_totale"],
                resume_produits.loc[produit, "CA_total"]
            )
        )

    plt.title("Quantité vendue vs chiffre d'affaires")
    plt.xlabel("Quantité totale vendue")
    plt.ylabel("Chiffre d'affaires (FCFA)")

    plt.tight_layout()

    plt.savefig(
        "outputs/charts/quantite_vs_ca.png"
    )

    plt.close()

    print("Graphique quantité vs CA créé !")

def export_to_excel(
    df,
    resume_produits,
    ca_par_ville,
    ca_par_mois
):
    """Exporte les résultats dans un fichier Excel."""

    ca_total = df["Chiffre_Affaires"].sum()
    quantite_total = df["Quantite"].sum()

    produit_top = resume_produits.index[0]
    ca_produit_top = resume_produits.iloc[0]["CA_total"]

    ville_top = ca_par_ville.idxmax()
    ca_ville_top = ca_par_ville.max()

    mois_top = ca_par_mois.idxmax()
    ca_mois_top = ca_par_mois.max()

    panier_moyen = df["Chiffre_Affaires"].mean()

    # Créer le tableau résumé
    resume = pd.DataFrame({
        "Indicateur": [
            "Chiffre d'affaires total",
            "Quantité totale vendue",
            "Produit n°1",
            "CA du produit n°1",
            "Ville n°1",
            "CA de la ville n°1",
            "Meilleur mois",
            "CA du meilleur mois",
            "Panier moyen"
        ],
        "Valeur": [
            ca_total,
            quantite_total,
            produit_top,
            ca_produit_top,
            ville_top,
            ca_ville_top,
            str(mois_top),
            ca_mois_top,
            panier_moyen
        ]
    })

    # Export Excel
    with pd.ExcelWriter(
        "outputs/Benin_Sales_Analytics.xlsx"
    ) as writer:

        resume.to_excel(
            writer,
            sheet_name="Résumé",
            index=False
        )

        df.to_excel(
            writer,
            sheet_name="Ventes brutes",
            index=False
        )

        resume_produits.to_excel(
            writer,
            sheet_name="Produits"
        )

        ca_par_ville.to_excel(
            writer,
            sheet_name="Villes"
        )

        ca_par_mois.to_excel(
            writer,
            sheet_name="Mois"
        )

    print("\nRapport Excel créé avec succès !")


def detect_outliers(df, column):
    """Détecte les valeurs aberrantes avec la méthode IQR."""

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)

    iqr = q3 - q1

    borne_basse = q1 - 1.5 * iqr
    borne_haute = q3 + 1.5 * iqr

    outliers = df[
        (df[column] < borne_basse) |
        (df[column] > borne_haute)
    ]

    print(f"\n=== OUTLIERS : {column} ===")
    print("Q1 :", q1)
    print("Q3 :", q3)
    print("IQR :", iqr)
    print("Borne basse :", borne_basse)
    print("Borne haute :", borne_haute)

    print("\nValeurs potentiellement aberrantes :")
    print(outliers)

    return outliers

def check_dates(df):
    """Vérifie la cohérence des dates."""

    date_min = df["Date"].min()
    date_max = df["Date"].max()

    print("\n=== CONTRÔLE DES DATES ===")
    print("Date la plus ancienne :", date_min)
    print("Date la plus récente :", date_max)

    print("\nNombre de ventes par date :")
    print(df["Date"].value_counts().sort_index())

def check_product_categories(df):
    """Vérifie la cohérence entre les produits et leurs catégories."""

    categories_attendues = {
        "Ordinateur": "Informatique",
        "Souris": "Accessoire",
        "Clavier": "Accessoire",
        "Telephone": "Electronique"
    }

    df["Categorie_attendue"] = df["Produit"].map(categories_attendues)

    erreurs = df[
        df["Categorie"] != df["Categorie_attendue"]
    ]

    print("\n=== COHÉRENCE PRODUIT / CATÉGORIE ===")

    if erreurs.empty:
        print("Aucune incohérence détectée. ✅")
    else:
        print("Incohérences détectées :")
        print(
            erreurs[
                ["Produit", "Categorie", "Categorie_attendue"]
            ]
        )

    return erreurs

def check_sales_calculation(df):
    """Vérifie que le chiffre d'affaires est correctement calculé."""

    ca_calcule = df["Quantite"] * df["Prix"]

    erreurs = df[
        df["Chiffre_Affaires"] != ca_calcule
    ]

    print("\n=== CONTRÔLE DU CHIFFRE D'AFFAIRES ===")

    if erreurs.empty:
        print("Tous les chiffres d'affaires sont corrects. ✅")
    else:
        print("Erreurs détectées :")
        print(
            erreurs[
                ["Produit", "Quantite", "Prix", "Chiffre_Affaires"]
            ]
        )

    return erreurs

def analyze_product_performance(df):
    """Analyse la contribution de chaque produit."""

    ca_par_produit = (
        df.groupby("Produit")["Chiffre_Affaires"]
        .sum()
        .sort_values(ascending=False)
    )

    ca_total = df["Chiffre_Affaires"].sum()

    part_ca = (ca_par_produit / ca_total) * 100

    performance = pd.DataFrame({
        "CA_total": ca_par_produit,
        "Part_CA_%": part_ca
    })

    print("\n=== PERFORMANCE DES PRODUITS ===")
    print(performance)

    return performance

def analyze_city_performance(df):
    """Analyse la contribution de chaque ville."""

    ca_par_ville = (
        df.groupby("Ville")["Chiffre_Affaires"]
        .sum()
        .sort_values(ascending=False)
    )

    ca_total = df["Chiffre_Affaires"].sum()

    part_ca = (ca_par_ville / ca_total) * 100

    performance = pd.DataFrame({
        "CA_total": ca_par_ville,
        "Part_CA_%": part_ca
    })

    print("\n=== PERFORMANCE DES VILLES ===")
    print(performance)

    return performance

def analyze_city_products(df):
    """Analyse les ventes de chaque produit par ville."""

    ca_ville_produit = pd.pivot_table(
        df,
        values="Chiffre_Affaires",
        index="Ville",
        columns="Produit",
        aggfunc="sum",
        fill_value=0
    )

    print("\n=== CA PAR VILLE ET PAR PRODUIT ===")
    print(ca_ville_produit)

    return ca_ville_produit

def analyze_monthly_growth(ca_par_mois):
    """Analyse la croissance mensuelle du chiffre d'affaires."""

    croissance = ca_par_mois.pct_change() * 100

    resultat = pd.DataFrame({
        "CA": ca_par_mois,
        "Croissance_%": croissance
    })

    print("\n=== CROISSANCE MENSUELLE ===")
    print(resultat)

    return resultat

def analyze_monthly_products(df):
    """Analyse le chiffre d'affaires par mois et par produit."""

    ca_mois_produit = pd.pivot_table(
        df,
        values="Chiffre_Affaires",
        index="Mois",
        columns="Produit",
        aggfunc="sum",
        fill_value=0
    )

    print("\n=== CA PAR MOIS ET PAR PRODUIT ===")
    print(ca_mois_produit)

    return ca_mois_produit

def analyze_monthly_quantities(df):
    """Analyse les quantités vendues par mois et par produit."""

    quantite_mois_produit = pd.pivot_table(
        df,
        values="Quantite",
        index="Mois",
        columns="Produit",
        aggfunc="sum",
        fill_value=0
    )

    print("\n=== QUANTITÉS PAR MOIS ET PAR PRODUIT ===")
    print(quantite_mois_produit)

    return quantite_mois_produit

def analyze_monthly_mix(df):
    """Analyse la répartition du CA par produit et par mois."""

    mix = pd.pivot_table(
        df,
        values="Chiffre_Affaires",
        index="Mois",
        columns="Produit",
        aggfunc="sum",
        fill_value=0
    )

    # Calcul du CA total de chaque mois
    mix["CA_Total"] = mix.sum(axis=1)

    # Calcul de la part de chaque produit dans le CA mensuel
    for produit in ["Clavier", "Ordinateur", "Souris", "Telephone"]:
        mix[f"Part_{produit}_%"] = (
            mix[produit] / mix["CA_Total"] * 100
        )

    print("\n=== MIX PRODUIT PAR MOIS ===")
    print(mix)

    return mix

def analyze_city_product_mix(df):
    """Analyse la répartition du CA par produit dans chaque ville."""

    ca_ville_produit = pd.pivot_table(
        df,
        values="Chiffre_Affaires",
        index="Ville",
        columns="Produit",
        aggfunc="sum",
        fill_value=0
    )

    ca_ville_produit["CA_Total"] = ca_ville_produit.sum(axis=1)

    produits = ["Clavier", "Ordinateur", "Souris", "Telephone"]

    for produit in produits:
        ca_ville_produit[f"Part_{produit}_%"] = (
            ca_ville_produit[produit]
            / ca_ville_produit["CA_Total"]
            * 100
        )

    print("\n=== MIX PRODUIT PAR VILLE ===")
    print(ca_ville_produit)

    return ca_ville_produit

def calculate_kpis(df, resume_produits, ca_par_ville, ca_par_mois):
    """Calcule les principaux KPI commerciaux."""

    ca_total = df["Chiffre_Affaires"].sum()
    quantite_total = df["Quantite"].sum()
    panier_moyen = df["Chiffre_Affaires"].mean()

    produit_top = resume_produits.index[0]
    ca_produit_top = resume_produits.iloc[0]["CA_total"]

    ville_top = ca_par_ville.idxmax()
    ca_ville_top = ca_par_ville.max()

    mois_top = ca_par_mois.idxmax()
    ca_mois_top = ca_par_mois.max()

    croissance_moyenne = ca_par_mois.pct_change().mean() * 100

    kpis = {
        "CA_total": ca_total,
        "Quantite_totale": quantite_total,
        "Panier_moyen": panier_moyen,
        "Produit_top": produit_top,
        "CA_produit_top": ca_produit_top,
        "Ville_top": ville_top,
        "CA_ville_top": ca_ville_top,
        "Meilleur_mois": str(mois_top),
        "CA_meilleur_mois": ca_mois_top,
        "Croissance_moyenne": croissance_moyenne
    }

    print("\n=== KPI COMMERCIAUX ===")

    for nom, valeur in kpis.items():
        print(f"{nom} : {valeur}")

    return kpis

def create_dashboard_charts(
    ca_par_produit,
    ca_par_ville,
    ca_par_mois,
    resume_produits
):
    """Crée les graphiques principaux du dashboard."""

    # 1. CA par produit
    ca_par_produit.sort_values(ascending=False).plot(
        kind="bar"
    )

    plt.title("Chiffre d'affaires par produit")
    plt.xlabel("Produit")
    plt.ylabel("CA (FCFA)")
    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.savefig("outputs/charts/ca_par_produit.png")
    plt.close()

    # 2. CA par ville
    ca_par_ville.sort_values(ascending=False).plot(
        kind="bar"
    )

    plt.title("Chiffre d'affaires par ville")
    plt.xlabel("Ville")
    plt.ylabel("CA (FCFA)")
    plt.xticks(rotation=0)

    plt.tight_layout()
    plt.savefig("outputs/charts/ca_par_ville.png")
    plt.close()

    # 3. Évolution mensuelle
    ca_par_mois.plot(
        kind="line",
        marker="o"
    )

    plt.title("Évolution mensuelle du chiffre d'affaires")
    plt.xlabel("Mois")
    plt.ylabel("CA (FCFA)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig("outputs/charts/evolution_ca_mensuel.png")
    plt.close()

    # 4. Quantité vs CA
    plt.scatter(
        resume_produits["Quantite_totale"],
        resume_produits["CA_total"]
    )

    for produit in resume_produits.index:
        plt.annotate(
            produit,
            (
                resume_produits.loc[produit, "Quantite_totale"],
                resume_produits.loc[produit, "CA_total"]
            )
        )

    plt.title("Volume des ventes vs chiffre d'affaires")
    plt.xlabel("Quantité vendue")
    plt.ylabel("CA (FCFA)")

    plt.tight_layout()
    plt.savefig("outputs/charts/volume_vs_ca.png")
    plt.close()

    print("\n=== DASHBOARD ===")
    print("Graphiques du dashboard créés avec succès !")

#Fonction principale

def main():

    # Charger les données
    df = load_data()

    print("\n=== INFORMATIONS SUR LES DONNÉES ===")
    print(df.info())
    
    print("\n=== VALEURS MANQUANTES ===")
    print(df.isnull().sum())
    
    print("\n=== DOUBLONS ===")
    print(df.duplicated().sum())

    print("\n=== PRODUITS UNIQUES ===")
    print(df["Produit"].unique())

    print("\n=== CATÉGORIES UNIQUES ===")
    print(df["Categorie"].unique())

    print("\n=== VILLES UNIQUES ===")
    print(df["Ville"].unique())

    print("\n=== VALEURS MINIMALES ===")
    print("Quantité minimale :", df["Quantite"].min())
    print("Prix minimal :", df["Prix"].min())

    print("\n=== VALEURS MAXIMALES ===")
    print("Quantité maximale :", df["Quantite"].max())
    print("Prix maximal :", df["Prix"].max())

    print("\n=== VALEURS ANORMALES ===")

    print("Quantités <= 0 :")
    print(df[df["Quantite"] <= 0])

    print("\nPrix <= 0 :")
    print(df[df["Prix"] <= 0])
    
    # Calculer le chiffre d'affaires
    df = calculate_sales(df)

    check_dates(df)

    detect_outliers(df, "Chiffre_Affaires")

    check_product_categories(df)

    check_sales_calculation(df)

    # Analyses
    ca_par_produit, resume_produits = analyze_products(df)
    ca_par_ville = analyze_cities(df)
    ca_par_mois = analyze_months(df)

    create_dashboard_charts(
    ca_par_produit,
    ca_par_ville,
    ca_par_mois,
    resume_produits
)

    create_quantity_vs_revenue_chart(resume_produits)

    kpis = calculate_kpis(
    df,
    resume_produits,
    ca_par_ville,
    ca_par_mois
)

    product_performance = analyze_product_performance(df)

    city_performance = analyze_city_performance(df)

    ca_ville_produit = analyze_city_products(df)

    city_product_mix = analyze_city_product_mix(df)

    monthly_growth = analyze_monthly_growth(ca_par_mois)

    ca_mois_produit = analyze_monthly_products(df)

    quantite_mois_produit = analyze_monthly_quantities(df)

    monthly_mix = analyze_monthly_mix(df)

   

    create_charts(
    ca_par_produit,
    ca_par_ville,
    ca_par_mois
)
    export_to_excel(
        df,
        resume_produits,
        ca_par_ville,
        ca_par_mois
)

 
    # Affichage
    print("\n=== BENIN SALES ANALYTICS ===")

    print("\nChiffre d'affaires total :",
          df["Chiffre_Affaires"].sum(), "FCFA")

    print("\nQuantité totale vendue :",
          df["Quantite"].sum())

    print("\nClassement des produits :")
    print(resume_produits)

    print("\nChiffre d'affaires par ville :")
    print(ca_par_ville)

    print("\nChiffre d'affaires par mois :")
    print(ca_par_mois)


if __name__ == "__main__":
    main()