# unigui #
Universal App Browser Unigui

### Purpose ###
Provide a programming technology that does not require client programming, for a server written in any language, for displaying on any device, in any resolution, without any tuning.

### How to work inside ###
The exchange protocol for the solution is JSON as the most universally accessible, comprehensible, readable, and popular format compatible with all programming languages.  The server sends JSON data to Unigui which has built-in tools (autodesigner) and automatically builds a standart Google Material Design GUI for user data. No markup, drawing instructions and the other dull job are required. Just the simplest description what you want. From the constructed Unigui screen the server receives a JSON message flow which fully describes what the user did. The message format is ["Block", "Elem", "type of action", value], where "Block"and "Elem"are the names of the block and its element, "value" is the JSON value of the action/event that has happened. The server can either accept the change or roll it back by sending an info window about an inconsistency. The server can open a dialog box, send popup Warning, Error,.. or an entirely new screen. Unigui instantly and automatically displays actual server state. 

### Programming ###
Unigui is the language and platform independent technology. This repo explains how to work with Unigui using Python  and the tiny but optimal framework for that.
Unigui web version is included in this library. Unigui for mobile and native platforms are in another repos.

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
#app name, port for initial connection and user_dir folder are optional
unigui.start('Test app', port = 8080) 
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

#### If a handler returns True or UpdateScreen constant the whole screen will be redrawn. Also it causes calling Screen function prepare() which used for syncronizing GUI elements one to another and with the program/system data. prepare() is also automatically called when the screen loaded. prepare() is optional.

```
def changed_range(_,value):
   if value < 0.5 and value > 1.0:
       #or UpdateError(_, message) if we want to return the previous visible value to the field
       return Error(f‘The value of {_.name} has to be > 0.5 and < 1.0!') 
    #accept value othewise
    _.value = value

edit = Edit('Range of involving', value = 0.6, changed = changed_range)
```
If a handler return None (or does not return) Unigui consider it as Ok.

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
Normal button.
```
Button('Push me', changed = push_callback) 
```
Short form
```
Button('Push me', push_callback) 
```
Icon button 
```
Button('_Check', push_callback, icon = 'check')
```

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
It can return None or objects for updating as usual handler.


#### Radio button ####
```
Switch('Radio button', value = True) #value has to be boolean
```

#### Select group. Contains options field. ####
```
Select('Select something', value = "choice1", options = ["choice1","choice2", "choice3"]) 
```
can be such type 'toggles','list','dropdown'. Unigui automatically choose between toogles and dropdown,
but user can set type = 'list' then Unigui build it as vertical select list.

#### Image. #### 
width,changed and height are optional, changed is called if the user click or touch the image.
```
Image("Image", image = "some url", changed = show_image_info, width = .., height = ..)
or short version
Image("Image", "some url", show_image_info, width = .., height = ..)

```

#### Tree. The element for tree-like data. ####
```
Tree(name, selected_item_key, changed_handler, [unique_elems = .., elems = ..])
```
unique_elems for data without repeating names. it is dictionary {item_name:parent_name}. If it defined then 'elems' is redundant.
elems for data which can contains repeating names. it is array of arrays [item_name,item_key,parent_key].
parent_name and parent_key are None for root items. changed_handler gets the tree object and item key as value which is the item name for unique items. 

### Table. ###
Tables is common structure for presenting 2D data and charts. Can contain append, delete, update handlers, multimode value is True if allowed single and multi select mode. True by default. All of them are optional. When you add a handler for such action Unigui will draw an appropriate action icon button in the table header automatically.
```
table = Table('Videos', [0], row_changed, headers = ['Video', 'Duration', 'Owner', 'Status', 'Links'],   rows = [
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed', 'Refererence 1'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed', 'Refererence 8']
], multimode = false, update = update)
```
If headers length is equal row length Unigui counts row id as an index in rows array.
If row length length is headers length + 1, Unigui counts row id as the last row field.
If table does not contain append, delete then it will be wrawn without add and remove icons.  value = [0] means 0 row is selected in multiselect mode (in array). multimode is False so switch icon for single select mode will be not drawn and switching to single select mode is not allowed.

By default Table has toolbar with search field and icon action buttons. It is possible to hide it if set tools = False to the Table constructor.

By default Table has paginator. It is possible to hide it set 'paginator = false' table parameter.

If the selected row is not on the currently visible page then setting 'show = True' table parameter causes Unigui will make visible the page with selected row. 

### Table handlers. ###
complete, modify and update have the same format as the others elements, but value is consisted from the cell value and its position in the table.
'update' is called when user presses the Enter, 'modify' when the cell value is changed.
If they return error string, the value is not accepted, othewise it will be automatically accepted after calling the handler.
```
def table_updated(table_, tabval):
    value, position = tabval
    #check or update something
    if error_found:
        return 'Can not accept the value!'
```
The 'changed' table handler accept the selected row number or id as a value.

'edit' handler if defined has a signature edit(table_, edit_mode_now) where the second parameter says is the table edited by the user or not.

#### Refererences ####
Unigui support a special mechanism for handling inner reference events. They are useful in table fields and shared blocks. If a string in a table field started from @ then it considered as a reference. If the user clicks such field in non-edit mode then Unigui generates reference event, which comes to dispatch function of its containters. First look at its block, if not found than in the screen, if not again User.dispatch will be called, which can be redefined for such cases. Any handler can return Reference(element_that_generated_the_event, the_event_value) for raising reference event.


### Dialog ###
```
Dialog(name, text, callback, buttons, content = None)
```
where buttons is a list of the dialog buttons like ['Yes','No', 'Cancel'].
Dialog callback has the signature as other with value = pushed button name
```
def dicallback(current_dialog, bname):
    if bname == 'Yes':
        do_this()
    elif ..
```
content can be filled by any Gui elements for additional dialog functionality.

### Milti-user programming? You don't need it! ###
Unigui automatically creates and serves an environment for every user.
The management class is User which contains all required methods for processing and handling the user activity. A programmer can redefine methods in the inherited class, point it as system user class and that is all. Such methods suit for using history, undo/redo and initial operations. The screen folder contains screens which are recreated for every user. The same thing about blocks. The code and modules outside that folders are common for all users as usual. By default Unigui use the system User class and you do not need to point it. If we need special user class logic, we can define own inheritor User.
```
class Hello_user(unigui.User):
    def __init__(self):
        super().__init__()
        print('New Hello user connected and created!')
    def dispatch(self, elem, ref):
        if http_link(ref[1:]):
            open_inbrowser()
        else:
            return Warning(f'What to do with {ref}?') 

unigui.start('Hello app', user_type = Hello_user)
```
More info about User class methods you can find in manager.py in the root dir.

The articles about Unigui:

in English https://docs.google.com/document/d/1G_9Ejt9ETDoXpTCD3YkR8CW508Idk9BaMlD72tlx8bc/edit?usp=sharing

in Russian https://docs.google.com/document/d/1EleilkEX-m5XOZK5S9WytIGpImAzOhz7kW3EUaeow7Q/edit?usp=sharing
