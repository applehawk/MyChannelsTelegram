from pprint import pprint
from telethon import TelegramClient
from telethon import utils
from telethon.utils import get_display_name
import sys
import argparse

def sprint(string, *args, **kwargs):
    """Safe Print (handle UnicodeEncodeErrors on some terminals)"""
    try:
        print(string, *args, **kwargs)
    except UnicodeEncodeError:
        string = string.encode('utf-8', errors='ignore')\
                       .decode('ascii', errors='ignore')
        print(string, *args, **kwargs)

def filter_dialogs_by_type(dialogs, type_name):
  return list(filter(lambda d: type(d.entity).__name__ == type_name, dialogs))

def print_dialogs(dialogs, title):
  print_title(title)
  print_entities(dialogs)
def print_filtered_dialogs(dialogs, type_name, title):  
  print_dialogs( filter_dialogs_by_type(dialogs, type_name), title ) 

def print_title(title):
    """Helper function to print titles to the console more nicely"""
    sprint('\n')
    sprint('=={}=='.format('=' * len(title)))
    sprint('= {} ='.format(title))
    sprint('=={}=='.format('=' * len(title)))

def print_entities(entities):
  for i, d in enumerate(entities):
    megagroup_suffix = ""
    if type(d.entity).__name__ == 'Channel' and d.entity.megagroup:
      megagroup_suffix = "megagroup={}".format(d.entity.megagroup)
    sprint('{}. {}. {} {}'.format(i, utils.get_display_name(d.entity), d.entity.username, megagroup_suffix))

def connectTelegramClient():
  #how to fetch ApiID and ApiHASH
  #http://telethon.readthedocs.io/en/latest/extra/basic/creating-a-client.html
  api_id = 123123
  api_hash = "0123456789abcdef0123456789abcdef"
  client = TelegramClient('session_id', api_id, api_hash)
  client.connect()
  if not client.is_user_authorized():
    client.send_code_request('+11122224333')
    client.sign_in('+11122224333', input('Enter code:'))
  return client

def argumentsParse():
  parser = argparse.ArgumentParser(description='Fetch Telegram channels and get info about channel.')
  parser.add_argument("-o", "--output", type=str, help="filename for output")
  parser.add_argument("-ch", "--channel", type=str, help="channel name with @ or chatUrl/channelUrl")
  parser.add_argument("-lmt", "--limit", type=int, help="limit dialogs in fetching")
  return parser.parse_args()

def main():
  arguments = argumentsParse()
  print(arguments)
  #made connect to Telegram Client
  client = connectTelegramClient()
  #parse arguments in console
  if arguments.output:
    sys.stdout = open(arguments.output, 'w')
  #with open("MyChannels.txt", "w") as text_file:
  if arguments.limit:
    dialogs = client.get_dialogs(limit=arguments.limit)
  else:
    dialogs = client.get_dialogs(limit=50)
    
  channels = list(filter(lambda d: type(d.entity).__name__ == 'Channel' and d.entity.broadcast == True, dialogs))
  chats = list(filter(lambda d: type(d.entity).__name__ == 'Channel' and type(d.entity.photo).__name__ == 'ChatPhoto' and d.entity.broadcast == False, dialogs))
  creator = list(filter(lambda d: type(d.entity).__name__ == 'Channel' and d.entity.creator == True, dialogs))
  bots = list(filter(lambda d: type(d.entity).__name__ == 'User' and d.entity.bot == True, dialogs))
  users = list(filter(lambda d: type(d.entity).__name__ == 'User' and d.entity.bot == False, dialogs))

  print_dialogs(chats, "Chats")
  print_dialogs(channels, "Channels")
  print_dialogs(creator, "Creator")
  print_dialogs(bots, "Bots")
  print_dialogs(users, "Users")
#filtered = list(filter(lambda d: type(d.entity).__name__ == type_name && d.entity, dialogs))
  
# `print_filtered_dialogs(dialogs, 'Channel', "Channels")
#  print_filtered_dialogs(dialogs, 'User', "Users")

if __name__ == '__main__':
  main()

