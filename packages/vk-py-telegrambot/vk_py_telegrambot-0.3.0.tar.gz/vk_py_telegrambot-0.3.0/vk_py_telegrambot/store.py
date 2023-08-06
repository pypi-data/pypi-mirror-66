import logging
from datetime import datetime
from datetime import timedelta
logger = logging.getLogger('chatbot')

try:
    import pymongo
except ImportError:
    logger.error("Can't import pymongo module. Check requirements.txt")
    exit(500)

from datetime import datetime 

"""
    SessionStore - хранилище данных для бота
"""
class SessionStore:
    def __init__(self):
        self.conn = pymongo.MongoClient()       
        self.db = self.conn['bot-session-store']
        self.sessions = self.db['sessions']
        self.pending_queue = self.db['pending_queue']
        logger.debug('Connection to mongoclinet estabished. We find {} sessions'.format(self.sessions.find().count()))

    def save_message(self, message):
        self.db['messages'].insert_one(message)
        
    def get_userdata_by_id(self, chat_id)->dict:
        """Получает значение переменных для чата"""
        
        user_data = {}
        try:
            query = self.sessions.find_one({"chat_id":chat_id})
            if query:
                logger.debug('Query to db with result {}'.format(query))
                user_data = query
            return user_data
        except Exception as identifier:
            print(identifier)        

        return user_data

    def set_locals_by_id(self, chat_id, data):
        """Устанавливает значение переменных для чата"""
        filter = {"chat_id"   : chat_id}
        new_doc = {
            "chat_id"       : chat_id,
            "context"       : data,
            "stage"         : None,
            "stage_expired" : None
        }

        rec = self.sessions.find_one(filter=filter)

        if rec == None: 
            self.sessions.insert_one(document=new_doc)
        else:
            new_doc['stage']= rec['stage']
            new_doc['stage_expired']= rec['stage_expired']

            self.sessions.replace_one(filter=filter, replacement=new_doc)
        pass

    def set_new_state(self, chat_id:str, new_state:str, ttl:int):
        """Переводит чат в стадию. Стадия используется для контекстной переписки"""
        if ttl>0:
            new_state_ttl = datetime.now() + timedelta(seconds=ttl)
        else:
            new_state_ttl = datetime.now() + timedelta(days=1)
            
        query = {'chat_id':chat_id}
        record = self.sessions.find_one(query)
        if record is None:
           record = {
               'chat_id' : chat_id,
               'state' : new_state,
               'state_ttl' : new_state_ttl
           } 
           self.sessions.insert_one(record)
        else:
            self.sessions.find_one_and_update(
                filter=query,update={
                    '$set':{
                        'state':new_state, 
                        'state_ttl': new_state_ttl
                }})
             
        logger.debug('Для пользователя {} установлено новое состояние {} на срок {} секунд'.format(chat_id, new_state,ttl))
        
        pass

    def drop_state(self, chat_id:str):
        """Сбрасывает текущую стадию с чата"""
        logger.debug('Для пользователя {} состояние сброшено'.format(chat_id))
        pass

    def get_chats_with_expired_stages(self):
        exp_sessions = self.sessions.find({'state_ttl':{'$lte':datetime.now()}})
        if exp_sessions.count()==0:
            return []
        else:
            logger.debug('Нашли {} стадии время ожидания по которым истекло'.format(exp_sessions.count()))
            events = []
            for s in exp_sessions:
                logger.debug('  chat_id: {}, state: {}, ttl: {}'.format(s['chat_id'], s['state'], s['state_ttl']))
                event = {
                    'event':'state_expired',
                    'state':s['state'],
                    'chat_id':s['chat_id']
                }
                if 'context' in s:
                    event['context'] = s['context']
                
                events.append(event)
                self.sessions.find_one_and_update(
                    filter={'_id':s['_id']},
                    update={'$set':{
                        'state':None,
                        'state_ttl':None
                }})
            
            return events
        pass

    def get_pending_messages(self)->[dict]:
        query = {
            'fire_date':{ '$lte':datetime.now()},
            'is_active':True
        }
        update = {'$set':{'is_active':False}}

        queue = self.pending_queue.find_and_modify(query=query, update=update)
        
        if queue is None:
            queue=[]

        if type(queue)==dict: 
            return [queue]

        return queue

    def put_message_in_queue(self, chat_id, text, when, new_state=None, new_state_ttl=0,disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None):
        if when < datetime.now():
            logger.warn('Попытка отправить отложенное сообщение которое уже просроченно')

        el = {
            'text' : text,
            'fire_date' : when,
            'chat_id' : chat_id,
            'new_state' : new_state,
            'new_state_ttl' : new_state_ttl,
            'is_active' : True,
            'disable_web_page_preview' : disable_web_page_preview,
            'reply_to_message_id' : reply_to_message_id,
            'reply_markup' : reply_markup,
            'parse_mode' : parse_mode,
            'disable_notification' : disable_notification,
            'timeout' : timeout

        }
        self.pending_queue.insert_one(el)

    def drop_session(self, id):
        self.sessions.delete_one({'chat_id':id})

    def __del__(self):
        if self.db:
            self.conn.close()
            self.conn = None
            self.db = None
            logger.debug('mongoclient was shuting down....')

