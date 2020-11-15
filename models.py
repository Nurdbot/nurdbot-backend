from sqlalchemy import orm, Integer, String, ForeignKey, Column, Text
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from config import *


Base = declarative_base()
#It's cool to change pool params, but by default we're gonna pre-ping and size to 1 connection.
engine = sa.create_engine(f'postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',pool_pre_ping=True,pool_size=1,max_overflow=0)

Base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    twitch_username = sa.Column(sa.String(255), unique=True)
    discord_id = sa.Column(sa.String(255), unique=True)

class Creator(Base):
    __tablename__ = 'creator'
    id = sa.Column(sa.Integer, primary_key=True)
    twitch_channel = sa.Column(sa.String(255), unique=True)
    #!HERE !TODO discord server should be non -unique re: bluecho && everydayemmy
    discord_server = sa.Column(sa.String(255), unique=True)
    commands = orm.relationship("Command", backref='creator')
    discord_logs = orm.relationship("DiscordLog", backref='creator')
    twitch_logs = orm.relationship("TwitchLog", backref='creator')
    configurables = orm.relationship("Configurable", backref='creator')

class Operator(Base):
    __tablename__ = 'operator'
    id = sa.Column(sa.Integer, primary_key=True)
    creator_id = sa.Column(Integer, ForeignKey('creator.id'))
    user_id = sa.Column(Integer, ForeignKey('user.id'))

class Command(Base):
    __tablename__ = 'command'
    id = sa.Column(sa.Integer, primary_key=True)
    keyword = sa.Column(sa.String(255))
    channel_id = sa.Column(Integer, ForeignKey('creator.id'))
    responses = orm.relationship("Response", backref='command', lazy=True)

class Response(Base):
    __tablename__ = 'response'
    id = sa.Column(sa.Integer, primary_key=True)
    output = sa.Column(sa.Text)
    command_id = sa.Column(Integer, ForeignKey('command.id'))

class TwitchLog(Base):
    __tablename__ = 'twitch_log'
    id = sa.Column(sa.Integer, primary_key=True)
    event_time = sa.Column(sa.String(255))
    username = sa.Column(sa.String(255)) 
    message = sa.Column(sa.Text)
    creator_id = sa.Column(Integer, ForeignKey('creator.id'))

class DiscordLog(Base):
    __tablename__ = 'discord_log'
    id = sa.Column(sa.Integer, primary_key=True)
    event_time = sa.Column(sa.String(255))
    display_name = sa.Column(sa.String(255))
    discord_id = sa.Column(sa.Integer)
    message = sa.Column(sa.Text)
    creator_id = sa.Column(Integer, ForeignKey('creator.id'))

class Configurable(Base):
    __tablename__ = 'configurable'
    id = sa.Column(sa.Integer, primary_key=True)
    alias = sa.Column(sa.String(255))
    value = sa.Column(sa.Integer)
    note = sa.Column(sa.String(255))
    creator_id = sa.Column(Integer, ForeignKey('creator.id'))

class Temporary(Base):
    __tablename__ = 'temporary'
    id = sa.Column(sa.Integer, primary_key=True)
    alias = sa.Column(sa.String(255))
    value = sa.Column(sa.String(255))
    note = sa.Column(sa.String(255))
    creator_id = sa.Column(Integer, ForeignKey('creator.id'))

class TwitchHarass(Base):
    __tablename__ = 'twitch_harass'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(255))
    creator_id = sa.Column(Integer, ForeignKey('creator.id'))

class DiscordHarass(Base):
    __tablename__ = 'discord_harass'
    id = sa.Column(sa.Integer, primary_key=True)
    discord_id = sa.Column(sa.String(255))
    creator_id = sa.Column(Integer, ForeignKey('creator.id'))

class Scrap(Base):
    __tablename__ = 'scrap'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(255))
    amount = sa.Column(Integer)
    creator_id = sa.Column(Integer, ForeignKey('creator.id'))

