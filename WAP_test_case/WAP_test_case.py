import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random


class SportlyTwitchTest(unittest.TestCase):

    def setUp(self):
        # Defining Chrome browser settings for emulation and starting browser
        mobile_emulation = {
            "deviceMetrics": {"width": 400, "height": 900, "pixelRatio": 3.0},
            "userAgent": "(Linux; Android 14; en-us; SM-A536B Build/UP1A.231005.007) Chrome/125.0.6422.165",
            "clientHints": {"platform": "Android", "mobile": True}}
        chrome_options = Options()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.failed = False

    def failTestCase(self, msg):
        self.fail(msg)

    def checkCookiePopup(self, driver):
        print("Step 1. Go to https://m.twitch.tv/")
        try:
            # Dismissing Accept Cookies popup is not working
            # Both button Accept and Reject perform no action on chrome mobile emulator
            # Only Customize button is working
            # Clicking Accept or Reject cookies returns Error:
            # [GraphQL] One or more GraphQL errors were detected on request 01J0KVBCY49KP66RS334WA15BB.
            id_cookie_accept_banner = driver.find_element(
                By.CLASS_NAME, 'ScCoreButton-sc-ocjdkq-0.ScCoreButtonPrimary-sc-ocjdkq-1.logzNn.eTsvyN')
            id_cookie_accept_banner.click()
            print("Accept Cookies popup detected - it doesn't work - GraphQL error on Chrome emulator.")
            self.failed = True
        except:
            print("No Accept Cookies popup detected.")
        try:
            id_cookie_banner = driver.find_element(By.CLASS_NAME, 'ScCoreButtonLabel-sc-s7h2b7-0.bVSfxT')
            id_cookie_banner.click()
            print("Cookies popup detected.")
        except:
            print("No cookies popup detected.")
            self.failed = True
        if self.failed:
            self.failTestCase("Accept Cookies popup detected - it doesn't work - ending test case.")

    def clickOnSearch(self, driver):
        print("Step 2. Click in the search icon")
        try:
            search_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/nav/div[2]/a')
            search_element.click()
            print("Search element found.")
        except:
            print("No search element.")
            self.failed = True
        if self.failed:
            self.failTestCase("Search element was not found.")

    def inputStarCraftII(self, driver):
        print("Step 3. Input StarCraft II")
        try:
            search_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/nav/div/div/div[2]/div/div/input')
            search_element.send_keys("StarCraft II")
            print("Input field found.")
        except:
            print("No input field found.")
            self.failed = True
        if self.failed:
            self.failTestCase("Input field for Twitch search not found.")
        time.sleep(5)
        try:
            search_element = driver.find_element(By.XPATH, '//*[@title="StarCraft II"]')
            search_element.click()
            print("Starcraft II category found.")
        except:
            print("No Starcraft II category found.")
            self.failed = True
        if self.failed:
            self.failTestCase("No Starcraft II category found.")

    def scrollTwoTimes(self, driver):
        print("Step 4. Scroll two times down")
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, window.innerHeight);")

    def selectStreamToPlay(self, driver):
        print("Step 5. Select one stream")
        try:
            list_of_loaded_streamers = driver.find_elements(By.CLASS_NAME, 'Layout-sc-1xcs6mc-0.bNMEpR')
            list_of_loaded_streamers[2].click()
            try:
                accept_mature_element = driver.find_element(By.XPATH, '//div[@text()="Start Watching"]')
                accept_mature_element.click()
            except:
                print("No mature popup.")
        except:
            print("No list of loaded streamers.")
            self.failed = True
        if self.failed:
            self.failTestCase("No Starcraft II streamers list found.")

    def takeScreenshot(self, driver):
        print("Step 6. Create screenshot")
        time.sleep(10)
        driver.save_screenshot("./test.png")

    def test_sportlyWapTest(self):
        driver = self.driver

        # Step 1. Go to https://m.twitch.tv/
        driver.get("https://m.twitch.tv/")
        time.sleep(2)
        self.checkCookiePopup(driver)
        time.sleep(2)
        # Step 2. Click in the search icon
        self.clickOnSearch(driver)
        time.sleep(2)
        # Step 3. Input StarCraft II
        self.inputStarCraftII(driver)
        time.sleep(2)
        # Step 4. Scroll two times down
        self.scrollTwoTimes(driver)
        time.sleep(2)
        # Step 5. Select one stream
        self.selectStreamToPlay(driver)
        # Step 6. Create screenshot
        self.takeScreenshot(driver)

    def tearDown(self):
       self.driver.quit()


if __name__ == "__main__":
    unittest.main()
