import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, CENTER, DISABLED

import Config

def build_labels(main_frame):
    
    row_frame = ttk.Frame(
        main_frame, 
        width = Config.APP_WIDTH,
        height = 25,
        style = "main.TFrame"
    )
    row_frame.pack_propagate(False)
    
    inv_label = ttk.Label(
        row_frame, 
        text = "Inventory CSV",
        style = "main.TLabel"
    )
    
    req_label = ttk.Label(
        row_frame, 
        text = "Requirements CSV",
        style = "main.TLabel"
    )
    
    van_label = ttk.Label(
        row_frame, 
        text = "Van",
        style = "main.TLabel"
    )
    
    clear_label = ttk.Label(
        row_frame,
        text = "Clear",
        style = "main.TLabel"
    )
    
    divider = ttk.Frame(
        main_frame, 
        width = Config.APP_WIDTH - 20,
        height = 2,
        style = "divider.TFrame"
    )
    
    row_frame.pack(pady = (10, 5)) 
    inv_label.pack(side = LEFT, padx = (120, 0))
    req_label.pack(side = LEFT, padx = (150, 0))
    van_label.pack(side = LEFT, padx = (55, 0))
    clear_label.pack(side = LEFT, padx = (25, 0))
    
    divider.pack()

def create_row(main_frame):
    
    row_frame = ttk.Frame(
        main_frame, 
        style = "main.TFrame"
    )
    
    inv_entry = ttk.Entry(
        row_frame,
        width = 20,
        state = DISABLED,
        style = "filename.TEntry",
        font = ('TkDefaultFont', 14),
        justify = "right"
    )
    open_inv_button = ttk.Button(
        row_frame,
        text ='\uD83D\uDCC2',
        style = "symbol.TButton",
        command = lambda : select_file(inv_entry)
    )
    
    req_entry = ttk.Entry(
        row_frame,
        width = 20,
        state = DISABLED,
        style = "filename.TEntry",
        font = ('TkDefaultFont', 14)
    )
    open_req_button = ttk.Button(
        row_frame,
        text='\uD83D\uDCC2',
        style = "symbol.TButton",
        command = lambda : select_file(req_entry)
    )
    
    van_entry = ttk.Entry(
        row_frame,
        width = 4,
        style = "main.TEntry",
        font = ('TkDefaultFont', 14)
    )
    
    clear_button = ttk.Button(
        row_frame,
        text='X',
        style = "symbol.TButton",
        command = lambda : clear_row(inv_entry, req_entry, van_entry)
    )

    open_inv_button.pack(side = LEFT, padx = (20, 0))
    inv_entry.pack(side = LEFT, padx = (2, 0))
    open_req_button.pack(side = LEFT, padx = (30, 0))
    req_entry.pack(side = LEFT, padx = (2, 0))
    van_entry.pack(side = LEFT, padx = (30, 0))
    clear_button.pack(side = LEFT, padx = (30, 0))
    
    van_entry.insert(0, "0")

    row_frame.pack(pady = (10, 0))
    
    return inv_entry, req_entry, van_entry
    
def clear_row(inv_entry, req_entry, van_entry):
    inv_entry.state(["!disabled"])
    inv_entry.delete(0, "end")
    inv_entry.state(["disabled"]) 
    
    req_entry.state(["!disabled"])
    req_entry.delete(0, "end")
    req_entry.state(["disabled"]) 
    
    van_entry.delete(0, "end")
    van_entry.insert(0, "0")

def select_file(entry):
    filetypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open File',
        initialdir='./data',
        filetypes=filetypes
    )

    entry.state(["!disabled"])
    entry.delete(0, "end")
    entry.insert(0, filename)
    entry.xview_moveto(1)
    entry.after(1, entry.xview_moveto, 1)
    entry.state(["disabled"]) 
    
def build_styles(root):
    frame_style = ttk.Style(root)
    frame_style.theme_use('clam')
    frame_style.configure(
        "main.TFrame", 
        background = Config.BLACK
    )
    
    debug_style = ttk.Style(root)
    debug_style.theme_use('clam')
    debug_style.configure(
        "debug.TFrame", 
        background = Config.RED
    )
    
    filename_style = ttk.Style(root)
    filename_style.theme_use('clam')
    filename_style.configure(
        "filename.TEntry",
        fieldbackground = Config.BLACK,
        disabledforeground = 'red'
    )
    
    entry_style = ttk.Style(root)
    entry_style.theme_use('clam')
    entry_style.configure(
        "main.TEntry",
        fieldbackground = Config.DARK_GRAY,
        foreground = Config.LIGHT_GRAY,
    )
    
    open_btn_style = ttk.Style(root)
    open_btn_style.theme_use('clam')
    open_btn_style.configure(
        "symbol.TButton", 
        borderwidth = 0,
        width = 0,
        background = Config.BLACK,
        foreground = Config.LIGHT_GRAY,
        focuscolor = 'none',
        font = ('TkDefaultFont', 14)
    )
    
    btn_style = ttk.Style(root)
    btn_style.theme_use('clam')
    btn_style.configure(
        "main.TButton", 
        background = Config.DARK_GRAY,
        foreground = Config.LIGHT_GRAY,
        focuscolor = 'none',
        font = ('TkDefaultFont', 18)
    )

    label_style = ttk.Style(root)
    label_style .theme_use('clam')
    label_style .configure(
        "main.TLabel", 
        background = Config.BLACK,
        foreground = Config.LIGHT_GRAY,
        font = ('TkDefaultFont', 14, "normal")
    )

    title_style = ttk.Style(root)
    title_style .theme_use('clam')
    title_style .configure(
        "divider.TFrame", 
        background = Config.LIGHT_GRAY,
    )