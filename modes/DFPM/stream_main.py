import time

import streamlit as st
import os
from dotenv import load_dotenv
from runner import run
import streamlit_google_oauth as oauth

load_dotenv()
client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
redirect_uri = os.environ["GOOGLE_REDIRECT_URI"]


def browser_fingerprint():
    st.title("Browser Fingerprinting Tool")
    st.markdown("This tool is based on the DFPM Library, it is also mentioned in the Anti-Bot Confluence article.")
    st.url = st.text_input("Enter URL", "https://www.google.com")
    st.markdown("The URL you entered is: " + st.url)

    if st.button("Submit"):
        st.markdown("Browser Fingerprinting starting for: " + st.url)
        try:
            output = run(st.url)
            # output = {'fingerprint': [{'danger': 'canvas'}, {'warning': 'canvas'}]}
            st.json(output)
        except TypeError as e:
            st.markdown("An Instance Already running, waiting for it to finish!")
            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(1)
                my_bar.progress(percent_complete + 1, text=progress_text)
            output = run(st.url)
            st.json(output)
    else:
        st.markdown("Please enter a URL")


if __name__ == "__main__":
    login_info = oauth.login(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        # login_button_text="Continue with Google",
        logout_button_text="Logout",
    )
    if login_info:
        user_id, user_email = login_info
        st.write(f"Welcome {user_email}")
        browser_fingerprint()
    else:
        st.write("Please login using Zyte Email address!")
