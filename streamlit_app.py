import streamlit as st
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

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

user_input = st.text_input("What do you want me to predict ? ")

@st.cache_data
def generate_response(user_input):
    #st.session_state['count'] += 1
    prompt = prompt_template.invoke({"input": user_input})
    response = model.invoke(prompt)
    query_result = response.content
    teams = query_result.split(",") if "," in query_result else [query_result]
    query_result1, query_result2 = teams[0], teams[1]


    return response.content, query_result1, query_result2

if user_input:
    st.write(generate_response(user_input))


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
