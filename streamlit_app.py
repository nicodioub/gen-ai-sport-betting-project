import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
from PIL import Image
from io import BytesIO
import streamlit as st
#from IPython.display import Markdown, display


#ajouts images et liens" 

#mettre le cache 

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["SPORT_API"] = st.secrets["SPORT_API"]

st.title("⚽ GenAI Football Match")
st.write(
    " **Welcome in your match predictions app !**"
    " **This app is powered by Google Gemini and SportAPI7.**"
    
)

@st.cache_resource
def get_model():
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash")

model = get_model()


user_input = st.text_input("""Que voulez-vous que je prédise ? 💎                     
                           Veuillez entrer le nom complet des équipes comme 'Real Madrid vs Barcelona'.
                           """)
                           
if not user_input:
    st.warning("Veuillez entrer les noms de deux équipes.")
    st.stop()  # Stop execution immediately




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

#st.write(extraire_equipes(user_input))

team_name1 = extraire_equipes(user_input)[0] # Récupération du nom de la première équipe.
team_name2 = extraire_equipes(user_input)[1] # Récupération du nom de la première équipe.

if not team_name1 or not team_name2:
    st.warning("Veuillez entrer une requête valide contenant deux équipes.")
    st.stop()

@st.cache_data
def get_team_data(team_name, api_key="dc45380d2dmsh3fd40e12d2127bdp1b2b78jsnf2c997253cce"):
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

# Récupération des données de l'équipe 1 et de l'équipe 2
team1_data = get_team_data(team_name1)
team2_data = get_team_data(team_name2)

@st.cache_data
def get_id_team(team_data):
    """
    Récupère l'ID d'une équipe à partir de ses données.

    Args:
        team_data (dict): Dictionnaire contenant les données de l'équipe.

    Returns:
        int: ID de l'équipe.
    """
    if team_data and "id" in team_data:
        return team_data["id"]
    else:
        return None


team1_id = get_id_team(team1_data)

#st.write(" team_id :" ,team1_id)
team2_id = get_id_team(team2_data)


# st.write(get_id_team(team1_data))
# st.write(get_id_team(team2_data))


@st.cache_data
def get_tournament_id(team_data):
    """
    Récupère l'ID du tournoi à partir des données de l'équipe.

    Args:
        team_data (dict): Dictionnaire contenant les données de l'équipe.

    Returns:
        int: ID du tournoi.
    """


    if team_data and "primaryUniqueTournament" in team_data and "id" in team_data["primaryUniqueTournament"]:
        return team_data["primaryUniqueTournament"]["id"]
    else:
        return None
    
# Récupération de l'ID du tournoi
tournament_id1 = get_tournament_id(team1_data)
#st.write("tounrament_id : ", tournament_id1)
tournament_id2 = get_tournament_id(team2_data)


@st.cache_data
def get_season_id(team_data):
    """
    Récupère l'ID de la saison à partir des données de l'équipe.

    Args:
        team_data (dict): Dictionnaire contenant les données de l'équipe.

    Returns:
        int: ID de la saison.
    """
    season_id = ""

    laliga_season_id = 61643
    premierleague_season_id = 61627
    ligue_1_season_id = 61736
    ligue_portugal_season_id = 63670
    bundesliga_season_id = 63516
    CAN_season_id = 71636



    if team_data["primaryUniqueTournament"]['slug'] == "laliga":
        season_id = laliga_season_id
    elif team_data["primaryUniqueTournament"]['slug'] == "premier-league":
        season_id = premierleague_season_id
    elif team_data["primaryUniqueTournament"]['slug'] == "ligue-1":
        season_id = ligue_1_season_id
    elif team_data["primaryUniqueTournament"]['slug'] == "bundesliga":
        season_id = bundesliga_season_id
    elif team_data["primaryUniqueTournament"]['slug'] == "ligue-portugal":
        season_id = ligue_portugal_season_id
    elif team_data["primaryUniqueTournament"]['slug'] == "africa-cup-of-nations":
        season_id = CAN_season_id

    return season_id

# Récupération de l'ID de la saison
season_id1 = get_season_id(team1_data)
#st.write("season_id", season_id1)
season_id2 = get_season_id(team2_data)


@st.cache_data
def get_team_image(team_id):
    """
    Fetches the image of a team using its ID.

    Args:
        team_id (int): The ID of the team.

    Returns:
        bytes: Image binary data if successful, otherwise None.
    """
    url = f"https://sportapi7.p.rapidapi.com/api/v1/team/{team_id}/image"

    headers = {
        "x-rapidapi-key": "dc45380d2dmsh3fd40e12d2127bdp1b2b78jsnf2c997253cce",  # Replace with your real API key
        "x-rapidapi-host": "sportapi7.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.content  # Returns raw binary image data (like .blob() in JS)
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None

    except requests.RequestException as e:
        print(f"Connection Error: {e}")
        return None

# Example usage:
team1_image_data = get_team_image(team1_id)  # Replace with a real team ID
team2_image_data = get_team_image(team2_id)  # Replace with a real team ID

# Display images side by side in Streamlit
col1, col2 = st.columns(2)

with col1:
    if team1_image_data:
        image = Image.open(BytesIO(team1_image_data))
        st.image(image, caption=team_name1)
    else:
        st.warning("⚠️ Image not available for Team 1")

with col2:
    if team2_image_data:
        image = Image.open(BytesIO(team2_image_data))
        st.image(image, caption=team_name2)
    else:
        st.warning("⚠️ Image not available for Team 2")


# Récupération des données de l'équipe 1

@st.cache_data
def get_team_stats(team_id, tournament_id, season_id, api_key="dc45380d2dmsh3fd40e12d2127bdp1b2b78jsnf2c997253cce"):
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

    return stats


team1_stats = get_team_stats(team1_id, tournament_id1, season_id1)


team2_stats = get_team_stats(team2_id, tournament_id2, season_id2)

#team1_stats
#st.write(team2_stats)




@st.cache_data
def calculer_statistiques_equipe(stats):
    """
    Calcule les statistiques d'une équipe de football à partir de données brutes.

    Args:
        stats (dict): Un dictionnaire contenant les statistiques brutes de l'équipe
                      (e.g., matches, goalsScored, goalsConceded, etc.).

    Returns:
        dict: Un dictionnaire contenant les statistiques calculées, telles que :
              'buts_par_match', 'precision_tir', 'possession', etc.
    """
    # Calcul des variables
    matches = stats['matches']
    goals = stats['goalsScored']
    goals_conceded = stats['goalsConceded']
    clean_sheets = stats['cleanSheets']
    big_chances_created = stats['bigChancesCreated']
    big_chances_missed = stats['bigChancesMissed']
    shots = stats['shots']
    shots_on_target = stats['shotsOnTarget']
    big_chances = stats['bigChances']
    shots_against = stats['shotsAgainst']
    shots_on_target_against = stats['shotsOnTargetAgainst']
    big_chances_against = stats['bigChancesAgainst']
    average_possession = stats['averageBallPossession']
    accurate_passes_percentage = stats['accuratePassesPercentage']

    # Attaque
    goals_per_match = goals / matches
    shots_on_target_per_match = shots_on_target / matches
    shot_accuracy = (shots_on_target / shots) * 100
    big_chance_conversion = ((big_chances - big_chances_missed) / big_chances) * 100

    # Défense
    goals_conceded_per_match = goals_conceded / matches
    clean_sheets_percentage = (clean_sheets / matches) * 100
    shots_conceded_per_match = shots_against / matches
    shot_conceded_accuracy = (shots_on_target_against / shots_against) * 100

    # Maîtrise du jeu
    possession = average_possession
    pass_accuracy = accurate_passes_percentage

    # Stockage et retour des statistiques calculées
    statistiques_calculees = {
        "buts_par_match": goals_per_match,
        "tirs_cadres_par_match": shots_on_target_per_match,
        "precision_tir": shot_accuracy,
        "conversion_grosses_occasions": big_chance_conversion,
        "buts_encaisses_par_match": goals_conceded_per_match,
        "pourcentage_clean_sheets": clean_sheets_percentage,
        "tirs_concedes_par_match": shots_conceded_per_match,
        "precision_tirs_concedes": shot_conceded_accuracy,
        "possession": possession,
        "precision_passes": pass_accuracy
    }

    return statistiques_calculees

team1_analyse = calculer_statistiques_equipe(team1_stats)
team2_analyse = calculer_statistiques_equipe(team2_stats)

# Exemple d'utilisation :
# stats_equipe1 = calculer_statistiques_equipe(stats)
# print(stats_equipe1)






def calculer_statistiques_equipes(stats1, stats2):
    """
    Calcule les statistiques de deux équipes de football à partir de données brutes.

    Args:
        stats1 (dict): Un dictionnaire contenant les statistiques brutes de l'équipe 1.
        stats2 (dict): Un dictionnaire contenant les statistiques brutes de l'équipe 2.

    Returns:
        tuple: Un tuple contenant deux dictionnaires, un pour chaque équipe,
               contenant les statistiques calculées.
    """

    # Calcul des statistiques pour l'équipe 1
    statistiques_equipe1 = calculer_statistiques_equipe_individuelle(stats1)

    # Calcul des statistiques pour l'équipe 2
    statistiques_equipe2 = calculer_statistiques_equipe_individuelle(stats2)

    return statistiques_equipe1, statistiques_equipe2


def calculer_statistiques_equipe_individuelle(stats):
    """
    Calcule les statistiques d'une seule équipe de football à partir de données brutes.

    Args:
        stats (dict): Un dictionnaire contenant les statistiques brutes de l'équipe.

    Returns:
        dict: Un dictionnaire contenant les statistiques calculées pour l'équipe.
    """
    # (Le code de calcul des statistiques reste le même que précédemment)
    # ... (Copiez le code de la fonction calculer_statistiques_equipe originale ici) ...
    return statistiques_calculees

def predict_match_outcome(list_stats, list_stats2, query_result1, query_result2):
    """
    Predicts the outcome of a match between two teams based on their statistics.

    Args:
        list_stats (dict): Statistics for the first team.
        list_stats2 (dict): Statistics for the second team.
        query_result1 (str): Name of the first team.
        query_result2 (str): Name of the second team.
        model: The language model to use for prediction.

    Returns:
        str: The predicted outcome of the match.
    """
    stats1_str = "\n".join([f"{key}: {value:.2f}" for key, value in team1_analyse.items()])
    stats2_str = "\n".join([f"{key}: {value:.2f}" for key, value in team2_analyse.items()])

    formatted_input = f"""Voici les statistiques des deux équipes :

    {query_result1} :
    {stats1_str}

    {query_result2} :
    {stats2_str}

    """

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", """Prends ces deux stats et compare les pour dire quelle équipe va gagner, ou si c'est un match nulle. Donne une affirmation du style(Real madrid va gagner)  sans aucune hésitation en citant le nom
            de l'équipe donne aussi des explications selon les différentes stats et avec un facteur pourcentage de victoire total  """),
            ("user", "{input}")
        ]
    )

    response_final = model.invoke(prompt_template.invoke({"input": formatted_input}))
    query_result = response_final.content
    return query_result

st.write(predict_match_outcome(team1_analyse, team2_analyse, team_name1, team_name2))



