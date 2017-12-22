# coding=utf-8
"""Primary program"""

import geo_create
import geo_export
import geo_get_basedata

opening = geo_get_basedata.get_dji_scrape()
start = geo_get_basedata.get_location()
hash_dec = geo_create.create_hash(opening)
goal = geo_create.create_goal(start, hash_dec)
geo_export.export_cli(goal[0], goal[1], start[2])
geo_export.export_map_html(start, goal)
