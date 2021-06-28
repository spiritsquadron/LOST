from functions import *
from time import sleep
from random import randint, random, choice
from creatures import creatures
from items import buy

alive = True
items = []
health = 100
gems = 50
directions = ["north", "east", "south", "west"]
commands = ["shop", "quit"]
howmany = randint(5, 10)
battles_won = 0
won = False
seen_portal = False

print("You are lost in the middle of nowhere and need to get home.\nThe goal of this game is to find as many treasure chests as you can, buy items, and use those items to fight creatures. Once you are done, you will see a portal to get home. However, you must have at least 50 gems to use the portal.\n")
sleep(1)
print('Commands:\nType "shop" to buy items (you cannot buy items when you are fighting).\nType "quit" to end the game.\n')
sleep(1)
print("The final score is how many gems you have left.\n")
sleep(1)
start = input("Press Enter to start the game:")
status(health, gems, items)

while alive:
  print('Enter the direction you want to go (north, east, south, west), or type "shop" to buy items:')
  move = input(">").lower()
  while move not in directions and move not in commands:
    print("Invalid")
    move = input(">").lower()
  shop = False
  done = False
  if move == "shop":
    shop = True
    status(health, gems, items)
    print("Welcome to shop!")
    keys = list(buy.keys())
    while True:
      print('Here are some items you can buy (once you are done shopping, type "done"):')
      number = 0
      for i in keys:
        number += 1
        print("{}. {} for {} gems".format(number, i, buy[i]))
      print("What do you want to buy?")
      player = input(">").lower()
      if player == "done":
        done = True
      while validNum(player, buy) == False:
        print("Invalid")
        player = input(">").lower()
        if player == "done":
          done = True
          break
      if done == True:
        status(health, gems, items)
        break
      answers = itemDict(buy)
      bought_item = answers[player]
      needed_gems = list(bought_item.values())[0]
      if gems < needed_gems:
        print("You don't have enough gems!")
        continue
      gems -= needed_gems
      item = list(bought_item.keys())[0]
      items.append(item)
      status(health, gems, items)
      print("Success! You bought {} for {} gems.".format(item, needed_gems))
      sleep(1)

  elif move == "quit":
    break

  if random() < 0.5 and shop == False:
    status(health, gems, items)
    keys = list(creatures.keys())
    creature = choice(keys)
    print("You see a {}.\nWhat are you going to do?\n1. Fight it (and possibly earn more gems).\n2. Escape".format(creature))
    move = input(">").lower()
    answers = ["1", "2"]
    while move not in answers:
      print("Invalid")
      move = input(">").lower()
    if move == "1":
      dic = creatures[creature]
      damage = randint(dic["damage"][0], dic["damage"][1])
      if fight(dic, items):
        gems += damage
        battles_won += 1
        status(health, gems, items)
        print(dic["win text"])
        sleep(1)
        print("You earned {} gems!".format(damage))
        sleep(1)
      else:
        health -= damage
        status(health, gems, items)
        print(dic["lose text"])
        sleep(1)
        print("You lost {} health.".format(damage))
    else:
      status(health, gems, items)
  else:
    if shop == False:
      if random() < 0.2:
        gems_found = randint(5, 15)
        gems += gems_found
        status(health, gems, items)
        print("You found a treasure chest and got {} gems!".format(gems_found))
      else:
        print("This place is safe!")
  
  if gems >= 50:
    seen_portal = False

  if battles_won >= howmany and seen_portal == False:
    sleep(1)
    print("You see a portal...")
    sleep(1)
    if gems >= 50:
      print("You use the portal and got home!\nYou win!")
      won = True
      break
    else:
      seen_portal = True
      print("But you don't have enough gems! You need to have at least 25 gems. You will need to gain more gems by either fighting or finding treasure chests!")
      sleep(1)
  
  if health <= 0:
    print("You lost all your health...\nYou lose!")
    break

if won:
  sleep(1)
  print("Your final score was {}.".format(gems))
