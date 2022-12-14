from PIL import Image
import streamlit as st
import streamlit_authenticator as stauth

class AlwaysView:
    def __init__(self) -> None:
        self.main_menu = ["Login", "Admin", "Contact"]
        self.choice_menu = st.sidebar.selectbox("メニュー", self.main_menu)

class GeneralUserView:
    def main_form(self) -> None:
        logo = Image.open('./static/img/アスシル画像.png')
        st.image(logo, use_column_width=True)

    def side_form(self, model: object) -> None:
        """
        認証フォームの表示と認証オブジェクトの表示
        """
        self.authenticator = stauth.Authenticate(
            model.df[model.name],
            model.df[model.username],
            model.df[model.password],
            'some_cookie_name',
            'some_signature_key',
            cookie_expiry_days=0)
        self.authenticator.login("ログイン", "sidebar")

class AdminUserView:
    def main_form(self, model: object) -> None:
        with st.form(key="create_acount"):
            st.subheader("新規ユーザの作成")
            self.name = st.text_input("ニックネームを入力してください", key="create_user")
            self.username = st.text_input("ユーザー名(ID)を入力してください", key="create_user")
            self.password = st.text_input("パスワードを入力してください", type='password', key="create_pass")
            self.adminauth = st.checkbox("管理者権限の付与")
            self.submit = st.form_submit_button(label='アカウントの作成')
        self.emp = st.empty()

        with st.expander("ユーザテーブルを表示"):
            model.get_table()
            st.table(model.df.drop(model.password, axis=1))

    def side_form(self) -> None:
        st.sidebar.write("---")
        st.sidebar.info("adminがキーです")
        return st.sidebar.text_input("管理者アクセスキー", type='password')

class ContactView:
    def _main_form(self) -> None:
        st.subheader("💡お問い合わせ先")
        st.write("""
                | 会社名 | 株式会社ipoca |
                |:--:|:--:|
                |電話番号📞 | 0000-0000-0000 |
                |メール📧 | xxxxxxx@example.com |
                """)