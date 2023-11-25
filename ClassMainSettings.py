import os
import json
import sys


class AnyErr(Exception):
    pass


# Класс для настроек, задаваемых пользователем через джесон
class JsonUserSet:
    def __init__(self, classmainset):  # Конструктор
        self.ms = classmainset
        self.ms.badInit = True
        try:
            self.__inifilename = os.path.join(self.ms.dircur, "hdmi44mtxset.json")
            if not os.path.exists(self.__inifilename):
                self.initParams()
            with open(self.__inifilename, "r", encoding='utf-8') as f:
                self.__inijson = json.load(f)
            self.ms.badInit = False
        except:
            pass

    def getparams(self):
        sparam = ""
        try:
            sparam = "dev_ipport"
            self.ms.dev_ipport = self.__inijson.get(sparam).lower().strip()
            self.ms.dev_ip, self.ms.dev_port = self.ms.dev_ipport.split(':')
            self.ms.dev_port = int(self.ms.dev_port)
            #Массив команд
            sparam = "command_list"
            self.ms.command_list = self.__inijson.get(sparam)

        except AnyErr as err:
            print("Ошибка при считывании параметра " + sparam + "\n" + str(err))
            raise

    def setparams(self):
        sparam = ""
        try:
            sparam = "dev_ipport"
            self.__inijson[sparam] = self.ms.dev_ipport
            sparam = "command_list"
            self.__inijson[sparam] = self.ms.command_list
            #Запись в файл
            with open(self.__inifilename, 'w', encoding='utf-8') as f:
                json.dump(self.__inijson, f, indent=2, ensure_ascii=False)
        except AnyErr as err:
            print("Ошибка при установке параметра " + sparam + "\n" + str(err))
            raise

    def initParams(self):
        self.ms.badInit = True
        try:
            s = '{"dev_ipport": "192.168.0.221:8899"}'
            if os.path.exists(os.path.join(self.__inifilename)):
                os.remove(self.__inifilename)
            if os.path.exists(os.path.join(self.__inifilename)):
                raise
            with open(self.__inifilename, 'w+', encoding='utf-8') as f:
                f.write(s)
            self.ms.badInit = False
        except AnyErr as err:
            self.ms.badInitError = "Ошибка при инициализации параметров \n" + str(err)

# Класс для настроек приложения
class MainSet:
    def __init__(self):  # Конструктор
        self.badInit = True
        self.badInitError = ""
        # Только винда и линух
        if sys.platform.startswith('linux'):
            self.oscur = "lin"
        elif sys.platform.startswith('win'):
            self.oscur = "win"
        else:
            print("Неподдерживаемая операционная система: " + sys.platform + "!")
            raise
        self.dev_ipport = ""
        self.dev_ip = ""
        self.dev_port = 0
        self.command_list = list()
        self.dircur = os.path.dirname(os.path.realpath(__file__))
        # установка начальных параметров
        self.__jus = JsonUserSet(self)
        self.__jus.getparams()

    def __del__(self):
        self.__jus.setparams()
