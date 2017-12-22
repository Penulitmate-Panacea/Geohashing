# coding=utf-8
"""Handles the exporting of a final geohash from the program"""


def export_cli(lat, lon, location):
    """Shows the user the goal"""
    print("Your geohash for:", location['city'], ",", location['region_name'], ",", location['country_name'], "is:\n",
          str(lat), ",", str(lon))


def export_map_html(home, result):
    """Saves the starting location and resulting geohash in a html file"""
    from datetime import date
    from folium import Map, Marker, Icon
    try:
        result_map = Map(location=[home[0], home[1]], tiles="Stamen Toner")
        Marker(location=[home[2]['latitude'], home[2]['longitude']], popup='Starting Location',
               icon=Icon(color='green')).add_to(result_map)
        Marker(location=[result[0], result[1]], popup='Geohash Location', icon=Icon(color='red')).add_to(result_map)
        path = ".\Saved\geohash_" + str(date.today().strftime("%Y-%m-%d")) + ".html"
        result_map.save(path)
    except FileNotFoundError:
        from os import mkdir
        mkdir(".\Saved")
        result_map = Map(location=[home[0], home[1]], tiles="Stamen Toner")
        Marker(location=[home[2]['latitude'], home[2]['longitude']], popup='Starting Location',
               icon=Icon(color='green')).add_to(result_map)
        Marker(location=[result[0], result[1]], popup='Geohash Location', icon=Icon(color='red')).add_to(result_map)
        path = ".\Saved\geohash_" + str(date.today().strftime("%Y-%m-%d")) + ".html"
        result_map.save(path)
