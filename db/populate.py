import random
from db.models import *
from faker import Faker

faker = Faker()


def get_sencence():
    return faker.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)


def get_text():
    return faker.text(max_nb_chars=200, ext_word_list=None)


def save_dbobjs(dbobjs):
    for dbobj in dbobjs:
        dbobj.save()


sections = [Section(name=faker.color_name(), section_logo=None) for _ in range(3)]

users = [
    User(
        username=faker.name(),
        avatar=None,
        aboutMe=get_sencence(),
        signature=get_sencence()
    ) for _ in range(10)
]

threads = [
    Thread(title=faker.bs(), createdBy=random.choice(users)) for _ in range(10)
]

thread_followers = [
    ThreadFollowers(thread=random.choice(threads), user=random.choice(users)) for _ in range(10)
]

posts = [
    Post(title=faker.catch_phrase(), post_content=get_text(), parentThread=random.choice(threads)) for _ in range(200)
]

private_message = [
    PrivateMessage(
        subject=faker.catch_phrase(),
        message_content=get_text(),
        sender=random.choice(users),
        receiver=random.choice(users)
    ) for _ in range(200)
]

for x in [sections, users, threads, thread_followers, posts, private_message]:
    save_dbobjs(x)

