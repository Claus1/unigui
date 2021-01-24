# unigui #
Universal GUI and App Browser

### Purpose ###
Provide a programming technology that does not require front-end programming, for a server written in any language, for displaying on any device, in any resolution, without any tuning. 

### Installing ###
```
pip install unigui
```

### How does work inside ###
The exchange protocol for the solution is JSON as the most universally accessible, comprehensible, readable, and popular format compatible with all programming languages.  The server sends JSON data to Unigui which has built-in tools (autodesigner) and automatically builds a standart Google Material Design GUI for user data. No markup, drawing instructions and the other dull job are required. Just the simplest description what you want. From the constructed Unigui screen the server receives a JSON message flow which fully describes what the user did. The message format is ["Block", "Elem", "type of action", value], where "Block"and "Elem"are the names of the block and its element, "value" is the JSON value of the action/event that has happened. The server can either accept the change or roll it back by sending an info window about an inconsistency. The server can open a dialog box, send popup Warning, Error,.. or an entirely new screen. Unigui instantly and automatically displays actual server state. 

### Programming ###
Unigui is the language and platform independent technology. This repo explains how to work with Unigui using Python and the tiny but optimal framework for that.
Unigui web version is included in this library. Unigui for mobile and native platforms are in another repos.

### High level - Screen ###
The program directory has to contain a screens folder which contains all screens which Unigui has to show.

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
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed', '@Signal 1'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed', '@Signal 8']
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
#app name, port for initial connection and upload_dir folder are optional
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

‘changed’ handlers have to return Gui object or array of Gui object that were changed by handler and Unigui has to redraw or nothing if all visible elements have the same state. Unigui will do all other jobs for synchronizing automatically. If Gui object doesn't have 'changed' handler the object accept incoming value automatically to the 'value' variable og gui object.

If 'value' is not acceptable instead of returning an object possible to return Error or Warning or UpdateError. The last function has a list object, which has to be synchronized simultaneously with informing about the Error.

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
If the handler return None (or does not return anything) Unigui considers it as Ok.

### Block details ###
The width and height of blocks is calculated automatically depending on their childs. It is possible to set the block width and make it scrollable in height, for example for images list. Possible to add MD icon to the header, if required. Width, scroll, .. are optional.
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
from blocks.tblock import concept_block
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

#### Layout of blocks. #### 
If the blocks are simply listed Unigui draws them from left to right or from top to bottom depending on the orientation setting. If a different layout is needed, it can be set according to the following rule: if the vertical area must contain more than one block, then the enumeration in the array will arrange the elements vertically one after another. If such an enumeration element is an array of blocks, then they will be drawn horizontally in the corresponding area.

#### Example ####
blocks = [ [b1,b2], [b3, [b4, b5]]]
#[b1,b2] - the first vertical area, [b3, [b4, b5]] - the second one.

![alt text](https://github.com/Claus1/unigui/blob/main/tests/multiscreen.png?raw=true)

### Basic gui elements ###
You have to know that class names are used only for programmer convenience and do not receive Unigui.
#### If the element name starts from _ , Unigui will not show its name on the screen. ####
if we need to paint an icon somewhere in the element, add 'icon': 'any MD icon name'.

#### All constructor parameters are optional for all Gui elements except the first - name. ####

Common form for element constructors:
```
Gui('Name', value = some_value, changed = changed_handler)
#It is possible to use short form, that is equal:
Gui('Name', some_value, changed_handler)
```
#### It is possible immediately to change any Gui object paramaters and even its type, i.e. a gui element can mutate to any other type. ####
Mutation is usefull when we want to keep actual reference from the others elements but change it to a new required type.
After mutation the handler has to return containing Block or UpdateScreen for automatic recalculating the block or the screen geometry.
```
selector.mutate(edit_fld) #the selector keeps alive with a totally different gui element.
```
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
#### Load to server Button ####
Special button which provide loading file from user device or computer to the server.
```
Button('Load', handler_when_loading_finish, icon='photo_library', type = 'gallery')
```
handler_when_loading_finish(button_, name_of_loaded_file) where name_of_loaded_file is name in upload server folder == 
optional upload_dir parameter of unigui.start

#### Camera Button ####
Special button which provide to make photo on the user mobile device. On PC behaves as 'Load to server Button'.
```
Button('Make photo', handler_when_shooting_finish, icon='camera_alt', type = 'camera')
```
handler_when_loading_finish(button_, handler_when_shooting_finish) where handler_when_shooting_finish is name in upload server folder == 
optional upload_dir parameter of unigui.start

#### Edit and Text field. ####
```
Edit('Some field', '') #for string value
Edit('Number field', 0.9) #for numbers
```
If set edit = false it will be readonly field or text label.
```
Edit('Some field', '', edit = false) 
#is equal to
Text('Some field')
```
complete handler is optional function which accepts current value and return a string list for autocomplete.
```
Edit('Edit me', value = '', complete = get_complete_list) #value has to be string or number

def get_complete_list(gui_element, current_value):
    return [s for s in vocab if current_value in s]    
```
Can contain optional 'update' handler which is called when the user press Enter in the field.
It can return None or objects for updating as usual handler.


#### Radio button ####
```
Switch('Radio button', value = True[,changed = ..]) #value has to be boolean, changed - optional
```

#### Select group. Contains options field. ####
```
Select('Select something', "choice1", options = ["choice1","choice2", "choice3"],changed = ..) # changed - optional as usual
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
unique_elems for the data without repeating names, it is dictionary {item_name:parent_name}. If 'unique_elems' defined then 'elems' is redundant.
'elems' for data which can contain repeating names. it is array of arrays [item_name,item_key,parent_key].
parent_name and parent_key are None for root items. changed_handler gets the tree object and item key as value which is the item name for unique items. 

### Table. ###
Tables is common structure for presenting 2D data and charts. Can contain append, delete, update handlers, multimode value is True if allowed single and multi select mode. True by default. All of them are optional. When you add a handler for such action Unigui will draw an appropriate action icon button in the table header automatically.
```
table = Table('Videos', [0], row_changed, headers = ['Video', 'Duration', 'Owner', 'Status'],  
  rows = [
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed']
  ], 
  multimode = false, update = update)
```
If headers length is equal row length Unigui counts row id as an index in rows array.
If row length length is headers length + 1, Unigui counts row id as the last row field.
If table does not contain append, delete arguments, then it will be wrawn without add and remove icons.  value = [0] means 0 row is selected in multiselect mode (in array). multimode is False so switch icon for single select mode will be not drawn and switching to single select mode is not allowed.


By default Table has toolbar with search field and icon action buttons. It is possible to hide it if set tools = False in the Table constructor.

Table has paginator if all rows can not be drawn on the screen. Otherwise a table paginator is redundant and omitted.

If the selected row is not on the currently visible page then setting 'show = True' table parameter causes Unigui to switch to the page with the selected row. 

### Table handlers. ###
complete, modify and update have the same format as the others elements, but value is consisted from the cell value and its position in the table.
'update' is called when user presses the Enter, 'modify' when the cell value is changed. By default it has standart modify method which updates rows data, it can be locked by
setting 'edit = False' in Table constructor.
They can return Error or Warning if the value is not accepted, othewise the handler has to call accept_value(table, value) for accepting the value and return None.
```
def table_updated(table_, tabval):
    value, position = tabval
    #check value
    ...
    if error_found:
        return Error('Can not accept the value!')
    accept_value(_, value)
```
The 'changed' table handler accept the selected row number or id as a value.

'editing' handler called when the user switch the table edit mode. it is optional and has signature editing(table, edit_mode_now) where the second parameter says the table is being edited or not.

### Chart ###
Chart is a table with additional Table constructor parameter 'view' which explaines unigui how to draw a chart. The format is '{x index}-{y index1},{y index2}[,..]'. '0-1,2,3' means that x axis values will be taken from 0 column, and y values from 1,2,3 columns of row data.
'i-3,5' means that x axis values will be equal the row index in rows, and y values from 3,5 columns of rows data. If a table constructor got view = '..' parameter then unigui displays a chart icon at the table header, pushing it switches table mode to the chart mode. If a table constructor got type = 'view' in addition to view parameter the table will be displayed as chart on start. In the chart mode pushing the icon button on the top right switches back to table row mode.

### Signals ###
Unigui supports a dedicated signal event handling mechanism. They are useful in table fields and shared blocks when the containing blocks and screens must respond to their elements without program linking. If a string in a table field started from @ then it considered as a signal. If the user clicks such field in non-edit mode then Unigui generates a signal event, which comes to dispatch function of its containters. First Unigui look at the element block, if not found than at the screen, if not found User.dispatch will be called, which can be redefined for such cases. Any handler can return Signal(element_that_generated_the_event, '@the_event_value') which will be processed.


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
content can be filled by any Gui element sequence for additional dialog functionality.

### Popup windows ###
They are intended for non-blocking display of error messages and informing about some events, for example, incorrect user input and the completion of a long process on the server.
```
Info(info_message)
Warning(warning_message)
Error(error_message)
UpdateError(updated_element, error_nessage)
```
They are returned by handlers and cause appearing on the top screen colored rectangles window for 3 second. UpdateError also says Unigui to update changed updated_element.


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
In screens and blocks sources we can access the user by call get_user()
```
user = get_user()
print(isinstance(user, Hello_user))
```

More info about User class methods you can find in manager.py in the root dir.

Example is in tests folder.

The articles about Unigui:

in English https://docs.google.com/document/d/1G_9Ejt9ETDoXpTCD3YkR8CW508Idk9BaMlD72tlx8bc/edit?usp=sharing

in Russian https://docs.google.com/document/d/1EleilkEX-m5XOZK5S9WytIGpImAzOhz7kW3EUaeow7Q/edit?usp=sharing
