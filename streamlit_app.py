import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import requests

#mettre le cache 

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

st.title("⚽ GenAI Predictions ")
st.write(
    " **Welcome in your match predictions app !**"
)

@st.cache_resource
def get_model():
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash")

model = get_model()



user_input = st.text_input("What do you want me to predict ? 0_O ")

# @st.cache_data
# def generate_response(user_input):
#     #st.session_state['count'] += 1
#     prompt = prompt_template.invoke({"input": user_input})
#     response = model.invoke(prompt)
#     query_result = response.content
#     teams = query_result.split(",") if "," in query_result else [query_result]
#     query_result1, query_result2 = teams[0], teams[1]


#     return response.content, query_result1, query_result2

# if user_input:
#     st.write(generate_response(user_input))


@st.cache_data
def extraire_equipes(user_input):
  """
  Extrait les noms de deux équipes à partir de la requête d'un utilisateur
  en utilisant un modèle de langage.
  Args:
      user_input (str): La requête de l'utilisateur concernant le résultat d'un match.
      model: L'objet du modèle de langage à utiliser pour l'inférence.
  Returns:
      tuple: Un tuple contenant les noms des deux équipes
             (query_result1, query_result2).
             Si une seule équipe est trouvée, le deuxième élément sera None.
  """
  # Création du template de prompt pour le modèle de langage.
  prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "do not answer the query but output the  teams from the query like 'Barcelona, Real Madrid' "),
        ("user", "{input}")
    ]
)

  # Appel du modèle de langage avec le prompt et la requête de l'utilisateur.
  response = model.invoke(prompt_template.invoke({"input": user_input}))
  query_result = response.content # Extraction du contenu de la réponse.

  # Séparation des noms d'équipes en utilisant la virgule comme délimiteur.
  teams = query_result.split(",") if "," in query_result else [query_result]

  # Attribution des noms d'équipes aux variables query_result1 et query_result2.
  # Si une seule équipe est trouvée, query_result2 sera None.
  query_result1 = teams[0].strip() if teams else None  # Suppression des espaces inutiles.
  query_result2 = teams[1].strip() if len(teams) > 1 else None  # Suppression des espaces inutiles.

  return query_result1, query_result2 # Retourne les noms des équipes.

st.write(extraire_equipes(user_input))

team_name1 = extraire_equipes(user_input)[0] # Récupération du nom de la première équipe.
team_name2 = extraire_equipes(user_input)[1] # Récupération du nom de la première équipe.

# st.write(team_name1)
# st.write(team_name2)

@st.cache_data
def get_team_data(team_name, api_key="081a622178msh47c970908ee3fe1p175ee7jsndc3e70382bf5"):
    """
    Récupère les informations détaillées d'une équipe sportive via SportAPI7.

    Args:
        team_name (str): Nom de l'équipe.
        api_key (str, optional): Votre clé API SportAPI7.
                                  Par défaut : api_key.

    Returns:
        dict: Dictionnaire contenant les données de l'équipe si trouvée,
              sinon un dictionnaire vide.
    """
    url = f"https://sportapi7.p.rapidapi.com/api/v1/search/teams/{team_name}/more"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "sportapi7.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    team_data = {}
    if "teams" in data and isinstance(data["teams"], list) and len(data["teams"]) > 0:
        team_data = data["teams"][0]

    return team_data

# st.write(get_team_data(team_name1))
# st.write(get_team_data(team_name2))

team_id = 2829

tournament_id = 8

season_id = 61643

# Récupération des données de l'équipe 1

def get_team_stats(team_id, tournament_id, season_id, api_key="081a622178msh47c970908ee3fe1p175ee7jsndc3e70382bf5"):
    """
    Récupère les statistiques d'une équipe pour un tournoi et une saison donnés via SportAPI7.

    Args:
        team_id (int): ID de l'équipe.
        tournament_id (int): ID du tournoi.
        season_id (int): ID de la saison.
        api_key (str, optional): Votre clé API SportAPI7.
                                  Par défaut : api_key.

    Returns:
        dict: Dictionnaire contenant les statistiques de l'équipe.
    """
    url = f"https://sportapi7.p.rapidapi.com/api/v1/team/{team_id}/unique-tournament/{tournament_id}/season/{season_id}/statistics/overall"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "sportapi7.p.rapidapi.com"}

    response = requests.get(url, headers=headers)

    stats = {}

    for key, value in response.json()['statistics'].items():
        stats[key] = value

    stats_data = response.json()

    return stats_data

st.write(get_team_stats(team_id, tournament_id, season_id))

