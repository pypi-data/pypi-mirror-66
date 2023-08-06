#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""romkan.py - a Python rewrite of the Perl Romaji<->Kana conversion module.

Romkan Copyright (C) 2000 Satoru Takabayashi <satoru-t@is.aist-nara.ac.jp>

romkan.py Copyright (C) 2006 Eric Nichols <eric-n@is.naist.jp>
    All rights reserved.
    This is free software with ABSOLUTELY NO WARRANTY.

You can redistribute it and/or modify it under the terms of
the GNU General Public License version 2.

Modified by Jason Moiron to work with utf-8 instead of euc-jp

Modified by Tart to be specific to UTAU
"""

__author__ = "Tart"
__author_email__ = "conemusicproductions@gmail.com"
__version__ = "1.2.0"
__revision__ = "1"


import tkinter as tk
from tkinter import *

from convert import *

#  Creates empty window
root = Tk()
root.geometry("400x400")
root.title("utaromkan")

#  Sets variables for determining if string is hiragana
hiraganaVar = tk.IntVar()

isHiragana = 0


def set_hiragana():
    global isHiragana
    isHiragana = 1


def set_romaji():
    global isHiragana
    isHiragana = 0


#  Creates radio buttons for selecting conversion method
romajiButton = Radiobutton(root, variable=hiraganaVar, value=0, text="Romaji -> Hiragana", command=set_romaji)
hiraganaButton = Radiobutton(root, variable=hiraganaVar, value=1, text="Hiragana -> Romaji", command=set_hiragana)
romajiButton.pack()
hiraganaButton.pack()

#  Creates input text label
inputLabel = Label(root, text="Input Text")
inputLabel.pack()

#  Creates entry box for input text
inputEntry = Entry(root)
inputEntry.pack()


#  Function for converting string when convert button is pressed
def convert_on_click():
    if isHiragana == 0:
        text_output = romgan(inputEntry.get())
        output_text = Text(root, height=1)
        output_text.insert(1.0, text_output)
        output_text.pack()
        output_text.configure(bg=root.cget('bg'), relief="flat")
        output_text.configure(state="disabled")
    else:
        text_output = ganrom(inputEntry.get())
        output_text = Text(root, height=1)
        output_text.insert(1.0, text_output)
        output_text.pack()
        output_text.configure(bg=root.cget('bg'), relief="flat")
        output_text.configure(state="disabled")


#  Creates conversion button
convertButton = Button(root, text="Convert", command=convert_on_click)
convertButton.pack()

#  Creates label for output text
outputLabel = Label(root, text="Output Text")
outputLabel.pack()

root.mainloop()
