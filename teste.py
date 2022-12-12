import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from faker import Faker

faker = Faker()

url = 'http://192.168.0.100:3000'

class HomeTestCase(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)
        self.addCleanup(self.browser.quit)


    def test_page_title(self):
        self.browser.get(url)
        self.assertIn("Escrever App", self.browser.title)

    def test_hero_header(self):
        self.browser.get(url)
        [elements] = self.browser.find_elements(By.TAG_NAME, 'h1')
        self.assertIn("Escrever é Desvendar o Mundo", elements.text)

    def test_call_to_action_and_signup(self):
        test_first_name = faker.first_name()
        test_last_name = faker.last_name()
        test_email = faker.email()
        test_username = faker.user_name()
        test_password = faker.password()
        self.browser.get(url)
        # fill signup form
        [button] = self.browser.find_elements(By.ID, "callToAction")
        button.click()
        [name] = self.browser.find_elements(By.NAME, "name")
        name.send_keys(test_first_name)
        [last_name] = self.browser.find_elements(By.NAME, "last_name")
        last_name.send_keys(test_last_name)
        [email] = self.browser.find_elements(By.NAME, "email")
        email.send_keys(test_email)
        [username] = self.browser.find_elements(By.NAME, "username")
        username.send_keys(test_username)
        [password] = self.browser.find_elements(By.NAME, "password")
        password.send_keys(test_password)
        [submit_button] = self.browser.find_elements(By.TAG_NAME, "button")
        submit_button.click()
        # TODO fix login and put this part in a separate function
        self.browser.get(url + "/login")
        [username] = self.browser.find_elements(By.NAME, "username")
        username.send_keys(test_username)
        [password] = self.browser.find_elements(By.NAME, "password")
        password.send_keys(test_password)
        [submit_button] = self.browser.find_elements(By.TAG_NAME, "button")
        submit_button.click()
        #TODO end of login
        # check greet user at /home
        WebDriverWait(self.browser, timeout=10).until(lambda d: d.find_element(By.TAG_NAME, "h3"))
        [user_greeting] = self.browser.find_elements(By.ID, "userGreeting")
        self.assertIn(test_username, user_greeting.text)
        # check logged in NavBar
        links = self.browser.find_elements(By.TAG_NAME, "a")
        self.assertIn("Home", links[0].text)
        self.assertIn(url, links[0].get_property("href"))
        self.assertIn("Trilha", links[1].text)
        self.assertIn(url + "/trilha", links[1].get_property("href"))
        self.assertIn("", links[2].text)
        self.assertIn(url + "/escrita", links[2].get_property("href"))
        self.assertIn("Logout", links[3].text)
        self.assertIn(url, links[3].get_property("href"))
        # trilha
        self.browser.get(url + "/trilha")
        WebDriverWait(self.browser, timeout=10).until(lambda d: d.find_element(By.TAG_NAME, "h3"))
        # toggle_details_button = 
        # escrever
        # logout
if __name__ == '__main__':
    unittest.main(verbosity=2)

