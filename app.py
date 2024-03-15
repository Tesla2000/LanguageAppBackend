from flask import Flask

app = Flask(__name__)
import endpoints

_ = endpoints
if __name__ == "__main__":
    app.run(debug=True)
