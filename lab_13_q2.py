from abc import ABC, abstractmethod


class Database:
    def insert(self):
        print("Record inserted")
        
    def update(self):
        print("Record updated")
        
    def delete(self):
        print("Record deleted")


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class InsertCommand(Command):
    def __init__(self, db:Database) -> None:
        self.__db = db

    def execute(self):
        self.__db.insert()

class UpdateCommand(Command):
    def __init__(self, db:Database) -> None:
        self.__db = db

    def execute(self):
        self.__db.update()

class DeleteCommand(Command):
    def __init__(self, db: Database) -> None:
        self.__db = db

    def execute(self):
        self.__db.delete()


class Invoker:
    def __init__(self) -> None:
        self.__commands: list[Command] = []

    def add_command(self, command: Command) -> None:
        self.__commands.append(command)

    def execute_commands(self) -> None:
        for command in self.__commands:
            command.execute()
        self.__commands.clear()


class Client:
    def __init__(self, invoker: Invoker) -> None:
        self.__invoker = invoker

    def addCommand(self, command: Command) -> None:
        self.__invoker.add_command(command)

    def executeCommands(self) -> None:
        self.__invoker.execute_commands()


def main():
    db = Database()
    invoker = Invoker()
    client = Client(invoker)

    insertCommand = InsertCommand(db)
    updateCommand = UpdateCommand(db)
    deleteCommand = DeleteCommand(db)
    
    client.addCommand(insertCommand)
    client.addCommand(updateCommand)
    client.addCommand(deleteCommand)
    
    client.executeCommands()

if __name__ == "__main__":
    main()

