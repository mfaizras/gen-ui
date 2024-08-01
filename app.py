from langchain_openai.chat_models import ChatOpenAI
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_groq.chat_models import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage , SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
import streamlit as st

class GenUI:
    def __init__(self) -> None:
        self.client = None
        self.model_list = []
        self.st = st
        self.system_messages = ""
        self.consider_history = False
        if "messages" not in self.st.session_state:
            self.st.session_state.messages = []
        if "chat_history" not in self.st.session_state:
            self.st.session_state.chat_history = []

    def add_to_history(self,chat):
        if len(self.st.session_state.chat_history) >= 10:
            self.st.session_state.chat_history.pop(0)
        self.st.session_state.messages.append(chat)
        self.st.session_state.chat_history.append(chat)

    def generate_response(self,input):
        template = self.system_messages
        if self.consider_history:
            template += """
            .Answer the following questions given using Indonesian. Consider the message history of the conversation. If the question does not match the message history provide the most appropriate answer outside of the context given. 
            """

            messageHistory = []
            messageHistory.append(SystemMessage(content=template))
            messageHistory.extend(self.st.session_state.chat_history)
        else :
            template += """
            .Answer the following questions given using Indonesian.     
            """
            messageHistory = []
            messageHistory.append(SystemMessage(content=template))
            messageHistory.append(HumanMessage(content=input))
        prompt = ChatPromptTemplate.from_messages(messageHistory)

        chain = prompt | self.client | StrOutputParser()

        return chain.invoke({
            "user_question" : input
        })
    
    # def generate_response(self,input):
    #     template = self.system_messages
    #     template += """
    #     .Answer the following questions given using Indonesian.and consider the message history of the conversation. If the question does not match the message history provide the most appropriate answer outside of the context given. 
    #     Chat History = {chat_history}
    #     User Question = {user_question}
    #     """
    #     # template = """
    #     # You are a very helpful assistant. Answer the following questions given using Indonesian. and consider the message history of the conversation.

    #     # Chat History = {chat_history}

    #     # User Question = {user_question}

    #     # """

    #     prompt = ChatPromptTemplate.from_template(template)
    #     chain = prompt | self.client | StrOutputParser()

    #     return chain.invoke({
    #         "chat_history" :self.st.session_state.messages,
    #         "user_question" : input
    #     })


    def main(self):
        openai_api_key_input = self.st.sidebar.text_input("Enter your OpenAi API key:", type="password")
        anthropic_api_key_input = self.st.sidebar.text_input("Enter your Anthropic API key:", type="password")
        groq_api_key_input = self.st.sidebar.text_input("Enter your Groq API key:", type="password")
        gemini_api_key_input = self.st.sidebar.text_input("Enter your Gemini API key:", type="password")

        self.system_messages = self.st.sidebar.text_area("Enter System Message",value="You are a very helpful assistant.")

        model_options = []
        anthropic_model = ["claude-3-opus-20240229","claude-3-sonnet-20240229","claude-2.1","claude-2.0","claude-instant-1.2"]
        openai_model = ["gpt-4o","gpt-4o-mini","gpt-3.5-turbo-0125"]
        groq_model = ["llama-3.1-70b-versatile","llama-3.1-8b-instant","llama3-groq-70b-8192-tool-use-preview","llama3-groq-8b-8192-tool-use-preview","mixtral-8x7b-32768","gemma-7b-it","gemma2-9b-it"]
        gemini_model = ["gemini-1.5-pro","gemini-1.5-flash","gemini-1.0-pro"]

        model_options.extend(anthropic_model)
        model_options.extend(openai_model)
        model_options.extend(groq_model)
        model_options.extend(gemini_model)
        selected_model = self.st.sidebar.selectbox("Select Model", model_options)

        self.consider_history = self.st.sidebar.checkbox("Use History Chat as Context?",value=False)
        self.st.sidebar.html(
            f'<div style="border: 1px solid; border-radius: 25px; padding: 10px;">What is <b>Use History Chat as Context?</b></br> <p>this menu makes chat history can be taken into consideration by AI, this menu will consume more Tokens than normal</p></div>'
        )


        if selected_model in openai_model:
            if openai_api_key_input:
                self.client = ChatOpenAI(api_key=openai_api_key_input,model=selected_model)
            else:
                self.st.warning("Please Provide OpenAi API Key To Use This Model")
        elif selected_model in anthropic_model:
            if anthropic_api_key_input:
                self.client = ChatAnthropic(api_key= anthropic_api_key_input,model=selected_model)
            else:
                self.st.warning("Please Provide Anthropic API Key To Use This Model")
        elif selected_model in groq_model:
            if groq_api_key_input:
                self.client = ChatGroq(api_key= groq_api_key_input,model=selected_model)
            else:
                self.st.warning("Please Provide Groq API Key To Use This Model")
        elif selected_model in gemini_model:
            if gemini_api_key_input:
                self.client = GoogleGenerativeAI(google_api_key=gemini_api_key_input,model=selected_model)
            else:
                self.st.warning("Please Provide Goggle API Key To Use This Model")
        else:
            self.st.error("Unknown model", icon="🚨")

        for message in self.st.session_state.messages:
            if isinstance(message, HumanMessage):
                with self.st.chat_message("user"):
                    self.st.markdown(message.content)
            else :
                with self.st.chat_message("assistant"):
                    self.st.markdown(message.content)

        if prompt := self.st.chat_input("What is up?"):
            # self.st.session_state.messages.append(HumanMessage(prompt))
            self.add_to_history(HumanMessage(prompt))
            with self.st.chat_message("user"):
                self.st.markdown(prompt)

            with self.st.chat_message("assistant"):
                stream = self.generate_response(prompt)
                self.st.markdown(stream)
            # self.st.session_state.messages.append(AIMessage(stream))
            self.add_to_history(AIMessage(stream))

            print(stream)

            print(st.session_state.messages)

app = GenUI()

app.main()