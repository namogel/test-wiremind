from selenium import webdriver

opts = webdriver.ChromeOptions()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36")
opts.add_argument('--proxy-server=localhost:8080')

driver = webdriver.Chrome('/home/namogel/dev/test-wiremind/chromedriver', options=opts)

response = driver.get("https://www.transavia.com/fr-FR/accueil/")
id_cookies = [c for c in driver.get_cookies() if c['name'].startswith('D_')]
print(id_cookies)

driver.close()
