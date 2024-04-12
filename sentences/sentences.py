import atexit
import json

from Config import Config


class _LanguageDict(dict):
    def get(self, language):
        result = super().get(
            language,
            json.loads(
                Config.sentences.joinpath(language).with_suffix(".json").read_text()
            ),
        )
        self[language] = result
        return result


sentences = _LanguageDict()


@atexit.register
def save_languages():
    for language_name, language_dict in sentences.items():
        Config.sentences.joinpath(language_name).with_suffix(".json").write_text(
            json.dumps(language_dict, indent=2)
        )
