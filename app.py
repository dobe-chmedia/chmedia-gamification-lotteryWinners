##**************************************************************************
##
## Description -------------------------------------------------------------
##
##**************************************************************************
##*
"""Build a Machine Learning Web App with Streamlit and Python"""
##*
##*
##* 1. open anaconda prompt and change directory to the folder where the app.py file is located
##*     > cd P:\Familie\Projekte\EigenEntwicklungen\chmedia-gamification-lotteryWinners
##* 2. run the following command:
##*     > streamlit run app.py
##*
##*
##* Supported Python versions: 3.8 - 3.12
##*     used python version: 3.11.3
##*     environment: CHMEDIA_gam_lottWin__3_11_3
##*
##* App-URL: chmedia-gamification-lottery-winners.streamlit.app
##*
##* App settings in [TOML format](https://toml.io/en/v1.0.0)
##*
##*     pip install streamlit
##*     pip install htbuilder
##*
##*
##* Modifications:
##* Date                User        Description
##* ------------------------------------------------------------------------
##* 2023-12-20          bettlerd    created script
##*
##*

import os
import uuid
import base64
import streamlit as st
from datetime import datetime
from io import BytesIO

from streamlit.runtime.uploaded_file_manager import UploadedFile

from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


st.set_page_config(
    page_title="CH Media Entertainment - WhisperAI",
    page_icon="./image/CH_Media_Logo_RGB_Blau.png",
    layout="wide",
)

def main():
    try:
        st.title("WhisperAI")
        st.markdown("Transcribe your audio and video files with OpenAI's WhisperAI.")

        st.sidebar.markdown("## File Upload")

        footer()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}", icon="🚨")
        

#region streamlit helper functions
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="white",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)
        else:
            raise ValueError(f"Invalid argument {arg} passed to layout(...)")

    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        "Created by Technology CH Media Entertainment (Team Paul)",
        " with ❤️ "
    ]
    layout(*myargs)
#endregion

if __name__ == '__main__':
    main()