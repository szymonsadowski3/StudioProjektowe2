from flask import Flask, jsonify
from playhouse.shortcuts import model_to_dict

from models import Section

app = Flask(__name__)


@app.route('/section')
def hello():
    try:
        sections = model_to_dict(Section.select().get())
    except Exception as e:
        print(e)
        sections = []

    return jsonify(
        {
            "sections": sections
        }
    )


if __name__ == '__main__':
    app.run()
