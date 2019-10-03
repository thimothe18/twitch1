#!/usr/bin/python3

# -*- coding: utf-8 -*-

import selenium

from selenium import webdriver

import time

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.options import Options

import clipboard

import boto3

starttime=time.time()

client = boto3.client('ec2', region_name='us-east-1')

ec2 = boto3.resource('ec2', region_name='us-east-1')

options = Options()

options.headless = True

#0d4eb30aa2f5142d7

streamers = {

	1 : {

		"name": "gotaga",

		"instance": "0e9434b17bece5070"

	},

	2 : {

		"name": "sardoche",

		"instance": "0d4eb30aa2f5142d7"

	},

	3 : {

		"name": "shroud",

		"instance": "014d06835b178c24d"

	},

	4 : {

		"name": "summit1g",

		"instance": "042bcd39582d86879"

	}

}



driver = webdriver.Firefox(options=options)

streamers_index = 0

while True: 

	if streamers_index > 3 :

		streamers_index = 1

	else: 

		streamers_index += 1

	driver.get("https://www.twitch.tv/" + streamers[streamers_index]['name'])

	driver.implicitly_wait(7)

	try:

		host = driver.find_elements_by_class_name('hosting-ui-header')
	except:
		print("hosting header not found")

	try:

		mature_btn = driver.find_element_by_id('mature-link')

		mature_btn.click()

	except:

		print("mature audiance btn not found")

	try:

		title1 = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/main/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div[3]/div/div[1]/p')

		titre1 = title1.text
		print(titre1)



	except: 

		print("carre rouge direct not found")
		titre1 = "notdfound"

	try:

		title = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div/div[2]/h2')

		titre = title.text

	except:

		print("title not found so it is cheval by default")

		titre = "cheval"

	


	# try: 

		# print(host.text)

		# lance la vm 

		# lance le script

	# except: 

		# print("pas de host")

	# try: 

		# print(overlay.text)

	# except: 

		# print("pas de overlay offline")

	# try: 

		# print(title)

	# except: 

		# print("pas de titre offline")

	

	# summit1g ne streame pas actuellement.

	print(streamers[streamers_index]['name'])

	print(titre)

	if titre ==  streamers[streamers_index]['name'] + " ne streame pas actuellements.":

		# check if la vm est en ligne

		print("offline success mais c'est pas le bon if donc ya rien qui se passe, le bon if c'es le else a la fin")

		filters = [

			{

				'Name': 'instance-state-name', 

				'Values': ['running']

			}

		]

		# filter the instances based on filters() above

		instances = ec2.instances.filter(Filters=filters)

		RunningInstances = []	

		for instance in instances:

			# for each instance, append to array and print instance id

			RunningInstances.append(instance.id)

			print ("instance running : " + instance.id)

		print(RunningInstances)

		if instance.id == "i-" + streamers[streamers_index]['instance']:

			#stop script

			#stop instance ec2

			print("script and vm stopped")

		else:

			print("instance not running")

	elif titre1 == "LIVE":

		print("en direct tmtc")


		filters = [

			{

				'Name': 'instance-state-name', 

				'Values': ['stopped']

			}

		]

		# filter the instances based on filters() above

		instances = ec2.instances.filter(Filters=filters)

		RunningInstances = []	

		for instance in instances:

			# for each instance, append to array and print instance id

			RunningInstances.append(instance.id)

			print ("instance stopped : " + instance.id)

			if instance.id == "i-" + streamers[streamers_index]['instance']:

				client = boto3.client('ec2' ,region_name='us-east-1')

				response = client.start_instances(

				InstanceIds=[

					"i-" + streamers[streamers_index]['instance'],

				],

				DryRun=False

			)

				client = boto3.client('ssm')

				time.sleep(100)

				response = client.send_command(

					InstanceIds=[

						"i-" + streamers[streamers_index]['instance'],

					],

   

   					DocumentName='AWS-RunShellScript',

   					DocumentVersion='$DEFAULT',

	   				 # DocumentHash='Sha256 ',

		 		  	 # DocumentHashType='Sha256',

		  		  	TimeoutSeconds=3600,

		  		 	Comment='test',

		  		 	Parameters={
					 	'executionTimeout':["172800"],

					 	'commands': [

						   	'cd ..','cd ..','cd ..','cd ..','cd home','cd ubuntu', 'cd Desktop' ,'pip3 install selenium','pip3 install keyboard','pip3 install pymongo','pip3 install boto3','pip3 install clipboard','export PATH=$PATH:/home/ubuntu/Desktop','pip3 install pymongo[srv]','python3 twitch1.py'

			   		 ]


		   		 },


		  		 	OutputS3BucketName='compartiment-thimothe',

				# OutputS3KeyPrefix='string',

				# MaxConcurrency='string',

				# MaxErrors='string',

				# ServiceRoleArn='string',

				# NotificationConfig={

				# 'NotificationArn': 'string',

				# 'NotificationEvents': [

				# 'All'|'InProgress'|'Success'|'TimedOut'|'Cancelled'|'Failed',

				# ],

				# 'NotificationType': 'Command'|'Invocation'

				# },

   					CloudWatchOutputConfig={

					 	'CloudWatchLogGroupName': 'clipit',

					 	'CloudWatchOutputEnabled': True

				}

			)

				print("vm and script launched : " + instance.id)

			else:

				print ("wrong vm" + instance.id)

	else: 

		filters = [

			{

				'Name': 'instance-state-name', 

				'Values': ['running']

			}

		]

		# filter the instances based on filters() above

		instances = ec2.instances.filter(Filters=filters)

		RunningInstances = []	

		for instance in instances:

			# for each instance, append to array and print instance id

			RunningInstances.append(instance.id)

			print ("instance running : " + instance.id)

		print(len(RunningInstances))

		for instance in RunningInstances:
			print(instance)

			if instance == "i-" + streamers[streamers_index]['instance']:

				client = boto3.client('ec2' ,region_name='us-east-1')

				response = client.stop_instances(

				InstanceIds=[

					"i-" + streamers[streamers_index]['instance']

				],

				DryRun=False

			)

				print("instance successfully stopped :" + instance)

			else: 

				print("instance already stopped :" + instance)




