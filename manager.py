import psycopg2
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
#database
db = psycopg2.connect("dbname=postgres user=postgres password=2130")
k = db.cursor()

def add_character(def_name = "", def_str = 10, def_multi = 0, def_flat = 0, var = 0):
    char_frame = tk.Toplevel()
    if var == 0:
        char_frame.title("Add Character")
    else:
        char_frame.title("Edit Character")
    char_frame.geometry("300x200")
    char_frame.resizable(False, False)
    
    #Name
    name_label = ttk.Label(char_frame, text = "Name:")
    name_var = tk.StringVar()
    name_entry = ttk.Entry(char_frame, textvariable=name_var)
    name_var.set(def_name)
    name_entry.focus_set

    #Strength
    strength_label = ttk.Label(char_frame, text = "Strength:")
    strength_var = tk.StringVar()
    strength_box = ttk.Spinbox(char_frame, from_ = 1, to = 100, textvariable=strength_var)
    strength_var.set(def_str)

    #Carry capacity increases
    carry_capacity_increases = ttk.Label(char_frame, text = "Carry capacity increases", font = "Calibri 10 bold")

    #Multiplier
    multiplier_label = ttk.Label(char_frame, text = "Multiplier:")
    multiplier_var = tk.StringVar()
    multiplier_entry = ttk.Combobox(char_frame, textvariable=multiplier_var, state = "readonly")
    multipliers = ["1x", "2x", "4x", "8x", "16x", "32x"]
    multiplier_entry["values"] = multipliers
    if def_multi == 0:
        multiplier_var.set(multipliers[def_multi])
    else:
        multiplier_var.set(str(def_multi)+"x")

    #Flat increase
    flat_label = ttk.Label(char_frame, text = "Flat increase (lb):")
    flat_var = tk.StringVar()
    flat_entry = ttk.Entry(char_frame, textvariable=flat_var)
    flat_var.set(def_flat)

    #Buttons
    if var == 0:
        add_button = ttk.Button(char_frame, text = "Create", command = lambda: (add_character_c(name_var.get(), strength_var.get(), multiplier_var.get(), flat_var.get()), char_frame.destroy()))
    elif var == 1:
        add_button = ttk.Button(char_frame, text = "Update", command = lambda: (add_character_c(name_var.get(), strength_var.get(), multiplier_var.get(), flat_var.get(), var = 1), char_frame.destroy()))
    cancel_button = ttk.Button(char_frame, text = "Cancel", command = lambda: char_frame.destroy())

    #Max carry
    max_carry_label = ttk.Label(char_frame, text = "Max carry:")
    limit = tk.IntVar(value = 2)
    max_carry_label2 = ttk.Label(char_frame, textvariable=limit)
    limit.set(150)
    if var == 1: 
        limit.set(calculate_weight(0, strength_var.get(), multiplier_var.get(), flat_var.get()))

    #Binds
        #Strength
    strength_box.bind("<<Increment>>", lambda event: limit.set(calculate_weight(1, strength_var.get(), multiplier_var.get(), flat_var.get())))
    strength_box.bind("<<Decrement>>", lambda event: limit.set(calculate_weight(-1, strength_var.get(), multiplier_var.get(), flat_var.get())))
    strength_box.bind("<KeyPress>", lambda event: keybind1(False, event))
    strength_box.bind("<KeyRelease>", lambda event: limit.set(calculate_weight(0, strength_var.get(), multiplier_var.get(), flat_var.get())))
        #Multiplier
    multiplier_entry.bind("<<ComboboxSelected>>", lambda event: limit.set(calculate_weight(0, strength_var.get(), multiplier_var.get(), flat_var.get())))
        #Flat
    flat_entry.bind("<KeyPress>", lambda event: keybind1(False, event))
    flat_entry.bind("<KeyRelease>", lambda event: limit.set(calculate_weight(0, strength_var.get(), multiplier_var.get(), flat_var.get())))

    def places():
        #place name
        name_label.place(relx = 0.17, rely = 0.05)
        name_entry.place(relx = 0.51, anchor="nw", rely = 0.05, relwidth=0.43)
        #place strength
        strength_label.place(relx = 0.17, rely = 0.18)
        strength_box.place(relx = 0.51, rely = 0.18, relwidth=0.43, anchor="nw")
        #Carry capacity increases label
        carry_capacity_increases.place(relx = 0.5, rely = 0.4, anchor="n" )
        #place multiplieer
        multiplier_label.place(relx = 0.17, rely = 0.52)
        multiplier_entry.place(relx = 0.51, rely = 0.52, anchor="nw", relwidth=0.43)
        #place flat increase
        flat_label.place(relx = 0.17, rely = 0.67)
        flat_entry.place(relx = 0.51, rely = 0.66, relwidth=0.43, anchor="nw")
        #place Buttons
        add_button.place(relx = 0.49, rely = 0.78, anchor='ne')
        cancel_button.place(relx = 0.51, rely = 0.78,  anchor="nw")
        #place Max Carry
        max_carry_label.place(relx = 0.49, rely = 1, anchor= "se")
        max_carry_label2.place(relx = 0.51, rely = 1, anchor= "sw")
        char_frame.update()
    places()

def add_character_c(name, strength, multiplier, flat, var = 0):
    global characters

    if not name:
        message = tk.messagebox.showerror(title = "Character not created", message = "Name field empty, character not created.")
        return
    if not strength:
        message = tk.messagebox.showerror(title = "Character not created", message = "Strength score field empty, character not created.")
        return
    if not flat:
        flat = 0
    if var == 0 and name in characters:
        message = tk.messagebox.showerror(title = "Character not created", message = "Character name already exists.")
        return
    m = ''.join(x for x in multiplier if x.isdigit())
    if var == 0:
        k.execute("SELECT MAX(id) FROM characters;")
        answer_id = k.fetchall()[0][0]
        if not answer_id:
            id = 1
        else:
            id = answer_id + 1
        k.execute("INSERT INTO characters (id, name, strength, multiplier, flat) VALUES (%s, %s, %s, %s, %s);", (id, name, strength, m, flat))
        db.commit()
        characters.append(name)
        characters = sorted(characters, key=str.casefold)
        character.set(name)
        char_select["values"] = characters
        updates()
        message = tk.messagebox.showinfo(title = "Character created", message = "Character created successfully!")
    elif var == 1:
        k.execute("UPDATE characters SET name = %s, strength = %s, multiplier = %s, flat = %s WHERE name = %s;", (name, strength, m, flat, character.get()))
        db.commit()
        old_name = character.get()
        new_name = name
        characters.remove(old_name)
        characters.append(new_name)
        character.set(new_name)
        characters = sorted(characters, key=str.casefold)
        char_select["values"] = characters
        updates()
        message = tk.messagebox.showinfo(title = "Character updated", message = "Character updated successfully!")

def add_item():
    item_frame = tk.Toplevel()
    item_frame.title("Add item")
    item_frame.geometry("400x450")
    item_frame.minsize(400, 450)
    #Searchbar
    search_frame = ttk.Frame(item_frame, borderwidth=0.5, relief=GROOVE)
    search_label = ttk.Label(search_frame, text = "Search items:")
    search_var = tk.StringVar()
    search = ttk.Entry(search_frame, textvariable=search_var)
    search.focus_set()
    #Pack searchbar
    search_frame.pack(pady = 10, ipady = 4)
    search_label.pack(side = "left", padx = 5)
    search.pack(side = "left", padx = 5)
    #Items tree
    items_label = ttk.Label(item_frame, text = "List of items:", font = 'calibri 14 bold')
    items_frame = ttk.Frame(item_frame)
    items = ttk.Treeview(items_frame, columns = ("name", "price", "weight"), show = "headings")
    items.heading("name", text = "Name")
    items.heading("price", text = "Price (gp)")
    items.heading("weight", text = "Weight (lb)")
    items.column("name", width=245)
    items.column("price", width=70)
    items.column("weight", width=70)
    #Items scrollbar
    items_scrollbar = ttk.Scrollbar(items_frame, orient = "vertical", command = items.yview)
    items.configure(yscrollcommand=items_scrollbar.set)
    #Populate items
    k.execute("SELECT * FROM items;")
    for row in k:
        items.insert(parent = '', index = row[0], values = (row[1], row[2], row[3]))
    #get description
    info = ttk.Label(item_frame, text = "*Double click item for additional information")
    #Amount
    amount_frame = ttk.Frame(item_frame)
    amount_label = ttk.Label(amount_frame, text = "Amount:")
    amount_var = tk.StringVar()
    amount_box = ttk.Spinbox(amount_frame, from_ = 1, to = 1000, textvariable=amount_var)
    amount_var.set(1)
    #Events:
    search.bind("<KeyPress>", lambda event: find(search_var.get(), items, event.char))
    amount_box.bind("<KeyPress>", lambda event: keybind1(False, event))
    items.bind("<Double-Button-1>", lambda event: get_info(items.item(items.focus())['values'][0]))
    #Buttons
    button_frame = ttk.Frame(item_frame)
    add_item_button = ttk.Button(button_frame, text = "Add item", command = lambda: add_item_c(items, amount_var))
    cancel = ttk.Button(button_frame, text = "Cancel", command = lambda: item_frame.destroy())
    #Layout
    items_label.pack()
    items_frame.pack(expand = True, fill = "both")
    items.pack(side = "left", expand = True, fill = "both")
    items_scrollbar.pack(side = "left", fill = "y")
    info.pack(padx = 5, pady = 10, fill = "x")
    amount_frame.pack()
    amount_label.pack(side = "left")
    amount_box.pack(side = "left")
    button_frame.pack(pady = 15)
    add_item_button.pack(side = "left", padx = 5)
    cancel.pack(side="left", padx = 5)

def add_item_c(tree, amount, var = 0):
    if var == 0:
        amount = amount.get()
        if not amount:
            message = tk.messagebox.showerror(title = "Item not added", message = "Amount field empty.")
            return
        try:
            item = tree.item(tree.focus())['values'][0] 
        except IndexError: 
            item = ""
        if not item:
            message = tk.messagebox.showerror(title = "Item not added", message = "No item selected.")
            return
    elif var == 1:
        item = tree
    k.execute("SELECT id FROM items WHERE name = %s;", (item, ))
    item_id = k.fetchall()[0][0]
    k.execute("SELECT id FROM characters WHERE name = %s;", (character.get(), ))
    character_id = k.fetchall()[0][0]
    k.execute("SELECT COUNT(*) FROM inventory WHERE char_id = %s AND item_id = %s", (character_id, item_id))
    if k.fetchall()[0][0] != 0:
        k.execute("UPDATE inventory SET amount = amount + %s WHERE char_id = %s AND item_id = %s", (amount, character_id, item_id))
        db.commit()
        message = tk.messagebox.showinfo(title = "Item added", message = "Item amount updated successfully!")
    else:
        k.execute("INSERT INTO inventory (char_id, item_id, amount) VALUES (%s,%s,%s);", (character_id, item_id, amount))
        db.commit()
        if var == 0:
            message = tk.messagebox.showinfo(title = "Item added", message = "Item added successfully!")
    updates()

def calculate_weight(var, strength, multiplier, flat_increase):

    if strength == "":
        return 0
    if int(strength) + int(var) > 100 or int(strength) + int(var) < 1:
        var = 0
    if flat_increase == "":
        flat_increase = 0
    m = ''.join(x for x in multiplier if x.isdigit())
    limit = (int(strength)+var) * 15 * int(m) + int(flat_increase)
    return limit

def change_amount(val, tree):
    try:
        name = tree.item(tree.focus())['values'][0]
    except IndexError:
        tk.messagebox.showerror(title = "Not selected", message = "No item selected")
        return
    name = str(name)
    k.execute("UPDATE inventory SET amount = amount + %s \
                WHERE char_id = (SELECT id FROM characters WHERE name = %s) \
                AND item_id = (SELECT id FROM items where name = %s);", (val, character.get(), name, ))
    db.commit()
    k.execute("SELECT amount FROM inventory \
                WHERE char_id = (SELECT id FROM characters WHERE name = %s) \
                AND item_id = (SELECT id FROM items where name = %s);", (character.get(), name))
    if k.fetchall()[0][0] < 1:
        k.execute("DELETE FROM inventory \
                    WHERE char_id = (SELECT id FROM characters WHERE name = %s) \
                    AND item_id = (SELECT id FROM items where name = %s);", (character.get(), name))
        db.commit()
    updates()
    tree.focus_set()
    children = tree.get_children()
    for child in children:
        if tree.item(child)["values"][0] == name:
            tree.focus(child)
            tree.selection_set(child)

def clear():
    message = tk.messagebox.askquestion(title = "Confirmation", message = f"Please confirm if you want to delete all items from {character.get()}'s inventory:")
    if message == "yes":
        k.execute("DELETE FROM inventory WHERE char_id = (SELECT id FROM characters WHERE name = %s);", (character.get(), ))
        db.commit()
        updates()

def create_item():
    new_item_frame = tk.Toplevel()
    new_item_frame.title("Create item")
    new_item_frame.geometry("450x250")
    new_item_frame.minsize(450,250)
    #frames
    left_frame = ttk.Frame(new_item_frame)
    right_frame = ttk.Frame(new_item_frame)
    left_frame.place(relx = 0, rely = 0, relheight=1, relwidth=0.4)
    right_frame.place(relx = 0.4, rely = 0, relheight=1, relwidth=0.6)
    #labels left frame
    name_label = ttk.Label(left_frame, text = "Item name:")
    price_label = ttk.Label(left_frame, text = "Item price (gp):")
    weight_label = ttk.Label(left_frame, text = "Item weight (lb):")
    #entry vars left frame
    name_var = tk.StringVar()
    price_var = tk.StringVar()
    weight_var = tk.StringVar()
    add_to_char_var = tk.BooleanVar()
    #Widgets left frame
    name_entry = ttk.Entry(left_frame, textvariable = name_var)
    price_entry = ttk.Entry(left_frame, textvariable = price_var)
    weight_entry = ttk.Entry(left_frame, textvariable = weight_var)
    add_to_char = ttk.Checkbutton(left_frame, text = "Add to current character", 
                                  variable=add_to_char_var,onvalue=True,offvalue=False)
    create_button = ttk.Button(left_frame, text = "Create item", command = lambda: 
                               create_item_c(name_var.get(), price_var.get(), weight_var.get(), 
                                             description.get("1.0",'end-1c'), add_to_char_var.get(), new_item_frame))
    #Events
    price_entry.bind("<KeyPress>", lambda event: keybind1(1, event))
    weight_entry.bind("<KeyPress>", lambda event: keybind1(1, event))
    #Layout left frame
    name_label.place(relx = 0.05, rely = 0.02)
    name_entry.place(relx = 0.05, rely = 0.1, relwidth=0.7)
    name_entry.focus_set()
    price_label.place(relx = 0.05, rely = 0.22)
    price_entry.place(relx = 0.05, rely = 0.3, relwidth=0.7)
    weight_label.place(relx = 0.05, rely = 0.42)
    weight_entry.place(relx = 0.05, rely = 0.5, relwidth=0.7)
    add_to_char.place(relx = 0.05, rely = 0.7)
    create_button.place(relx = 0.5, rely = 0.925, anchor="center")
    #Widgets rigth frame
    description_label = ttk.Label(right_frame, text = "Item description:")
    description = tk.Text(right_frame)
    cancel_button = ttk.Button(right_frame, text = "Cancel", command = new_item_frame.destroy)
    #Layout right frame
    description_label.place(relx = 0.05, rely = 0.02)
    description.place(relx = 0.05, rely = 0.1, relwidth=0.9, relheight= 0.75)
    cancel_button.place(relx = 0.5, rely = 0.925, anchor="center")

def create_item_c(name, price, weight, description, add, window):
    if not name:
        info_window("Name field left blank.")
        return
    elif not price:
        info_window("Price field left blank.")
        return
    elif not weight:
        info_window("Weight field left blank.")
        return
    elif not description:
        info_window("Description field left blank.")
        return
    k.execute("SELECT COUNT(*) FROM items WHERE name = %s", (name, ))
    if k.fetchall()[0][0] > 0:
        info_window("Item name already exists")
        return

    k.execute("INSERT INTO items (name, price, weight, description) VALUES (%s, %s, %s, %s)", (name, float(price), float(weight), description, ))
    db.commit()
    message = tk.messagebox.showinfo(title = "Item created", message = "Item created successfully!")
    if add:
        add_item_c(name, 1, 1)
    window.destroy()

def delete_character():
    global characters
    message = tk.messagebox.askquestion(title = "Confirmation", message = "Please confirm that you want to delete this character and their inventory:")
    if message == "yes":
        k.execute("DELETE FROM inventory WHERE char_id = (SELECT id FROM characters WHERE name = %s);", (character.get(), ))
        k.execute("DELETE FROM characters WHERE name = %s;", (character.get(),))
        db.commit()
        characters.remove(character.get())
        characters = sorted(characters, key=str.casefold)
        char_select["values"] = characters
        if len(characters) > 0:
            char_select.set(characters[0])
        else:
            char_select.set("")
        updates()
    return

def edit_character():
    k.execute("SELECT * FROM characters WHERE name = %s;",(character.get(), ))
    stats = k.fetchall()
    add_character(stats[0][1], stats[0][2], stats[0][3], stats[0][4], var = 1)
    update_strength_bar()

def find(search_var, items, char, var = 0 ):
    if char == '\x08':
        new = search_var[:-1]
    else:
        new = search_var + char
    if var == 0:
        k.execute("SELECT * FROM items WHERE name ILIKE %s;", ('%'+new+'%', ))
    else:
        char_name = str(character.get())
        k.execute("SELECT name, amount, price, weight FROM items INNER JOIN inventory ON inventory.item_id=items.id WHERE char_id = (SELECT id FROM characters WHERE name = %s) AND items.name ILIKE %s", (char_name, '%'+new+'%',))
    new2 = k.fetchall()
    items.delete(*items.get_children())
    if var == 0:
        for row in new2:
            items.insert(parent = '', index = row[0], values = (row[1], row[2], row[3]))
    else:
        if new == "":
            update_inventory()
            return
        for row in new2:
            items.insert(parent = '', index = new2.index(row), values = (row[0], row[1], row[2]*row[1], row[3]*row[1]))

def get_info(item):
    info_window = tk.Toplevel()
    info_window.geometry("400x200")
    info_window.title("Information")
    frame = tk.Frame(info_window, bg="#%02x%02x%02x" % ((252, 234, 116)))
    k.execute("SELECT description FROM items WHERE name = %s;", (item, ))
    desc = k.fetchall()[0][0]
    info = ttk.Label(frame, text = desc, wraplength = 180, background="#%02x%02x%02x" % ((252, 234, 116)))
    close_button = ttk.Button(frame, text = "Close", command = lambda: info_window.destroy())
    #Pack
    frame.pack(fill="both", expand = True)
    info.pack(side = "top", ipadx = 10, fill = "both", expand=True)
    close_button.pack(side = "bottom", pady = 10)
    #Bind
    frame.bind("<Configure>", lambda event: info.configure(wraplength=event.width))

def info_window(text, var = 0):
    information = tk.Toplevel()
    information.title("Information")
    information.geometry("200x100")
    information.resizable(False, False)
    if var == 0:
        info = ttk.Label(information, text = text)
    button = ttk.Button(information, text = "OK", command = lambda: information.destroy())
    info.pack(pady = 10)
    button.pack(pady = 10)

def keybind1 (var, event):
    v = event.char
    if var == 1 and (v == "."):
        return
    try:
        v = int(v)
    except ValueError:
        if v!="\x08" and v!="" and v != "\t":
            return "break"

def update_inventory(a = 0):
    inventory.delete(*inventory.get_children())
    k.execute("SELECT * FROM inventory WHERE char_id = (SELECT id FROM characters WHERE name = %s)ORDER BY id;", (character.get(), ))
    items = k.fetchall()
    ind = 0
    for row in items:
        k.execute("SELECT * FROM items WHERE id = %s ORDER BY id", (row[2], ))
        items2 = k.fetchall()
        inventory.insert(parent = '', index = ind, values = (items2[0][1], row[3], row[3]*items2[0][2], row[3]*items2[0][3]))
        ind += 1

def update_strength_bar(a = 0):
    global slider
    global inventory
    global slider_var
    global main_frame
    global slider_label
    slider.destroy()
    slider_label.destroy()
    k.execute("SELECT strength, multiplier, flat FROM characters WHERE name = %s;", (character.get(), ))
    stats = k.fetchall()
    if not stats:
        max_weight = 0
    else:
        max_weight = calculate_weight(0, stats[0][0], str(stats[0][1]), stats[0][2])
    #Current weight
    children = inventory.get_children()
    current_weight = 0
    for child in children:
        current_weight += float(inventory.item(child)["values"][3])
    #Slider itself
    slider_var.set(current_weight)
    slider = ttk.Progressbar(main_frame, maximum = max_weight, orient = "horizontal", variable = slider_var)
    slider_label = ttk.Label(main_frame, text = f"{current_weight} / {max_weight}")
    slider.place(relx = 0.25, rely = 0.95, relwidth=0.5, relheight=0.025)
    slider_label.place(relx = 0.755, rely = 0.94, relheight=0.05)
    return

def updates(a = 0):
    update_inventory()
    update_strength_bar()

#main window
window = tk.Tk()
window.title("DND 5e Inventory manager")
window.geometry("800x500")
window.minsize(800, 500)

#Main frame
main_frame = ttk.Frame(window)
#Char Select
char_select_frame = ttk.Frame(main_frame)
label1 = ttk.Label(char_select_frame, text = "Select character:")
character = tk.StringVar()
characters = []
k.execute("SELECT name FROM characters;")
answer = k.fetchall()
for i in answer:
    characters.append(i[0])
characters = sorted(characters, key=str.casefold)
if len(characters) > 0:
    character.set(characters[0])
else: 
    character.set("")
char_select = ttk.Combobox(char_select_frame, textvariable=character, state = "readonly")

char_select["values"] = characters
#char_buttons
add_button = ttk.Button(main_frame, text = "Add Character", command= add_character)
edit_button = ttk.Button(main_frame, text = "Edit Character", command= edit_character)
delete_button = ttk.Button(main_frame, text = "Delete Character", command = delete_character)
#place mainframe
main_frame.place(relx = 0, rely = 0, relwidth= 1, relheight = 1)
#place char_select
char_select_frame.place(relx = 0.5, rely = 0.03, anchor = "n")
label1.pack(side="left")
char_select.pack(side="left")
#place char_buttons
add_button.place(relx = 0.35, rely = 0.075, relwidth=0.13, anchor="n")
edit_button.place(relx = 0.5, rely = 0.075, relwidth=0.13, anchor="n")
delete_button.place(relx = 0.65, rely = 0.075, relwidth=0.13, anchor="n")
#Character inventory
inventory = ttk.Treeview(main_frame, columns = ("name", "amount", "price", "weight"), show = "headings")
inventory.heading("name", text = "Item")
inventory.heading("amount", text = "Amount")
inventory.heading("price", text = "Total Price (gp)")
inventory.heading("weight", text = "Total Weight (lb)")
inventory.column("name", width = 200)
inventory.column("amount", width = 20)
inventory.column("price", width = 20)
inventory.column("weight", width = 20)
update_inventory()
info = ttk.Label(main_frame, text = "*Double click item for additional information", font = 'calibri 10')
#Scrollbar
scrollbar = ttk.Scrollbar(main_frame, orient = "vertical", command = inventory.yview)
inventory.configure(yscrollcommand=scrollbar.set)
#Searchbar
search_frame = ttk.Frame(main_frame, borderwidth=0.5, relief=GROOVE)
search_label = ttk.Label(search_frame, text = "Search inventory:")
search_var = tk.StringVar()
search = ttk.Entry(search_frame, textvariable=search_var)
#Binds
char_select.bind("<<ComboboxSelected>>", updates)
inventory.bind("<Double-Button-1>", lambda event: get_info(inventory.item(inventory.focus())['values'][0]))
search.bind("<KeyPress>", lambda event: find(search_var.get(), inventory, event.char, var = 1))
#inventory buttons
button_frame_1 = ttk.Frame(main_frame)
inc_button = ttk.Button(button_frame_1, text = "+ 1", command = lambda: change_amount(1, inventory))
dec_button = ttk.Button(button_frame_1, text = "- 1", command = lambda: change_amount(-1, inventory))
button_frame_2 = ttk.Frame(main_frame)
add_button = ttk.Button(button_frame_2, text = "Add item", command = add_item)
remove_button = ttk.Button(button_frame_2, text = "Remove", command = lambda: change_amount(-inventory.item(inventory.focus())['values'][1], inventory))
clear_inventory = ttk.Button(button_frame_2, text = "Clear inventory", command = clear)
create_items = ttk.Button(button_frame_2, text = "Create Item", command = create_item)
#Weight progress bar:
#Max Weight
k.execute("SELECT strength, multiplier, flat FROM characters WHERE name = %s;", (character.get(), ))
stats = k.fetchall()
if character.get() == "":
    max_weight = 0
else:
    max_weight = calculate_weight(0, stats[0][0], str(stats[0][1]), stats[0][2])
#Current weight
children = inventory.get_children()
current_weight = 0
for child in children:
    current_weight += float(inventory.item(child)["values"][3])
#Slider itself
slider_var = tk.IntVar(value = current_weight)
slider = ttk.Progressbar(main_frame, maximum = max_weight, orient = "horizontal", variable = slider_var)
slider_label = ttk.Label(main_frame, text = f"{current_weight} / {max_weight}")
#place searchbar
search_frame.place(relx = 0.5, anchor="center", rely = 0.16, relheight=0.06)
#Pack searchbar
search_label.pack(side = "left", padx = 5)
search.pack(side = "left", padx = 5)
#place inventory
inventory.place(relx = 0.02, rely = 0.2, relheight= 0.6, relwidth = 0.96)
info.place(relx = 0.02, rely =  0.8)
scrollbar.place(relx = 0.96, rely = 0.2, relheight= 0.6, relwidth = 0.04)
#place inventory buttons
button_frame_1.place(relx = 0.5, rely = 0.84, anchor = "center")
inc_button.pack(side="left", padx = 5)
dec_button.pack(side="left", padx = 5)
button_frame_2.place(relx = 0.5, rely = 0.90, anchor = "center")
add_button.pack(side = "left", padx = 5)
remove_button.pack(side = "left", padx = 5, ipadx = 7)
clear_inventory.pack(side = "left", padx = 5)
create_items.pack(side = "left", padx = 5)
slider.place(relx = 0.25, rely = 0.95, relwidth=0.5, relheight=0.025)
slider_label.place(relx = 0.755, rely = 0.94, relheight=0.05)
#Mainloop
window.mainloop()