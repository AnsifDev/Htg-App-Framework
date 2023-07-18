from gi.repository import Gtk, Adw
from .Activity import Activity
from .SubActivity import SubActivity

class ComponentManager:
    __active_activity = None
    __nav_button = None
    __nav_button_clicked_handler = None
    __header_state_changed_cb = None
    __header_attached = True
    __sub_activity_params = dict()
    __stack = list()
    
    def __init__(self, components, gtk_stack, stack_empty_cb) -> None: 
        self.__components = components
        self.__get_stack = gtk_stack
        self.__stack_empty_cb = stack_empty_cb

    def __find_instance(self, component_class):
        for instance in self.__stack:
            if isinstance(instance, component_class): return instance

    def __set_active_activity(self, instance, *args):
        if self.__active_activity:
            self.__active_activity._on_stopped()
        self.__active_activity = instance
        if instance: instance._on_started(*args)
    
    def __btn_clicked(self, *args):
        self._end_activity(self.__stack[-1])

    def set_navigation_button(self, nav_button):
        if self.__nav_button: 
            self.__nav_button.disconnect(self.__nav_button_clicked_handler)

        self.__nav_button = nav_button
        if self.__nav_button: 
            self.__nav_button_clicked_handler = self.__nav_button.connect("clicked", self.__btn_clicked)
        else: self.__nav_button_clicked_handler = None

    def _set_header_state_change_callback(self, cb): self.__header_state_changed_cb = cb

    def start_activity(self, label: str, *args): 
        keys = list()
        for key in self.__sub_activity_params: keys.insert(0, key)
        for sub_activity in keys: 
            self.__sub_activity_params.pop(sub_activity)[0].destroy()
            sub_activity._on_destroy()

        component_class = self.__components[label]["class"]
        single_instanced = self.__components[label]["single-instance"]

        if not issubclass(component_class, Activity): raise Exception("Invalid Activity Class")

        if single_instanced:
            instance = self.__find_instance(component_class)
            if instance:
                if instance == self.__active_activity: return
                self.__stack.remove(instance)
                self.__get_stack.remove(instance._get_content())
            else: 
                instance = component_class()
                instance._on_create()
        else:
            instance = component_class()
            instance._on_create()
        
        if self.__components[label]["custom-header"] ^ (not self.__header_attached) and self.__header_state_changed_cb:
            self.__header_attached = not self.__header_attached
            self.__header_state_changed_cb(self.__header_attached)

        self.__stack.append(instance)
        self.__get_stack.add_child(instance._get_content())
        self.__get_stack.set_visible_child(instance._get_content())
        self.__set_active_activity(instance, *args)
        if self.__nav_button: self.__nav_button.set_visible(not self.is_stack_empty())

    def _end_activity(self, instance): 
        activity_was_active = self.__active_activity == instance

        self.__stack.remove(instance)
        stack_empty = len(self.__stack) < 1

        if activity_was_active:
            keys = list()
            for key in self.__sub_activity_params: keys.insert(0, key)
            for sub_activity in keys: 
                self.__sub_activity_params.pop(sub_activity)[0].destroy()
                sub_activity._on_destroy()
                
            if not stack_empty:
                self.__get_stack.set_visible_child(self.__stack[-1]._get_content())
                self.__set_active_activity(self.__stack[-1])
            else: self.__set_active_activity(None)
        
        self.__get_stack.remove(instance._get_content())
        instance._on_destroy()
        if stack_empty: self.__stack_empty_cb()
        if self.__nav_button: self.__nav_button.set_visible(not self.is_stack_empty())
    
    def start_sub_activity(self, component: Activity|SubActivity, label: str, req_id: int = None, *args):
        component_class = self.__components[label]["class"]
        custom_header = self.__components[label]["custom-header"]

        if not isinstance(component, (Activity, SubActivity)): raise Exception("Invalid Component Class")
        if not issubclass(component_class, SubActivity): raise Exception("Invalid Activity Class")

        window = Adw.Window(transient_for = component._get_window(), default_height = 450, default_width = 340, modal = True)
        main_box = Gtk.Box(orientation = 1)
        window.set_content(main_box)
        if not custom_header: main_box.append(Adw.HeaderBar())

        instance = component_class()
        self.__sub_activity_params[instance] = window, component, req_id
        
        instance._on_create(*args)
        main_box.append(instance._get_content())
        window.present()

    def _get_sub_activity_window(self, instance): return self.__sub_activity_params[instance][0]

    def _end_sub_activity(self, instance: SubActivity, *responses): 
        component: Activity = None
        window, component, request = self.__sub_activity_params.pop(instance)
        window.destroy()

        component._on_sub_activity_returns(request, *responses)
        instance._on_destroy()

    def clear_stack(self): 
        for instance in self.__stack[:-2]:
            self._endActivity(instance)

    def _shutdown(self):
        self.__set_active_activity(None)

        keys = list()
        for key in self.__sub_activity_params: keys.insert(0, key)
        for sub_activity in keys: 
            self.__sub_activity_params.pop(sub_activity)[0].destroy()
            sub_activity._on_destroy()

        for instance in self.__stack:
            self.__get_stack.remove(instance._get_content())
            instance._on_destroy()
        
        self.__stack.clear

    def is_stack_empty(self) -> bool: return len(self.__stack) < 2
