#!/usr/bin/env python3

from asciimatics.effects import Print
from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, ListBox, MultiColumnListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, PopUpDialog, Divider, THEMES
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.renderers import FigletText
import sys
import os
import time
import datetime
from configparser import ConfigParser
from collections import namedtuple

VERSION = "01.00"

DEFAULT_DATA_PATH = os.path.expanduser("~/.tac1")

DEBUG = True

class colors:
    RED = (245, 90, 66)
    ORANGE = (245, 170, 66)
    YELLOW = (245, 252, 71)
    GREEN = (92, 252, 71)
    BLUE = (71, 177, 252)
    PURPLE = (189, 71, 252)
    WHITE = (255, 255, 255)

#def initColorIt():
#    os.system("cls")

def color(text, rgb):
    return "\033[38;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) +"m" + text + "\033[0m"
    
def background(text, rgb):
    return "\033[48;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) +"m" + text + "\033[0m"


# 3-tuple of (foreground colour, attribute, background colour)
THEMES["jayz"]= \
{
    "background": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "shadow": (Screen.COLOUR_BLUE, None, Screen.COLOUR_BLUE),
    "disabled": (Screen.COLOUR_BLUE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "invalid": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_RED),
    "label": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "borders": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "scroll": (Screen.COLOUR_CYAN, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "title": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "edit_text": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "focus_edit_text": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "readonly": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "focus_readonly": (Screen.COLOUR_CYAN, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "button": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "focus_button": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_WHITE),
    "control": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "selected_control": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "focus_control": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "selected_focus_control": (Screen.COLOUR_BLUE, Screen.A_BOLD, Screen.COLOUR_WHITE),
    "field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "selected_field": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLACK),
    "focus_field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK),
    "selected_focus_field": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_WHITE),
}


# global buffering object
_LOG_BUFFER = sys.stdout if not DEBUG else open("tac1.log", 'wb')

def lprint(msg):
    """Print to stout and log into file"""
    if DEBUG:
        _LOG_BUFFER.write((msg + "\n").encode('UTF-8'))
        _LOG_BUFFER.flush()

class TempDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

def format_tpl(tpl, data):
    return tpl.format_map(TempDict(**data))

class Notebook():

    def __init__(self, path=DEFAULT_DATA_PATH):
        self._path = path
        self.current_id = None
        self.notes = dict()
        os.makedirs(path, exist_ok=True)
        for root, dirs, files in os.walk(path):
            for file in files:
                note_path = root + os.sep + file
                n = Note(note_path)
                self.notes[file] = n
        #print(self.notes.keys())

    def new_note(self, title, tags, content):
        file_name = str(time.time())
        note_path = self._path + os.sep + file_name
        note = Note(note_path, title, tags, content)
        note.write()
        self.notes[file_name] = note
        return note

    def set_note(self, file_name, title, tags, content):
        note = self.notes[file_name]
        note.title = title
        note.tags = tags
        note.content = content
        note.write()
        return note

    def get_indexed_note_list(self):
        #return sorted([([color(n.time , colors.BLUE), n.title, color(n.tags, colors.ORANGE)], k) for k,n in self.notes.items()])
        return sorted([([n.time, n.title, n.tags], k) for k,n in self.notes.items()])

    def delete(self, file_name):
        if file_name in self.notes:
            del self.notes[file_name]
        note_path = self._path + os.sep + file_name 
        if os.path.exists(note_path):
            os.remove(note_path)

                
NOTE_CONTENT_TPL = \
"""[title]: {TITLE}
[tags]: {TAG_LIST}
[time]: {TIME}
{CONTENT}
"""
class Note():

    def __init__(self, path, 
                    title="", 
                    tags="", 
                    content=""):
        self.title = title
        self.tags = tags
        self.time = ""
        self.content = content
        self._path = path
        #print(self._path)
        if os.path.exists(self._path):
            self.read()

    @classmethod
    def format_note(cls, title, tag_list, time, content):
        params = \
        {
            "TITLE" : title,
            "TAG_LIST" : tag_list,
            "TIME" : time,
            "CONTENT" : content,
        }
        return format_tpl(NOTE_CONTENT_TPL, params)

    def read(self):
        with open(self._path, "r") as fr:
            content = fr.readlines()
            #print(content)
            if len(content) > 2:
                self.title = content[0].replace("[title]: ", "").replace("\n", "")
                self.tags = content[1].replace("[tags]: ", "").replace("\n", "")
                self.time = content[2].replace("[time]: ", "").replace("\n", "")
                self.content = "".join(content[3:])

    def write(self):
        self.time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        with open(self._path, "w") as fw:
            fw.write(str(self))

    def __str__(self):
        return self.format_note(self.title, self.tags, self.time, self.content)

#############

class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height,
                                       screen.width,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Note List")
        self.set_theme("jayz")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = MultiColumnListBox(
            Widget.FILL_FRAME,
            columns=["<25%", "<50%", "<25%"],
            options=self._model.get_indexed_note_list(),
            titles=["Modified", "Title", "Tags"],
            name="note",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit)

        self._delete_button = Button("-", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("+", self._add), 0)
        layout2.add_widget(self._delete_button, 1)
        layout2.add_widget(Button("X", self._quit), 2)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        #self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_indexed_note_list()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Note")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["note"]
        raise NextScene("Edit Note")

    def _delete(self):
        self.save()
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        on_close=self._delete_on_yes))

    def _delete_on_yes(self, selected):
        if selected == 0:
            self._model.delete(self.data["note"])
            self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('x'), ord('X'), Screen.ctrl("c")]:
                raise StopApplication("User quit")
            elif event.key_code in [ord('+')]:
                self._add()
            elif event.key_code in [ord('-')]:
                self._delete()

        return super().process_event(event)

class MyTextBox(TextBox):

    def _draw_label(self):
        self._display_label = None


class NoteView(Frame):
    def __init__(self, screen, model):
        super(NoteView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Note Details",
                                          reduce_cpu=True)
        self.set_theme("jayz")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Title:", "title"))
        layout.add_widget(Text("Tags:", "tags"))
        layout.add_widget(Divider())
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Text:", "content", as_string=True, line_wrap=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(NoteView, self).reset()
        if self._model.current_id is None:
            self.data = \
            {
                "title": "", 
                "tags": "", 
                "content": "",
            }
        else:
            n = self._model.notes[self._model.current_id]
            self.data = \
            {
                "title": n.title, 
                "tags": n.tags, 
                "content": n.content,
            }

    def _ok(self):
        self.save()
        if self._model.current_id is None:
            note = self._model.new_note(self.data["title"], 
                                        self.data["tags"], 
                                        self.data["content"])
        else:
            n = self._model.notes[self._model.current_id]
            n.title = self.data["title"]
            n.tags = self.data["tags"]
            n.content = self.data["content"]
            n.write()
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


def setup(screen, scene):
    effects = [
        Print(screen, FigletText("TAC1", font="standard"),
                y=screen.height//2-3, 
                stop_frame=50),
        Print(screen, FigletText(VERSION, font="term"),
                y=screen.height//2-3, 
                stop_frame=50),
    ]
    scenes = [
        Scene(effects, 0),
        Scene([ListView(screen, the_notebook)], -1, name="Main"),
        Scene([NoteView(screen, the_notebook)], -1, name="Edit Note")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


the_notebook = Notebook()

def main():
    last_scene = None
    while True:
        try:
            Screen.wrapper(setup, catch_interrupt=True, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene

if __name__ == "__main__":
    main()
    