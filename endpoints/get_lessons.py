from Config import Config
from flask_app import app


@app.route("/lessons", methods=["GET"])
def get_lessons():
    return ";".join(path.with_suffix("").name for path in Config.sentences.glob("*.json"))
