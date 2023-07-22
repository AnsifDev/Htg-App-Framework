import Htg
from os import path

from .Activity import Activity
from gi.repository import Gtk

class ActivityFragment:
    __content = None
    __window_close_request_handler = None
    __started = False

    def __init__(self, parent_activity: Activity, auto_started = True) -> None:
        parent_activity._associate_activity_fragment(self, auto_started)
    
    def _set_content(self, filename: str, id: str = None):
        ui_file_path = path.join("ui", filename)
        self.__builder, self.__content = Htg.get_default_application()._build_ui(ui_file_path, id)

    def _get_content(self): return self.__content

    def _get_window(self): return Htg.get_default_application()._win
    
    def find_view_by_id(self, id: str): return self.__builder.get_object(id)
    
    def _on_create(self): pass

    def _on_started(self, *args): self.__window_close_request_handler = self._get_window().connect("close-request", self._on_window_closing)

    def _on_stopped(self): self._get_window().disconnect(self.__window_close_request_handler)

    def _on_destroy(self): pass

    def _on_window_closing(self, window) -> bool: return False
    
    def perform_start(self): 
        if self.__started: return
        self.__started = True
        self._on_started()

    def perform_stop(self): 
        if not self.__started: return
        self.__started = False
        self._on_stopped()