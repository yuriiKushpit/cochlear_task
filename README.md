# How to run tests on Appium

## IOS
1. Clone project in your folder using git clone https://github.com/yuriiKushpit/cochlear_task.git
2. Install all required packages using command pip3 install -r requirements.txt 
3. Install Appium Client and Appium Desktop http://appium.io/docs/en/drivers/ios-xcuitest-real-devices/
4. Run Appium Desktop 1.6.1 on Mac machine;
5. After launch Appium Desktop you need to connect iPhone to Mac machine (using USB cable);
6. Make sure that application is build in Xcode with correct settings (prepared for automation testing) (see step 5);
7. Describe your udid and app in configuration_data/ios_config.json. Key udid is your device udid. Key app is your path to application.
8. Locators for elements located in pages/start_page.json. If you want to add testing for any other language, you should add code of this language and expected text in language part of json file.
9. If you want to change languages or platform you should navigate to pytest.ini and change starting parameters. You could change starting parameters from command line using --platform and --languages keys. You could set any number of languages separated by ','. Example: python3 -m pytest main_test.py --platform=ios --languages=en,fr,de,el.
10. WARNING: I have used https://drive.google.com/open?id=1_OCWlthZ5NwDx8nY_vnequtFxzKQ0By8 as testing application. Run were tested on ios 11.2.2.
11. I have involved Pavlo Tsiupka for testing task with overlapping (text wrapping). You could check test on video https://drive.google.com/file/d/1PWrxfZy9dpotzT2b0eI1r1xXAhub28qa/view Appium returns text as attribute and it's impossible to check overlapping by appium or any existing  tools. Overlapping task is very important because you could use different fonts with different size of letters so it could lead to unexpected issues. For this task we created custom library which uses image recognition technology.

## Android
All steps are the same for Android app except 4-th. In this case you should change platformVersion and deviceName to your 
platform and device id. This application was used as target  https://drive.google.com/open?id=1Vy_oAI8yTPwzHGpzqqvCImaNIcJ8h6CT

WARNING: Please install this app ABD Change Language https://play.google.com/store/apps/details?id=net.sanapeli.adbchangelanguage on your Android device and run adb shell pm grant net.sanapeli.adbchangelanguage android.permission.CHANGE_CONFIGURATION before first execution of tests.

Here is folder with test running:
https://drive.google.com/open?id=1wQ-W1c1HXc1ql4g4DThjoHjBtPLiCiBU
