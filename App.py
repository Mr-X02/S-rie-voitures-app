import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gestion des Chauffeurs", page_icon="🚗")

st.title("🚗 Recherche Chauffeur & Voiture")

DB_FILE = "data.csv"


def load_data():
    try:
        return pd.read_csv(DB_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Nom", "Serie"])
        df.to_csv(DB_FILE, index=False)
        return df


def save_data(df):
    df.to_csv(DB_FILE, index=False)


df = load_data()

st.subheader("🔍 Rechercher un chauffeur")
search_term = st.text_input("Entrez le nom du chauffeur :")

if search_term:
    results = df[df["Nom"].str.contains(search_term, case=False, na=False)]
    if not results.empty:
        st.success(f"{len(results)} résultat(s) trouvé(s) :")
        for index, row in results.iterrows():
            st.info(
                f"👤 **Chauffeur :** {row['Nom']}\n\n🚘 **Série Voiture :** {row['Serie']}"
            )
    else:
        st.warning("Aucun chauffeur trouvé avec ce nom.")

st.divider()

st.subheader("➕ Ajouter un nouveau chauffeur")
with st.form("add_form", clear_on_submit=True):
    new_nom = st.text_input("Nom du chauffeur :")
    new_serie = st.text_input("Série / Matricule de la voiture :")
    submitted = st.form_submit_button("Enregistrer")

    if submitted:
        if new_nom and new_serie:
            new_data = pd.DataFrame(
                [{"Nom": new_nom.strip(), "Serie": new_serie.strip()}]
            )
            df = pd.concat([df, new_data], ignore_index=False)
            save_data(df)
            st.success(
                f"✅ {new_nom} avec la série {new_serie} a été ajouté avec succès !"
            )
            st.rerun()
        else:
            st.error("Veuillez remplir tous les champs.")

with st.expander("📋 Voir toute la liste"):
    st.dataframe(df, use_container_width=True)
