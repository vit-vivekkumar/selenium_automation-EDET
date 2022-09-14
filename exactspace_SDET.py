# Import the required modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from browsermobproxy import Server
import time
import json
import sys


# Main Function
if __name__ == "__main__":

	# extracting browsermob-proxy-2.1.4-bin
	path_to_browsermobproxy = "/home/vivek/Downloads/browsermob-proxy-2.1.4/bin/"
	# Start the server with the path and port 8090
	server = Server(path_to_browsermobproxy + "browsermob-proxy", options={'port': 8090})
	server.start()

	# Create the proxy with following parameter as true
	proxy = server.create_proxy(params={"trustAllServers": "true"})

	# Create the webdriver object and pass the arguments
	options = webdriver.ChromeOptions()

	# Chrome will start in Headless mode
	options.add_argument('headless')

	# Ignores any certificate errors if there is any
	options.add_argument("--ignore-certificate-errors")

	# Setting up Proxy for chrome
	options.add_argument("--proxy-server={0}".format(proxy.proxy))

	# Start the chrome webdriver 
	service = Service("/usr/bin/chromedriver")
	driver = webdriver.Chrome(service=service)

	# Create a new HAR file of the following domain
	# using the proxy.
	proxy.new_har("exactspace.co/")

	# Send a request to the website and let it load
	driver.get("https://exactspace.co/")

	# Sleeps for 10 seconds
	time.sleep(10)

	# Write it to a HAR file.
	with open("exactspace.har", "w", encoding="utf-8") as f:
		f.write(json.dumps(proxy.har))

	print("Quitting Selenium WebDriver")
	driver.quit()

	# Read HAR File and parse it using JSON
	# to find the urls containing images.
	har_file_path = "exactspace.har"
	with open(har_file_path, "r", encoding="utf-8") as f:
		logs = json.loads(f.read())

	# Store the network logs from 'entries' key and
	# iterate them
	network_logs = logs['log']['entries']
	
	status,response_2xx,response_4xx,response_5xx=[],[],[],[]
	for log in network_logs:

		# Except block will be accessed if any of the
		# following keys are missing
		try:
			# status is present inside the following keys
			url = log['response']['status']
			status.append(str(url))
			response_2xx=[x for x in status if x.startswith('2')]
			response_4xx = [x for x in status if x.startswith('4')]
			response_5xx = [x for x in status if x.startswith('5')]
				
		except Exception as e:
			# print(e)
			pass

	#Redirect output into text file
	print('Output successfully, stored into output.txt file.')
	file_path = 'output.txt'
	sys.stdout = open(file_path, "w")
	print('output :')
	print('a. Total status code : ',len(status))
	print('b. Total count for 2XX status code :', len(response_2xx))
	print('c. Total count for 4XX status code :', len(response_4xx))
	print('d. Total count for 5XX status code :', len(response_5xx))



