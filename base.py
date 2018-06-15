import time

from appium.webdriver.common.touch_action import TouchAction


class Driver:
    def __init__(self, web_driver):
        self._web_driver = web_driver

    def __getattr__(self, item):
        return getattr(self._web_driver, item)

    def swipe(self, direction='up', repeat_count=1, timeout=0):
        for _ in range(repeat_count):
            self._web_driver.execute_script("mobile: swipe", {"direction": direction})
            time.sleep(timeout)


class Locator:
    def __init__(self, **selector):
        assert len(selector) == 1
        self.selector = list(selector.items())[0]

    def __get__(self, instance, owner):
        return Component(self.selector, instance.driver)


class Component:
    def __init__(self, selector, driver: Driver):
        self.selector = selector
        self.driver = driver

    @property
    def value(self):
        return self.ref().get_attribute('value')

    def is_present(self):
        return bool(self.ref(True))

    def is_visible(self):
        return self.ref().is_displayed()

    def is_selected(self):
        return self.ref().is_selected()

    def scroll_into_view(self, direction='up'):
        element = self.ref()
        while not element.is_displayed():
            self.driver.swipe(direction)

    def click(self, sleep_time=0, direction='up'):
        element = self.ref()
        while not element.is_displayed():
            self.driver.swipe(direction)

        element.click()
        time.sleep(sleep_time)

    def click_with_offset(self, x, y):
        action = TouchAction(self.driver)
        action.tap(self.ref(), x=x, y=y)
        action.perform()

    def ref(self, multiple=False):
        if multiple:
            return self.driver.find_elements(*self.selector)
        return self.driver.find_element(*self.selector)


class View:
    def __init__(self, driver):
        self.driver = driver


class NucleusSmartApp(View):
    demo_button = Locator(name='demoModeButton')
    volume_open_button = Locator(xpath='//XCUIElementTypeCell[@name="volume"]')

    plus_button = Locator(
        xpath='//XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeButton[1]'
    )
    minus_button = Locator(
        xpath='//XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeButton[2]'
    )
    value_element = Locator(xpath='//XCUIElementTypeCell[@name="volume"]')
    menu_button = Locator(xpath='//XCUIElementTypeButton[@name="Settings menu"]')
    exit_button = Locator(xpath='//XCUIElementTypeCell[@name="exitPracticeMode"]')


class HearDeviceSettings(View):
    cochlear_device = Locator(xpath='//XCUIElementTypeCell[contains(@name, "Cochlear")]')
    presets = Locator(xpath='//XCUIElementTypeOther[@name="Master Volume"]')
    master_volume_slider = Locator(xpath='//XCUIElementTypeOther[@name="Master Volume"]')
    streaming_switch = Locator(xpath='//XCUIElementTypeSwitch[contains(@name, "Streaming")')
    start_live_listen_button = Locator(xpath='//XCUIElementTypeOther[contains(@name, "Start")]')
    stop_live_listen_button = Locator(xpath='//XCUIElementTypeOther[contains(@name, "Start")]')
