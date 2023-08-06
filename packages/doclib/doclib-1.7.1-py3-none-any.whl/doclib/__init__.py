import websockets
import websocket
import json
import re
import random
import argparse
import sys
from attrdict import AttrDict
import attrdict
from getpass import getpass

class Bot:

    @staticmethod
    def log(message, error = False, _copy = False):
        ERROR = "\033[1;31;40m"
        NORMAL = "\033[m"
        print(f'{ERROR if error else NORMAL}{"COPY: " if _copy else ""}{message}{NORMAL}')
        sys.stdout.flush()

    @staticmethod
    def randomize_between(*responses):
        response = random.choice(responses)
        if callable(response):
            return response(self, msg, re.search(regex, msg.data.content))
            if isinstance(result, str):
                return result
            elif isinstance(result, dict):
                for send, nick in result.items():
                    self.set_nick(nick)
                    self.send_msg(send, parent = msg)
                self.set_nick(self.nick)
            elif isinstance(result, list):
                for send in result:
                    self.send_msg(send, parent = msg)
        else:
            if isinstance(response, str):
                self.send_msg(msgString = result, parent = msg)
            elif isinstance(response, dict):
                for send, nick in response.items():
                    self.set_nick(nick)
                    self.send_msg(send, parent = msg)
                self.set_nick(self.nick)
            elif isinstance(response, list):
                for send in response:
                    self.send_msg(send, parent = msg)
            else:
                raise BadMessageError(f"Response type: {type(response)}")
        break

    def __init__(self, nick, **kwargs):
        vars = ["userEmail",
            "userPassword",
            "help",
            "ping",
            "killed",
            "function",
            "_cookie",
            "human",
            "_copy",
            "sendable",
            "APITimeout",
            "advanced",
            "owner",
            "important"]
        noneVars = ["userEmail",
            "userPassword",
            "help",
            "ping",
            "killed",
            "function",
            "_cookie"]
        self.nick = nick
        self.normname = re.sub(r"\s+", "", self.nick)
        self.owner = "nobody"
        self.handlers = {}
        self.copies = []
        self.important = False
        self.APITimeout = 10
        self.advanced = False
        self.sendable = False
        self.copyThreads = []
        self.conn = None
        self.human = False
        self._regexes = {}
        self._copy = False
        for item in vars:
            if item in kwargs:
                self.setattr(item, kwargs[item])
            elif item in noneVars:
                self.setattr(item, None)
        self.normowner = re.sub(r"\s+", "", self.owner)
        self.parser = argparse.ArgumentParser(description=f'{nick}: A euphoria.io bot.' if 'description' not in kwargs else kwargs['description'])
        self.args = self.parser.parse_args()
        if 'customArgs' in kwargs and kwargs['customArgs']:
            self.room = "bots" if "room" not in kwargs else kwargs["room"]
            self.password = "" if "password" not in kwargs else kwargs["password"]
        else:
            self.add_command_line_arg(args = ["--test", "--debug", "-t"], help = "Used to debug dev builds. Sends bot to &test instead of its default room.", action = 'store_true')
            self.add_command_line_arg(args = ["--room", "-r"], help = f"Set the room the bot will be placed in. Default: {'bots' if 'room' not in kwargs else kwargs['room']}", default = "bots" if "room" not in kwargs else kwargs["room"])
            self.add_command_line_arg(args = ["--password", "-p"], help = "Set the password for the room the bot will be placed in.", default = "" if "password" not in kwargs else kwargs["password"])
            self.room = self.args.room if self.args.test != True or _copy else "test"
            self.password = self.args.password
            if not self._copy:
                log(f"Debug: {str(self.args.test)}", _copy = self._copy)

    def add_command_line_arg(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)
        self.args = self.parser.parse_args()
        if "name" in kwargs:
            return self.args.kwargs["name"]
        else:
            return self.args

    def connect(self):
        self.conn = websocket.create_connection(f'wss://euphoria.io/room/{self.room}/ws{"?h=0" if not self.human else "?h=1"}', cookie = self.cookie, enable_multithread = True)
        if self.cookie is None:
            self.cookie = self.conn.headers['set-cookie']
        hello = AttrDict(json.loads(self.conn.recv()))
        reply = AttrDict(json.loads(self.conn.recv()))
        self._handle_ping(reply)
        reply = AttrDict(json.loads(self.conn.recv()))
        if reply.type == "snapshot-event":
            self.set_nick(self.nick)
        elif reply.type == "bounce-event":
            self._handle_auth(self.password)
            self.set_nick(self.nick)
        else:
            log(reply, error = True, _copy = self._copy)
        log(f'connected to &{self.room}.', _copy = self._copy)
        return hello

    def send_msg(self, msgString, parent = None):
        try:
            if isinstance(parent, AttrDict):
                self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString, 'parent': parent.data.id}}))
            elif isinstance(parent, str):
                self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString, 'parent': parent}}))
            elif parent is None:
                self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString}}))
            else:
                raise BadMessageError(f'message not sent, because type of parent was {type(parent)}. \nParent printed: \n{parent}')
            reply = None
            i = 0
            for msgJSON in self.conn:
                i += 1
                msg = AttrDict(json.loads(msgJSON))
                if msg.type == "send-reply":
                    reply = msg
                    if isinstance(parent, AttrDict):
                        log(f'Message sent: {reply} replying to: {parent.data.id} by {parent.data.sender.name}', _copy = self._copy)
                    elif isinstance(parent, str):
                        log(f'Message sent: {reply} replying to: {parent}', _copy = self._copy)
                    elif parent is None:
                        log(f'Message sent: {reply}', _copy = self._copy)
                    return reply
                if i > self.APITimeout:
                    log("send-reply API response not recorded. reason: too many events before send-reply.", True, _copy = self._copy)
                    return None
        except BadMessageError:
            pass

    def restart(self, msg = None, _copyStart = False):
        if self.conn is not None:
            self.conn.close()
            del self.conn
            log("restarting...", _copy = self._copy)
        else:
            log("starting...", _copy = self._copy)
        self.connect()
        self.start()

    def start(self, function = None, advanced = False):
        if not (self.advanced or advanced):
            try:
                for msgJSON in self.conn:
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == 'ping-event':
                        self._handle_ping(msg)
                    elif msg.type == 'send-event' and msg.data.sender.name != self.nick:
                        self._handle_message(msg)
                    elif msg.type == 'error':
                        log(msg, error = True, _copy = self._copy)
                    elif msg.type == 'bounce-event':
                        self._handle_auth(msg)
                    else:
                        self._handle_other(msg)
            except KilledError:
                pass
        else:
            if self.function is None and function is not None and callable(function):
                self.function = function
            else:
                log("No function passed to advanced bot's start function. Using filler function", _copy = self._copy)
                self.function = lambda msg: None
            try:
                for msgJSON in self.conn:
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == 'send-event' and msg.data.sender.name != self.nick:
                        if re.search(f'^!kill @{re.escape(self.normname)}$', msg.data.content) is not None:
                            self._handle_kill(msg)
                        if re.search(f'^!forcekill @{re.escape(self.normname)}$', msg.data.content) is not None:
                            self.kill()
                        if re.search(f'^!restart @{re.escape(self.normname)}$', msg.data.content) is not None:
                            self.restart(msg = msg)
                    if msg.type in self.handlers:
                        self.handlers[msg.type](msg)
                    else:
                        if function is not None and callable(function):
                            function(msg)
                        elif callable(self.function):
                            self.function(msg)
                        else:
                            log("Advanced start must be given a callable message handler function that takes an AttrDict as its argument.", error = True, _copy = self._copy)
            except KilledError:
                pass

    def _is_privileged(self, user):
        if "is_manager" in user or user.name == self.owner:
            return True
        else:
            return False

    def set_regexes(self, regexes):
        self._regexes = regexes
        if self.help is None:
            if f"^!help @{re.escape(self.normname)}$" in regexes:
                self.help = regexes[f"^!help @{re.escape(self.normname)}$"]
            else:
                self.help = f"@{self.normname} is a bot made with Doctor Number Four's Python 3 bot library, DocLib (link: https://github.com/milovincent/DocLib) by @{self.normowner}.\nIt follows botrulez and does not have a custom !help message yet."
        if self.ping is None:
            if '^!ping$' in regexes:
                self.ping = regexes['^!ping$']
            elif f'^!ping @{re.escape(self.normname)}$' in regexes:
                self.ping = regexes[f'^!ping @{re.escape(self.normname)}$']
            else:
                self.ping = "Pong!"
        if self.killed is None:
            if f"^!kill @{re.escape(self.normname)}$" in regexes:
                self.killed = regexes[f"^!kill @{re.escape(self.normname)}$"]
            else:
                self.killed = "/me has died."

    def _handle_ping(self, msg):
        self.conn.send(json.dumps({'type': 'ping-reply', 'data': {'time': msg.data.time}}))

    def _handle_message(self, msg):
        if re.search(f'^!kill @{re.escape(self.normname)}$', msg.data.content) is not None:
            self._handle_kill(msg)
        if re.search(f'^!forcekill @{re.escape(self.normname)}$', msg.data.content) is not None:
            self.kill()
        if re.search(f'^!restart @{re.escape(self.normname)}$', msg.data.content) is not None:
            self.restart(msg = msg)
        if re.search('^!ping$', msg.data.content) is not None or re.search(f'^!ping @(?i){re.escape(self.normname)}$', msg.data.content) is not None:
            self.send_msg(self.ping, parent = msg)
        if re.search(f'^!help @(?i){re.escape(self.normname)}$', msg.data.content) is not None:
            self.send_msg(self.help, parent = msg)
        if re.search(f'^!send @(?i){re.escape(self.normname)} &(\w+)$', msg.data.content) is not None and self.sendable:
            self.move_to(re.search(f'^!send @(?i){re.escape(self.normname)} &(\w+)$', msg.data.content).group(0))
        for regex, response in self._regexes.items():
            if re.search(regex, msg.data.content) is not None:
                if callable(response):
                    result = response(self, msg, re.search(regex, msg.data.content))
                    if isinstance(result, str):
                        self.send_msg(msgString = result, parent = msg)
                    elif isinstance(result, dict):
                        for send, nick in result.items():
                            self.set_nick(nick)
                            self.send_msg(send, parent = msg)
                        self.set_nick(self.nick)
                    elif isinstance(result, list):
                        for send in result:
                            self.send_msg(send, parent = msg)
                else:
                    if isinstance(response, str):
                        self.send_msg(msgString = result, parent = msg)
                    elif isinstance(response, dict):
                        for send, nick in response.items():
                            self.set_nick(nick)
                            self.send_msg(send, parent = msg)
                        self.set_nick(self.nick)
                    elif isinstance(response, list):
                        for send in response:
                            self.send_msg(send, parent = msg)
                    else:
                        raise BadMessageError(f"Response type: {type(response)}")
                break

    def _handle_kill(self, msg):
        if self._is_privileged(msg.data.sender) or not self.important:
            self.send_msg(self.killed, msg)
            for process in self.copyThreads:
                process.terminate()
            for copy in self.copies:
                copy.send_msg("/me was killed via parricide")
                copy.kill()
            self.kill()
        else:
            self.send_msg(f"Bot not killed because you are not a host or @{self.normowner}, and this bot is marked as important.\nFor emergencies, use !forcekill.", parent = msg)

    def _handle_auth(self, pw):
        self.conn.send(json.dumps({'type': 'auth', 'data': {'type': 'passcode', 'passcode': pw}}))
        reply = None
        i = 0
        for msgJSON in self.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "auth-reply":
                reply = msg
                if reply.data.success == True:
                    log(f'Successfully logged into {self.room}.', _copy = self._copy)
                else:
                    log(f'Login unsuccessful. Reason: {reply.data.reason}', error = True, _copy = self._copy)
                    self._handle_auth(getpass("Enter the correct password: "))
                break
            if i > self.APITimeout:
                log("Auth Error: auth-reply API response not recorded.", error = True, _copy = self._copy)
                break

    def _handle_other(self, msg):
        if msg.type in self.handlers:
            self.handlers[msg.type](msg)

    def set_nick(self, nick):
        self.conn.send(json.dumps({'type': 'nick', 'data': {'name': nick}}))

    def kill(self):
        self.conn.close()
        raise KilledError(f'{self.normname} killed.')

    def get_userlist(self):
        self.conn.send(json.dumps({'type': 'who'}))
        reply = None
        i = 0
        for msgJSON in self.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "who-reply":
                reply = msg
                return reply.data.listing
            if i > self.APITimeout:
                log("who-reply API response not recorded. reason: too many events before who-reply.", error = True, _copy = self._copy)
                return None

    def move_to(self, roomName, password = "", _copyStart = False):
        self.room = roomName
        self.password = password
        self.restart(_copyStart = _copyStart)
        if _copyStart:
            log(f"Copy started in &{self.room}.", _copy = self._copy)

    def set_handler(self, eventString, function):
        if callable(function):
            self.handlers[eventString] = function
        else:
            log(f"WARNING: handler for {eventString} not callable, handler not set.", error = True, _copy = self._copy)

    def set_handlers(self, handlers):
        for eventString, function in handlers.items():
            self.set_handler(eventString, function)

    def copy_to(self, roomName, password = None):
        copy = Bot(nick = self.nick,
            room = roomName,
            owner = self.owner,
            userEmail = self.userEmail,
            userPassword = self.userPassword,
            password = self.password if password is None else password,
            help = self.help,
            ping = self.ping,
            important = self.important,
            killed = self.killed,
            APITimeout = self.APITimeout,
            advanced = self.advanced,
            function = self.function,
            sendable = self.sendable,
            _copy = True,
            _cookie = self.cookie,
            human = self.human)
        copy.set_handlers(self.handlers)
        copy.set_regexes(self._regexes)
        t = threading.Thread(target = copy.move_to)
        self.copies.append(copy)
        self.copyThreads.append(t)
        t.run(roomName = roomName, password = password, _copyStart = True)
        t.join(0)
        return copy

    def login(self, email = None, password = None, setDefaults = False):
        if email is not None and password is not None:
            self.conn.send(json.dumps({'type': 'login', 'data': {'namespace' : "email", 'id' : email, 'password' : password}}))
            if setDefaults:
                self.userEmail = email
                self.userPassword = password
        elif (self.userEmail is not None and email is None) or (self.userPassword is not None and password is None):
            self.login(email = self.userEmail if email is None else email, password = self.userPassword if password is None else password, setDefaults = setDefaults)
        else:
            self.login(email = input("Enter your email: ") if email is None else email, password = getpass("Enter your password: ") if password is None else password, setDefaults = setDefaults)
        reply = None
        i = 0
        for msgJSON in self.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "login-reply":
                reply = msg
                if reply.data.success:
                    log("Login successful.", _copy = self._copy)
                    self.account = reply.data.account_id
                else:
                    log(f"Access denied. Reason: {reply.data.reason}", error = True, _copy = self._copy)
                    self.login(email = input("Enter your email: "), password = getpass("Enter your password: "), setDefaults = setDefaults)
                return reply
            if i > self.APITimeout:
                log("login-reply API response not recorded. reason: too many events before pm-initiate-reply.", error = True, _copy = self._copy)
                return None

    def initiate_pm(self, id, bot = None, room = "pmtest", hostEmail = None, hostPassword = None):
        copy = Bot(nick = self.nick, room = room)
        copy.connect()
        copy.login(email = hostEmail, password = hostPassword, setDefaults = False)
        copy.conn.close()
        del copy.conn
        copy.connect()
        copy.conn.send(json.dumps({'type': 'pm-initiate', 'data': {'user_id' : id}}))
        to = None
        i = 0
        for msgJSON in copy.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "pm-initiate-reply":
                copy.conn.close()
                to = msg
                if to.data is not None:
                    if bot is not None:
                        bot.copy_to(f"pm:{to.data.pm_id}")
                    else:
                        self.copy_to("pm:{to.data.pm_id}")
                else:
                    log("Access Denied: This bot does not have permission to initiate PMs.", error = True, _copy = self._copy)
                    log(f"reply: {msg}", error = True, _copy = self._copy)
                return to
            if i > self.APITimeout:
                log("pm-initiate-reply API response not recorded. reason: too many events before pm-initiate-reply.", error = True, _copy = self._copy)
                return None

class BotError(Exception):
    pass

class KilledError(BotError):
    def __init__(self, message = "bot killed."):
        self.message = message
        log(f'KilledError: {message}', error = True)

class BadMessageError(BotError):
    def __init__(self, message):
        self.message = message
        log(f'BadMessageError: {message}', error = True)
