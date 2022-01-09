from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from bs4 import BeautifulSoup

driver = webdriver.Chrome("/usr/bin/chromedriver")
email='UserEmail'
password='UserPsw'
textFieldSearch='site:linkedin.com/in Πωλητής αυτοκινήτων'

#login at linkedin
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

emailLogin = driver.find_element_by_name("session_key");
passwordLogin = driver.find_element_by_name("session_password");

emailLogin.send_keys(email);
passwordLogin.send_keys(password);

loginButton = driver.find_element_by_class_name("from__button--floating");
loginButton.click();

#google search
driver.get("https://www.google.com/")

removeWindow = driver.find_element_by_id("L2AGLb");
removeWindow.click();

googleSearch = driver.find_element_by_name("q");

googleSearch.send_keys(textFieldSearch);

sleep(0.2);
googleSearch.send_keys(Keys.ENTER);

soupAllResults = BeautifulSoup(driver.page_source, "html.parser")

urls=[]
search = soupAllResults.find_all('div',class_="g")

for h in search:
	urls.append(h.a.get('href'))

i=1
for url in urls:		
	driver.get(url)
	sleep(10);
	soup = BeautifulSoup(driver.page_source, "html.parser")

	name = soup.find(class_="text-heading-xlarge inline t-24 v-align-middle break-words")
	if(name):
		name = name.get_text().replace("\n","").strip()
		
	location = soup.find(class_="text-body-small inline t-black--light break-words")
	if(location):
		location = location.get_text().replace("\n","").strip()
		
	company = soup.find(class_="inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline")
	if(company):
		company = company.get_text().replace("\n","").strip()
		
	
	print("User with ",i," number")
	print("User Name: ", name, " User Location: ", location, " User Company: ", company)
	i=i+1
	
print("End crawling")

driver.close()
