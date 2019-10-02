#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import os
here = os.path.dirname(os.path.realpath(__file__))
import credentials as CR


token, chatID = CR.get_credentials(here+'/r4v3n.token')

def send_message(text, chatID=chatID, token=token, time=10):
   """
   Send a text to the telegram chat defined by chatID, using the bot defined
   by token.
   """
   url = f'https://api.telegram.org/bot{token}/sendMessage'
   com = f'curl -s --max-time {time} '
   com += f'-d "chat_id={chatID}&disable_web_page_preview=1&text={text}" {url}'
   resp = os.popen(com).read().strip()
   return json.loads(resp)


def send_picture(pic, text='', chatID=chatID, token=token,time=10):
   """
   Send a text to the telegram chat defined by chatID, using the bot defined
   by token.
   """
   url = f'https://api.telegram.org/bot{token}/sendPhoto'
   com = f'curl -s -X  POST {url}'
   com += f' -F chat_id={chatID} -F photo=@{pic} -F caption={text}'
   resp = os.popen(com).read().strip()
   return json.loads(resp)


def send_video(vid, text='', chatID=chatID, token=token,time=10):
   """
   Send a text to the telegram chat defined by chatID, using the bot defined
   by token.
   """
   url = f'https://api.telegram.org/bot{token}/sendVideo'
   com = f'curl -s -X  POST {url}'
   com += f' -F chat_id={chatID} -F video=@{vid} -F caption={text}'
   resp = os.popen(com).read().strip()
   return json.loads(resp)

def send_audio(audio, text='', chatID=chatID, token=token,time=10):
   """
   Send a text to the telegram chat defined by chatID, using the bot defined
   by token.
   """
   url = f'https://api.telegram.org/bot{token}/sendAudio'
   com = f'curl -s -X  POST {url}'
   com += f' -F chat_id={chatID} -F audio=@{audio} -F caption={text}'
   resp = os.popen(com).read().strip()
   return json.loads(resp)

def report(text='', pic='', audio='', vid='', chatID=chatID, token=token):
   """
   This function is a wrapper to use the appropriate function
   """
   if pic != '':
      return send_picture(pic=pic, text=text, chatID=chatID, token=token)
   elif vid != '':
      return send_video(vid=vid, text=text, chatID=chatID, token=token)
   elif audio != '':
      return send_audio(audio=audio, text=text, chatID=chatID, token=token)
   elif text != '':
      return send_message(text=text, chatID=chatID, token=token)

if __name__ == '__main__':
   M = report('testing',chatID=chatID,token=token)
   pic = '../nubes.png'
   #M = report('nubes',pic='../nubes.png',chatID=chatID,token=token)
   vid = '../Documents/RASP/PLOTS/w2/SC2/sfcwind.mp4'
   #M = report('nubes',pic=pic,vid=vid,chatID=chatID,token=token)
   audio = 'miserables1.mp3'
   #M = report('Miserables', audio=audio, chatID=chatID, token=token)
