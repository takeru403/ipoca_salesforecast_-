import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import streamlit as st
import pandas as pd
import datetime
import os
import streamlit.components.v1 as stc
import time
from pycaret.regression import *
from typing import List
import shap
import matplotlib.ticker as ticker
from PIL import Image


import japanize_matplotlib


from library.s3_service import S3Service
from library.data_manager import DataManager

BASE_PATH = 'landroam/pycaret/regression/'
TODAY = datetime.date.today().strftime('%Y%m%d')

def dropfiles():
    DataManager.dropfile("pkl")
    DataManager.dropfile("csv")
    DataManager.dropfile("png")

#@st.cache(suppress_st_warning=True,allow_output_mutation=True,max_entries=100000)
def app():
    s3 = S3Service()
    # st.markdown(button_css, unsafe_allow_html=True)
    st.markdown("# 学習フェーズ")
    st.markdown("## 1.学習させるデータをアップロードしてください")
    uploaded_file = st.file_uploader("CSVファイルをドラッグ&ドロップ", type='csv', key='train')


    #学習用データをアップロードされた後の処理
    if uploaded_file is not None:
        #オプションのthousandsでカンマを文字列として扱わなくなる。

        df = pd.read_csv(uploaded_file,thousands=',')
        st.write("学習用データのアップロードが完了しました")
        try:
            df = df.set_index('店舗名')
        except KeyError:
            print("出店予想データで会っていますか？")

        # st.dataframe(df,800,300)
        st.write(df)
        st.markdown("## 2.データの前処理")
        #セレクトボックスから変数を選んで散布図のxとyを決める機能
        x:str = st.selectbox("x軸を選んでください",list(df.columns))
        y:str = st.selectbox("y軸を選んでください",list(df.columns))
        x_list:List[float] = df[x]
        y_list:List[float] = df[y]
        #fig, ax = plt.subplots()
        sns.set(font='IPAexGothic')
        plt.rcParams["font.size"] = 10
        fig = plt.figure(figsize=(5, 2))
        ax = fig.add_subplot()

        ax.scatter(x_list,y_list,color='blue',alpha=0.6,s=20, cmap='Blues')
        ax.set_xlabel(x)
        ax.set_ylabel(y,rotation="vertical")
        ax.set_title("説明変数の散布図")
        ax.legend()
        plt.ticklabel_format(style='plain',axis='x')
        plt.ticklabel_format(style='plain',axis='y')
        #　目盛りの大きさ
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=6)

        plt.tight_layout()

        # ax.get_xaxis().get_major_formatter().set_useOffset(False)
        # ax.get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
        st.pyplot(fig)

        #説明変数を削除する機能
        st.markdown("### 削除したい説明変数はありますか?")
        @st.cache()
        def delete_feature(deletes):
            df = df.drop(deletes, axis=1)
            return df
        deletes:str = st.multiselect("セレクトボックスから削除したい説明変数を選択してください",list(df.columns))
        df = df.drop(deletes, axis=1)
        st.dataframe(df, 800,300)
        st.markdown("## 3.予測したいターゲットの選択")
        #オプション　value = df.column[0]
        #あとで検討、一旦radioボタン
        # try:
        target:str = st.radio("ラジオボタンから予測したいターゲットを一つ選んでください",("年商","レジ客数","客単価"))
        if target != "":
            st.markdown("## 4.機械学習フェーズ")
        if st.button("学習開始"):
            with st.spinner('学習中です…しばらくお待ち下さい…'):

            #streamlitの前処理を表示できなくする。jupyter環境とは違うため。
            #使えそうなオプション
            #normarize_method => いくつかの方法で正規化等ができる。
            #transformation =>　Trueにすることで乗数変換を用いて、データがガウス分布に従うようにする
            #remove_outliers =>Trueにすると、特異値分解を利用したPCA線形時限削減を用いて、トレーニングデータから外れ値が削除される。
            #log_data => Trueにすることで、訓練データとテストデータがcsvとして保存される。
            #min_child_sampleはデフォルトで20に設定されている。
                ml = setup(data=df,target=target, html=False, train_size=0.8,fold_shuffle=True)
                best = compare_models()
                best_model_results = pull()
            st.success('学習が完了しました！')
            #日本語に変換する
            best_model_results_columns = best_model_results.rename(columns={'Model': '機械学習モデル','MAE':'平均絶対誤差','MSE':'平均二乗誤差','RMSE':'二乗平均平方根誤差','R2':'決定係数','RMSLE':'対数平均二乗誤差','MAPE':'平均絶対%誤差'})
            best_model_results_japan = best_model_results_columns.replace({'Linear Regression': '線形回帰', 'Bayesian Ridge': 'ベイジアン回帰','Lasso Regression':'ラッソ回帰','Ridge Regression':'リッジ回帰','Elastic Net':'エラスティックネット','Lasso Least Angle Regression':'LARS', 'Huber Regressor':'ロバスト回帰','Random Forest Regressor':'ランダムフォレスト','K Neighbors Regressor':'k-近傍回帰','Gradient Boosting Regre':'勾配ブースティング','AdaBoost Regressor':'AdaBoost回帰','Light Gradient Boosting Machine':'Light勾配ブースティング','Decision Tree Regressor':'回帰木','Dummy Regressor':'ダミー回帰','Orthogonal Matching Pursuit':'マッチング追跡'})
            st.write(best_model_results_japan) # 比較結果の表示
            #今回は、何が高いのか調べる。ものを予測モデルとして選んでいるが、自分で学習モデルを選べるようにすることも考える。

            select_model = best_model_results.index[0]
            # select_model = "xgboost"
            model = create_model(select_model)
            final = finalize_model(model)
            # str(model_name) = select_model+target+'_saved_'+datetime.date.today().strftime('%Y%m%d')
            model_name = str(select_model+target+'_saved_')
            # SHAPの値を出すコードを作る
            # setup()で前処理が終わったデータ
            X_train = get_config("X_train")
            X_test = get_config("X_test")
            y_train =get_config("y_train")
            y_test = get_config("y_test")

            #save_model(final, model_name)
            save_model(final, select_model+target+'_saved_'+datetime.date.today().strftime('%Y%m%d'))
                #特徴量説明量
            plot_model(model, plot="feature", display_format="streamlit")

            #残差
            plot_model(model, plot="error", display_format="streamlit")                

       

            # このモデルが選ばれた場合は直接描画できる。
            if select_model == 'ridge' or select_model == 'en' or select_model == 'huber' or select_model == 'lasso' or select_model == 'lr' or select_model == 'llar' or select_model == 'lar' or select_model == 'par' or select_model == 'et' or select_model == 'br' or select_model == 'ada' or select_model == 'gbr':
                xai_filename = {'model_type': 1, 'filename': f'{TODAY}_FeatureImportance_{select_model}.png'}
                plot_model(model, plot="feature",display_format='streamlit', save=True)
                st.write("pngとしてfeatureimportanceが出力されます。")

            elif select_model == 'catboost' or select_model == "lightgbm":
                xai_filename = {'model_type': 2, 'filename': f'{TODAY}_Shap_Summary_{select_model}.png'}
                interpret_model(model, save=True)
                st.write("pngとしてshapが出力されます。")
            
            ### xgboostのみ対応していなかったので、PFIを実装
            elif select_model == "xgboost":
                from sklearn.inspection import permutation_importance
                # PFIの値を計算
                PFI = permutation_importance(estimator = model,X = X_test, y = y_test,scoring="neg_root_mean_squared_error",n_repeats=5,n_jobs=-1,random_state=42)
                # 説明変数のカラムを追加
                att = df.drop("年商",axis=1)
                attributes = att.columns

                fig, ax = plt.subplots()
                fig.subplots_adjust(left=0.2)
                ax.barh(attributes,PFI.importances_mean)
                plt.title("PFI")
                plt.savefig("PFI.png")
                st.pyplot()
            



            # # これ以降のモデルは保存して出力を行う。
            elif select_model == 'rf' or select_model == 'dt':
                xai_filename = {'model_type': 0, 'filename': f'{TODAY}_Shap_TreeExplainer_{select_model}.png'}
                explainer = shap.TreeExplainer(model=model,data=X_test, feature_perturbation="interventional")
                shap_values = explainer.shap_values(X_test)
                fig = shap.summary_plot(shap_values,X_train, plot_type="bar",plot_size=0.2)
                f = plt.gcf() 
                f.savefig(xai_filename['filename'], dpi=100)
                st.pyplot()
                st.write("回帰木系のshap値")

            elif select_model == 'omp' or select_model == 'svm' or select_model == 'kr' or select_model == 'huber' or select_model == 'knn':
                xai_filename = {'model_type': 0, 'filename': f'{TODAY}_Shap_KernelExplainer_{select_model}.png'}
                explainer = shap.KernelExplainer(model.predict, X_train)
                shap_values = explainer.shap_values(X_train.loc[[0]])
                fig = shap.summary_plot(shap_values, X_train, plot_type="bar",plot_size=0.2)
                f = plt.gcf() 
                f.savefig(xai_filename['filename'], dpi=100)
                st.pyplot()
                st.write("Kernel系のshap値")
            else:
                xai_filename = {'model_type': 999, 'filename': ''}
                st.write("解釈できるモデルではありませんでした。(dummy回帰のみ、解釈できない)")
            st.markdown("モデル構築が完了しました")
            st.markdown("自分のパソコンに拡張子がpklのファイルがあることを確認して、予測フェーズへと進んでください")
            # try:
            #     if xai_filename['model_type'] != 999:
            #         # rename
            #         if xai_filename['model_type'] == 1:
            #             os.rename('Feature Importance.png', xai_filename['filename'])
            #             img = Image.open(xai_filename['filename'])
            #             st.image(img, use_column_width=True)
            #         elif xai_filename['model_type'] == 2:
            #             os.rename('SHAP summary.png', xai_filename['filename'])
            #             img = Image.open(xai_filename['filename'])
            #             st.image(img, use_column_width=True)
            #         else:
            #             pass # model_type: 0 は何もしない
            #         if os.path.exists(os.path.join('.', xai_filename['filename'])):
            #             str_xai_filename = xai_filename['filename']
            #             s3.upload(os.path.join(BASE_PATH, 'xai', f'{str(str_xai_filename)}'), f'{str(str_xai_filename)}')
            #     else:
            #         pass #* 解釈できるモデルではない時
            # except Exception as error:
            #     print(error)
            #     st.error(f"XAIの画像アップロードに失敗しました。: {error}")
            #     dropfiles()
           

            # st.markdown("予測フェーズへと進んでください。")

            # try:
            #     # model upload
            #     # s3.upload(os.path.join(BASE_PATH, 'models', f'{str(model_name)}.pkl'), f'{str(model_name)}.pkl')
            #     # model & data delete
            #     # dropfiles()

            # except Exception as error:
            #     print(error)
            #     st.error(f"モデルとデータのuploadに失敗しました。: {error}")
            #     dropfiles()
