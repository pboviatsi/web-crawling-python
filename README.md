# web-crawling-python

Η υλοποίηση του προγράμματος έγινε σε Python. 

Αρχικά ξεκινάμε τον driver του Chrome, για να μπορέσουμε να ανοίξουμε την σελίδα του linkedin.com - `driver = webdriver.Chrome("/usr/bin/chromedriver")`. Στην συνέχεια ανοίγουμε την σελίδα που θέλουμε για να μπορέσουμε να συνδεθούμε - 
`driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")`

Μόλις ανοίξει η σελίδα, εντοπίζουμε τα στοιχεία που θέλουμε να συμπληρώσουμε για να μπορέσουμε να συνδεθούμε, αναζητώντας τα με το element name τους (session_key και session_password) -
```
emailLogin = driver.find_element_by_name("session_key");
passwordLogin = driver.find_element_by_name("session_password");
```

Στην συνέχεια στέλνουμε τις αντίστοιχες τιμές στο κατάλληλο πεδίο  -
```
emailLogin.send_keys(email);
passwordLogin.send_keys(password);.
```

Και για να πραγματοποιηθεί η σύνδεση του χρήστη με τα παραπάνω στοιχεία συνδεσης, βρίσκουμε το κουμπί με την class που πραγματοποιεί την σύνδεση - 
`loginButton = driver.find_element_by_class_name("from__button--floating");`
και το επιλέγουμε κάνοντας click - `loginButton.click();`. Έτσι έχει πραγματοποιηθεί η σύνδεση ενός χρήστη στο περιβάλλον του linkedin και μπορούμε να περιηγηθούμε σε προφίλ άλλων χρηστών και διάφορες δημοσιεύσεις.
 	
  Θέλοντας να πάρουμε τα αποτελέσματα από την αναζήτηση της google για την αναζήτηση μέσα από το linkedin, ανοίγουμε το google.com - `driver.get("https://www.google.com/")`. Όμως εντοπίζουμε ότι δεν μπορούμε να συμπληρώσουμε το πεδίο της αναζήτησης, αν δεν αφαιρέσουμε το παράθυρο που μας εμφανίζει η google για την αποδοχή της λήψης των cookies. Οπότε πατώντας την αποδοχή, βρίσκοντας το κουμπί με το σωστό id του element - 
`removeWindow = driver.find_element_by_id("L2AGLb");` και το επιλέγουμε κάνοντας click - `removeWindow.click();`, μας επιτρέπει να συνεχίσουμε. Στην συνέχεια αναζητούμε το element με το κατάλληλο id (q) για να επιλεχθεί το πεδίο αναζήτησης της σελίδας της google - `googleSearch = driver.find_element_by_name("q");`, και στέλνουμε  στην αναζήτηση το λεκτικό που θέλουμε να ψάξουμε - 
```
textFieldSearch='site:linkedin.com/in Πωλητής αυτοκινήτων' 
googleSearch.send_keys(textFieldSearch);
```

Πατώντας απλά το ‘enter’ γίνεται η αναζήτηση του λεκτικού που έχουμε στείλει προηγουμένως- `googleSearch.send_keys(Keys.ENTER);`.

Σε αυτό το σημείο έχουμε όλα τα αποτελέσματα της αναζήτησης που πραγματοποιήσαμε στο προηγούμενο βήμα. Χρησιμοποιώντας την BeautifulSoup δημιουργούμε ένα αντικείμενο για να αναλύσουμε την σελίδα των αποτελεσμάτων - 
`soupAllResults = BeautifulSoup(driver.page_source, "html.parser")`. Στην συνέχεια μαζεύουμε όταν τα div που έχουν class ‘g’ - 
`search = soupAllResults.find_all('div',class_="g")`, δηλαδή όλα τα αποτελέσματα της πρώτης σελίδας, για πάρουμε τα link τους στην συνέχεια σε μια μεταβλητή μεσα απο μια for...loop - 
```
urls=[]
for h in search:
urls.append(h.a.get('href')) 
```

Μέχρι αυτό το σημείο έχουμε στην μεταβλητή urls, όλα τα link-προφίλ χρηστών που θέλουμε να επισκεφτούμε και να πάρουμε κάποιες πληροφορίες από το κάθε ένα. Κάθε ένα url - `for url in urls`:  το ανοίγουμε - `driver.get(url)` και περιμένουμε 10 δευτερόλεπτα για να φορτωθεί όλη η σελίδα - `sleep(10);`. Έπειτα ξανα δημιουργούμε ένα αντικείμενο BeautifulSoup για να μπορέσουμε να αναλύσουμε την σελίδα μας - `soup = BeautifulSoup(driver.page_source, "html.parser")`. Από την κάθε html σελίδα, βρίσκω τις class που έχουν το όνομα, η τοποθεσία του και η σημερινή θέση εργασίας του -
```
name = soup.find(class_="text-heading-xlarge inline t-24 v-align-middle break-words")
location = soup.find(class_="text-body-small inline t-black--light break-words")
company = soup.find(class_="inline-show-more-text inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp inline")
```

Έχοντας πλέον τα πεδία που θέλουμε το περιεχόμενο τους, για το κάθε ένα ελέγχουμε αν έχει περιεχόμενο και το εκχωρούμε σε αντίστοιχες μεταβλητές (αφαιρώντας τις κενές γραμμές ‘/n’) - 
```
if(name):
	name = name.get_text().replace("\n","").strip()
if(location):
	location = location.get_text().replace("\n","").strip()
if(company):
	company = company.get_text().replace("\n","").strip().
```

Έχοντας πλέον την πληροφορία που επιθυμούσαμε την εκτυπώνουμε σε κάθε επανάληψη, ώστε στο τέλος να έχουμε όλα τα αποτελέσματα. Μόλις τελειώσουν οι παραπάνω ενέργειες, κλείνουμε τον driver του Chrome - `driver.close()`.
