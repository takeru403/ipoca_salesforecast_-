import streamlit as st
import os
import pickle
import base64
# sample_list = [1,2,3]
# f = open('sample.textfile','w')
# pickle.dump(sample_list,f)
# f.close

path = '/workspace/opt/'

def app():
    st.markdown("# 現在作成中です。しばらくお待ちください。")
    st.markdown("""## このページは学習済みモデルを保存しておくところです。次のような機能を考えています。
        - モデル名変更機能 \
        - モデル削除機能
   """)
    # st.write("学習済みモデル一覧をここに表示します。")
    # #model_name = st.selectbox('ダウンロードするモデルを選択', list_model())
    # st.write(os.listdir(path))
    # st.write(__file__)
    # pkl_lt = [''] + [f[:-4] for f in os.listdir(os.getcwd()) if f[-4:]=='.pkl']
    # model_name = st.selectbox(label='ドロップダウンリストからモデルを選択してください',options=pkl_lt,key='model')
    # def download_model(model):
    #     output_model = pickle.dumps(model)
    #     b64 = base64.b64encode(output_model).decode()
    #     href = f'<a href="data:/opt/output_model;base64,{b64}">Download Trained Model .pkl File</a> (right-click and save as &lt;some_name&gt;.pkl)'
    #     st.markdown(href, unsafe_allow_html=True)
    # download_model(model_name)
    # #model_name = st.selectbox(label='ドロップダウンリストからモデルを選択してください',options=pkl_lt,key='model')

    #st.download_button('ダウンロード',open(os.path.join(IMG_PATH, filename), 'br'),filename)