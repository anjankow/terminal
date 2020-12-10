# This Python file uses the following encoding: utf-8
import typing
from lxml import etree
import os

class Command:
    def __init__(self, content, label=''):
        self.content = content
        self.label = label

class CommandHolder:
    def __init__(self, xmlFile):
        # one command set consists of a name (key)
        # and a list of commands (value)
        self.__allCommandSets = {}
        self.__xmlFile = xmlFile
        # load the data from xml, if it exists
        if os.path.exists(xmlFile):
            self.loadFromXml()


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

    def saveToXml(self):
        '''
        The XML file is stored in the following format:
        <commandConfig>
                <commandSet name=...>
                        <command label=...> ... </command>
                        <command label=...> ... </command>
                </commandSet>
                <commandSet name=...>
                        <command label=...> ... </command>
                </commandSet>
        </commandConfig>
        '''
        root = etree.Element('commandSets')
        print(len(self.__allCommandSets))
        for key in self.__allCommandSets:
            commandSet = etree.SubElement(root, 'commandSet', attrib={'name':key})
            for command in self.__allCommandSets[key]:
                # iterate on Command objects from the list
                xmlCommand = etree.SubElement(commandSet, 'command', attrib={'label':command.label})
                xmlCommand.text = command.content

        print('Saving commands configuration')
        etree.dump(root)

        with open(self.__xmlFile, 'w') as file:
           file.write(etree.tostring(root, encoding='unicode', pretty_print = True))

    def loadFromXml(self):
        '''
        The XML file is stored in the following format:
        <commandConfig>
                <commandSet name=...>
                        <command label=...> ... </command>
                        <command label=...> ... </command>
                </commandSet>
                <commandSet name=...>
                        <command label=...> ... </command>
                </commandSet>
        </commandConfig>
        '''
        tree = etree.parse(self.__xmlFile)
        root = tree.getroot()
        for child in root:
            self.__allCommandSets[child.attrib['name']] = []
            for command in child:
                self.__allCommandSets[child.attrib['name']].append(Command(command.text, command.attrib['label']))


if __name__ == "__main__":
    ch = CommandHolder('pleple.xml')
    ch.saveInXml()

