# coding=utf-8
"""Creates the GUI for the Program"""


from appJar import gui

import geo_get_basedata


def location_mode(btnname):
    """Determines the location mode"""
    print(btnname)
    if btnname == "Automatic":
        location = geo_get_basedata.get_location()
    elif btnname == "Manual":
        location = "temp"
    else:
        location = "ERROR"
    print(location)
    return location

def date_mode(btnname):
    print(btnname)


prompt_mode_gui = gui("Geohashing GUI v.1")
prompt_mode_gui.addLabel("Location Label", "Location Mode:", 0)
prompt_mode_gui.addButtons(["Automatic", "Manual"], location_mode,0,1, colspan=2)
prompt_mode_gui.addLabel("Date Label", "Date:", 1)
prompt_mode_gui.addButtons(["Today", "Pick"], date_mode, 1, 1, colspan=2)
prompt_mode_gui.go()
prompt_mode_gui.stop()
