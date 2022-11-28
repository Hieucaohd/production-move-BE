from webargs.core import Parser
import enum

location_maps = [{location: location} for location in Parser.__location_map__]
dict_to_enum = {}
for location_map in location_maps:
    dict_to_enum.update(location_map)
LocationParseArgs = enum.Enum('LocationParseArgs', dict_to_enum)
