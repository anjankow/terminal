# This Python file uses the following encoding: utf-8
import typing

class Command:
    def __init__(self, content, label):
        self.content = content
        self.label = label

class CommandSet:
    def __init__(self, name, commandList):
        self.name = name
        self.commandList = commandList

class CommandHolder:
    def __init__(self):
        # all commands consists of CommandSet list
        self.__allCommands = []

    def add(self, newCommandSet: CommandSet):
        self.__allCommands.append(newCommandSet)

    def getCommandSet(self, name: str):
        retVal = None
        for commandSet in self.__allCommands:
            if commandSet.name == name:
                retVal = commandSet
        return retVal

    def getAll(self):
        return self.__allCommands
