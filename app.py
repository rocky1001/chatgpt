import openai
import streamlit as st

openai.api_key = st.secrets["api_key"]

message_log = [{"role": "user", "content": "你好！"}]


def generate_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=messages,  # The conversation history up to this point, as a list of dictionaries
        temperature=0.7,  # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


st.set_page_config(page_title="lesen_chatgpt")

st.markdown("# 欢迎使用ChatLesen[乐森ChatGPT] - for Jane")
# 增加一个按钮，点击后清空对话记录，重新开始对话
if st.button('清空对话'):
    st.balloons()
    st.session_state['generated'] = []
    st.session_state['past'] = []
    message_log.clear()
    st.experimental_rerun()
st.markdown("### 请在下方输入对话内容")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = st.text_area("You:", key='input')

if user_input:
    # print(message_log)
    message_log.append({"role": "user", "content": user_input})
    output = generate_response(message_log)
    message_log.append({"role": "assistant", "content": output})
    # store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        # message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        st.markdown('**You:**%s' % st.session_state['past'][i])
        # message(st.session_state["generated"][i], key=str(i))
        st.markdown('**ChatLesen:**%s' % st.session_state['generated'][i])
        # 添加分隔符，跟输入框的长度一致
        st.markdown('---')
