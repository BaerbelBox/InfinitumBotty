import csv
import re

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class ICDObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def get_icd(self, code):
        if code == "C64" or code == "P20":
            return ""
        icd10_codes = open('care_icd10_de.csv', 'r',encoding='utf8')
        icd10 = csv.reader(icd10_codes, delimiter=';', quotechar='"')
        for row in icd10:
            if row[0] == code:
                return code +' - ' + row[1]
        return 0

    def update_on_priv_msg(self, data, connection: Connection):
        if data['channel'] != connection.details.get_channel():
            return
        regex = r'\b(\w\d{2}\.?\d?\d?)\b'
        codes = re.findall(regex, data['message'])
        for code in codes:
            code = code.capitalize()
            text = self.get_icd(code)
            if text == 0:
                if code.find('.') != -1:
                    code += '-'
                else:
                     code += '.-'
            text = self.get_icd(code)
            if text != 0:
                connection.send_back(text, data)
