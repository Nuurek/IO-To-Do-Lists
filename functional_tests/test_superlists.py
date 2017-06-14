from .base import FunctionalTest
from superlists.models import ToDoList, ToDoListItem
from selenium.common.exceptions import NoSuchElementException


class Superlists(FunctionalTest):

    def test_public_list_create(self):
        list_title = 'New list name'

        self.browser.get(self.server_url)
        form = self.browser.find_element_by_id('list-form')
        form.find_element_by_name('name').send_keys(list_title)
        form.find_element_by_id('list-submit').click()
        title = self.browser.find_element_by_css_selector('h2').text
        self.assertEqual(title, list_title)

    def test_public_list_item_create(self):
        list_title = 'New list name'
        list_item_text = 'List item'

        todo_list = ToDoList(name=list_title)
        todo_list.save()
        url = todo_list.get_absolute_url()
        self.browser.get(self.server_url + url)
        form = self.browser.find_element_by_id('list-item-form')
        form.find_element_by_name('name').send_keys(list_item_text)
        form.find_element_by_id('list-item-submit').click()
        list_item = self.browser.find_element_by_class_name('list-group-item').text
        self.assertEqual(list_item, list_item_text)

    def test_public_list_item_delete(self):
        list_title = 'New list name'
        list_item_text = 'List item'

        todo_list = ToDoList(name=list_title)
        todo_list.save()
        todo_list_item = ToDoListItem(todo_list=todo_list)
        todo_list_item.name = list_item_text
        todo_list_item.save()
        url = todo_list.get_absolute_url()
        self.browser.get(self.server_url + url)
        list_item = self.browser.find_element_by_class_name('list-group-item')
        link = list_item.find_element_by_css_selector('a').get_attribute('href')
        self.browser.get(link)
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_class_name('list-group-item')