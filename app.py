import streamlit as st
import os
from modules.components.assistant import AiCanAssistant
from modules.db.conn import get_session
from models import User, UserFile 
import pandas as pd

session = get_session()

st.set_page_config(layout="wide")

st.title('a.i.Can - Demo App')

selected_user = None
user_files = None 
user_file_paths = []

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    if openai_api_key:
        os.environ.setdefault("OPENAI_API_KEY", openai_api_key)

    assistant_id  = st.text_input("OpenAI Assitant ID", key="openai_asst_id") # "asst_VgAWFIpruEDXU88KeDd3NNxd"
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[Get an OpenAI Assistant](https://platform.openai.com/assistants)"
    "[View the source code](https://github.com/NisugaJ/a.i.Can-demo)"

    users = session.query(User).all()
    user_ids = {user.user_id: user for user in users}

    selected_user = user_ids[st.selectbox('Select a user', list(user_ids.keys()), index=0, format_func=lambda x: user_ids[x].name)]
    st.write(f'You selected {selected_user.name} ({selected_user.user_id})')

    user_files = session.query(UserFile).filter(UserFile.user_id == selected_user.user_id)
    user_files_dict = {user_file.file_id :[user_file.file_name, user_file.file_id] for user_file in user_files}

    df = pd.DataFrame(user_files_dict.values(), columns=['File Name', 'File ID'])
    st.table(df)

    st.divider()


thread = None

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not assistant_id:
        st.info("Please add your OpenAI Assistant ID to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    asst = AiCanAssistant(assistant_id=assistant_id, openai_key=openai_api_key)
    asst.update()
    asst.refresh_agent()

    if thread is None:
        thread = asst.create_thread()

    # if len(user_file_paths) == 0: # TODO: Improve the app use the previously uploaded files
    for user_file in user_files:
        user_file_paths.append(f"./data/user-data/{user_file.file_name}")
    print(user_file_paths)

    AiCanAssistant.add_message(thread.id, "user", prompt, files=user_file_paths) 

    with st.spinner('Wait for it...'):
        response = asst.run_thread(thread)
        text = response.data[0].content[0].text.value
        st.session_state.messages.append({"role": "assistant", "content": text})
        st.chat_message("assistant").write(text)