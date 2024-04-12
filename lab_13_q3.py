import sqlite3
from abc import ABC, abstractmethod
from typing import Any, Dict

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def execute(self, query, params=None):
        if params is None:
            params = []
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor.fetchall()

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CreateTableCommand(Command):
    def __init__(self, database: Database, table_name: str, columns: dict[str, str]) -> None:
        self.__database = database
        self.__table_name = table_name
        self.__columns = columns

    def execute(self):
        query = "CREATE TABLE " + self.__table_name + "("
        for column, data_type in self.__columns.items():
            query += column + " " + data_type + ", "
        query = query[:-2] + ")"
        self.__database.execute(query)

class InsertCommand(Command):
    def __init__(self, database: Database, table_name: str, values_list: list[Dict[str, Any]]) -> None:
        self.__database = database
        self.__table_name = table_name
        self.__values_list = values_list

    def execute(self):
        for values in self.__values_list:
            columns = ', '.join(values.keys())
            placeholders = ', '.join(['?' for _ in values])
            query = f"INSERT INTO {self.__table_name} ({columns}) VALUES ({placeholders})"
            self.__database.execute(query, list(values.values()))

class SelectCommand(Command):
    def __init__(self, database: Database, table_name: str, where: str) -> None:
        self.__database = database
        self.__table_name = table_name
        self.__where = where

    def execute(self):
        query = f"SELECT * FROM {self.__table_name}" + (f" WHERE {self.__where}" if self.__where else "")
        results = self.__database.execute(query)
        for row in results:
            print(row)
        return results

class UpdateCommand(Command):
    def __init__(self, database: Database, table_name: str, updates: list[Dict[str, Any]], where: str) -> None:
        self.__database = database
        self.__table_name = table_name
        self.__updates = updates
        self.__where = where

    def execute(self):
        for values in self.__updates:
            set_values = ', '.join([f"{column} = ?" for column in values.keys()])
            query = f"UPDATE {self.__table_name} SET {set_values} WHERE {self.__where}"
            self.__database.execute(query, list(values.values()))

class DeleteRecordCommand(Command):
    def __init__(self, database: Database, table_name: str, where: str) -> None:
        self.__database = database
        self.__table_name = table_name
        self.__where = where

    def execute(self):
        query = f"DELETE FROM {self.__table_name} WHERE {self.__where}"
        self.__database.execute(query)
        print(f"Deleted from {self.__table_name} where {self.__where}")

class Invoker:
    def __init__(self):
        self.__commands = []

    def add_command(self, command):
        self.__commands.append(command)

    def execute_commands(self):
        for command in self.__commands:
            command.execute()
        self.__commands.clear()

def reset_database_state(db, table_name):
    db.execute(f"DROP TABLE IF EXISTS {table_name}")

def main():
    database = Database("test.db")
    reset_database_state(database, "users")
    invoker = Invoker()
    
    command = CreateTableCommand(database, "users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
    command.execute()

    print("Inserting users list:")
    users_to_insert = [
        {"name": "Md Maniruzzaman"},
        {"name": "Atik"},
        {"name": "Suman"},
        ]
    
    invoker.add_command(InsertCommand(database, "users", users_to_insert))
    for user in users_to_insert:
        print(f"Inserted user into row: {user}")
    
    print("\nDisplay user list after insert:")
    invoker.add_command(SelectCommand(database, "users", ""))
    invoker.execute_commands()

    print("\nUpdating 'Suman' to 'Suman Das'")
    invoker.add_command(UpdateCommand(database, "users", [{"name": "Suman Das"}], "name = 'Suman'"))
    print("Updated users name with {'name': 'Suman Das'} where, previous name = 'Suman'")
    
    print("\nDisplay user list after update:")
    invoker.add_command(SelectCommand(database, "users", ""))
    invoker.execute_commands()

    user_confirmation = input("\nDo you want to delete 'Atik'? (y/n): ").lower()
    if user_confirmation == "y":
        invoker.add_command(DeleteRecordCommand(database, "users", "name = 'Atik'"))
        invoker.execute_commands()

    print("\nDisplay user list after deleted user:")
    display_users(database)

def display_users(db):
    users = db.execute("SELECT * FROM users")
    for user in users:
        print(user)

if __name__ == "__main__":
    main()




