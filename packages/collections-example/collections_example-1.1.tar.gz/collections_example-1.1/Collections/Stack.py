class Stack:
    def __init__(self):
        self.__data = []

    def push(self, data):
        self.__data.append(data)

    def pop(self):
        return self.__data.pop()

    def top(self):
        return self.__data[-1]

    def empty(self):
        return len(self.__data) == 0

    def __str__(self):
        return str(self.__data)