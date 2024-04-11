from collections import OrderedDict
from time import sleep

from googletrans import Translator

from sentences import pl_en

if __name__ == "__main__":
    translator = Translator()
    new_translation = OrderedDict()
    for question in pl_en.keys():
        new_translation[question] = translator.translate(question, dest="pt").text
        sleep(1)
        print(new_translation)
