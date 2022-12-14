#* 全体のアプリのフロントエンドとなる画面。
#* 基本的にはプログラムに型アノテーションをつけていく。
import learn
import predict
import explanation
import endmodel
import ts_learn
import ts_predict
import streamlit as st
import streamlit.components.v1 as stc
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def app():
    PAGES = {
        "学習": learn,
        "予測": predict,
        "説明": explanation,
        "学習済みモデル": endmodel,
        "時系列学習": ts_learn,
        "時系列予測": ts_predict,
    }

    st.sidebar.title('学習か予測かを選んでください')
    selection:str = st.sidebar.radio("選択", list(PAGES.keys()))
    sns.set(font='IPAexGothic')
    # plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    # plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    # ax.get_xaxis().get_major_formatter().set_useOffset(False)
    # ax.get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    pd.options.display.float_format = '{:.4g}'.format
    if st.session_state['authentication_status']:
        st.write("-"*3)
        if st.sidebar.button("ログアウト"):
            st.session_state['authentication_status'] = None
            st.experimental_rerun()
    #* 各ページモジュールのappを実行
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    import library
    st.set_page_config(page_title='asusiru', page_icon='./static/img/favicon/asusiru_favicon.png', layout="wide")
    library.config.remove_menu_footer()
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None

