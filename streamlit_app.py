import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

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

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "do not answer the query but output the  teams from the query like 'Barcelona, Real Madrid' "),
        ("user", "{input}")
    ]
)

user_input = st.text_input("What do you want me to predict ? 0_0 ")

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
          ("system", "Ne réponds pas à la question, mais extrais les équipes de la requête comme 'Barcelona, Real Madrid' "),
          ("user", "{input}") # La requête de l'utilisateur sera insérée ici.
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




def get_team_data(team_name, api_key="081a622178msh47c970908ee3fe1p175ee7jsndc3e70382bf5"):
    """
    Récupère les informations détaillées d'une équipe sportive via SportAPI7.

    Args:
        team_name (str): Nom de l'équipe.
        api_key (str, optional): Votre clé API SportAPI7.
                                  Par défaut : "a77e4d69aemshd774591d8fbc877p15616cjsn65f81709282b".

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


# query_result = response.content

# # Je stocke les valeurs des deux équipes pour une utilisation future

# teams = query_result.split(",") if "," in query_result else [query_result]

# # Stocker dans des variables distinctes
# query_result1, query_result2 = teams[0], teams[1]



#####

# prompt = st.text_input("Enter your prompt:")

# @st.cache_data
# def generate_response(prompt):
#     return "Hello, " + prompt

# if prompt:
#     st.write(generate_response(prompt))


# prompt = st.chat_input("Say something")
# if prompt : 
#     st.write(f"User has sent the following prompt: {prompt}")


# #st.chat_message


# import numpy as np
# message = st.chat_message("assistant")
# message.write("Hello human")
# message.bar_chart(np.random.randn(30, 3))



# import streamlit as st
# import os 

# os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# from langchain_google_genai import ChatGoogleGenerativeAI

# model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# from langchain_core.prompts import ChatPromptTemplate

# prompt = st.text_input("What match do you want our AI to predict ex : 'manchester city vs real madrid '", key="match")


# prompt_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", "do not answer the query but output the  teams from the query like 'Barcelona, Real Madrid' "),
#         ("user", "{prompt}")
#     ]
# )

# # user_input = 'What is the result between liverpool  and barcelona  '  # @param {type: "string"}



# response = model.invoke(prompt_template.invoke({"input": prompt}))

# query_result = response.content

# st.session_state.match

# # # Je stocke les valeurs des deux équipes pour une utilisation future

# # teams = query_result.split(",") if "," in query_result else [query_result]

# # # Stocker dans des variables distinctes
# # query_result1, query_result2 = teams[0], teams[1]

# # print(query_result1)
# # print(query_result2)




# # import streamlit as st
# # import pandas as pd

# # st.write("Hello, what would you like our AI to predict ? ")

# # df = pd.DataFrame({
# #     'first column': [1, 2, 3, 4],
# #     'second column': [10, 20, 30, 40]
# # })

# # option = st.selectbox(
# #     "Which number do you like best?",
# #     df['first column']
# # )

# # if option > 2:
# #     st.write("The option selected is above 2")

# # else :
# #     st.write("The option selected is below or equal to 2")



# # x = st.slider('x')  # 👈 this is a widget
# # st.write(x, 'squared is', x * x)


# # prompt = st.text_input("What match do you want our AI to predict ex : 'manchester city vs real madrid '", key="match")

# # # You can access the value at any point with:
# # st.session_state.match

# # @st.cache_data
# # def generate_response(prompt):
# #     return "This is a response to your prompt: " + prompt
