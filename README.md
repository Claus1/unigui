# unigui #
Universal App Browser Unigui

### Purpose ###
Provide programming technology that does not require client programming, for a server written in any language, for displaying on any device, in any resolution, without any tuning.

### How to work inside ###
The exchange protocol for the solution is JSON as the most universally accessible, comprehensible, readable, and popular format compatible with all programming languages.  The server sends JSON data to Unigui which has built-in tools (autodesigner) and automatically generate a standart Google Material Design GUI for user data. No markup, drawing instructions and the other dull job is required. Just the simplest description what you want. From the constructed Unigui screen the server receives a JSON message flow which fully describes what the user did. The message format is ["Block", "Elem", "type of action", value], where "Block"and "Elem"are the names of the block and its element, "value" is the JSON value of the action/event that has happened. The server can either accept the change or roll them back by sending an info window about any inconsistencies. The server can open a dialog box that is described as a block or send an entirely new screen. Unigui instantly and automatically displays actual server state. 

### Programming ###
Unigui is language and platform independent technology. This repo explains how to work with Unigui using Python  and the tiny framework for that.
Unigui web version is included in this library. Unigui for mobile and native platform are in another repos.

### High level - Screen ###
The program directory has to contain a screens folder which contains all screens the Unigui has to show.

Screen example tests/screens_hello/main.py
```
name = "Main" #name of screen to show
icon = 'blur_linear' #MD icon of screen to show
order = 0 #order in the program menu
blocks = [block] #what to show on the screen
```

The block example with a table and 2 selectors
```
table = Table('Videos', headers = ['Video', 'Duration', 'Owner', 'Status', 'Links'],   rows = [
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed', 'Refererence 1'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed', 'Refererence 8']
], value = 0)
#widgets are groped in blocks (complex widgets with logic)
block = Block('X Block', 
    [   Select('Select', value='All', options=['All','Based','Group']),
        Select('Group', value='Group1', options=['Group 1','Group 2', 'Group 3'])
    ], table)
```

### Server start ###
tests/run_hello.py
```
import unigui
#app name, port for initial connection and screen_folder are optional
unigui.start('Test app', port = 8080, screen_dir = 'screens_hello') 
```
Unigui builds the interactive app for the code above.
Connect a browser to localhast:8080 and will see:

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
    table.rows = []
    return table
clean_button = Button('Clean the table’, changed = clean_table)
```

‘changed’ handlers have to return Gui object or array of Gui object which Unigui has to redraw, if we changed their visible state in code. Unigui will do all other jobs for synchronizing automatically. If Gui object doesn't have 'changed' handler the object accept incoming value automatically to value class variable.

If value is not acceptable instead of returning an object possible to return Error or Warning or UpdateError. The last function has a list object, which has to be synchronized simultaneously with informing about the Error.

#### If a handler returns True or UpdateScreen constant the whole screen has to be redrawn. Also it causes calling Screen function prepare() which used for syncronizing GUI elements one to another and with program data. prepare() is also automatically called when screen loaded. prepare() is optional.

```
def changed_range(_,value):
   if value < 0.5 and value > 1.0:
       #or UpdateError(_, message) if we want to return the previous visible value to the field
       return Error(f‘The value of {_.name} has to be > 0.5 and < 1.0!') 
    #accept value othewise
    _.value = value

edit = Edit('Range of involving', value = 0.6, changed = changed_range)
```
If a handler return None (or does not return) Unigui consider it like Ok from the server logic.

#### Do not use lambdas for handlers, jsonpickle has a serialization issue for lambdas but ok with normal functions! ####

### Block details ###
The width and height of blocks is calculated automatically depending on their childs. It is possible to set the block width and make it scrollable in height, for example for images list. Possible to add MD icon to the header, if required.
```
block = Block(‘Pictures’,add_button, *images, width = 500, scroll = True,icon = 'api')
```
 
The second parameter of the Block constructor is an array of widgets which has to be in the header just after the name.
Blocks can be shared between the user screens with its states. Such a block has to be located in the blocks folder of the python layer.
Examples of such block tests/blocks/tblock.py:
```
from unigui import *
..
concept_block = Block('Concept block',
   [   #some gui elements       
       Button('Run',run_proccess),
       Edit('Working folder','run_folder')
   ], result_table)
```
If some elements enumerated inside an array, Unigui will display them on a line, otherwise everyone will be displayed on a new own line(s).
 
Using a shared block in some screen:
```
from blocks.tblock import *
...
blocks = [.., concept_block]
```

#### Events interception of shared blocks ####
Interception handlers have the same in/out format as usual handlers.
#### They are called before the inner element handler call. They cancel the call of inner element handler but you can call it as shown below.
For example above interception of select_mode changed event will be:
```
@handle(select_mode, 'changed')
def do_not_select_mode_x(_, value):
    if value == 'mode_x':
        return UpdateError(_, 'Do not select mode_x')
    return _.changed(_, value) #otherwise call the default handler
```

### Basic gui elements ###
You have to know that class names are used only for programmer convenience and do not receive Unigui.
If the element name starts from _ , Unigui will not show its name on the screen.
if we need to paint an icon somewhere in the element, add 'icon': 'any MD icon name'.
Common form for element constructors:
```
Gui('Name', value = some_value, changed = changed_handler)
#It is possible to use short form, that is equal:
Gui('Name', some_value, changed_handler)
```
Any gui element can mutate to any other type. It is usefull when we want to keep actual reference from the others but change it to a new required type.
```
selector.mutate(edit_property)
```
selector reference keep alive with a totally different gui element.

#### Button ####
Button('Push me') is a normal button.
Icon button respectively will be described like Button('_Check', 'icon': 'check')

#### Edit and Text field. ####
If set edit = false it will be readonly field or text label.
```
Edit('Some field', '', edit = false) 
#is equal to
Text('Some field')
```
complete handler is optional function which accepts current value and return a string list for autocomplete.
```
Edit('Edit me', value = '', complete = get_complete_list) #value has to be string

def get_complete_list(current_value):
    return [s for s in vocab if current_value in s]    
```
Can contain optional 'update' handler which is called when the user press Enter in the field.
It can return Error or None for automatically declining or accepting new value.


#### Radio button ####
```
Switch('Radio button', value = True) #value has to be boolean
```

#### Select group. Contains options field. ####
```
Select('Select something', value = "choice1", options = ["choice1","choice2", "choice3"]) 
```

#### Image. #### 
width,changed and height are optional, changed is called if the user click or touch image.
```
Image("Image", image = "some url", changed = show_image_info, width = .., height = ..)
or short version
Image("Image", "some url", show_image_info, width = .., height = ..)

```

#### Tree. The element for tree-like data. ####
Tree()

### Table. ###
Tables is common structure for presenting 2D data and charts. Can contain append, delete, update handlers, multimode value is True if allowed single and multi select mode.
all of them are optional. When you add a handler for such action Unigui will draw an appropriate action icon button in the table header automatically.
```
table = Table('Videos', [0], row_changed, headers = ['Video', 'Duration', 'Owner', 'Status', 'Links'],   rows = [
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed', 'Refererence 1'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed', 'Refererence 8']
], multimode = false, update = update)
```
If headers length is equal row length Unigui counts row id as an index in rows array.
If row length length is headers length + 1, Unigui counts row id as the last row field.
table does not contain append, delete so it will be wrawn without add and remove icons.  value = [0] means 0 row is selected 
in multiselect mode (in array). multimode is False so switch icon for single select mode will be not drawn and switching to single select mode is 
not allowed.

By default Table has toolbar with search field and icon action buttons. It is possible to hide it if set tools = False to the Table constructor.

By default Table has paginator. It is possible to hide it set 'paginator = false' table parameter.

If the selected row is not on the currently visible page then setting 'show = True' table parameter causes Unigui will make visible the page with selected row. 

### Table handlers. ###
complete, modify and update have the same format as the others elements, but value is consisted from the cell value and its position in the table.
'update' is called when user presses the Enter, 'modify' when the cell value is changed.
If they return Error(..) value is not accepted, othewise it will be automatically accepted after calling the handler.
```
def table_updated(table_ , tabval):
    value, position = tabval
    #check something
    if error_found:
        return Error('Can not accept the value!')
```
The 'changed' table handler accept the selected row number or id as a value.

'edit' handler if defined has a signature tedit(table_, edit_mode_now) where the second parameter says the current edit table mode choosen by the user.















