class Queue:
    def __init__(self):
        self.__data = []

    def enqueue(self, data):
        self.__data.append(data)

    def dequeue(self):
        return self.__data.pop(0)

    def first(self):
        return self.__data[0]

    def empty(self):
        return len(self.__data) == 0

    def __str__(self):
        return str(self.__data)