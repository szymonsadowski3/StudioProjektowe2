import datetime

from peewee import *

from rest_api.db_configuration import pgdb


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = pgdb


class Section(BaseModel):
    name = CharField()
    section_logo = TextField(null=True)


class User(BaseModel):
    username = CharField()
    createdOn = DateTimeField(default=datetime.datetime.now)
    avatar = TextField(null=True)
    aboutMe = TextField(null=True)
    signature = TextField(null=True)


class Thread(BaseModel):
    title = CharField()
    createdBy = ForeignKeyField(User)
    createdOn = DateTimeField(default=datetime.datetime.now)
    section = ForeignKeyField(Section)


class ThreadFollowers(BaseModel):
    thread = ForeignKeyField(Thread)
    user = ForeignKeyField(User)


class Post(BaseModel):
    title = CharField(null=True)
    createdBy = ForeignKeyField(User)
    post_content = TextField()
    createdOn = DateTimeField(default=datetime.datetime.now)
    parentThread = ForeignKeyField(Thread)


class PrivateMessage(BaseModel):
    subject = CharField(null=True)
    message_content = TextField()
    sentOn = DateTimeField(default=datetime.datetime.now)
    sender = ForeignKeyField(User)
    receiver = ForeignKeyField(User)

# -----------------------------------------------------------


if __name__ == '__main__':
    pgdb.create_tables([
        Section,
        User,
        Thread,
        ThreadFollowers,
        Post,
        PrivateMessage,
    ])
