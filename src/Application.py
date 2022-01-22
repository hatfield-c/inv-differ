import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import Label
from tkinter import Entry
from tkinter.messagebox import showinfo

import Config
import UIGen

def main():
    root = tk.Tk()
    root.title('Inventory Check')
    root.iconbitmap("media/icon.ico")
    root.resizable(False, False)
    root.geometry(str(Config.APP_WIDTH) + 'x' + str(Config.APP_HEIGHT))
    
    UIGen.build_styles(root)
    
    main_frame = ttk.Frame(root, width = Config.APP_WIDTH, height = Config.APP_HEIGHT, style = "main.TFrame")
    main_frame.pack_propagate(False)
    
    UIGen.build_labels(main_frame)
    
    entries = []
    for i in range(10):
        inv_entry, req_entry, van_entry = UIGen.create_row(main_frame)
        
        all_entry = {
            "inv": inv_entry,
            "req": req_entry,
            "van": van_entry
        }
        
        entries.append(all_entry)
    
    process_button = ttk.Button(
            main_frame,
            text='Go',
            style = "main.TButton",
            command = lambda : process_files(entries)
        )
    
    process_button.pack(pady = (50, 0))
    main_frame.pack(expand=True)
    
    root.mainloop()

def process_files(entries):
    
    results = []
    for all_entry in entries:
        inv_entry = all_entry["inv"]
        req_entry = all_entry["req"]
        van_entry = all_entry["van"]
        
        inv_path = inv_entry.get()
        req_path = req_entry.get()
        van_id = van_entry.get()
        
        if inv_path == "" or req_path == "":
            continue
        
        if van_id == "":
            van_id = 0
        
        result = {
            "reorder": reorder_check(inv_path, req_path),
            "van": van_id
        }
        
        if result["reorder"] is None:
            return
        
        results.append(result)
        
    for result in results:
        reorder = result["reorder"]
        van_id = result["van"]
        
        out_path = Config.OUT_PATH + "_van" + str(van_id) + ".csv"

        try:
            with open(out_path, "w", newline = Config.NEWLINE) as f:
                writer = csv.writer(f, delimiter = Config.DELIMITER)
                writer.writerows(reorder)
        except:
            write_error(out_path)
        
    notify_complete()

def reorder_check(inv_path, req_path):
        
    try:
        inv = get_inv(inv_path)
    except:
        read_error(inv_path)
        return None
    
    if inv is None:
        return None
    
    try:
        req, orig_names = get_req(req_path)
    except:
        read_error(req_path)
        return None
   
    if req is None:
        return None
     
    reorders = []
    
    for name in req:
        if name not in inv:
            inv[name] = 0
            
        inv_qty = inv[name]
        req_data = req[name]
        
        if inv_qty < req_data["reorder"]:
            orig_name = orig_names[name]
            restock = req_data["restock"]
            
            entry = [ orig_name, str(restock) ]
            
            reorders.append(entry)
    
    return reorders

def get_inv(inv_path):
    inv = {}
    
    with open(inv_path, newline = Config.NEWLINE) as f:
        reader = csv.reader(f, delimiter = Config.DELIMITER)
        
        while True:
            name = next(reader, None)
            qty = next(reader, None)
            
            if name is None or qty is None:
                break
            
            name = name[0]
            orig = name
            qty = qty[0]
            
            name = name.replace(" ", "")
            
            empty = next(reader, None)
            empty = next(reader, None)
            empty = next(reader, None)
            
            if name in inv:
                duplicate_error(orig, inv_path)
                return None
                
            if not qty.isdigit():
                qty_error(orig, qty, inv_path)
                return None
                
            inv[name] = int(qty)
            
    return inv

def get_req(req_path):
    req = {}
    orig_names = {}
    
    with open(req_path, newline = Config.NEWLINE) as f:
        reader = csv.reader(f, delimiter = Config.DELIMITER)
        
        for row in reader:

            if len(row) < 2:
                continue
            
            name = row[0]
            restock = row[1]
            reorder = row[2]
            
            orig_name = name
            name = name.replace(" ", "")

            if name in req:
                duplicate_error(orig_name, req_path)
                return None, None
                
            if not restock.isdigit():
                qty_error(orig_name, restock, req_path)
                return None, None
            
            if not reorder.isdigit():
                qty_error(orig_name, reorder, req_path)
                return None, None
            
            req[name] = {
                "restock": int(restock),
                "reorder": int(reorder)
            }
            orig_names[name] = orig_name
                    
    return req, orig_names

def read_error(path):
    msg = "[ERROR!]\n\nCould not read the file at the following path:\n\n'" + path + "'\n\nAborting inventory check."
    
    showinfo(
        title='Read Error',
        message = msg
    )
    
def write_error(path):
    msg = "[ERROR!]\n\nCould not write the reorder file at the following path:\n\n" + path + "\n\nAborting inventory check."
    
    showinfo(
        title='Read Error',
        message = msg
    )

def qty_error(name, qty, path):
    msg = "[ERROR!]\n\nThere is a problem with the file at the following path:\n\n" + path + "\n\nThe quantity of name '" + name + "' is invalid. Quantity given as '" + str(qty) + "', but this program expects an integer."
    
    showinfo(
        title='Quantity Error',
        message = msg
    )

def duplicate_error(duplicate, path):
    msg = "[ERROR!]\n\nThere is a problem with the file at the following path:\n\n" + path + "\n\nThe name '" + duplicate + "' was detected twice."
    
    showinfo(
        title='Duplicate Error',
        message = msg
    )

def notify_complete():
    msg = "Inventory check complete."
    
    showinfo(
        title='Success!',
        message = msg
    )

main()