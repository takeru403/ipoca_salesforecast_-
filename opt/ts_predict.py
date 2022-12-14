import os
import streamlit as st
import pandas as pd
import datetime
import streamlit.components.v1 as stc
from pycaret.time_series import *
import joblib

#最終学習モデルの変数ををimport するため
import ts_learn
from library.s3_service import S3Service

MODEL_PATH = 'landroam/pycaret/time_series/models'

def app():

    # 問題のところ 1
    a = joblib.load("final.txt")
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
                # 予測用データに対して、無理やり型変換を行う。
                df_new["purchase_date"] = pd.to_datetime(df_new["purchase_date"])
                df_new = df_new.groupby("purchase_date").sum()
                #sumで欠損値が出るので、前後の値で欠損値を埋める。
                df_new = df_new.resample('D').interpolate()
                ### 問題のところ 2
                predictions = predict_model(dt_saved)

                predictions.to_csv(model_name+'_predict_'+datetime.date.today().strftime('%Y%m%d')+'.csv')
                st.dataframe(predictions)
                st.write("学習した変数が適用されます。")
                plot_model(predictions)
        except ValueError as error:
            st.write("データの形が間違っています")
            st.write(error)
        except KeyError as key:
            st.markdown("## 学習モデルとデータの形が違います。再度予測したいデータをアップロードしてください。")
            st.write(key)
        except:
            print("そのような変数はございません。")

        os.remove(f'{model_name}.pkl')