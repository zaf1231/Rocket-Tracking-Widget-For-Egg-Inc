# Rocket-tracking-widget-for-Egg-Inc.
Python based widget to show your rocket progress in Egg Inc. on your desktop! (windows only)

How to run the Egg inc. Rocket Tracking widget for windows
- Install python by going to this website: https://www.python.org/downloads/
- Download "Python 3.12.1"
- Intall ChromeDriver from this site: https://sites.google.com/chromium.org/driver/downloads
- Install pip by running this in command prompt:

	python -m ensurepip --default-pip

-Then install PyQt5, selenium and pillow by running this in command prompt:

	pip3 install PyQt5 selenium pillow

Changes you need to make to the code!
- Line 11: Change file path to correct folder
- Line 12: Put your own player ID in the field
- Line 118: Change the starting coordinates for the widget
- To run the program, the cleanest way is to run "launcher.py" however if you want to see the console because you are getting errors, you can run "Rocket widget.py". If you are still confused and you think there is something wrong with the webdriver, you can run "Rocket widget (without headless).py" which will show you what is going on in the selium webdriver.

For it to open on startup
- Create a shortcut of "launcher.py"
- Press "WINDOWS + R"
- Type in "shell:startup" and press enter
- Drag the shortcut of launcher.py into that folder and it will start up when you restart your computer :)

Using other rocket icons
- I've centered the icon for the "Atreggies Henliner", if you are launching different rockets, you will have to download a transparent picture of the rocket you are using and replace the name of it on line 18. You may also want to recentre the icon and change its scale (it may be stretched). 

Debugging
- If you run into any issues, DM me and I'll see if I can help with your issues :)


Made by: Zonkantor - 10.03.24
