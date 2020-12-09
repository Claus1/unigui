# unigui #
Universal App Browser Unigui

### Purpose ###
Provide programming technology that does not require client programming, for a server written in any language, for displaying on any device, in any resolution, without any turning.

### How to work inside ###
The exchange protocol for the solution is JSON as the most universally accessible, comprehensible, readable, and popular format compatible with all programming languages.  The server sends JSON data to Unigui which has built-in tools (autodesigner) that allows you to easily generate a beautiful GUI that conforms to Google’s Material Design standard.
From the constructed Unigui screen the server receives a JSON message flow which fully describes what the user did. The message format is ["Block", "Elem", "type of action", value], where "Block"and "Elem"are the names of the block and its element, "value" is the JSON value of the action/event that has happened.
The server can either accept the change or roll them back by sending an info window about any inconsistencies. The server can open a dialog box that is described as a block or send an entirely new screen. uniGUI instantly displays current server data and their changes. 

### Programming ###
Unigui is language independent. This repo explains how to work with Unigui using Python.
The program directory has to contain a folder screens. The folder contains all screens which the Unigui has to show.
Example.

tests/screens_hello/main.py
```
name = "Main" #name of screen to show
icon = 'blur_linear' #MD icon of screen to show
order = 0 #order in the program menu
#add widgets to the screen
table = Table('Videos', headers = ['Video', 'Duration', 'Owner', 'Status', 'Links'],   rows = [
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed', 'Refererence 1'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed', 'Refererence 8']
], value = 0)
#widgets are groped in blocks (complex widgets with logic)
block = Block('X Block', 
    [   Select('Select', value='All', options=['All','Based','Group']),
        Select('Group', value='Group1', options=['Group 1','Group 2', 'Group 3'])
    ], table)
#what to show on the screen
blocks = [block] 
```

### Server start ###
tests/run_hello.py
```
import unigui
unigui.start('Test app', screen_dir = 'screens_hello') #app name to show in Unigui and port for initial connection
```
Unigui builds the interactive app on client side for the code above:
![alt text](https://github.com/Claus1/unigui/blob/main/tests/screen1.png?raw=true)

### Handling events ###
All handlers are functions which have a signature
```
def handler_x(gui_object, value_x)
```
where gui_object is a Python object the user interacted with and value for the event.

All Gui objects except Button have a field ‘value’. 
For an edit field the value is a string or number, for a switch or check button the value is boolean, for table is row id or index, e.t.c.
When a user changes the value of the Gui object or presses Button, the server calls the ‘changed’ function handler.

```
def clean_table(_, value):
    tables.rows = []
    return tables

clean_button = Button(‘Clean table’, changed = clean_table)
```

‘Changed’ handlers have to return Gui object or array of Gui object which Unigui has to redraw, because we changed them in code. Unigui will do all other jobs for synchronizing automatically.

If value is not acceptable instead of returning an object possible to return Error or Warning or UpdateError. The last function has a list object, which has to be synchronized simultaneously with informing about the Error.

```
def changed_range(_,value):
   if value < 0.5 and value > 1.0:
       return Error(f‘The value of {_.name} has to be > 0.5 and < 1.0! ’) //or UpdateError(.., _) if we want to return the previous value to the field
```






