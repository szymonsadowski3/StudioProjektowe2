import datetime

from peewee import TextField, DateTimeField, Model, CharField, ForeignKeyField
from db_configuration import pgdb


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
    name = CharField()
    createdBy = ForeignKeyField(User)
    createdOn = DateTimeField(default=datetime.datetime.now)


class ThreadFollowers(BaseModel):
    thread = ForeignKeyField(Thread)
    user = ForeignKeyField(User)


class Post(BaseModel):
    title = CharField(null=True)
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
