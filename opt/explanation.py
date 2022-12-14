import streamlit as st
import pandas as pd
import datetime
import streamlit.components.v1 as stc
import os
from pycaret.regression import *

def app():
    st.markdown("# 現在作成中です。少し待ってください")
    st.markdown("## このページにはXAIのSHAPなどの手法を用いて、random forest 等の複雑な回帰モデルの説明を行う予定です。")
    
    # st.markdown("# 1.モデルを読み込みます")
    # pkl_lt = [''] + [f[:-4] for f in os.listdir(os.getcwd()) if f[-4:]=='.pkl']
    # model_s = load_model(pkl_lt)
    # model_name = st.selectbox(label='ドロップダウンリストからモデルを選択してください',options=pkl_lt,key='model')
    # model_s = load_model(model_name)

    # if model_s is not None:
    #     plot_model(model_s, plot="error", display_format="streamlit")