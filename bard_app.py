import asyncio
import streamlit as st
from streamlit_chat import message
from bardapi import Bard
import json

with open('credentials.json','r') as f:
    file = json.load(f)
    token = file['token']

def generate_response(prompt):
    bard = Bard(token=token)
    response = bard.get_answer(prompt)
    return response['content']

async def main():
    st.title("🤖Personal Tutoring!")

    changes = '''
    <style>
    [data-testid="stAppViewContainer"]
    {
    background-image:url('https://images.unsplash.com/photo-1501389683017-9f916b4671b0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80');
    background-size:cover;
    }
    .st-bx {
    background-color: rgba(255, 255, 255, 0.05);
    }
    
    /* .css-1hynsf2 .esravye2 */
    
    html {
    background: transparent;
    }
    div.esravye2 > iframe {
        background-color: transparent;
    }
    </style>
    '''

    st.markdown(changes, unsafe_allow_html=True)
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    def get_text():
        input_text = st.text_input("You: ", "Hey bot!", key="input")
        return input_text

    user_input = get_text()

    if user_input:
        output = await asyncio.to_thread(generate_response, user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            print(st.session_state["generated"],i)
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

asyncio.run(main())
