import os
import json
import sys


class AnyErr(Exception):
    pass


# Класс для настроек, задаваемых пользователем через джесон
class JsonUserSet:
    def __init__(self, classmainset):  # Конструктор
        self.ms = classmainset
        self.__inifilename = os.path.join(self.ms.dircur, "hdmi44mtxset.json")
        if not os.path.exists(self.__inifilename):
            raise FileNotFoundError("Не найден файл: "+self.__inifilename)
        with open(self.__inifilename, "r", encoding='utf-8') as f:
            self.__inijson = json.load(f)

    def getparams(self):
        sparam = ""
        try:
            sparam = "dev_ipport"
            self.ms.dev_ipport = self.__inijson.get(sparam).lower().strip()
            self.ms.dev_ip, self.ms.dev_port = self.ms.dev_ipport.split(':')
            self.ms.dev_port = int(self.ms.dev_port)
            #Массив шаблонов команд
            sparam = "command_templates"
            self.ms.command_templates = self.__inijson.get(sparam)

        except AnyErr as err:
            print("Ошибка при считывании параметра " + sparam + "\n" + str(err))
            raise

    def setparams(self):
        sparam = ""
        try:
            sparam = "dev_ipport"
            self.__inijson[sparam] = self.ms.dev_ipport
            sparam = "command_templates"
            self.__inijson[sparam] = self.ms.command_templates
            #Запись в файл
            with open(self.__inifilename, 'w', encoding='utf-8') as f:
                json.dump(self.__inijson, f, indent=2, ensure_ascii=False)
        except AnyErr as err:
            print("Ошибка при установке параметра " + sparam + "\n" + str(err))
            raise

# Класс для настроек приложения
class MainSet:
    def __init__(self):  # Конструктор
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
        self.command_templates = list()
        self.dircur = os.path.dirname(os.path.realpath(__file__))
        #установка начальных параметров
        self.__jus = JsonUserSet(self)
        self.__jus.getparams()

    def __del__(self):
        self.__jus.setparams()
