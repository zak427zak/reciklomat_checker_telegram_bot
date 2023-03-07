import sqlite3


class Database:
    def __init__(self, path_to_db="data/bot.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_user(self):
        sql = """
        CREATE TABLE Users (
        id int NOT NULL,
        language varchar(255) NOT NULL,
        PRIMARY KEY (id);
        """
        self.execute(sql, commit=True)

    def add_user(self, id: int, language: str):
        sql = "INSERT INTO Users(id, language) VALUES (?, ?)"
        parameters = (id, language)
        self.execute(sql, parameters=parameters, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        sql = "SELECT * FROM User WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        sql.execute(sql, parameters, fetchone=True)

    def update_language(self, language, id):
        sql = "UPDATE Users SET language=? WHERE id=?"
        return self.execute(sql, parameters=(language, id), commit=True)
