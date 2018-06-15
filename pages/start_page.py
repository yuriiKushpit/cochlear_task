import json
import os
import sys
from conftest import IOS_TYPE, ANDROID_TYPE


class View:
    def __init__(self, driver):
        # Protected method ny design
        self.active_platform = driver._platform
        self.json_data = self.collect_json_data()
        self._driver = driver

    @property
    def driver(self):
        return self._driver

    def collect_json_data(self):
        """
        Find full path of module where this method is called.
        Find for the json config file with the same name.
        Parse found json config file.

        :return: Parsed data from json config file(dictionary).
        """
        current_module = sys.modules[self.__module__].__file__
        current_module_path = os.path.dirname(current_module)
        current_module_name = os.path.splitext(os.path.basename(current_module))[0]
        config_name = '{0}.json'.format(current_module_name)
        config_full_path = os.path.join(os.path.sep, current_module_path, config_name)
        config_data = json.load(open(config_full_path, encoding='utf-8'))
        return config_data

    def collect_elements(self):
        """
        Creates attributes for self accordingly to collected (key,value) pairs in self.json_data.

        :return: None.
        """

        for key in self.json_data:
            setattr(self, key, Element(self.json_data[key], self.driver))


class Element:
    def __init__(self, element_data, driver):
        """
        Initialize new Element instance.
        Get id for the element accordingly to active driver instance platform.

        :param locators: Dictionary with id of the element for the both platforms.
        """
        platform = driver._platform
        locators = element_data["locators"]
        languages = element_data["language"]
        self.id = locators['android'] if platform == ANDROID_TYPE else locators['ios']
        self.languages = languages
        self._platform = platform
        self._driver = driver

    def _get_text(self, element_id, attribute):
        if self.platform == IOS_TYPE:
            element = self.driver.find_element_by_xpath(element_id.id)
        else:
            element = self.driver.find_element_by_id(element_id.id)

        text = element.get_attribute(attribute)
        return text

    def get_text(self):
        """
       Trigger get_attribute() method of the active driver instance.

       :param attribute: Attribute for an element(string).
       :return: Attribute value.
       """
        if self.platform == ANDROID_TYPE:
            attribute = self._get_text(self, "text")
        else:
            attribute = self._get_text(self, "value")
        return attribute

    @property
    def platform(self):
        return self._platform

    @property
    def driver(self):
        return self._driver


class StartingView(View):
    def __init__(self, driver):
        super().__init__(driver)
        self.collect_elements()
