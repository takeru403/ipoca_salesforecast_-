import sqlite3
import bcrypt
import pandas as pd

class ConnectDataBase:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self.conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.df = None

    def get_table(self, table: str = "userstable", key: str = "*") -> pd.DataFrame:
        self.df = pd.read_sql(f'SELECT {key} FROM {table}', self.conn)
        return self.df

    def close(self) -> None:
        self.cursor.close()
        self.conn.close()

    def __del__(self) -> None:
        self.close()

class UserDataBase(ConnectDataBase):
    def __init__(self, db_path: str) -> None:
        super().__init__(db_path)
        #* カラム名
        self.__name = "name"
        self.__username = "username"
        self.__password =  "password"
        self.__admin = "admin"

        self.__create_user_table()
        self.get_table()

    @property
    def name(self) -> str:
        return self.__name
    @property
    def username(self) -> str:
        return self.__username
    @property
    def password(self) -> str:
        return self.__password
    @property
    def admin(self) -> str:
        return self.__admin


    def __create_user_table(self) -> None:
        """
        該当テーブルが無ければ作る
        """
        self.cursor.execute('CREATE TABLE IF NOT EXISTS userstable({} TEXT, {} TEXT unique, {} TEXT, {} INT)'.format(self.name, self.username, self.password, self.admin))

    def _hashing_password(self, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def __chk_username_existence(self, username: str) -> bool:
        """
        ユニークユーザの確認
        """
        self.cursor.execute('select {} from userstable'.format(self.username))
        exists_users = [_[0] for _ in self.cursor]
        if username in exists_users:
            return True

    def add_user(self, name: str, username: str, password: str, admin: str) -> str or None:
        """
        新しくユーザを追加します
            [args]
                [0] name: str
                [1] username : str (unique only)
                [2] password : str
                [3] admin : bool
            [return]
                res: str or None
        """

        if name == "" or username == "" or password == "":
            return
        if self.__chk_username_existence(username):
            return
        #* 登録
        hashed_password = self._hashing_password(password)
        self.cursor.execute('INSERT INTO userstable({}, {}, {}, {}) VALUES (?, ?, ?, ?)'.format(self.name, self.username, self.password, self.admin),
                                (name, username, hashed_password, int(admin)))
        self.conn.commit()
        return f"{name}さんのアカウントを作成しました"
