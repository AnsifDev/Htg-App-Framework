import os, gi, Htg

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, Adw
from .ComponentManager import ComponentManager
from .Settings import Settings

class Application(Adw.Application):
    __manifest = None
    __component_manager = None
    __settings_refs = list[Settings]()

    def get_default(): return Htg.get_default_application()

    def _get_component_manager(self) -> ComponentManager: return self.__component_manager

    def __stack_empty_cb(self):
        self._win.close()

    def __header_state_changed(self, state):
        if state: self.__main_box.prepend(self.__header)
        else: self.__main_box.remove(self.__header)

    def __init__(self, app_id, manifest: dict, pkg_dir: str, *args, **kwargs):
        super().__init__(application_id=app_id, *args, **kwargs)
        
        self.__manifest = manifest
        self.__pkg_dir = pkg_dir

        self.connect("activate", self.__activate)
        self.connect("shutdown", self.__shutdown)

        theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        theme.add_search_path(self._actual_path("icons"))

    def _build_ui(self, ui_file_path: str, id: str = None):
        builder = Gtk.Builder.new_from_file(self._actual_path(ui_file_path))
        if id: return builder, builder.get_object(id)

        objects = builder.get_objects()
        for object in objects:
            if type(object) == Adw.Bin: return builder, object
        
        return builder, None
    
    def __build_window(self):
        builder = Gtk.Builder.new_from_file(os.path.join("/", *tuple(os.path.abspath(__file__).split("/")[:-2]), "ui/window.ui"))
        win = builder.get_object("window")
        win.set_application(self)

        self.__main_box = builder.get_object("main_box")
        self.__header = builder.get_object("header")
        self.__stack = builder.get_object("stack")
        self.__nav_button = builder.get_object("back")

        # style_mgr = Adw.StyleManager.get_default()
        # style_mgr.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

        return win

    def add_flag(self, flag): self.set_flags(self.get_flags() | flag)
    
    def remove_flag(self, flag): self.set_flags(self.get_flags() & ~flag)

    def register_activity(self, label: str, activity_class: type):
        self.__activities[label] = activity_class
    
    def _actual_path(self, path: str): 
        return os.path.join(self.__pkg_dir, path)

    def get_settings(self, filename: str) -> Settings:
        s = Settings(filename)
        self.__settings_refs.append(s)
        return s

    def __activate(self, *args):
        self._win = self.props.active_window
        if not self._win: 
            self._win = self.__build_window()
            self.__component_manager = ComponentManager(self.__manifest["components"], self.__stack, self.__stack_empty_cb)
            self.__component_manager.set_navigation_button(self.__nav_button)
            self.__component_manager._set_header_state_change_callback(self.__header_state_changed)

            if "launcher" in self.__manifest:
                self.__component_manager.start_activity(self.__manifest["launcher"])
            else: self.__stack.add_child(self._build_ui(os.path.join("/", *tuple(os.path.abspath(__file__).split("/")[:-2]), "ui/demo.ui"), "root")[1])
        self._win.present()

    def __shutdown(self, *args):
        self.__component_manager._shutdown()
        for settings in self.__settings_refs: settings.save()

def main():
    """The application's entry point."""
    app = Application()
    return app.run()
