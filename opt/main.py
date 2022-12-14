import streamlit as st

import app
import library
from api.controller.auth.login import Login

#* Lyaouts
st.set_page_config(page_title='asusiru', page_icon='./static/img/favicon/asusiru_favicon.png',layout="wide")
library.config.remove_menu_footer()

#* 共通のsession state ログイン情報
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if __name__ == "__main__":
    #* ログイン認証に成功すればmain_appに切り替え
    if st.session_state['authentication_status']:
        app.app()
    else:
        obj_auth = Login("db/user.db")
