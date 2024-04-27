import os
from flask import Flask

app = Flask(__name__)

PUBLISH_TARGET = os.getenv("PUBLISH_TARGET")
PORT = os.getenv("PORT")

if __name__ == '__main__':
    if PUBLISH_TARGET == "development":
        app.run(host="127.0.0.1", debug=True, port=int(PORT))
    else:
        app.run(host="0.0.0.0", debug=False, port=int(PORT))