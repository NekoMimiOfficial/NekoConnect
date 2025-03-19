#!/bin/bash
source ./bin/activate

# Sometimes Wayland doesn't like mouse drag events so we default to Xorg
QT_QPA_PLATFORM=xcb python3 main.py
