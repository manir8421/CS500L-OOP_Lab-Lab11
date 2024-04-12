from abc import ABC, abstractmethod

class OrderProcessTemplate(ABC):
    def processOrder(self):
        self.__greetCustomer()
        self._orderHook()
    
    def __greetCustomer(self):
        print("Hello! Welcome to our restaurant.")
    
    @abstractmethod
    def _orderHook(self):
        pass

class DineInOrder(OrderProcessTemplate):
    def _orderHook(self):
        self.__takeOrder()
        self.__prepareOrder()
        self.__serveOrder()
        
    def __takeOrder(self):
        print("Taking customer's dine-in order.")

    def __prepareOrder(self):
        print("Preparing the dine-in order in the kitchen.")

    def __serveOrder(self):
        print("Serving the dish to the customer's table.")

class TakeOutOrder(OrderProcessTemplate):
    def _orderHook(self):
        self.__takeOrder()
        self.__prepareOrder()
        self.__serveOrder()
    
    def __takeOrder(self):
        print("Taking customer's take-out order.")

    def __prepareOrder(self):
        print("Preparing the take-out order in the kitchen.")

    def __serveOrder(self):
        print("Wrapping the take-out order and giving it to the customer at the counter.")

def processOrder(orderType):
    if orderType == "dine-in":
        order = DineInOrder()
    elif orderType == "take-out":
        order = TakeOutOrder()
    else:
        print("Unknown order type.")
        return

    order.processOrder()

def main():
    print(f"\nProcessing a Dine-In Order:\n{'-' * 27}")
    processOrder("dine-in")  
    print(f"\nProcessing a Take-Out Order:\n{'-' * 28}")
    processOrder("take-out")

if __name__ == "__main__":
    main()
