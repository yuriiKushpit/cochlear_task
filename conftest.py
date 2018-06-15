import json
import subprocess

import pytest

from appium.webdriver.webdriver import WebDriver
from base import Driver


def pytest_generate_tests(metafunc):
    if 'language' in metafunc.fixturenames:
        metafunc.parametrize('language', metafunc.config.option.languages.split(','))


def pytest_addoption(parser):
    parser.addoption('--languages', action='store', type=str, default="en", help='Please specify languages to test')
    parser.addoption('--platform', action='store', type=str, default="android",
                     help='Please specify platform (android,ios) to test')


ANDROID_TYPE = 'android'
IOS_TYPE = 'ios'

POSSIBLE_PLATFORM = (ANDROID_TYPE, IOS_TYPE)


def adb_shell(command, serial=None, adbpath='adb shell'):
    args = adbpath
    if serial is not None:
        args += ' -s ' + serial
    args += ' ' + command
    return subprocess.check_output(args, shell=True)


def change_language_android(language="en"):
    cmd = "am start -n net.sanapeli.adbchangelanguage/.AdbChangeLanguage -e language {}".format(language)
    return adb_shell(cmd)


def create_driver(request, language):
    platform = request.config.option.platform

    assert platform in POSSIBLE_PLATFORM

    cap = open(f'configuration_data/{platform}_config.json').read()
    capabilities = json.loads(cap)

    if platform == ANDROID_TYPE and language:
        change_language_android(language)

    elif platform == IOS_TYPE:
        capabilities["language"] = language

    driver = WebDriver("http://0.0.0.0:4723/wd/hub", desired_capabilities=capabilities)
    driver._platform = platform

    driver.implicitly_wait(5)
    request.addfinalizer(driver.quit)

    return Driver(driver)


@pytest.fixture()
def nucleus_smart_app(request, language):
    return create_driver(request, language)
