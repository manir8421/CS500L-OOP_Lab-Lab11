from abc import  ABC, abstractmethod
from typing import Optional

class Light:
    def turn_on(self):
        print("Turning on light")

    def turn_off(self):
        print("Turning off light")

class Fan:
    def start(self):
        print("Starting a fan")

    def stop(self):
        print("Stopping a fan")

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class FanStartCommand(Command):
    def __init__(self, fan:Fan) ->None:
        self.__obj = fan
        
    def execute(self):
        self.__obj.start()

class FanStopCommand(Command):
    def __init__(self, fan:Fan) ->None:
        self.__obj = fan
        
    def execute(self):
        self.__obj.stop()

class LightOnCommand(Command):
    def __init__(self, light:Light) ->None:
        self.__obj = light
        
    def execute(self):
        self.__obj.turn_on()

class LightOffCommand(Command):
    def __init__(self, light:Light) ->None:
        self.__obj = light
        
    def execute(self):
        self.__obj.turn_off()

class RemoteControl:
    def __init__(self) -> None:
        self.__lightOnCommand: Optional[LightOnCommand] = None
        self.__lightOffCommand: Optional[LightOffCommand] = None
        self.__fanStartCommand: Optional[FanStartCommand] = None
        self.__fanStopCommand: Optional[FanStopCommand] = None

    def set_command(self, command: Command):
        if  isinstance(command, LightOnCommand):
            self.__lightOnCommand = command
        elif isinstance(command, LightOffCommand):
            self.__lightOffCommand = command
        elif isinstance(command, FanStartCommand):
            self.__fanStartCommand = command
        elif  isinstance(command, FanStopCommand):
            self.__fanStopCommand = command
        

    def lightOnButtonPressed(self):
        if self.__lightOnCommand is not None:
            self.__lightOnCommand.execute()

    def lightOffButtonPressed(self):
        if self.__lightOffCommand is not None:
            self.__lightOffCommand.execute()

    def fanStartButtonPressed(self):
        if  self.__fanStartCommand is not None:
            self.__fanStartCommand.execute()

    def fanStopButtonPressed(self):
        if  self.__fanStopCommand is not None:
            self.__fanStopCommand.execute()


def main():
    light = Light()
    fan = Fan()
    control  = RemoteControl()

    control.set_command(LightOnCommand(light))
    control.set_command(LightOffCommand(light))
    control.set_command(FanStartCommand(fan))
    control.set_command(FanStopCommand(fan))

    control.lightOnButtonPressed()
    control.lightOffButtonPressed()
    control.fanStartButtonPressed()
    control.fanStopButtonPressed()

if __name__ == "__main__":
    main()
    