from overlapping import Screenshoot
from pages.start_page import StartingView


def test_language(nucleus_smart_app, language):
    view = StartingView(nucleus_smart_app._web_driver)

    description_text = view.description_area.get_text()
    welcome_text = view.welcome_label.get_text()
    swipe_arrow = view.swipe_arrow.get_text()

    assert description_text == view.description_area.languages[language]
    assert welcome_text == view.welcome_label.languages[language]
    assert swipe_arrow == view.swipe_arrow.languages[language]

def test_with_overlapping_checker(nucleus_smart_app, language):
    view = StartingView(nucleus_smart_app._web_driver)

    description_text = view.description_area.get_text()
    welcome_text = view.welcome_label.get_text()
    swipe_arrow = view.swipe_arrow.get_text()

    assert description_text == view.description_area.languages[language]
    assert welcome_text == view.welcome_label.languages[language]
    assert swipe_arrow == view.swipe_arrow.languages[language]

    nucleus_smart_app.swipe('left', 5, 0.125)

    # Getting screenshoot from driver
    s = Screenshoot(nucleus_smart_app._web_driver)

    # Defining elements to check overlapping, for example you can define Buttons, Labels, or something else
    elements = s.find_elements('*//XCUIElementTypeButton') # here described element selector for ios, so please check it for android

    # method returns list with id of overlapped elements, you can look at it in screens/ directory
    overlapped_elements = s.check_overlapping(elements)

    # Check if there is overlapped text
    assert not overlapped_elements



