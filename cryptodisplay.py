#!/usr/bin/env python
# -*- coding: utf-8 -*-



# Author Tom Fyuri.
# Pillaged by aybase ~07-2016 for use with Raspberry PI using 2.8" TFT display
# Simple bitcoin usd ticker (btc-e), you're free to modify or share following code however you like.
# Version 0.0.6.

import threading
import pygame
import httplib
import urllib
import json
import time
import sys, os
import copy
from pygame.locals import *

# setup some global stuff
pygame.init()
screen = pygame.display.set_mode((1280,720),pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
pygame.display.set_caption('BTC-e Live')
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
font = pygame.font.Font(None, 280)
font2 = pygame.font.Font(None, 280)
font3 = pygame.font.Font(None, 280)
update_time = 1500
tickrate = 50

class currency_data():
  pass

ticker_data = [["bitcoin","BTC",""," B",currency_data(),0],
               ["ethereum","ETH","","L",currency_data(),0],
               ["iota","IOTA","","L",currency_data(),0]]
               
def quit():
    pygame.quit(); sys.exit()

def get_price(which): # 
  try:
    conn = httplib.HTTPSConnection("api.coinmarketcap.com", timeout=4)
    conn.request("GET", "/v1/ticker/"+which+"/")
    response = conn.getresponse()
    j = json.load(response)
    conn.close()
    return j
  except StandardError:
    return None

def process_input():
  key = pygame.key.get_pressed()
  for event in pygame.event.get():
      if event.type == KEYDOWN:
          if event.key == K_ESCAPE: quit()
          
def update_data():
  # basic stuff
  for i in ticker_data:
    currency_name = i[0]
    i[5] = copy.deepcopy(i[4]) # save previous?
    pdata = i[5]
    data = i[4]
    data.name = i[1]
    data.nom = i[2]
    data.nom2 = i[3]
    json_data = get_price(currency_name)
    if json_data is None:
      data.error = True
    else:
      data.error = False
      data.last = str(round(float(json_data[0]['price_usd']),2)).rjust(8," ")

    if ((hasattr(data,'error')) and (hasattr(pdata,'error')) and (data.error == False) and (pdata.error == False)):
      if hasattr(data,'last_color'):
        data.last_color = pdata.last_color
      else:
    # WHITE originally 255, 255, 255  
        data.last_color = (242, 204, 133)
      if (data.last > pdata.last):
        # GREEN originally 0, 255, 0
        data.last_color = (49, 181, 49)
      elif (data.last < pdata.last):
    # RED   originally 255, 0, 0
        data.last_color = (209, 29, 29)

def redraw():
  surface.fill((0, 0, 0))
  pos = 0; pos2 = 0;
  for i in ticker_data:
    data = i[4]
    if data.error:
      text = font.render("ERROR", 1, (44, 96, 209))
        #x = ist abstand zu erstem wert
      text_pos = text.get_rect(); text_pos.y = pos; text_pos.x = 250
      surface.blit(text, text_pos)
    else:
      if (hasattr(data,'last_color')):
        color = data.last_color
      else:
        color = (242, 204, 133)
      text = font2.render("{0}{1}".format(data.last,data.nom), 1, color)

      text_pos = text.get_rect(); text_pos.y = pos2; text_pos.x = 400
      surface.blit(text, text_pos)

    # name
    text = font.render(data.name, 1, (44, 96, 209))
    text_pos = text.get_rect(); text_pos.y = pos; text_pos.x = 0
    surface.blit(text, text_pos)
  # zeilenabstand von den 3 zeilen
    pos+=200
    pos2+=200

  screen.blit(surface, (0, 0))
  pygame.display.flip()

def main():
  clock = pygame.time.Clock()
  update_delay = 0
  update_data()
  redraw()
  while True:
    process_input()
    update_delay = update_delay + tickrate
    if (update_delay >= update_time):
      update_delay = 0
      update_data()
    redraw()
    clock.tick(tickrate)

if __name__ == '__main__': main()




