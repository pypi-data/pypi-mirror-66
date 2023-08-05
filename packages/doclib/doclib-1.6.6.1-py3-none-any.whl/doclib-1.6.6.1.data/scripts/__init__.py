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
from multiprocessing import Process
import multiprocessing as mp
from websocket import _cookiejar


mp.set_start_method('fork')

def botlog(message, error = False, _copy = False):
    ERROR = "\033[1;31;40m"
    NORMAL = "\033[m"
    print((ERROR if error else NORMAL) + ("COPY: " if _copy else "") + message + NORMAL)
    sys.stdout.flush()

class Bot:


    def __init__(self, nick, room = "bots", owner = None, password = "", help = None, ping = None, important = False, killed = None, API_timeout = 10, advanced = False, function = None, sendable = False, _copy = False, _cookie = None, human = False):
        parser = argparse.ArgumentParser(description=f'{nick}: A euphoria.io bot.')
        parser.add_argument("--test", "--debug", "-t", help = "Used to debug dev builds. Sends bot to &test instead of its default room.", action = 'store_true')
        parser.add_argument("--room", "-r", help = f"Set the room the bot will be placed in. Default: {room}", action = "store", default = room)
        parser.add_argument("--password", "-p", help = "Set the password for the room the bot will be placed in.", action = "store", default = password)

        args = parser.parse_args()
        self.nick = nick
        self.room = args.room if args.test != True or _copy else "test"
        self.normname = re.sub(r"\s+", "", self.nick)
        self.owner = owner if owner != None else "nobody"
        self.normowner = re.sub(r"\s+", "", self.owner)
        self.password = args.password
        self.handlers = {}
        self.copies = []
        self.help = help
        self.ping = ping
        self.important = important
        self.killed = killed
        self.API_timeout = API_timeout
        self.advanced = advanced
        self.function = function
        self.sendable = sendable
        self.copyProcesses = []
        self.cookie = _cookie
        self.conn = None
        self.human = human
        self._regexes = {}
        self._copy = _copy
        if not _copy:
            botlog("Debug: " + str(args.test), _copy = self._copy)


    def connect(self):
        self.conn = websocket.create_connection(f'wss://euphoria.io/room/{self.room}/ws{"?h=0" if not self.human else "?h=1"}', cookie = self.cookie, enable_multithread = True)
        if self.cookie == None:
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
            botlog(reply, error = True, _copy = self._copy)
        botlog(f'connected to &{self.room}.', _copy = self._copy)
        return hello

    def send_msg(self, msgString, parent = None):
        if re.search(r"^\[.+,.+\]$", msgString):
            msgString = random.choice(msgString[1:-1].split(","))
        try:
            if isinstance(parent, AttrDict):
                self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString, 'parent': parent.data.id}}))
                reply = None
                i = 0
                for msgJSON in self.conn:
                    i += 1
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == "send-reply":
                        reply = msg
                        botlog(f'Message sent: {reply} replying to: {parent.data.id} by {parent.data.sender.name}', _copy = self._copy)
                        return reply
                    if i > self.API_timeout:
                        botlog("send-reply API response not recorded. reason: too many events before send-reply.", True, _copy = self._copy)
                        return None

            elif isinstance(parent, str):
                self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString, 'parent': parent}}))
                reply = None
                i = 0
                for msgJSON in self.conn:
                    i += 1
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == "send-reply":
                        reply = msg
                        botlog(f'Message sent: {reply} replying to: {parent}', _copy = self._copy)
                        return reply
                    if i > self.API_timeout:
                        botlog("send-reply API response not recorded. reason: too many events before send-reply.", True, _copy = self._copy)
                        return None
            elif parent == None:
                self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString}}))
                reply = None
                i = 0
                for msgJSON in self.conn:
                    i += 1
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == "send-reply":
                        reply = msg
                        botlog(f'Message sent: {reply}', _copy = self._copy)
                        return reply
                    if i > self.API_timeout:
                        botlog("send-reply API response not recorded. reason: too many events before send-reply.", True, _copy = self._copy)
                        return None

            else:
                raise BadMessageError(f'message not sent, because type of parent was {type(parent)}. \nParent printed: \n{parent}')
        except BadMessageError:
            pass




    def restart(self, msg = None, _copyStart = False):
        if self.conn != None:
            self.conn.close()
            del self.conn
            botlog("restarting...", _copy = self._copy)
        else:
            botlog("starting...", _copy = self._copy)
        self.connect()
        self.start()


    def nothing(msg):
        return

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
                        botlog(msg, error = True, _copy = self._copy)
                    elif msg.type == 'bounce-event':
                        self._handle_auth(msg)
                    else:
                        self._handle_other(msg)
            except KilledError:
                pass
        else:
            if self.function == None and function != None and callable(function):
                self.function = function
            else:
                botlog("No function passed to advanced bot's start function.", _copy = self._copy)
            try:
                for msgJSON in self.conn:
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == 'send-event' and msg.data.sender.name != self.nick:
                        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None:
                            self._handle_kill(msg)
                        if re.search(f'^!forcekill @{self.normname}$', msg.data.content) != None:
                            self.kill()
                        if re.search(f'^!restart @{self.normname}$', msg.data.content) != None:
                            self.restart(msg = msg)
                    if msg.type in self.handlers.keys():
                        self.handlers[msg.type](msg)
                    else:
                        if function != None and callable(function):
                            function(msg)
                        elif callable(self.function):
                            self.function(msg)
                        else:
                            botlog("Advanced start must be given a callable message handler function that takes an AttrDict as its argument.", error = True, _copy = self._copy)
            except KilledError:
                pass



    def _is_privileged(self, user):
        if "is_manager" in user.keys() or user.name == self.owner:
            return True
        else:
            return False

    def set_regexes(self, regexes):
        self._regexes = regexes
        if self.help == None:
            if f"^!help @{self.normname}$" in regexes.keys():
                self.help = regexes[f"^!help @{self.normname}$"]
            else:
                self.help = f"@{self.normname} is a bot made with Doctor Number Four's Python 3 bot library, DocLib (link: https://github.com/milovincent/DocLib) by @{self.normowner}.\nIt follows botrulez and does not have a custom !help message yet."
        if self.ping == None:
            if '^!ping$' in regexes.keys():
                self.ping = regexes['^!ping$']
            elif f'^!ping @{self.normname}$' in regexes.keys():
                self.ping = regexes[f'^!ping @{self.normname}$']
            else:
                self.ping = "Pong!"
        if self.killed == None:
            if f"^!kill @{self.normname}$" in regexes.keys():
                self.killed = regexes[f"^!kill @{self.normname}$"]
            else:
                self.killed = "/me has died."

    def _handle_ping(self, msg):
        self.conn.send(json.dumps({'type': 'ping-reply', 'data': {'time': msg.data.time}}))

    def _handle_message(self, msg):
        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None:
            self._handle_kill(msg)
        if re.search(f'^!forcekill @{self.normname}$', msg.data.content) != None:
            self.kill()
        if re.search(f'^!restart @{self.normname}$', msg.data.content) != None:
            self.restart(msg = msg)
        if re.search('^!ping$', msg.data.content) != None or re.search(f'^!ping @(?i){self.normname}$', msg.data.content) != None:
            self.send_msg(self.ping, parent = msg)
        if re.search(f'^!help @(?i){self.normname}$', msg.data.content) != None:
            self.send_msg(self.help, parent = msg)
        if re.search(f'^!send @(?i){self.normname} &(\w+)$', msg.data.content) != None and self.sendable:
            self.move_to(re.search(f'^!send @(?i){self.normname} &(\w+)$', msg.data.content).group(0))
        for regex, response in self._regexes.items():
            if re.search(regex, msg.data.content) != None:
                if callable(response):
                    result = response(self, msg, re.search(regex, msg.data.content))
                    if type(result) == str:
                        self.send_msg(msgString = result, parent = msg)
                    elif type(result) == dict:
                        for send, nick in result.items():
                            self.set_nick(nick)
                            self.send_msg(send, parent = msg)
                        self.set_nick(self.nick)
                    elif type(result) == list:
                        for send in result:
                            self.send_msg(send, parent = msg)
                else:
                    self.send_msg(response, parent = msg)
                break

    def _handle_kill(self, msg):
        if self._is_privileged(msg.data.sender) or not self.important:
            self.send_msg(self.killed, msg)
            for process in self.copyProcesses:
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
                    botlog(f'Successfully logged into {self.room}.', _copy = self._copy)
                else:
                    botlog(f'Login unsuccessful. Reason: {reply.data.reason}', error = True, _copy = self._copy)
                    self._handle_auth(getpass("Enter the correct password: "))
                break
            if i > self.API_timeout:
                botlog("Auth Error: auth-reply API response not recorded.", error = True, _copy = self._copy)
                break

    def _handle_other(self, msg):
        if msg.type in self.handlers.keys():
            self.handlers[msg.type](msg)


    def set_nick(self, nick):
        self.conn.send(json.dumps({'type': 'nick', 'data': {'name': nick}}))

    def kill(self):
        self.conn.close()
        raise KilledError(f'{self.normname} killed.')

    def get_userlist(self):
        self.conn.send(json.dumps({'type': 'who', 'data': {}}))
        reply = None
        i = 0
        for msgJSON in self.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "who-reply":
                reply = msg
                return reply.data.listing
            if i > self.API_timeout:
                botlog("who-reply API response not recorded. reason: too many events before who-reply.", error = True, _copy = self._copy)
                return None


    def move_to(self, roomName, password = "", _copyStart = False):
        self.room = roomName
        self.password = password
        self.restart(_copyStart = _copyStart)
        if _copyStart:
            botlog(f"Copy started in &{self.room}.", _copy = self._copy)

    def set_handler(self, eventString, function):
        if callable(function):
            self.handlers[eventString] = function
        else:
            botlog(f"WARNING: handler for {eventString} not callable, handler not set.", error = True, _copy = self._copy)

    def set_handlers(self, handlers):
        for eventString in handlers:
            self.set_handler(eventString, handlers[eventString])

    def copy_to(self, roomName, password = None):
        copy = Bot(nick = self.nick,
        room = roomName,
        owner = self.owner,
        password = self.password if password == None else password,
        help = self.help,
        ping = self.ping,
        important = self.important,
        killed = self.killed,
        API_timeout = self.API_timeout,
        advanced = self.advanced,
        function = self.function,
        sendable = self.sendable,
        _copy = True,
        _cookie = self.cookie,
        human = self.human)
        copy.set_handlers(self.handlers)
        copy.set_regexes(self._regexes)
        p = Process(target = copy.move_to, kwargs = {"roomName" : roomName, "password" : password, "_copyStart" : True})
        self.copies.append(copy)
        self.copyProcesses.append(p)
        p.start()
        p.join(0)
        return copy

    def login(self, email = "", password = ""):
        self.conn.send(json.dumps({'type': 'login', 'data': {'namespace' : "email", 'id' : email, 'password' : password}}))
        reply = None
        i = 0
        for msgJSON in self.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "login-reply":
                reply = msg
                if reply.data.success:
                    botlog("Login successful.", _copy = self._copy)
                    self.account = reply.data.account_id
                else:
                    botlog(f"Access denied. Reason: {reply.data.reason}", error = True, _copy = self._copy)
                    self.login(email = input("Enter your email: "), password = getpass("Enter your password: "))
                return reply
            if i > self.API_timeout:
                botlog("login-reply API response not recorded. reason: too many events before pm-initiate-reply.", error = True, _copy = self._copy)
                return None

    def initiate_pm(self, id, bot = None):
        copy = Bot(nick = self.nick, room = "pmtest")
        copy.connect()
        copy.login(email="anonymous@magrittescow.com", password = "correcthorsebatterystaple")
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
                if to.data != None:
                    if bot != None:
                        bot.copy_to("pm:" + to.data.pm_id)
                    else:
                        self.copy_to("pm:" + to.data.pm_id)
                else:
                    botlog("Access Denied: This bot does not have permission to initiate PMs.", error = True, _copy = self._copy)
                    botlog(f"reply: {msg}", error = True, _copy = self._copy)
                return to
            if i > self.API_timeout:
                botlog("pm-initiate-reply API response not recorded. reason: too many events before pm-initiate-reply.", error = True, _copy = self._copy)
                return None


class BotError(Exception):
    pass

class KilledError(BotError):
    def __init__(self, message = "bot killed."):
        self.message = message
        botlog(f'KilledError: {message}', error = True)

class BadMessageError(BotError):
    def __init__(self, message):
        self.message = message
        botlog(f'BadMessageError: {message}', error = True)
