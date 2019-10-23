from flask import Flask, jsonify, request
from playhouse.shortcuts import model_to_dict

from config import DEFAULTS
from models import Section

app = Flask(__name__)


def get_int_arg(key):
    return int(request.args.get(key, DEFAULTS[key]))


def handler_by_query(query_object):
    try:
        sections = [model_to_dict(x) for x in query_object]
    except Exception as e:
        print(e)
        sections = []
    is_response_empty = len(sections) == 0
    return jsonify({
        "sections": sections
    }), 204 if is_response_empty else 200


@app.route('/section')
def get_sections():
    return handler_by_query(Section.select().paginate(get_int_arg('page'), get_int_arg('per_page')))


@app.route('/section/<int:section_id>')
def get_section_by_id(section_id):
    return handler_by_query(
        Section.select().where(Section.id == section_id).paginate(get_int_arg('page'), get_int_arg('per_page'))
    )


if __name__ == '__main__':
    app.run()
