import string
import os
import uuid
from os import path
from models import *

def add_command(creator_id, keyword):
    new_command = Command(keyword = keyword, channel_id = creator_id)
    session.add(new_command)
    session.commit()

def add_response(command_id, response):
    new_response = Response(command_id = command_id, output = response)
    session.add(new_response)
    session.commit()

def create_creator(username):
    user_exists = session.query(User).filter_by(twitch_username = username).first()
    if not user_exists:
        new_user = User(twitch_username= username)
        session.add(new_user)
        session.commit()
    creator_exists = session.query(Creator).filter_by(twitch_channel = username).first()
    if not creator_exists:
        new_creator = Creator(twitch_channel = username)
        session.add(new_creator)
        session.commit()

def load_commands(username):
    commands = [
        ('!joke','replies/jokes.txt'),
        ('!fart','replies/fart.txt'),
        ('!panic','replies/panic.txt'),
    ]
    creator = session.query(Creator).filter_by(twitch_channel = username).first()
    print(creator.id)
    for command in commands:
        print (command[0])

    for command in commands:
        add_command(creator.id, command[0])
        is_command = session.query(Command).filter_by(channel_id = creator.id, keyword = str(command[0])).first()
        if is_command:
            reply_file = open(command[1], "r").read().splitlines()
            for line in reply_file:
                add_response(is_command.id, line)
    print('commands done')

def load_configurables(username):
    creator = session.query(Creator).filter_by(twitch_channel = username).first()
    aggression = Configurable(alias ='aggression', value = 10, note = 'range', creator_id = creator.id)
    stupidity = Configurable(alias = 'stupidity', value = 100, note ='range', creator_id = creator.id)
    raffle_state = Configurable(alias = 'raffle_state', value = 0, note = 'bool', creator_id = creator.id)
    operator_state = Configurable(alias = 'operator_state', value = 1, note ='bool', creator_id = creator.id)
    mute_state = Configurable(alias = 'mute_state', value = 0 , note = 'bool', creator_id = creator.id)
    raffle_keyword = Temporary(alias = 'raffle_keyword', value = uuid.uuid4(), note ='raffle keyword, randomized on init', creator_id = creator.id)
    session.add(aggression)
    session.add(stupidity)
    session.add(raffle_state)
    session.add(operator_state)
    session.add(mute_state)
    session.add(raffle_keyword)
    session.commit()
    print('configurables done')

def init_creator(username):
    create_creator(username)
    load_commands(username)
    load_configurables(username)
    print('ok')

init_creator("something")
