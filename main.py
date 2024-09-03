import os
from ast import For
import json, requests, tls_client, threading, time, random, httpx
import logging
from colorama import Fore, Style
import colorama
import datetime
from base64 import b64encode
import sys
from enum import Enum, IntEnum
from threading import Thread
from typing import Dict, List, Optional, Tuple, Union
import websockets.typing
from colorama import Back, Fore, Style
from websockets.exceptions import ConnectionClosedError
from websockets.sync.client import connect
import string
from websockets.sync.connection import Connection
import os
import hashlib
import json as jsond  # json
import time  # sleep before exit
import binascii  # hex encoding
from uuid import uuid4  # gen random guid
import platform  # check platform
import subprocess  # needed for mac device


gradient_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

for i in range(len(gradient_colors) * 2):
    def animate_gradient():
        print(Fore.BLUE + Style.BRIGHT + '''\n█▀█ ▄▀█ █▀▀ ▀█▀ ▄▀█ █▀█   █▄▄ █▀█ █▀█ █▀ ▀█▀   ▀█▀ █▀█ █▀█ █░░
█▀▄ █▀█ █▀░ ░█░ █▀█ █▀▄   █▄█ █▄█ █▄█ ▄█ ░█░   ░█░ █▄█ █▄█ █▄▄
''')
        print(Fore.CYAN + Style.BRIGHT + '''             THANKS FOR USING : ) | discord.gg/raftar | discord.gg/govt
                                                         Please Don't Skid/Rebrand/Resell This Boost Tool Othervise Hell is Ready for You''')
        time.sleep(0.1)


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")

def create_file_if_not_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('')
        print(f"File '{file_path}' created.")

def setup_folders_and_files():
    output_folder_path = 'output'
    create_folder_if_not_exists(output_folder_path)
    success_file_path = os.path.join(output_folder_path, 'success.txt')
    create_file_if_not_exists(success_file_path)
    failed_boosts_file_path = os.path.join(output_folder_path, 'failed_boosts.txt')
    create_file_if_not_exists(failed_boosts_file_path)    
    data_folder_path = 'data'
    create_folder_if_not_exists(data_folder_path)    
    one_million_file_path = os.path.join(data_folder_path, '1m.txt')
    create_file_if_not_exists(one_million_file_path)
    three_month = os.path.join(data_folder_path, '3m.txt')
    create_file_if_not_exists(three_month)
    proxies_path = os.path.join(data_folder_path, '3m.txt')
    create_file_if_not_exists(proxies_path)

setup_folders_and_files()
useragent = "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/85.8.5 (KHTML, like Gecko) Safari/85"
class Fore:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
log_format = f'{Fore.BLUE}%(levelname)s{Style.RESET_ALL} %(asctime)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format, datefmt='%H:%M')

logging.addLevelName(logging.INFO, f'{Fore.BLACK}INF{Style.RESET_ALL}')
logging.addLevelName(logging.ERROR, f'{Fore.RED}ERR{Style.RESET_ALL}')
logging.addLevelName(logging.WARNING, f'{Fore.YELLOW}WARNING{Style.RESET_ALL}')

config = json.load(open("config/config.json", encoding="utf-8"))

hcoptcha_key = config['captcha_solver']['hcoptcha_api_key']

def getProxy():
      if config['proxyless'] != True:  
        try:
            proxy = random.choice(open("data/proxies.txt", "r").read().splitlines())
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        except Exception as e:
            if config['advance_mode'] == True:
                print(f"Exception while using proxies: {e}")

            return None
      else:
          return None  
api_key = config['captcha_solver']['hcoptcha_api_key']
cs_api_key = config['captcha_solver']['capsolver_api_key']
def h_captcha(sitekey, url, rqdata):
    p1 = {
	"task_type": "hcaptchaEnterprise",
	"api_key": f"{api_key}",
	"data": {
		"sitekey": sitekey,
		"url": url,
		"rqdata": rqdata ,
        "proxy": "YdKBIYOpPMSQhkJu:PokzwSEX82mi2hLk_country-gb@geo.iproyal.com:12321"
	}
    }
    h1 = {"Content-Type": "application/json"}

    r1 = requests.post("https://api.hcoptcha.online/api/createTask", headers=h1, json=p1)
    if r1.json()['error'] != True:
        try:    
            a = r1.json()['task_id']
            return a
        except:
            return False
    else:
        logging.error("Unable to create task")
        print(r1.json())       
        return False

def h_result(task_id):
    p2 = {
	"api_key": f"{api_key}",
	"task_id": task_id }
    h2 = {"Content-Type": "application/json"}
    r2 = requests.post("https://api.hcoptcha.com/api/getTaskData", headers=h2, json=p2)
    if 'captcha_key' in r2.text:
        try:    
            a = r2.json()
            return a
        except:
            return False
    else:
        if config['advance_mode']:
            logging.error(f"Unable to get solution : {r2.json()}")
        return False

def cs_captcha(sitekey, url, rqdata):
    p1 = {

	"clientKey": cs_api_key,
	"task": {
        	"type": "HCaptchaTaskProxyLess",
		"websiteKey": sitekey,
		"websiteURL": url,
		"enterprisePayload": {
      "rqdata": rqdata,
    },
	}
    }
    h1 = {"Content-Type": "application/json"}

    r1 = requests.post("https://api.capsolver.com/createTask", headers=h1, json=p1)
    if not r1.json()['errorId']:
        try:    
            a = r1.json()['taskId']
            return a
        except:
            return False
    else:
        logging.error("Unable to create task")
        if config['advance_mode'] == True:
            logging.error(f"Reason {r1.json()}")    
        return False

def cs_result(task_id):
    p2 = {
	"clientKey": cs_api_key,
	"taskId": task_id }
    h2 = {"Content-Type": "application/json"}
    r2 = requests.post("https://api.capsolver.com/getTaskResult", headers=h2, json=p2)
    if 'solution' in r2.text:
        try:    
            a = r2.json()
            return a
        except:
            a = r2.json()
            return False
            
    else:
        logging.error("Unable to solve captcha")
        if config['advance_mode'] == True:
            print(r2.json())       
        return False


            
class Booster:
    def __init__(self):
        self.client = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )
        self.proxy = getProxy()
        self.tokens = []
        self.proxies = []
        self.failed = []
        self.success = []
        self.captcha_solved = []
        self.captcha_unsolved = []
        self.failed_tokens = []
    

    def headers(self, token: str):
        headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjExMDQzNzg1NDMwNzg2Mzc1OTEiLCJsb2NhdGlvbl9jaGFubmVsX2lkIjoiMTEwNzI4NDk3MTkwMDYzMzIzMCIsImxvY2F0aW9uX2NoYW5uZWxfdHlwZSI6MH0=',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-GB',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6Iml0LUlUIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTEyLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE5MzkwNiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==',
        }
        return headers
    

    def get_cookies(self):
        cookies = {}
        try:
          response = self.client.get('https://discord.com')
          for cookie in response.cookies:
            if cookie.name.startswith('__') and cookie.name.endswith('uid'):
                cookies[cookie.name] = cookie.value
          return cookies
        
        except Exception as e:
          logging.info('Failed to obtain cookies ({})'.format(e))
          return cookies


    

    def boost(self, token, invite, guild):
        tkv = token[:-25] + "*" * 8
        headers = self.headers(token)

        
        try: 
            advanced_mode = config['advance_mode']
            proxy_info = False
            try:
                if self.proxy != None:
                    proxy_info = True
            except:
                proxy_info = False
            if advanced_mode == True:
                proxy_details = self.client.get(f"http://ip-api.com/json", proxy=self.proxy)
                uwu = proxy_details.json()
                print(f"{Fore.YELLOW}   {Style.RESET_ALL} Current Proxy Details: Country = {uwu['country']}, IP = {uwu['query']}, Using-Custom-Proxy = {proxy_info}")
        except Exception as e:
            pass
        payload = {
            'session_id': ''.join(random.choice(string.ascii_lowercase) + random.choice(string.digits) for _ in range(16))
        }
        r = self.client.post(
            url='https://discord.com/api/v9/invites/{}'.format(invite),
             headers=self.headers(token=token),
             json=payload,
             cookies=self.get_cookies(),
             proxy=self.proxy
        )
        join_outcome = False
        max_retries = None
        solve_captcha = None
        tr = 1
        tr0 = 1
        try:
            solve_captcha = config['captcha_solver']['solve_captcha']
        except:
            solve_captcha = False    
        try:
            max_retries = config['captcha_solver']['max_retries']

        except:
            max_retries = 2
        cap_service = None
        try:
            if config['captcha_solver']['use'] == "hcoptcha":
                cap_service = 1
            elif config['captcha_solver']['use'] == "capsolver":
                cap_service = 2
            else:
                cap_service = 1
        except:
            logging.error("Captcha service can be either hcoptcha or capsolver please update it in config file!")

        if "captcha" in r.text:
            logging.error(f"Captcha Detected : {tkv}")
            if config['captcha_solver']['solve_captcha'] == True:
              retry = 0
              while join_outcome != True and retry < max_retries and cap_service != None:
                r = self.client.post(
            url='https://discord.com/api/v9/invites/{}'.format(invite),
             headers=self.headers(token=token),
             json=payload,
             cookies=self.get_cookies(),
             proxy=self.proxy
        )
                response = r.json()
                if cap_service == 1:
                    s1 = h_captcha(response['captcha_sitekey'], f"https://discord.com/invite/{invite}", response['captcha_rqdata'])
                else:
                    s1 = cs_captcha(response['captcha_sitekey'], f"https://discord.com/invite/{invite}", response['captcha_rqdata'])
                task_id = s1
                logging.info(f"Solving Captcha : {tkv}")
                time.sleep(10)
                if cap_service == 1:
                    s2 = h_result(task_id)
                else:
                    s2 = cs_result(task_id)
                s3 = None
                try:
                    if cap_service == 1:
                        s3 = s2['task']['captcha_key']
                    else:
                        s3 = s2['solution']['gRecaptchaResponse']
                except:
                    pass
                req2headers = self.headers(token)
                req2headers.pop("Content-Length", None)
                try: 
                    req2headers["X-Captcha-Key"] = s3 
                    req2headers["X-Captcha-Rqtoken"] = response['captcha_rqtoken']
                except:
                    pass
                response = self.client.post(url='https://discord.com/api/v9/invites/{}'.format(invite),
             headers=req2headers,
             json=payload,
             cookies=self.get_cookies(),
             proxy=self.proxy)
                print(response.text)
                if response.status_code in [200, 204]:
                    join_outcome = True
                    print(Fore.BLUE + f"Joined Server Succesfully : {tkv}")
                   
                else:
                    if "10008" in response.text:
                        logging.error(f"Token Flagged [ Unable To Join Even After A Valid Captcha Solution ]: {tkv}")
                        break
                    retry += 1
                    logging.info(f"Retrying Solving Captcha : {tkv} [ {retry}/{max_retries} ]")

              if join_outcome != True:
                  self.captcha_unsolved.append(token)
                  with open ("output/unsolved_cap.txt" , "a") as f:
                      f.write(token+ "\n")
                      
        
        if not "captcha" in r.text:
            tkv = token[:-25] + "*" * 8
            logging.info(colorama.Fore.LIGHTBLUE_EX + f"Successfully Joined Server {tkv}")

            
    def thread(self, invite, tokens, guild):
        """"""
        threads = []

        for i in range(len(tokens)):
            token = tokens[i]
            t = threading.Thread(target=self.boost, args=(token, invite, guild))
            t.daemon = True
            threads.append(t)

        for i in range(len(tokens)):
            threads[i].start()

        for i in range(len(tokens)):
            threads[i].join()

        return {
            "success": self.success,
            "failed": self.failed,
            "captcha_solved": self.captcha_solved,
            "captcha_unsolved":self.captcha_unsolved
        }
    def boost_server(self,token, guild):
                tkv = token[:-25] + "*" * 8
                
                
                headers=self.headers(token)
                
                slots = httpx.get(
            "https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots",
            headers=headers,
        )

                slot_json = slots.json()
                if slots.status_code == 401:
                    self.failed_tokens.append(token)
                    logging.error(f"Invalid/Flagged/No-Nitro : {tkv}")
                with open("output/failed_boosts.txt", "a") as file:
                    file.write(token + "\n")              
                    boostsList = []
                    for boost in slot_json:
                        boostsList.append(boost["id"])

                    payload = {"user_premium_guild_subscription_slot_ids": boostsList}

                    headers["method"] = "PUT"
                    headers["path"] = f"/api/v9/guilds/{guild}/premium/subscriptions"

                    boosted = self.client.put(
                        f"https://discord.com/api/v9/guilds/{guild}/premium/subscriptions",
                        json=payload,
                        headers=headers, proxy=self.proxy, cookies=self.get_cookies()
                    )

                    if boosted.status_code == 201:
                        self.success.append(token)
                        with open("output/success.txt", "a") as file:
                            file.write(token + "\n")
                        logging.info(colorama.Fore.LIGHTGREEN_EX + f"Boosted Successfully : {tkv}")
                        return True
                    else:
                        with open("output/failed_boosts.txt", "a") as file:
                            file.write(token + "\n")
                            self.failed.append(token)
                            logging.error(f"Boosts Failed : {tkv}")
    def boost_thread(self, tokens, guild):
        """"""
        threads = []

        for i in range(len(tokens)):
            token = tokens[i]
            t = threading.Thread(target=self.boost_server, args=(token, guild))
            t.daemon = True
            threads.append(t)

        for i in range(len(tokens)):
            threads[i].start()

        for i in range(len(tokens)):
            threads[i].join()

        return {
            "success": self.success,
            "failed": self.failed,
            "captcha_solved": self.captcha_solved,
            "captcha_unsolved":self.captcha_unsolved
        }
    def nickbio(self, token, guild, nick, bio):
        tkv = token[:-25] + "*" * 8
        headers = self.headers(token)

        payload = {"global_name": nick, 'session_id': ''.join(random.choice(string.ascii_lowercase) + random.choice(string.digits) for _ in range(16))}
        try:
            nick_r = self.client.patch(
            f"https://discord.com/api/v9/users/@me",
            headers=headers,
            json=payload, cookies=self.get_cookies()
        )
            if int(nick_r.status_code) < 250:
                logging.info(f"Nickname Changed Successfully : {tkv}")
            else:
                logging.info(colorama.Fore.LIGHTRED_EX + f"Unable to change Nickname {tkv}")
        except:
            logging.error(f"Unable to change nickname : {tkv}")    

        try:
            bio_r = httpx.patch(
            f"https://discord.com/api/v9/users/@me/profile",
            headers=headers,
            json={"bio": bio}, cookies=self.get_cookies()
        )
            if int(bio_r.status_code) < 250:
                logging.info(colorama.Fore.LIGHTYELLOW_EX + f"Bio Changed Succesfully : {tkv}")
            else:
                logging.warning(f"Can't Change Bio : {tkv}")
        except:
            logging.error(f"Unable to change bio : {tkv}")    

    def nickbioThread(self, tokens, guild, nick, bio):
        """"""
        threads = []

        for i in range(len(tokens)):
            token = tokens[i]
            t = threading.Thread(target=self.nickbio, args=(token, guild, nick, bio))
            t.daemon = True
            threads.append(t)

        for i in range(len(tokens)):
            threads[i].start()

        for i in range(len(tokens)):
            threads[i].join()

        return True

def getStockk(filename: str):
    tokens = []
    count = 0
    for i in open(filename, "r").read().splitlines():
        if ":" in i:
            i = i.split(":")[2]
            tokens.append(i)
        else:
            tokens.append(i)
        count += 1
    if not len(tokens) < 10:
        ee = input(Fore.RED + "Error: No Tokens Found In Stock Press e To Exit.")
        if ee == "e":
            exit()

    print(Fore.BLUE + f"Succesfully Loaded {count} Tokens")
    return tokens

def getStock(filename: str):
    tokens = []
    count = 0
    for i in open(filename, "r").read().splitlines():
        if ":" in i:
            i = i.split(":")[2]
            tokens.append(i)
        else:
            tokens.append(i)
        count += 1
    if not len(tokens) < 10:
        ee = input(Fore.RED + "Error: No Tokens Found In Stock Press e To Exit.")
        if ee == "e":
            exit()

    return tokens

def getinviteCode(inv):
    if "discord.gg" in inv:
        invite = inv.split("discord.gg/")[1]
        return invite
    if "https://discord.gg" in inv:
        invite = inv.split("https://discord.gg/")[1]
        return invite
    if 'discord.com/invite' in inv:
        invite = inv.split("discord.com/invite/")[1]
        return invite
    if 'https://discord.com/invite/' in inv:
        invite = inv.split("https://discord.com/invite/")[1]
        return invite
    else:
        return inv

def checkInvite(invite: str):
    data = requests.get(
        f"https://discord.com/api/v9/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true"
    ).json()

    if data["code"] == 10006:
        return False
    elif data:
        return data["guild"]["id"]
    else:
        return False

booster = Booster()

def remove(token: str, filename: str):
    tokens = getStock(filename)
    tokens.pop(tokens.index(token))
    f = open(filename, "w")

    for x in tokens:
        f.write(f"{x}\n")

    f.close()
def stylish_input(prompt, required=True, numeric=False, max_length=None, options=None):

    print(f'{Fore.CYAN} {Style.RESET_ALL} {prompt}{Fore.CYAN}{Fore.GREEN}{Fore.UNDERLINE}{Style.RESET_ALL} {Fore.CYAN}', end='')

    user_input = input()

    while required and not user_input.strip():
        print(f'''{Fore.RED}Input Can't be Empty! Please Provide Valid Info{Style.RESET_ALL}''')
        print(f'{Fore.CYAN} {Style.RESET_ALL} {prompt}{Fore.CYAN}: {Style.RESET_ALL}', end='')
        user_input = input()

    while numeric and not user_input.isdigit():
        print(f"{Fore.RED}Error: Input must be a valid number.{Style.RESET_ALL}")
        print(f'{Fore.CYAN} {Style.RESET_ALL} {prompt}{Fore.CYAN}: {Style.RESET_ALL}', end='')
        user_input = input()

    if max_length is not None and len(user_input) > max_length:
        print(f"{Fore.RED}Error: Input cannot exceed {max_length} characters.{Style.RESET_ALL}")
        print(f'{Fore.CYAN} {Style.RESET_ALL} {prompt}{Fore.CYAN}: {Style.RESET_ALL}', end='')
        user_input = input()

    if options is not None and user_input not in options:
        print(f"{Fore.RED}Error: Input must be one of the following options: {', '.join(options)}.{Style.RESET_ALL}")
        print(f'{Fore.CYAN} {Style.RESET_ALL} {prompt}{Fore.CYAN}: {Style.RESET_ALL}', end='')
        user_input = input()

    return user_input


class Status(Enum):
    ONLINE = "online"
    DND = "dnd"
    IDLE = "idle"

class Activity(Enum):
    GAME = 0  
    STREAMING = 1 
    LISTENING = 2 
    WATCHING = 3 
    CUSTOM = 4 
    COMPETING = 5  

class OPCodes(Enum):
    Dispatch = 0  
    Heartbeat = 1
    Identify = 2  
    PresenceUpdate = 3  
    VoiceStateUpdate = 4  
    Resume = 6  
    Reconnect = 7  
    RequestGuildMembers = (
        8  
    )
    InvalidSession = 9 
    Hello = (
        10 
    )
    HeartbeatACK = 11 

class DiscordIntents(IntEnum):
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_MODERATION = 1 << 2
    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14
    MESSAGE_CONTENT = 1 << 15
    GUILD_SCHEDULED_EVENTS = 1 << 16
    AUTO_MODERATION_CONFIGURATION = 1 << 20
    AUTO_MODERATION_EXECUTION = 1 << 21

class Presence:
    def __init__(self, online_status: Status) -> None:
        self.online_status: Status = online_status
        self.activities: List[Activity] = []

    def addActivity(
        self, name: str, activity_type: Activity, url: Optional[str]
    ) -> int:
        self.activities.append(
            {
                "name": name,
                "type": activity_type.value,
                "url": url if activity_type == Activity.STREAMING else None,
            }
        )
        return len(self.activities) - 1

    def removeActivity(self, index: int) -> bool:

        if index < 0 or index >= len(self.activities):
            return False
        self.activities.pop(index)
        return True

class DiscordWebSocket:
    def __init__(self) -> None:
        try:
            self.websocket_instance = connect(
            "wss://gateway.discord.gg/?v=10&encoding=json", proxy=random.choice(open("data/proxies.txt", "r").read().splitlines())
        )
        except:
            self.websocket_instance = connect(
            "wss://gateway.discord.gg/?v=10&encoding=json"
        )

        self.heartbeat_counter = 0

        self.username: str = None
        self.required_action: str = None
        self.heartbeat_interval: int = None
        self.last_heartbeat: float = None

    def get_heatbeat_interval(self) -> None:
        resp: Dict = json.loads(self.websocket_instance.recv())
        self.heartbeat_interval = resp["d"]["heartbeat_interval"]

    def authenticate(self, token: str, rich: Presence) -> Union[Dict, bool]:
        self.websocket_instance.send(
            json.dumps(
                {
                    "op": OPCodes.Identify.value, 
                    "d": {
                        "token": token, 
                        "intents": DiscordIntents.GUILD_MESSAGES
                        | DiscordIntents.GUILDS,  
                        "properties": {
                            "os": "linux",
                            "browser": "Brave", 
                            "device": "Desktop", 
                        },
                        "presence": {
                            "activities": [
                                activity for activity in rich.activities
                            ],
                            "status": rich.online_status.value, 
                            "since": time.time(), 
                            "afk": False, 
                        },
                    },
                }
            )
        )
        try:
            resp = json.loads(self.websocket_instance.recv())
            self.username: str = resp["d"]["user"]["username"]
            self.required_action = resp["d"].get("required_action")
            self.heartbeat_counter += 1
            self.last_heartbeat = time.time()

            return resp
        except ConnectionClosedError:
            return False

    def send_heartbeat(self) -> websockets.typing.Data:
        self.websocket_instance.send(
            json.dumps(
                {"op": OPCodes.Heartbeat.value, "d": None}
            ) 
        )

        self.heartbeat_counter += 1
        self.last_heartbeat = time.time()

        resp = self.websocket_instance.recv()
        return resp
def main(token: str, activity: Presence):
    socket = DiscordWebSocket()
    socket.get_heatbeat_interval()

    auth_resp = socket.authenticate(token, activity)
    if not auth_resp:
        return
    while True:
        try:
            if (
                time.time() - socket.last_heartbeat
                >= (socket.heartbeat_interval / 1000) - 5
            ): 
                resp = socket.send_heartbeat()
            time.sleep(0.5)
        except IndentationError:
            print(resp)





try:
    main = True
    while main == True:
        try:
            
            animate_gradient()
            i = stylish_input(Fore.BLUE + "\n\nInvite Link = ", max_length=40)
            i1= getinviteCode(i)
            check_i = checkInvite(i1)
        except:
            print(f"{Fore.RED} Error: Something went wrong while fetching invite link please try using a vpn! [ Your ip is blocked from accessing discord api ]")
            break

        if check_i == False:
            print(f"{Fore.RED}Error: Please make sure to provide a valid invite link!{Style.RESET_ALL}")
            break
        try:
            nick = None
            bio = None
            if len(config['customisation']['bio']) < 2:
                nick = stylish_input("Enter Nickname:", required=False, max_length=18)
                bio = stylish_input("Enter Bio:", required=False, max_length=120)
            else:
                logging.info("Using Config Data (Bio/Nick).")
                nick = config['customisation']['nick']
                bio = config['customisation']['bio']
        except:
            nick = stylish_input(Fore.GREEN + "Enter Nickname :", required=False, max_length=18)
            bio = stylish_input(Fore.GREEN + "Enter Bio:", required=False, max_length=120)
        amount = stylish_input(Fore.GREEN + "Enter amount To Boost:", numeric=True, max_length=3)
        months = stylish_input(Fore.GREEN + "Enter months 1/3:", required=True, numeric=True, max_length=2, options=["1","3"])
        requiredStock = int(amount)/2
        if int(amount)% 2 != 0:
            print(f"{Fore.RED}Amount should be a even number{Style.RESET_ALL}")
            break

        invite_link = getinviteCode(i)
        try:
            months = int(months)
        except:
            print(f"{Fore.RED}Months should be a valid int not a string{Style.RESET_ALL}")
            break

        if months == 1:
                filename = "data/1m.txt"
        if months == 3:
                filename = "data/3m.txt"
        guild_id = checkInvite(invite_link)
        tokens = []
        try:
            tokensStock = getStockk(filename)
        except:
            print(f"{Fore.RED}Months should be a valid int not a string{Style.RESET_ALL}")
            break

        try:
            for x in range(int(requiredStock)):
                tokens.append(tokensStock[x])
                remove(tokensStock[x], filename)
        
        except:
            print(f"{Fore.RED + Style.BRIGHT}Error! You Don't Have Token Stock{Style.RESET_ALL}")
            break
        start = time.time()        
        status = booster.thread(invite_link, tokens, guild_id)
        success_tokens = tokens
        boosts = booster.boost_thread(success_tokens, guild_id)
        nickbio = booster.nickbioThread(success_tokens, guild_id, nick, bio)


        time_taken = round(time.time() - start, 2)      
        input(f"\n{colorama.Fore.LIGHTBLUE_EX}Successful-Tokens : {len(status['success'])} - {colorama.Fore.LIGHTRED_EX}Failed-Tokens : {len(status['failed'])} - {colorama.Fore.LIGHTGREEN_EX}Captcha-Solved : {len(status['captcha_solved'])} - {colorama.Fore.LIGHTMAGENTA_EX}Captcha-Unsolved : {len(status['captcha_unsolved'])} - {Fore.UNDERLINE}{Fore.CYAN}Time-Taken : {time_taken}{Style.RESET_ALL} \n")
        os.system('cls')

        n = input(f"{Fore.BLUE}  {Fore.WHITE}Press : \n a -> Continue \n b -> Exit \n {Fore.YELLOW} {Style.RESET_ALL} Choose :  {Style.RESET_ALL}")
        if n == "b":
            print(f"{Fore.RED}{Fore.GREEN}Closing The Window In 3 Seconds!{Style.RESET_ALL}")
            time.sleep(3)
            sys.exit()
        else:
            main=True 
        os.system('cls')
except Exception as e:
    logging.error(f"Ahh! You Don't Have Stock in data")
    if config['advance_mode'] == True:
        print(f"Error: {e}")
        time.sleep(10)
        sys.exit()

ex = stylish_input(Fore.CYAN + "Press e To Exit...")
if ex == "e":
    exit()
