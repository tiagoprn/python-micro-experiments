#!/usr/bin/env python3
import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

last_clipboard = ""

def callBack(*args):
  global last_clipboard
  new_clipboard = clip.wait_for_text()
  if new_clipboard != last_clipboard:
    last_clipboard = new_clipboard
    print("new Clipboard")
    print(new_clipboard)

clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
clip.connect('owner-change',callBack)
Gtk.main()
