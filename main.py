from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():

    return "index1231123"


if __name__ == '__main__':
    app.run(debug=True)