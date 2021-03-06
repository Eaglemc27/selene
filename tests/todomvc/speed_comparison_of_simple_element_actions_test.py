from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from selene.conditions import visible
from selene.tools import s, set_driver, get_driver, visit
from tests.helpers import time_spent
from tests.todomvc.helpers.todomvc import TODOMVC_URL

browser = None
shaded_browser = None


def setup_function(f):
    global browser
    global shaded_browser

    set_driver(webdriver.Firefox())
    visit(TODOMVC_URL)
    s("#new-todo").should_be(visible)

    browser = webdriver.Firefox()
    browser.get(TODOMVC_URL)
    WebDriverWait(browser, 4).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#new-todo")))

    shaded_browser = webdriver.Firefox()


def teardown_function(f):
    global browser
    global shaded_browser
    browser.quit()
    get_driver().quit()
    shaded_browser.quit()


def create_tasks_with_raw_selenium():
    global browser
    new_todo = browser.find_element_by_css_selector("#new-todo")
    for task_text in map(str, range(10)):
        new_todo.send_keys(task_text + Keys.ENTER)


def create_tasks_with_selenium_with_research():
    global browser
    for task_text in map(str, range(10)):
        new_todo = browser.find_element_by_css_selector("#new-todo")
        new_todo.send_keys(task_text + Keys.ENTER)


def create_tasks_with_selene_and_send_keys():
    for task_text in map(str, range(10)):
        s("#new-todo").send_keys(task_text + Keys.ENTER)


def create_tasks_with_selene_with_cash():
    new_todo = s("#new-todo").cash()
    for task_text in map(str, range(10)):
        new_todo.send_keys(task_text + Keys.ENTER)


def test_selene_is_almost_as_fast_selenium_with_research_and_initial_wait_for_visibility():
    selene_time = time_spent(create_tasks_with_selene_and_send_keys)
    selenium_time = time_spent(create_tasks_with_selenium_with_research)
    # print("%s vs %s" % (selene_time, selenium_time))
    assert selene_time < 1.12 * selenium_time


def test_selene_is_from_32_to_50_percents_slower_than_raw_selenium():
    selene_time = time_spent(create_tasks_with_selene_and_send_keys)
    selenium_time = time_spent(create_tasks_with_raw_selenium)
    # print("%s vs %s" % (selene_time, selenium_time))
    assert selene_time <= 1.51 * selenium_time


def test_cashed_selene_is_almost_as_fast_raw_selenium():
    selene_time = time_spent(create_tasks_with_selene_with_cash)
    selenium_time = time_spent(create_tasks_with_raw_selenium)
    # print("%s vs %s" % (selene_time, selenium_time))
    assert selene_time < 1.12 * selenium_time
