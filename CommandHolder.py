# This Python file uses the following encoding: utf-8
import typing

class Command:
    def __init__(self, content, label):
        self.content = content
        self.label = label

class CommandHolder:
    def __init__(self):
        # one command set consists of a name (key)
        # and a list of commands (value)
        self.__allCommandSets = {}

    def add(self, name, newCommandSet):
        self.__allCommandSets[name] = newCommandSet

    def delete(self, name: str):
        if name in self.__allCommandSets:
            del self.__allCommandSets[name]

    def getCommandSet(self, name: str):
        if name in self.__allCommandSets:
            return self.__allCommandSets[name]
        else:
            return None

    def getAll(self):
        return self.__allCommandSets

    def saveInXml(self):
        pass

    def loadFromXml(self):
        pass

if __name__ == "__main__":
    ch = CommandHolder()
    ch.add('lalalalpp', 'sssss')
    ch.delete('ooo')
    ch.add('lalalal', 'ppppp')
    com = ch.getCommandSet('lalalal')
    print(com)
    ch.delete('lalalal')
    com = ch.getCommandSet('lalalal')
    print(com)
