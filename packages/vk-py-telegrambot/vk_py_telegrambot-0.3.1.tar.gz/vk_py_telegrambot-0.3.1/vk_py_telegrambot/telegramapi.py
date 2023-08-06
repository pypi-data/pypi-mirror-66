import json
import logging

logger = logging.getLogger('chatbot')

try:
    import requests
except ImportError:
    logger.error("can't import requests module")
    exit(500)

try:    
    from requests.packages.urllib3 import fields
    format_header_param = fields.format_header_param
except ImportError:
    format_header_param = None

proxy = None

API_URL = None
FILE_URL = None

CONNECT_TIMEOUT = 3.5
READ_TIMEOUT = 9999

class APIException(Exception):

    def __init__(self, msg, function_name, result):
        super(APIException, self).__init__("A request to the Telegram API was unsuccessful. {0}".format(msg))
        self.function_name = function_name
        self.result = result

def _get_req_session(reset=False):
    session = requests.Session()
    return session

def _make_request(token, method_name, method='get', params=None, files=None):
    """
    Makes a request to the Telegram API.
    :param token: The bot's API token. (Created with @BotFather)
    :param method_name: Name of the API method to be called. (E.g. 'getUpdates')
    :param method: HTTP method to be used. Defaults to 'get'.
    :param params: Optional parameters. Should be a dictionary with key-value pairs.
    :param files: Optional files.
    :return: The result parsed to a JSON dictionary.
    """
    if API_URL is None:
        request_url = "https://api.telegram.org/bot{0}/{1}".format(token, method_name)
    else:
        request_url = API_URL.format(token, method_name)
    
    logger.debug("Request: method={0} url={1} params={2} files={3}".format(method, request_url, params, files))
    read_timeout = READ_TIMEOUT
    connect_timeout = CONNECT_TIMEOUT
    if files and format_header_param:
        fields.format_header_param = _no_encode(format_header_param)
    if params:
        if 'timeout' in params: read_timeout = params['timeout'] + 10
        if 'connect-timeout' in params: connect_timeout = params['connect-timeout'] + 10
    result = _get_req_session().request(method, request_url, params=params, files=files,
                                        timeout=(connect_timeout, read_timeout), proxies=proxy)
    logger.debug("The server returned: '{0}'".format(result.text.encode('utf8')))
    return _check_result(method_name, result)['result']

def _check_result(method_name, result):
    """
    Checks whether `result` is a valid API response.
    A result is considered invalid if:
        - The server returned an HTTP response code other than 200
        - The content of the result is invalid JSON.
        - The method call was unsuccessful (The JSON 'ok' field equals False)

    :raises ApiException: if one of the above listed cases is applicable
    :param method_name: The name of the method called
    :param result: The returned result of the method request
    :return: The result parsed to a JSON dictionary.
    """
    if result.status_code != 200:
        msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
            .format(result.status_code, result.reason, result.text.encode('utf8'))
        raise APIException(msg, method_name, result)

    try:
        result_json = result.json()
    except:
        msg = 'The server returned an invalid JSON response. Response body:\n[{0}]' \
            .format(result.text.encode('utf8'))
        raise APIException(msg, method_name, result)

    if not result_json['ok']:
        msg = 'Error code: {0} Description: {1}' \
            .format(result_json['error_code'], result_json['description'])
        raise APIException(msg, method_name, result)
    return result_json

def get_me(token):
    method_url = r'getMe'
    return _make_request(token, method_url)

def send_message(token, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                 parse_mode=None, disable_notification=None, timeout=None):
    """
    Use this method to send text messages. On success, the sent Message is returned.
    :param token:
    :param chat_id:
    :param text:
    :param disable_web_page_preview:
    :param reply_to_message_id:
    :param reply_markup:
    :param parse_mode:
    :param disable_notification:
    :return:
    """
    method_url = r'sendMessage'
    payload = {'chat_id': str(chat_id), 'text': text}
    if disable_web_page_preview:
        payload['disable_web_page_preview'] = disable_web_page_preview
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = reply_markup
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification:
        payload['disable_notification'] = disable_notification
    if timeout:
        payload['connect-timeout'] = timeout
    return _make_request(token, method_url, params=payload, method='post')

def send_photo(token, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None,
               parse_mode=None, disable_notification=None):
    method_url = r'sendPhoto'
    payload = {'chat_id': chat_id}
    files = None
    if not isinstance(photo, str):
        files = {'photo': photo}
    else:
        payload['photo'] = photo
    if caption:
        payload['caption'] = caption
    if reply_to_message_id:
        payload['reply_to_message_id'] = reply_to_message_id
    if reply_markup:
        payload['reply_markup'] = _convert_markup(reply_markup)
    if parse_mode:
        payload['parse_mode'] = parse_mode
    if disable_notification:
        payload['disable_notification'] = disable_notification
    return _make_request(token, method_url, params=payload, files=files, method='post')


def get_updates(token, offset=None, limit=None, timeout=None, allowed_updates=None):
    method_url = r'getUpdates'
    payload = {}
    if offset:
        payload['offset'] = offset
    if limit:
        payload['limit'] = limit
    if timeout:
        payload['timeout'] = timeout
    if allowed_updates:
        payload['allowed_updates'] = json.dumps(allowed_updates)
    return _make_request(token, method_url, params=payload)

def answer_callback_query(token, callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
    """
    Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, True is returned.
    Alternatively, the user can be redirected to the specified Game URL. For this option to work, you must first create a game for your bot via BotFather and accept the terms. Otherwise, you may use links like telegram.me/your_bot?start=XXXX that open your bot with a parameter.
    :param token: Bot's token (you don't need to fill this)
    :param callback_query_id: Unique identifier for the query to be answered
    :param text: (Optional) Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters
    :param show_alert: (Optional) If true, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to false.
    :param url: (Optional) URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @Botfather, specify the URL that opens your game – note that this will only work if the query comes from a callback_game button.
    Otherwise, you may use links like telegram.me/your_bot?start=XXXX that open your bot with a parameter.
    :param cache_time: (Optional) The maximum amount of time in seconds that the result of the callback query may be cached client-side. Telegram apps will support caching starting in version 3.14. Defaults to 0.
    :return:
    """
    method_url = 'answerCallbackQuery'
    payload = {'callback_query_id': callback_query_id}
    if text:
        payload['text'] = text
    if show_alert:
        payload['show_alert'] = show_alert
    if url:
        payload['url'] = url
    if cache_time is not None:
        payload['cache_time'] = cache_time
    return _make_request(token, method_url, params=payload, method='post')


def answer_inline_query(token, inline_query_id, results, cache_time=None, is_personal=None, next_offset=None,
                        switch_pm_text=None, switch_pm_parameter=None):
    method_url = 'answerInlineQuery'
    payload = {'inline_query_id': inline_query_id, 'results': _convert_list_json_serializable(results)}
    if cache_time is not None:
        payload['cache_time'] = cache_time
    if is_personal:
        payload['is_personal'] = is_personal
    if next_offset is not None:
        payload['next_offset'] = next_offset
    if switch_pm_text:
        payload['switch_pm_text'] = switch_pm_text
    if switch_pm_parameter:
        payload['switch_pm_parameter'] = switch_pm_parameter
    return _make_request(token, method_url, params=payload, method='post')

def _convert_markup(markup):
    # if isinstance(markup, types.JsonSerializable):
    #     return markup.to_json()
    # return markup
    return []

def _convert_list_json_serializable(results):
    # ret = ''
    # for r in results:
    #     if isinstance(r, types.JsonSerializable):
    #         ret = ret + r.to_json() + ','
    # if len(ret) > 0:
    #     ret = ret[:-1]
    # return '[' + ret + ']'
    return []

def _no_encode(func):
    def wrapper(key, val):
        if key == 'filename':
            return u'{0}={1}'.format(key, val)
        else:
            return func(key, val)

    return wrapper
