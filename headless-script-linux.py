#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
import sys
from cookies5 import cookies
import time
from time import gmtime, strftime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import clipboard
import boto3
from pymongo import MongoClient
import csv
import urllib.request
import keyboard
import random
import string
import re
import os
import datetime
import subprocess
options = Options()
options.headless = True
starttime=time.time()
# streamer_name = "domingo"
streamer_name = "shroud"
streamer_link = "https://www.twitch.tv/" + streamer_name
 # Ouvre le navigateur Firefox et navigue sur la page
driver = webdriver.Firefox(options=options)
driver.get(streamer_link)
driver.implicitly_wait(15)
# ajoute les cookies de cookies4.py que j'ai telecharge via cookie manager et dont j'ai supprime les cookies expire 
#ainsi que les identifiants uniques ( et tout ce qui n'ai pas statiques entre les idfferents imports)
for cookie in cookies:
	driver.add_cookie(cookie)
print("cookies sucessfully added")
driver.refresh()
# si un capatch apparait, il faut rajouter du temps au time.sleep juste en dessous pour pouvoir ecrire manuellement l id et le mot de passe  et donc mettre en commentaire
# les lignes de id = ... a login.click()
time.sleep(15)
try:
	id = driver.find_element_by_id('username')
	mdp = driver.find_element_by_name('password')
	login = driver.find_element_by_class_name('js-login-text')
	id.send_keys("thimothe")
	mdp.send_keys("tiganala18")
	login.click()
	print("successfully logged")
except:
	print("login not working")
time.sleep(7)
driver.get(streamer_link)
# les cookies n'identifient pas directement mais permettent d'utiliser send_keys pour se log grace a selenium sans avoir a valider le captcha
time.sleep(3)
# driver.find_element_by_class_name('pl-settings-icon').click()
# time.sleep(3)
# driver.find_element_by_class_name('qa-quality-button').click()
# time.sleep(3)
# driver.find_elements_by_class_name('pl-quality-option-button')[5].click()
# breakpoint = 1
try:
	mature_btn = driver.find_element_by_id('mature-link')
	mature_btn.click()
except:
	print("mature audiance btn not found")
delai_time = 1800 + 1 
while True: 
	if time.time() - delai_time > 1800:
		counter_moyenne = 0
		addition_msg = 0
		while counter_moyenne < 10:
			time.sleep(6)
			delai_time = time.time()
			titre = driver.find_elements_by_class_name('chat-line__message')
			num_page_items = len(titre)
			counter_moyenne += 1
			addition_msg += num_page_items
			breakpoint = addition_msg/counter_moyenne
			print("Nombre de msg : ")
			print(num_page_items)
			print("Compteur : ")
			print(counter_moyenne)
			print("message additionné : ")
			print(addition_msg)
			print("resultat de la divi: ")
			print(breakpoint)
			driver.refresh()
			time.sleep(30.0 - ((time.time() - starttime) % 30.0))
	else : 
		print("ca fais moins d'une heure")
	print(breakpoint)
	titre = driver.find_elements_by_class_name('chat-line__message')
	num_page_items = len(titre)
	window_before = driver.window_handles[0]
	#ecrire ici if chat in sub only then breakpoint * 1.7 OU /2 etc...
	#if in slow mode do breakpoint*1.4
	print("breakpoint : ")
	print(breakpoint*2)
		
	if num_page_items > breakpoint*2:
		clip_time = time.time()
		timestampp = clip_time*1000
		timestamp = round(timestampp)
		realtimestamp = str(timestamp)

		try: 
			elapsed = clip_time - cliplast_time
			print("temps elapsed : ")
			print(elapsed)
			# 350 represente 30s * 12 donc 12 clips non selectionne --> si il y a 12 clips ou plus non selectionne entre chaque clip selectionne alors diminue le breakpoint
			if elapsed > 350:
				breakpoint = breakpoint - 1
			# 70 represente 30s * 2 donc si il y a que 2 clips ou moins  non slectionne entre chaque clip selectionne alors augmente le breakpoint
			if elapsed < 70:
				breakpoint = breakpoint + 1
			# Pour que ca augmente en fonction du temps sans clip et que ca soit plus precis que juste au desssus de x ou en dessous de y
			# if(grade >= 90):
				# print(“You’re doing great!”)
			# elif(grade <= 89 and >= 78):
				# print(“You’re doing good!”)
			# elif(grade >65 and <= 77)
				# print("You need some work")
			# else:
				# print("Contact your teacher")
		except:
			print("Calcul du délai entre le clip précédent et celui-ci échoué")
		current_date = strftime("%A %d %B", gmtime())
		current_time = strftime("%I:%M%p", gmtime())
		nb_viewers = driver.find_element_by_class_name('tw-stat__value')
		viewers_string = nb_viewers.text
		tri = repr(nb_viewers.text)
		brut_text = re.split(r"\s", tri)
		streamer_Titre = driver.find_element_by_css_selector('h2')
		streamer_Title = streamer_Titre.get_attribute('innerHTML')
		streamer_jeu = driver.find_element_by_css_selector('#root > div > div.tw-flex.tw-flex-column.tw-flex-nowrap.tw-full-height > div > main > div.root-scrollable.scrollable-area.scrollable-area--suppress-scroll-x > div.simplebar-scroll-content > div > div > div.channel-root.tw-full-height > div.channel-root__player-container.tw-pd-b-2 > div > div.channel-info-bar.tw-border-b.tw-border-bottom-left-radius-large.tw-border-bottom-right-radius-large.tw-border-l.tw-border-r.tw-border-t.tw-flex.tw-flex-wrap.tw-justify-content-between.tw-lg-pd-b-0.tw-lg-pd-t-1.tw-lg-pd-x-1.tw-pd-1 > div > div > div > div.channel-info-bar__content-right.tw-full-width > div:nth-child(2) > div > p > a')
		streamer_game = streamer_jeu.get_attribute('innerHTML')
		truestreamer_game = streamer_game.lower()
		realstreamergame = truestreamer_game.replace(" ", "_")
		time.sleep(4)
		try:
			driver.find_element_by_css_selector('.pl-clips-button').click()
		except:
			driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[5]/div/div[2]/div[2]/div[2]/div/div/button').click()

		print("Successfully clicked on clip button")
		time.sleep(30)
		driver.implicitly_wait(250)
		window_after = driver.window_handles[1]
		driver.switch_to_window(window_after)
		video = driver.find_element_by_class_name('player-video')
		cheval = video.get_attribute('innerHTML')
		print(cheval)

		css = driver.find_element_by_css_selector('.player-video > video:nth-child(1)')
		poney = css.get_attribute('innerHTML')
		outer = css.get_attribute('outerHTML')
		oui = css.get_attribute('src')
		print(poney)
		print(css)
		print(oui)
		print(outer)
		time.sleep(13)
		# oui = text[84:160]
		print("Lien de la video : ")
		print(oui)
		url = oui
		print("texte brut : ")
		print(brut_text)
		final_string = viewers_string.replace('\u202f', '')
		print("Nombre brut converti : ")
		print(final_string)
		print("Nombre de messages en 30 secondes qui a engendre la creation du clip :")
		print("nombre de messages enregistrer : ")
		print(num_page_items)
		vrainumpage = float(num_page_items)
		vrainbviewers = float(final_string)
		calcul = vrainumpage/vrainbviewers
		with open("test.csv", "a", newline='\n') as fp:
			a = csv.writer(fp)
			row = [streamer_link] + [final_string] + [num_page_items] + [url] + [current_time] + [calcul] + [breakpoint]
			a.writerow(row)
			print("Enregestrement du csv dans test.csv avec succès")
			#repr permet de ne pas avoir l'erreur "codec cant encode character"	
		print("DONE")
		# oui = text[84:160]
		print("lien de la video : ")
		print(oui)
		url = oui
		# name1 = input("Enter the name for the video\n")
		def randomString(stringLength=10):
			"""Generate a random string of fixed length """
			letters = string.ascii_lowercase
			return ''.join(random.choice(letters) for i in range(stringLength))
		str_end = randomString(5)
		name1 = "test" + str_end
		print(name1)
		print(str_end)
		name = name1 + ".mp4"
		try:
			print("Downloading starts...\n")
			urllib.request.urlretrieve(oui, name)
			print("Download completed..!!")
		except Exception as e:
			print(e)
				
		# aws s3 configure
		# les deux keys la region 3 et json 
		#aws s3 ls
		s3 = boto3.client('s3')
		source = "source"
		date = "date"
		filename = name
		bucket_name = 'compartiment-thimothe'
		nom = "name"
			
		# Uploads the given file using a managed uploader, which will split up large
		# files automatically and upload parts in parallel.
		s3.upload_file(filename, bucket_name, filename)
		client = MongoClient('mongodb+srv://cheval:Tiganala18@test-y9xs2.gcp.mongodb.net/test?retryWrites=true')
		db = client.test
		collection = db.items
		collection.create_index("date", expireAfterSeconds=604800)
		
		object = { 
		source: "https://s3.eu-west-3.amazonaws.com/compartiment-thimothe/" + name1 + ".mp4",
		date: datetime.datetime.utcnow(),
		nom: streamer_name,
		"title": streamer_Title,
		"game": streamer_game,
		"trimmed-game": realstreamergame,
		"date": current_date,
		"time": current_time,
		"timestamp": realtimestamp,
		"message": calcul

		} 
		collection.insert_one(object)
		print("Successfully sent to MongoDB and AWS")
		driver.close()
		driver.switch_to_window(window_before)
		driver.get(streamer_link)
		os.remove(name1 + ".mp4")
	try:
		cliplast_time = clip_time
	except:
		print("logique, y'a pas eu de clip")
	print("nombres de pages enregistrer a la fin du script : ")
	print(num_page_items)
	driver.refresh()
	time.sleep(30.0 - ((time.time() - starttime) % 30.0))	
	driver.implicitly_wait(10)