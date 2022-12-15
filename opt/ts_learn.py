import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import streamlit as st
import pandas as pd
import datetime
import os
import streamlit.components.v1 as stc
import time
import altair as alt
import joblib
import sys 
from dateutil.relativedelta import relativedelta 
#from pycaret.internal.pycaret_experiment import TimeSeriesExperiment

from pycaret.time_series import *
from typing import List

from library.s3_service import S3Service

BASE_PATH = 'landroam/pycaret/time_series/'

def app():
    s3 = S3Service()
    sys.setrecursionlimit(10000)#再帰処理の上限を定めることでエラー回避する。

    st.markdown("# 時系列学習フェーズ")
    st.markdown("## 1.学習させるデータをアップロードしてください")
    uploaded_file = st.file_uploader("CSVファイルをドラッグ&ドロップ", type='csv', key='train')
    #学習用データをアップロードされた後の処理
    if uploaded_file is not None:
        #オプションのthousandsでカンマを文字列として扱わなくなる。
        df = pd.read_csv(uploaded_file,thousands=',')
        st.write("学習用データのアップロードが完了しました")
        st.dataframe(df, 800,300)

        #ここで、一旦予測に使えない説明変数を削除してもらう
        #説明変数を削除する機能
        st.markdown("## 2.削除したい説明変数はありますか?")
        @st.cache()
        def delete_feature(deletes):
            df = df.drop(deletes, axis=1)
            return df
        deletes:str = st.multiselect("セレクトボックスから削除したい説明変数を選択してください",list(df.columns))
        df = df.drop(deletes, axis=1)
        st.dataframe(df, 800,300)

        #ここで、sum関数を使って、データセットの日毎の合計を出す。
        df["purchase_date"] = pd.to_datetime(df["purchase_date"])
        df = df.groupby("purchase_date").sum()
        #sumで欠損値が出るので、前後の値で欠損値を埋める。
        df = df.resample('D').interpolate()

        st.line_chart(df)

        target:str =  st.selectbox("セレクトボックスから学習したい目的変数を選択してください",list(df.columns))

        if target != "":
            st.markdown("## 3.機械学習を始めます。")

        if st.button("学習開始"):
            st.markdown("学習中です...しばらくお待ちください...")
            exp_name = setup(data=df ,target=target,fh = 7, fold = 3, session_id = 123,seasonal_period="M",html=False)
            # デフォルトでもっとも優れたモデルが手に入る。
            best = compare_models()

            # 方法１  ***3つのモデルをブレンドする***
            # top3 = compare_models(n_select = 3)
            # blender = blend_models(top3)

            #tune_model() # 計算に時間がかかるので、今回は行わない。

            model = create_model(best)
            # final = finalize_model(model)
            #final変数を予測で使えるように書き出しておく

            # 問題のところ
            # joblib.dump(final,"final.txt")

            # arima = create_model('arima')
            # ts は　timeseries プロットのこと
            plot_model(plot = 'ts',display_format="streamlit")

            model_name = 'saved_model'+datetime.date.today().strftime('%Y%m%d')
            save_model(model, model_name)

            st.write("学習が終了しました。時系列予測フェーズに進んで下さい。")

            # try:
            #     # model upload
            #     s3.upload(os.path.join(BASE_PATH, 'models', f'{model_name}.pkl'), f'{model_name}.pkl')
            #     # data upload
            #     s3.upload(os.path.join(BASE_PATH, 'train_data', uploaded_file), uploaded_file)
            #     # model & data delete
            #     os.remove(f'{model_name}.pkl')
            #     os.remove(uploaded_file)
            # except Exception as error:
            #     print(error)
            #     st.write(f"モデルとデータがuploadに失敗しました。: {error}")
# importエラーの可能性
# scikit-learnのversionを0.23.2から、1.0.2に変更しなくてはいけない?