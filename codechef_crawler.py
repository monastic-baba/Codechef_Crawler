import requests
from bs4 import BeautifulSoup

base_url="https://www.codechef.com/"

def crawl(username):
	url = "https://www.codechef.com/users/" + str(username) 
	source_code = requests.get(url)
	plain_text = source_code.content
	soup =BeautifulSoup(plain_text,'html.parser')
	section = soup.find(class_='rating-data-section problems-solved')
	links = section.find_all('a')
	for link in links:
		problem_status_url=base_url+ link['href']
		name = link.string
		crawl_some_more(problem_status_url,name)
		
def crawl_some_more(url,name):
	url = url + "?sort_by=All&sorting_order=asc&language=All&status=15&Submit=GO" #show only Correct Submissions!
	source_code = requests.get(url)
	plain_text = source_code.content
	soup = BeautifulSoup(plain_text,'html.parser')
	id_list = soup.find_all('td',width='60')
	try:
		submission_id=id_list[0].string  #taking the latest correct submission's ID
	except:
		submission_id=id_list.string	
	lang_list = soup.find_all('td', width='70')
	try:
		lang = lang_list[0].string       #taking the language of latest correct submission
	except:
		lang = lang_list.string 	
	submission_url = base_url + "viewplaintext/" + str(submission_id) 
	code = a_little_more_crawl(submission_url)
	print(submission_url)
	name = name + ".txt"
	f = open(name,'w')	
	f.write(code)
	f.close()
		
def a_little_more_crawl(url):
	source_code = requests.get(url)
	plain_text = source_code.content
	soup = BeautifulSoup(plain_text,'html.parser')
	problem_code = soup.get_text()
	return (problem_code) 
	
	

username = input("Enter the username: ")	
crawl(str(username))