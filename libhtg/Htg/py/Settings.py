import json
import Htg

from os import mkdir, path
from gi.repository import GLib, GObject
from typing import Any
from .Relation import Relation

class Settings:
    __handlers = dict[GObject, dict[str, int]]()

    def __init__(self, filename: str) -> None:
        self.__relation = Relation("settings_key", "gobject", "prop")
        self.__filepath = path.join(GLib.get_user_config_dir(), Htg.get_default_application().get_application_id(), filename)
        if path.exists(self.__filepath): 
            with open(self.__filepath) as file: self.__settings = json.loads(file.read())
        else: self.__settings = dict()
    
    def save(self):
        parent_path = path.join(GLib.get_user_config_dir(), Htg.get_default_application().get_application_id())
        if not path.exists(parent_path): mkdir(parent_path)
        with open(self.__filepath, "w") as file: file.write(json.dumps(self.__settings))

    def set(self, key: str, value):
        itemlist = self.__relation.get(lambda d: d["settings_key"] == key)
        for item in itemlist:
            # print("Setting", item["prop"], value)
            item["gobject"].set_property(item["prop"], value)
        if len(itemlist) <= 0: self.__settings[key] = value

    def get(self, key: str):
        if key not in self.__settings: return None
        return self.__settings[key]

    def unbind_properties(self, settings_keys: list[str] = None, gobjects: list[GObject] = None, props: list[str] = None): 
        itemlist = self.__relation.delete(lambda d: ((not settings_keys) or d["settings_key"] in settings_keys) and ((not gobjects) or d["gobject"] in gobjects) and ((not props) or d["prop"] in props))
        
        combinations = list[tuple[GObject, str]]()
        for i in range(len(itemlist)):
            for j in range(len(itemlist)):
                combination = itemlist[i]["gobject"], itemlist[j]["prop"]
                if combination not in combinations: combinations.append(combination)
            
        for gobject, prop in combinations:
            length = len(self.__relation.get(lambda d: d["gobject"] == gobject and props or d["prop"] == prop))
            # print(gobject, prop, length)
            if length <= 0: gobject.disconnect(self.__handlers[gobject].pop(prop))
        
    def bind_property(self, settings_key: str, gobject: GObject, prop: str, default_value):
        installable = len(self.__relation.get(lambda d: d["gobject"] == gobject and d["prop"] == prop)) <= 0
        if installable: 
            if gobject not in self.__handlers: self.__handlers[gobject] = dict[str, int]()
            self.__handlers[gobject][prop] = gobject.connect("notify::"+prop, self.__notification)
        self.__relation.insert(settings_key, gobject, prop)
        gobject.set_property(prop, self.__settings[settings_key] if settings_key in self.__settings else default_value)
    
    def __notification(self, gobject, param_spec):
        # print("Changed", gobject.get_property(param_spec.name))
        list = self.__relation.get(lambda d: d["gobject"] == gobject and d["prop"] == param_spec.name)
        for row in list: self.__settings[row["settings_key"]] = gobject.get_property(param_spec.name)
        # print(self.__settings, param_spec.name, settings_keys)
