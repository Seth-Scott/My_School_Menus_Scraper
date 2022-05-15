import json
from flask import Flask

app = Flask(__name__)


@app.route('/')
def api():
    with open("data.json", mode="r") as data:
        menu_items = json.load(data)
    return menu_items


# remove this to run in docker?
if __name__ == '__main__':
    app.run(port=5001, host="0.0.0.0")
