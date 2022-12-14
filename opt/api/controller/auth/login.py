import time
import streamlit as st

from ...models.auth.login import UserDataBase
from ...views.auth.login import AlwaysView, AlwaysView, GeneralUserView, AdminUserView, ContactView

class LoginController:
    def __init__(self, db_path: str) -> None:
        self.model = UserDataBase(db_path)
        self.av = AlwaysView()
        self.gu = GeneralUserView()
        self.au = AdminUserView()
        self.cv = ContactView()

    #* 各ページのコントロール
    def _general(self) -> None:
        """
        アカウント認証が成功している場合st_sessionが更新される
        """
        self.gu.main_form()
        self.gu.side_form(self.model)
        auth = 'authentication_status'

        #* アカウント認証に成功
        if st.session_state[auth]:
            st.success(f"ようこそ {st.session_state['name']} さん")
            with st.spinner('アカウント情報を検証中...'):
                time.sleep(0.8)

        #* アカウント認証の情報が間違っているとき
        elif st.session_state[auth] == False:
            st.error("ログイン情報に誤りがあります。再度入力確認してください。")
            st.warning("アカウントをお持ちでない方は管理者に連絡しアカウントを作成してください")

        #* アカウント認証の情報が何も入力されていないとき
        elif st.session_state[auth] is None:
            st.warning("アカウント情報を入力してログインしてください。")

    def _admin(self) -> None:
        admin_chk = self.au.side_form()
        # TODO.. パスべた書き
        if admin_chk == "admin":
            self.au.main_form(self.model)
            if self.au.submit:
                res = self.model.add_user(self.au.name, self.au.username, self.au.password, self.au.adminauth)
                if res:
                    self.au.emp.success(res)
                else:
                    self.au.emp.warning("入力値に問題があるため、登録出来ませんでした")
        elif admin_chk == "":
            st.subheader("アクセスキーを入力してください")
        else:
            st.error("管理者キーが違います")

    #* ページを切り替えた際に実行する関数を変える
    def page_choice(self) -> None:
        """
        ページの遷移
        """
        if self.av.choice_menu == self.av.main_menu[0]:
            self._general()
        if self.av.choice_menu == self.av.main_menu[1]:
            self._admin()
        if self.av.choice_menu == self.av.main_menu[2]:
            self.cv._main_form()

#* Main
class Login:
    def __init__(self, db_path: str) -> None:
        self.controller = LoginController(db_path)
        self.controller.page_choice()

if __name__ == "__main__":
    Login()
    if st.session_state['authentication_status']:
        if st.button("Bye"):
            st.session_state['authentication_status'] = None
            st.experimental_rerun()
