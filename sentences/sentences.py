import atexit
import json

from Config import Config


class _LanguageDict(dict):
    def get(self, language):
        result = super().get(language, json.loads(Config.sentences.joinpath(language).read_text()))
        self[language] = result
        return result


sentences = _LanguageDict()


@atexit.register
def save_languages():
    for language_name, language_dict in sentences.items():
        Config.sentences.joinpath(language_name).write_text(json.dumps(language_dict))
