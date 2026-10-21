import requests
import streamlit as st

API_URL = 'http://127.0.0.1:5000'
st.title('AI Sentiment Analysis')
st.caption('Software Engineering: Flask API + Hugging Face + SQLite + JWT')

username = st.text_input('Username')
password = st.text_input('Password', type='password')
if st.button('Login'):
    try:
        response = requests.post(f'{API_URL}/login', json={'username': username, 'password': password}, timeout=10)
        response.raise_for_status()
        st.session_state['token'] = response.json()['token']
        st.success('Logged in successfully')
    except requests.RequestException:
        st.error('Login failed. Check your credentials and start the Flask server.')

if 'token' in st.session_state:
    headers = {'Authorization': f"Bearer {st.session_state['token']}"}
    text = st.text_area('Enter a sentence', placeholder='I really enjoyed this class!')
    if st.button('Analyze Sentiment'):
        try:
            response = requests.post(f'{API_URL}/analyze', json={'text': text}, headers=headers, timeout=180)
            if response.ok:
                result = response.json()
                st.success(f"Sentiment: {result['sentiment']} | Confidence: {result['score']:.2%}")
            else:
                st.error(response.json().get('error', 'Request failed'))
        except requests.RequestException as e:
            st.error(f'Could not connect to API: {e}')

    if st.button('Show Saved Predictions (Table)'):
        try:
            response = requests.get(f'{API_URL}/history', headers=headers, timeout=10)
            if response.ok:
                st.dataframe(response.json(), use_container_width=True)
            else:
                st.error(response.json().get('error', 'Request failed'))
        except requests.RequestException as e:
            st.error(f'Could not connect to API: {e}')
