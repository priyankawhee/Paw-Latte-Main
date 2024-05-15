# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestOrder():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_order(self):
    self.driver.get("http://127.0.0.1:5000/")
    self.driver.set_window_size(874, 816)
    self.driver.find_element(By.NAME, "username").click()
    self.driver.find_element(By.NAME, "username").send_keys("priyankaa")
    self.driver.find_element(By.NAME, "password").click()
    self.driver.find_element(By.NAME, "password").send_keys("pri")
    self.driver.find_element(By.CSS_SELECTOR, "button").click()
    self.driver.find_element(By.LINK_TEXT, "Menu").click()
    self.driver.find_element(By.CSS_SELECTOR, ".menu-section:nth-child(1) .menu-item:nth-child(2) > .order-btn").click()
    self.driver.find_element(By.CSS_SELECTOR, ".menu-section:nth-child(1) .menu-item:nth-child(3) > .order-btn").click()
  
