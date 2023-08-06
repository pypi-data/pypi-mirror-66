from .telegramapi import proxy
from .store import SessionStore
from .telegramapi import *

import logging
import os
import re
import sys
import time

logger = logging.getLogger('chatbot')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
)

console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)

class User:
    def __init__(self, source:dict):
        self.chat_id = source['id']
        self.name = source['username']
        self.first_name = source['first_name']
        self.language_code = source['language_code']
        self.context = {}
        self.state = ''
        self.store = None

    def load_context (self, store:SessionStore):
        self.store = store
        ud = store.get_userdata_by_id(self.chat_id) 
        if 'context' in ud:
            self.context = ud['context']
        if 'state' in ud:
            self.state = ud['state']
    
    def get_attr(self, attr):
        if attr in self.context: 
            return self.context[attr]
        else:
            return None
    
    def set_attr(self, attr, value):
        self.context[attr]=value

        if not self.store is None:
            self.store.set_locals_by_id(self.chat_id, self.context)

class ReplyKeyboard:
    def __init__(self):
        self.rows=[[]]
        self.remove_keyboard = False
        self.resize_keyboard = False
        self.one_time_keyboard = False
        pass
    
    def clear(self):
        self.rows = [[]]

    def add_button(self, name, row, request_contact=False,request_location=False):
        button = {
            'text' : name,
            'request_contact' : request_contact,
            'request_location' : request_location
        }
        self.rows[row].append(button)
        pass

    def add_row(self):
        self.rows.append([])
        pass

    def to_json(self)->str:
        res = {
            'keyboard' : self.rows,
            'resize_keyboard' : True,
            'one_time_keyboard' : True,
            'remove_keyboard' : self.remove_keyboard
        }
        return json.dumps(res)

class Message:
    def __init__(self, source:dict):
        self.message_id = source['message_id']
        self.user = User(source['from'])
        self.content_type = None
        self.command = None
        if 'froward_from' in source:        
            self.forward_from = User(source['forward_from'])
        if 'text' in source:                
            self.text:str = source['text']
            self.content_type='text'
            if self.text.startswith('/'):
                # this is a comand
                command = self.text.split()[0].split('@')[0][1:] 
                self.command = command
        if 'audio' in source:
            self.content_type='audio'
        if 'animation' in source:
            self.content_type='animation'
        if 'document' in source:
            self.content_type='document'
        if 'game' in source:
            self.content_type='game'
        if 'photo' in source:
            self.content_type='photo'
        if 'sticker' in source:
            self.content_type='sticker'



class InlineQuery:
    def __init__(self, source):
        pass

class ChosenInlineResult:
    pass

class CallbackQuery:
    pass

class Event:
    def __init__(self):
        self.name = ''


class EventHandler:
    def __init__(self, func, events=None, states=None):
        self.func = func
        self.states = states
        self.events = events
    
    def fire_event(self, event):
        if len(self.events):
            if not event['event'] in self.events:
                return False
        if len(self.states):
            if not event['state'] in self.states:
                return False

        stop = self.func(event)
        return stop

class MessageHandler:
    def __init__(self, func, commands=None, regexp=None, test_func=None, content_types=['text'], states=None):
        self.func = func
        if commands is None: 
            self.commands = [] 
        else: 
            self.commands=commands

        if states is None: 
            self.states = [] 
        else: 
            self.states=states

        self.regexp = regexp
        self.test_func = test_func
        self.content_types = content_types

    def handle_message(self, message:Message):
        if len(self.commands):
            if not message.command in self.commands:
                return False

        if len(self.states):
            if not message.user.state in self.states:
                return False
        
        if not self.regexp is None:
            if not re.search(self.regexp, message.text, re.IGNORECASE):
                return False
        
        if not self.test_func is None:
            if not self.test_func(message):
                return False   

        stop = self.func(message)
        return stop


class Bot:
    def __init__(self, token:str, skip_pending:bool=False, num_threads:int=2):
        self.token = token
        self.store:SessionStore = SessionStore()
        self.last_update_id = 0
        self.skip_pending = skip_pending

        self.message_handlers:list(MessageHandler)=[]
        self.events_hendlers:list(EventHandler)= []
        self.jobs_queue = None
        self.running = False
    
    def start(self, none_stop=False, interval=0, timeout=20):
        logger.info('Started .......')
        self.running=True
        while self.running:
            try:
                logger.debug('Pull')
                
                # Забираем отложенные сообщения и отправляем пользователям
                pending_messages = self.store.get_pending_messages()
                for message in pending_messages:
                    self.send_message(
                        chat_id=message['chat_id'],
                        text=message['text'],
                        new_state_ttl=message['new_state_ttl'],
                        new_state=message['new_state'], 
                        disable_web_page_preview=message['disable_web_page_preview'],
                        reply_to_message_id=message['reply_to_message_id'],
                        reply_markup=message['reply_markup'],
                        parse_mode=message['parse_mode'],
                        disable_notification=message['disable_notification'],
                        timeout=message['timeout']
                    )


                # Смотрим в базе по каким пользователям наступило время сбрасывать статус    
                events = self.store.get_chats_with_expired_stages()
                for event in events:
                    for handler in self.events_hendlers:
                        if handler.fire_event(event): break

                # Смотрим сообщения для бота и извлекаем в коллекцию сообщения
                json_updates = get_updates(self.token,offset=self.last_update_id+1)
                messages = []
                inline_query = []
                others=[]
                for ju in json_updates:
                    self.store.save_message(ju)
                    if 'message' in ju: messages.append(Message(ju['message']))
                    if 'edited_message' in ju: messages.append(Message(ju['edited_message']))
                    if 'channel_post' in ju: messages.append(Message(ju['channel_post']))
                    if 'edited_channel_post' in ju: messages.append(Message(ju['edited_channel_post']))
                    if 'inline_query' in ju: inline_query.append(InlineQuery(ju['inline_query']))
                    if 'chosen_inline_result' in ju: others.append(ChosenInlineResult(ju['chosen_inline_result']))
                    if 'callback_query' in ju: others.append(CallbackQuery(ju['callback_query']))
                    self.last_update_id=ju['update_id']
 
                for message in messages:
                    for handler in self.message_handlers:
                        message.user.load_context(self.store)
                        if handler.handle_message(message): break
                
                time.sleep(timeout)
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt received.")
                break
        logger.info('Stopped polling.')

    def stop(self):
        self.running=False
        logger.info("Bot was stopped")
        pass

    def send_message(self, chat_id, text, when=None, new_state=None, new_state_ttl=0, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None):
        """
            :when: - Дата и время, когда сообщение должно быть отправлено. если не заполнено отправляется немеделенно
            :new_state: - состоения в которое должен перейти чат после отправки
            :new_state_ttl: - срок жизни нового состояния в секундах. если не установлено - сутки
            :reply_markup: - клавиатура для ответа. Можно собрать руками, но проще используя класс  ReplyKeyboard
        """
        if not when is None:
            self.store.put_message_in_queue(
                chat_id=chat_id,
                text=text,
                when=when, 
                new_state=new_state,
                new_state_ttl=new_state_ttl,
                disable_web_page_preview=disable_web_page_preview,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                disable_notification=disable_notification,
                timeout=timeout
            )
        else:
            send_message(
                token=self.token,
                chat_id=chat_id,
                text = text,
                disable_web_page_preview=disable_web_page_preview,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                disable_notification=disable_notification,
                timeout=timeout
            )
            logger.debug('message {} was sent to {} state {} was activated'.format(text, chat_id, new_state))

            if not new_state is None:
                self.store.set_new_state(
                    chat_id=chat_id,
                    new_state = new_state,
                    ttl=new_state_ttl
                )

    def register_event_handler(self, states=None, events=None):

        def decorator(handler):
            _handler = EventHandler(handler, states=states, events=events)
            self.events_hendlers.append(_handler)
            return handler
        
        return decorator


    def register_message_handler(self, commands=None, regexp=None, func=None, states=None, content_types=['text']):
        def decorator(handler):
            _handler = MessageHandler(handler, commands=commands, regexp=regexp, test_func=func,states=states, content_types=content_types)
            self.message_handlers.append(_handler)            
            return handler

        if content_types is None:
            content_types = ['text']
        
        return decorator