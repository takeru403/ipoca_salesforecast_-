import os
import streamlit as st
import pandas as pd
import datetime
import streamlit.components.v1 as stc
from pycaret.regression import *

from library.s3_service import S3Service
from library.data_manager import DataManager

MODEL_PATH = 'landroam/pycaret/regression/models'

def dropfiles():
    DataManager.dropfile("pkl")
    DataManager.dropfile("csv")

def app():
    st.markdown("# 予測フェーズ")
    st.markdown("# 1.モデルを読み込みます")
    s3 = S3Service()
    model_lt = s3.ls(MODEL_PATH)
    pkl_lt = [''] + [os.path.splitext(f)[0].replace(f'{MODEL_PATH}/', '') for f in model_lt if os.path.splitext(f)[0].rsplit("/", 1)[0] == MODEL_PATH]
    model_name = st.selectbox(label='ドロップダウンリストからモデルを選択してください',options=pkl_lt,key='model')

    if model_name != '':

        s3.download(f'{model_name}.pkl', os.path.join(MODEL_PATH, f'{model_name}.pkl'))
        dt_saved = load_model(model_name)

        st.markdown("# 2.予測したいデータをアップロードします")
        uploaded_file = st.file_uploader("CSVファイルをドラッグ&ドロップ、またはブラウザから選択してください", type='csv', key='test')

        try:

            if uploaded_file is not None:
                df_new = pd.read_csv(uploaded_file,thousands=',')
                predictions = predict_model(dt_saved, data=df_new,round=0)
                predictions = predictions.rename(columns={'Label': '予測結果'})
                predictions.to_csv(model_name+'_predict_'+datetime.date.today().strftime('%Y%m%d')+'.csv')
                st.dataframe(predictions)
                st.write("学習した変数が適用されます。")
                plot_model(predictions)
                dropfiles()

        except ValueError as error:
            st.warning("データの形が学習とは違いますが結果を出力しました。")
            dropfiles()
        except Exception as error:
            print(error)
            st.error("学習モデルとデータの形が違います。再度予測したいデータをアップロードしてください。")
            st.error(error)
            dropfiles()