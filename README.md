# DND 5e Inventory manager
#### Video Demo:  https://youtu.be/4kndOK74Ngg
#### Description:
##### What is "DND 5e Inventory manager":
"DND 5e Inventory manager" is an application for managing the inventories of multiple Dungeons & Dragons 5th edition (D&D 5e) characters. 
##### Motivation:
I love playing D&D and have participated in many Dungeons and Dragons (as well as several other titles) games. While playing, especially in extended campaigns spanning multiple months, keeping track of all the items that the platyers received, used, bought, sold, found and broke was always a difficult task. There were occasions when players would have dedicated lists (which would get lost), or kept track of their inventory in their notebook (separating items by taking notes) and of course there were those who tried to keep their items within the small "Equipment" portion of the character sheet, which led to so many instances of writing, then erasing stuff that the person erased right through the sheet.

Additionally whenever we have played, even though the game includes an encumburance system and has a weight parameter for all items (even though for some it is "0"), we have never used it, as that was deemed way too much of a hassle to track and therefore not worth it as it bogged the game down too much.

For these reasons I decided as my final CS50 project to create something that would be useful to myself, my friend group and hopefully anyone else who faced the same issues while playing. 
##### Compatibility with other systems:
The application can be used as a general character inventory manager, however, it has a functionality of calculating the character's carry capacity based on the formula used in D&D 5e, which when using a different system can be ignored. Additionally the table for items has been filled with the basic items for D&D 5e, however, it does provide the ability to create new items.
#### Components
This fairly simple app uses a single python3 file, tkinter to create a Graphical User Interface (GUI) and a PostgreSQL database (db).

##### Database
The PostgreSQL db utilises 3 tables. The first table "characters" keeps track of all created characters and consists of 5 columns:  
The first column "id" is an unique id integer for each entry and is the primary key for the table.  
The second column "name" is a text data type with the character's name.  
The third column "strength" is an integer data type with the character's strength score.  
The fourth column "multiplier" is an integer data type.
The fifth column "flat" is an integer data type.  
Columns three, four and five are used when calculating a character's maximum carrying capacity.

The second table "items" keeps track of all available items and consists of 5 columns:  
The first column "id" is an unique id integer for each entry and is the primary key for the table.  
The second column "name" is a text data type with the item's name.  
The third column "price" is a real data type, indicating an item's price in gold pieces. As D&D currency has silver pieces, 10 of which equal 1 gold piece and copper pieces, 10 of which equal 1 silver piece, there are values, which are smaller than 1.  
The fourth column "weight" is a real data type, indicating an item's weight in pounds. 
The fifth column "description" in a text data type, which consists of a short description for the item.

The third table "inventory" keeps track of each separate character's inventory and consists of 4 columns:  
The first column "id" is an unique id integer for each entry and is the primary key for the table.  
The second column "char_id" is an integer data type foreign key referencing the characters.id indicating which character the item belongs to.  
The third column "item_id" is an integer data type foreign key referencing the items.id indicating which item belongs to the character.  
The fouth column "amount" is an integer data type, which indicates how many of a specific item does the chracter have.

#### Python Code
When running the main file, a tkinter window opens, which inlcudes a label, combobox allowing for character selection, 3 character related buttons, a search entry field an inventory treeview widget, a scrollbar for the inventory, a label providing information regarding obtaining additional information for the inventory items, 6 item related buttons, a slider giving a visual indication of how much of the maximum carrying capacity is currently being used, as well as a label, indicating the same thing with numbers. 

##### Character related widgets
All character related widgets are contained, using the "pack" method, within a "char_select_frame", which uses the "place" method of positioning.
###### Character selection
The first character related widget is a label placed inside the "char_select_frame" using the pack method, indicating character selection in the combobox beside it.

The second character related widget is the character selection combobox ("char_select"), which is also placed inside the "char_select_frame" using the pack method. It is populated by selecting all the names from the characters table, which are, using a "for loop", added to a "characters" list, then sorted alphabetically using "sorted" with "key=str.casefold" and then added as "char_select["values"]". The "char_select" has a text variable "character", which is set to the first item in "characters" if there are any values and if the list is empty it is set to empty (""). The ".bind" method has been used so that when the "ComboboxSelected" event occurs, the "updates" function is called. 
###### Character Buttons
The first button is the "add_button", contained in the "main_frame" via the ".place" method. The text it contains is "Add Character" and calls the "add_character" function when pressed. 

The second button is the "edit_button", contained in the "main_frame" via the ".place" method. The text it contains is "Edit Character" and calls the "edit_character" function when pressed. 

The third button is the "delete_button", contained in the "main_frame" via the ".place" method. The text it contains is "Edit Character" and calls the "delete_character" function when pressed.
#### Inventory widgets
##### Inventory
The "inventory" is a Treeview widget, contained within the main frame via the ".place" method, with 4 columns and headings, with each column being allocated a specific width. The inventory shows the selected character's items' names, amount, total price of each item and total weight of each item. The ".bind" method has been used so that when the "Double-Button-1" event occurs, the "get_info" function is called with name of the currently selected item passed as a parameter.
##### Info
"info" is a label widget, contained within the main frame using the ".place" method. It is used to indicate that by double-clicking an item, additional information will be provided. 
##### Scrollbar
The "scrollbar" is a Scrollbar widget contained within the main frame using the ".place" method, which is linked to the inventory via "yscrollcommand" configuration.
##### Search
The "search_frame" is a Frame widget, which is contained within the "main_frame", above the inventory and set apart via "GROOVE" relief. It utilizes ".place" method. 


The "search_label" is a Label widget used to indicate that the entry field next to it is used to search the character's inventory for a specific item. It is contained in the "search_frame" via the ".pack" method. 


"search" is an Entry widget used to search the character's inventory for a specific item. It has a textvariable "search_var", which is a StringVar. It is contained in the "search_frame" via the ".pack" method. The ".bind" method has been used so that when the "KeyPress" event occurs, the "find" function is called with "search_var", "inventory", "event.char" and "var = 1" passed as values.
#### Inventory Buttons
"button_frame_1" and "button_frame_2" are Frame widgets, which are containe within the "main_frame" via the ".place" method
##### inc/dec buttons
The "inc_button" and "dec_button" are contanied within "button_frame_1" via the ".pack" method. The text they display is "+1" and "-1" respectively. They change the amount of the selected item in the inventory by both call the "change_amount" function when pressed passing 1 and -1 respectively, as well as "inventory" as parameters.
##### add_button
The "add_button" is contanied within "button_frame_2" via the ".pack" method. It contains the text "Add item" and when pressed calls the "add_item" function.
##### remove_button
The "remove_button" is contanied within "button_frame_2" via the ".pack" method. It contains the text "Remove" and when pressed calls the "change_amount" function passing a negative integer, equal to the current amount of the selected item as well as "inventory" as parameters.
##### clear_inventory
The "clear_inventory" is contanied within "button_frame_2" via the ".pack" method. It contains the text "Clear inventory" and when pressed calls the "clear" function.
##### create_items
The add_button is contanied within "button_frame_2" via the ".pack" method. It contains the text "Create Item" and when pressed calls the "create_item" function.
#### Weight progress Bar
The weight progress bar includes the "slider" and and "slider_label" widgets. They are both related to the "max_weight" and "current_weight" varables. The "max_weight" variable is calculated by using the "calculate_weight" function passing the currently selected character's statistics, which are selected from the characters table, as parameters, unless there is no character selected, it which case it defaults to "0". The "current_weight" is set as a default to "0" and is increased by the weight of each item in the character's "inventory".
##### Slider
"slider" is a Progressbar widget contained in the main frame via the ".place" method with the "max_weight" variable as its maximum. It has the "slider_var" as a variable, which is an IntVar with it's value set to the "current weight variable".
#### Functions
##### "add_character"
This function is called when the "add_button" is pressed as well at the end of the "edit_character" function, after pressing the "edit_button". It takes the parameters "def_name",  "def_str", "def_multi", "def_flat" and "var", which are set to the default values "", 10, 0, 0 and 0 respectively. The function creates a Toplevel widget named "char_frame", of size 300x200 which is not resizable. Depending on the value of "var", the name can be "Add character" if "var == 0" or "Edit character" if else.

There are no frames inside Topwindow and all widgets inside are position utilizing the ".place" method. There are 2 Entry widgets, a spinbox widget and a combobox widget, each paired side by side with a Label widget to the left of them. Each pair of widgets is placed below the preceding pair. After the first 2 pairs, there is another Label widget and after the four pairs, there 2 buttons and 2 more labels, which are also paired side by side.

The first Label widget is the "name_label", which has text "Name:" and to it's right is the "name_entry" Entry widget, which has the StringVar "name_var" as textvariable. The "name_var" is set to the "def_name" the focus of the window is set to "name_entry".

The second Label widget is the "strength_label", which has text "Strength:" and to it's right is the "strength_box" Spinbox widget. It's values range between 1 to 100 and it has the textvariable "strength_var", which is a StringVar and is set to "def_str".

Separating the first 2 pairs of entry-type widgets from the latter 2 is the "carry_capacity_increases" Label widget, which has the text "Carry capacity increases" and utlizes the "Calibri 10 bold" font.

Following is the multiplier_label Label widget, which has the text "Multiplier" and to it's right is the "multiplier_entry" Combobox. The "multiplier_entry" widget has a textvariable of "multiplier_var", which is a StringVar and its state is "readonly". The values for the multiplier_entry are set to bea list named "multipliers". If the "def_multi" variable == 0, then the "multiplier_var" is set to be the first item from the multipliers list. Else it is set to be the value of def_multi as a string + "x". 

The final entry type pair inlcudes the "flat_label" which is a Label widget with the text "Flat increase (lb):" and the "flat_entry" Entry widget, which has a textvariable flat_var, which is a StringVar. "flat_var" is set to the "def_flat" value. 

The two available buttons are the "add_button" and the "cancel_button". The cancel_button contains the text "Cancel" and pressing it destroys the "char_frame". The "add_button" depending on if var == 0 or 1 contains the text "Create" or "Update" respectively and in both cases calls the "add_character_c" function, passing the values of "name_var", "strength_var", "multiplier_var", "flat_var" and then destroying the "char_frame". If var == 1, when calling the "add_character_c" function it also passes "var = 1"

Below the buttons are two Label widgets. The first one being the "max_carry_label" which contains the text "Max carry:" and the second one being the "max_carry_label2" which has the textvariable "limit", which is an IntVar. Initially limit is set to 150. If var == 1, limit is set to a call of the calculate_weight function with 0, "strength_var", "multiplier_var", "flat_var" values passed.

The strength_box events "Increment", "Decrement", "KeyRelease", as well as the multiplier_entry "ComboboxSelected" event and the flat_entry "KeyRelease" event all call a lambda function to set the value of "limit" to the result from the "calculate_weight" function passing in the values of "strength_var" "multiplier_var" and "flat_var", as well as 1, -1, 0 or 0 respectively for "var". Additionally when the "KeyPress" event occurs for "strength_box" or "flat_entry" a lambda event function is triggered for the "keybind1" function, passing "False" and "event" as parameters so that only integers can be put into the fields. 
##### add_character_c
This function is called through the "add_character" function and it takes the parameters "name", "strength", "multiplier", "flat", and "var" with "var" being set to a default value of 0, which is for when a new character is being created, as opposed to 1, when an already existing character is being edited.

First the function makes sure that no fields have been left empty when filling out the "add_character" function an if they have it prompts the user via messagebox titled "Character not created" and the message indicating, what the missing value is and the function returning. After that it checks if the character name is already taken, by comparing "name" with the "characters" list if a new character is being created (var = 0). Then the "multiplier" value is converted to a string using a for loop and creating a list of all characters, which are digits. 

If var == 0, the highest current id from the characters table is selected. If there is no current id (no characters are available) id is set to 1, else id = the selected id + 1. After that the new character is inserted into the "characters" table using the "id", "name", "strength", new multiplier and "flat" values. The changes are commited to the database. The "characters" list is updated with the new name and sorted, "character" is set to the "name" variable, the updates function is called and finally a messagebox, indicating that the character has been created successfully is created.

If var == 1, the values for "name", "strength", "multiplier" and "flat" are updated in the "characters" table where the name is the same as the currently selected character. The db changes are commited, then the old name in the "characters" list is updated to the new name and the "characters" list is sorted and the values of "char_select" are set to the updated "characters" list. The "updates" function is called and a messagebox indicating that the character has been successfully updated is created.
##### add_item
This function is called through the "add_button". It created a Toplevel widget named "item_frame" with the title "Add Item", geometry of 400x450 and minsize of 400x450. 
###### searchbar
A "search_frame", which is a Frame widget, is packed on the "item_frame". It contains a "search_label" which contains the text "Search items:" and an Entry widget naemd "search". Both are packed within the search frame with "side = "left"". The window focus is set on the "search" widget by default and the "search" widget has a textvariable named "search_var", which is a StringVar. 

A "KeyPress" event in the "search" widget triggers a lambda event, executing the "find" function passing the "search_var" value, "items" and event.char as parameters.
###### items
Below the searchbar is a Label widget naemd "items_label" containing the text "List of items:" with the "calibri 14 bold" font.

Beneath the "items_label" is a Treeview widget named "items" which contains 3 columns for each item's name, price and weight. The width of the columns is set to allow for longer item names. "items is populated by selecting all entries from the "items" table.Additionally, below it is a Label widget named "info" indicating that double-clinking on an item opens additional information regarding the item. "info" is contained within the "item_frame" via the ".pack" method.

A "Double-Button-1" event in the "items" widget triggers a lambda event, executing the "get_info" function passing the name of the currently selected item.

There is a vertical Scrollbar widget named "items_scrollbar", which is linked to the "items" Treeview via the yscrollcommand.

"items" and "item_scrollbar" are both contained in a "items_frame" via the ".pack" method, which is in turned contained in the "item_frame", again via the ".pack" method.
###### Amount
Below the "info" widget is the "amount_frame" Frame widget, contained within the "item_frame" via the ".pack" method. It contains the "amount_label", which is a Label widget, containing the text "Amount:" and "amount_box", which is a Spinbox widget, which has "amount_var" as textvariable. The ".pack" method is used for both of these. The "amount_label". "amount_var" is a StringVar, initially set to 1.

A "KeyPress" event in the "amount_box" widget triggers a lambda event, executing the "keybind1" function passing "False" and the event as parameters, so that only integers can be entered.
###### Buttons
Below the "amount_frame" is the "button_frame", which is contained in the "item_frame" via the pack method. It contains "add_item_button" and "cancel" both of which are Button type widgets, utilizing the .pack method. "cancel" contains the text "Cancel" and when pressed, destroys "item_frame". "add_item_button" contains the text "Add item" and when pressed triggers the "add_item_c" function, passing "items" and "amount_var" as parameters.

##### add_item_c
This function is called via the "add_item" function and it takes 3 arguments: "tree", "amount" and "var" with "var" being set to a default value of 0.

 If var == 0, "amount" is checked if it is an empty value and if so, messagebox indicating that the item has not been added is created and the function is completed via "return". If "amount" is not an empty value, a variable named "item" is created which
is the name of the selected item from "tree". If there is no selected item a messagebox indicating that the item has not been added is created and the function is completed via "return". If "var" == 1, item = tree.

After that, the count of instances in the "inventory" table where this character has this item is checked. If is such an instance, the amount of the entry is updated, the db change is commited and a messagebox indicating that the amount has been increased successfully is created. If there is no such instance, one is created reflecting the selected character, item and amount, the db change is commited and a mssagebox indicating that the item has been added is created. After either scenario, the "updates" function is called.
##### calculate_weight
This function is called when trying to determine "max_weight" when initiating the application, or from the "update_strength_bar" function, and from the "add_character" function. It takes the arguments "var", "strength", "multiplier" and "flat_increase". 

It uses a formula multiplying the strength score of a character after adding the variable by 15, then by the multiplier and finally adding the flat increase to determine a characters max carry limit ("limit") and returns that. 
##### change_amount
This function can be called from "inc_button", "dec_button" and "remove_button" from the "window". It takes the arguments "val" and "tree". 

The function first checks if there is an item selected in "tree" and if there is not one, it returns a messagebox, indicating that is the case. If there is an item selected it it creates the variable "name" which is set as the name of the selected item and then formats it as a string. The function then updates the amount of the item in the selected character's inventory entry in the "inventory" table and commits the change. After that a check is executed, which provides the current amount of the specific item in the currently selected character's inventory. If the amount is less than 1, the entry is deleted from the "inventory" table and the chang commited. Then the "updates" function is called and finally the "tree" focus is set to the item with the same name if available.
##### clear
This function can be called from the "clear_inventory" button in "window". 

It creates a messagebox, asking if the user is sure they would like to continue with clearing the entirety of the selected character's inventory. If the user confirms, all entries from the "inventory" table where the "char_id" matches that of the currently selected character are deleted. The changes are commited and the "updates" function is called.
##### create_item
This function can be called from the "create_items" button in "window". The function creates a Toplevel widget named "new_item_frame" with "Create Item" as title and geometry of 450x250 and matching minsize. It is divided by two Frame widgets named "left_frame" and "rigth_frame".All widgets use the ".place" method. 

In the left frame there are 3 Labels, each of which is followed by an Entry widget. The first pair are the "name_label" which contains the text "Item name" and "name_entry" which has the textvariable "name_var", which is a StringVar. The window's focus is set to "name_entry". This is followed by the "price_label" , which contains the text "Item price (gp):" and the "price_entry" with the "price_var" textvariable, which is also StringVar. The last pair are the "weight_label" containing the text "Item weight (lb):" and the "weight_entry" with the "weight_var" textvariable, which is again a StringVar. Below them is the "add_to_char" Checkbutton widget, which contains the text "Add to current character" and has the variable "add_to_char_var", which is a BooleanVar, with the "on" value being "True" and the "off" value being "False". Finally in the "left_frame" is the "create_button" Button type widget, which contains the text "Create Item" and when pressed calls the "create_item_c" function, passing the values of "name_var", "price_var", "weight_var", "add_to_char_var", the "description" from the first character to the last and "new_item_frame".

In the right frame there is the "description_label" Label widget, which contains the text "Item Description:", "description", which is a Text type widget and "cancel_button" which is a Button widget, which contains thetext "Cancel" and when pressed destroys "create_items".
##### create_item_c
This function can be called from the "create_item" function. It takes the "name", "price", "weight", "description", "add" and "window" arguments. 

It first checks if any fields have been left blank and if so it provides a messagebox, letting the user know what the issue is and then exits via "return". If all fields have been filled, it then checks if there are already any items with the same name and if so let's the user know that the item cannot be created due to this. If everything is in order it inserts the new item into the "items" table and commits the changes. If the "add_to_char" field has been tcked it also ccalls the "add_item_c" function, passing the values "name", 1 and 1. At the end it destroys the "window" argument that was passed to it.
##### delete_character
This function can be called via the "delete_button" from the main "window". 

It requests confirmation via messagebox if the user would really like to delete this character and all their inventory. If they confirm, the function deletes all entries from the "inventory" table, where the "char_id" is the same as the selected character and then deletes the entry in the "characters" table where the name matches the one of the selected character. The changes are commited to the db, the name is removed from the "characters" list, te list is sorted, the "char_select" values are updated to match the new list and if there are remaining characters, "char_select" is changed to the first entry on the "characters" list. If there are no remaining entries, "char_select" is set to "". The "updates" function is called
##### edit_character
This function can be called via the "edit_button" from the main "window". 

It gets the entry from the "characters" table where the name matches that of the currently selected character and calls the "add_character" function passing the stats of the character to replace the default values and var = 1. The "update_strength_bar" function is called.
##### find
This function is called when the "KeyPress" event occurs in the "search" Entry widget in the "add_item" function and when the  "KeyPress" event occurs in the "search" Entry widget in the main "window". It takes "search_var", "items", "char", and "var" as parameters with "var" being given the default value of 0. 

The function first checks if "char" is backspace, and if that is the case it removes the last letter of "search_var" and if not it adds "char" to "search_var" in both cases creating a variable named "new". It then checks if var == 0 and if that is the case it selects all entries from the "items" table where the name includes "new" in any combination. Else it selects all items from the name, amount, price and weight of all items from a joined table of "items" an "inventory" joined on item_id, where the "char_id" matches that of the currenly selected character and the "item.name" includes includes "new" in any combination. 

A new variable named "new2" is created which gets the results from the selection. All children of "items" are deleted and then items is populated with the entries of "new2".
##### get_info
This function is called when the "Double-Button-1" event occurs in the "items" Treeview widget in the "add_item" function and when the "Double-Button-1" event occurs in the "inventory" Treeview widget in the main "window". It takes "item" as an argument. 

The function creates a Toplevel window named "info_window" with default geometry 400x200 and title "Information". A Frame widget is created which is named "frame" and given a yellow background color. The description from "items" table where the name matches "item" is selected and a Label widget named "info" is created, which has a wraplegth of 180, the same background color as "frame" and the text matches the received description. A "close_button" Button widget is created, with the text "Close", which when pressed closes "info_window". All widgets utilize the ".pack" method and when a changes to the size of the window occure they triggers an event, which changes the wraplength of "info" to match the "event.width".
##### info_window
This function is called from the "create_item_c" function when one or more of the parameters were left empty. It takes "text and "var" as parameters with "var" having a default value of 0. 

The function creates a Toplevel widget named "information" with the title "Information" and sie of 200x100, which cannot be changed. If "var" == 0, a Label widget named info is created, which is contained within "information" via the ".pack" method. The text of the label is "text". A Button widget named "button" is created with a lambda function, which destroys "information". It is contained within "information" via the ".pack" method.
##### keybind1
This is a function, which "var" and "event" as parameters. It can be called via the "add_character" function when the "KeyPress" event occurs within the "strength_box" and the "flat_entry", via the add_item function when the "KeyPress" event in the "amount_box" or via the "create_item" function when the "KeyPress" event occurs within the "price_entry" and "weight_entry".

 A variable "v" is created where which is set as the event.char. The function stops the user from entering characters other than digits, backspace or tab. Depending on the "var" value, the "." character may also be allowed.
##### update_inventory
This function can be called through the "updates" function and is called when initially starting the application. It takes a single argument "a", which has a default value of 0.

The function deletes all children of the "inventory" Treeview, then selects all entries from the "inventory" where the "char_id" matches the currently selected characters "id" from the "characters" table. These entries are added to a list, named "items" and a variable named "ind" is created, given the value 0. 

After that a for loop is used to select all entires from the "items" table, where the id of the item matches the id of the item_id from "items" entry. The selected information is placed within a new variable named "items2 and "inventory" is populated with the values of "items2", with the index being equal to "ind". At the end of the for loop, "ind" is increased by 1. 
##### update_strength_bar
This function is called through the "updates" function and the "edit_character" functions. It tkes a single argument "a" with a default value of 0. The variables "slider", "inventory", "slider_var", "main_frame" and "slider_label" are declared to be global within the function.

The first thing the function does is it destroys "slider" and "slider_label". After that it selects the entry from the "characters" table where the name matches that of the currently selected character and creates the variable "stats" which contains the values. It sets a new "max_weight" by calling the "calculate_weight" function passing the "stats" items as arguments. It then gets the children from "inventory", creates the "current_weight" variable and gives it the value "0". For each "child" in children the "current_weight" variable is icreased by the weight of the entry. After that, "slider_var" is set to match "current_weight". A new "slider" Progressbar widget is created, contained within "main_frame", with "max_weight" as its maximum and "slired_var" as its variable. A new "slired_label" Label widget is created with the text being an fstring based on the "current_weight" and "max_weight". Finally the 2 widgets are position using the ".place" method.

##### updates
"updates" is a wrap function, which calls the "update_inventory" and "updte_strength_bar" functions. 

THANK YOU FOR READING!