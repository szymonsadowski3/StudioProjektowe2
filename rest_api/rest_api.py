from flask import Flask, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_cors import CORS


from config import DEFAULTS
from models import *

app = Flask(__name__)
CORS(app)


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
        "items": sections
    }), 204 if is_response_empty else 200


def count(query_object):
    try:
        sections = [model_to_dict(x) for x in query_object]
    except Exception as e:
        print(e)
        sections = []
    is_response_empty = len(sections) == 0
    return str(len(sections)), (204 if is_response_empty else 200)


@app.route('/sections')
def get_sections():
    return handler_by_query(Section.select().paginate(get_int_arg('page'), get_int_arg('per_page')))


@app.route('/sections/<int:section_id>')
def get_section_by_id(section_id):
    return handler_by_query(
        Section.select().where(Section.id == section_id).paginate(
            get_int_arg('page'), get_int_arg('per_page'))
    )


@app.route('/sections/<int:section_id>/thread')
def get_threads_by_section_id(section_id):
    return handler_by_query(
        Thread.select().join(Section).where(Section.id == section_id)
    )


@app.route('/users')
def get_users():
    return handler_by_query(User.select().paginate(get_int_arg('page'), get_int_arg('per_page')))


@app.route('/users/<int:user_id>')
def get_user_by_id(user_id):
    return handler_by_query(
        Section.select().where(User.id == user_id).paginate(
            get_int_arg('page'), get_int_arg('per_page'))
    )


@app.route('/threads')
def get_threads():
    return handler_by_query(Thread.select().paginate(get_int_arg('page'), get_int_arg('per_page')))


@app.route('/threads/<int:thread_id>')
def get_thread_by_id(thread_id):
    return handler_by_query(
        Thread.select().where(Thread.id == thread_id).paginate(
            get_int_arg('page'), get_int_arg('per_page'))
    )


@app.route('/threads/<int:thread_id>/followers')
def get_thread_followers_by_id(thread_id):
    return handler_by_query(
        User
        .select()
        .join(ThreadFollowers, on=(ThreadFollowers.user == User.id))
        .where(ThreadFollowers.thread == thread_id)
        .paginate(get_int_arg('page'), get_int_arg('per_page'))
    )


@app.route('/posts')
def get_posts():
    return handler_by_query(Post.select().paginate(get_int_arg('page'), get_int_arg('per_page')))


@app.route('/posts/<int:post_id>')
def get_post_by_id(post_id):
    return handler_by_query(
        Post.select().where(Post.id == post_id).paginate(
            get_int_arg('page'), get_int_arg('per_page'))
    )


@app.route('/threads/<int:thread_id>/posts')
def get_posts_by_thread_id(thread_id):
    return handler_by_query(
        Post.select().join(Thread).where(Thread.id == thread_id).paginate(
            get_int_arg('page'), get_int_arg('per_page')
        )
    )


@app.route('/threads/<int:thread_id>/postCount')
def get_post_count(thread_id):
    return count(
        Post.select().join(Thread).where(Thread.id == thread_id)
    )


@app.route('/private_messages')
def get_private_messages():
    return handler_by_query(PrivateMessage.select().paginate(get_int_arg('page'), get_int_arg('per_page')))


@app.route('/private_messages/<int:private_message_id>')
def get_private_message_by_id(private_message_id):
    return handler_by_query(
        PrivateMessage.select().where(PrivateMessage.id == private_message_id).paginate(
            get_int_arg('page'), get_int_arg('per_page'))
    )


if __name__ == '__main__':
    app.run(threaded=True, port=5050)
