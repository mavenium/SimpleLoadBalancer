from flask import Flask

from os import environ

app = Flask(__name__)


@app.route('/')
def main():
    return f'This is the {environ["APP"]} application.\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
