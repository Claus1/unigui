# unigui #
Universal GUI Framework and Protocol (Python)

### Purpose ###
Provide a programming technology that does not require front-end programming, for a server written in any language, for displaying on any device, in any resolution, without any tuning. 

### Installing ###
```
pip install unigui
```

### How it works inside ###
The exchange protocol for the solution is JSON as the most universally accessible, readable, and popular format for Web. The server sends JSON data to the front-end unigui which has built-in tools (autodesigner) and automatically builds a standart Google Material Design GUI for the user data. No markup, drawing instructions and the other dull job are required. From the constructed Unigui screen the server receives a JSON message flow which fully describes what the user did. The message format is ["Block", "Elem", "type of action", value], where "Block"and "Elem"are the names of the block and its element, "value" is the JSON value of the action/event that has happened. The server can either accept the change or roll it back by sending an info window about an inconsistency. The server can open a dialog box, send popup Warning, Error,.. or an entirely new screen. Unigui instantly and automatically displays actual server state. 

### Programming ###
Unigui is the language and platform independent technology. This repo explains how to work with Unigui using Python and the tiny but optimal framework for that. Unigui web version is included in this library. Unigui for Go is accessible in https://github.com/Claus1/unigui-go

### High level - Screen ###
The program directory has to contain a screens folder which contains all screens which Unigui has to show.

Screen example tests/screens/main.py
```
name = "Main"
blocks = [block] 
```
The block example with a table and a selector
```
table = Table('Videos', 0, headers = ['Video', 'Duration',  'Links', 'Mine'],rows = [
    ['opt_sync1_3_0.mp4', '30 seconds',  '@Refer to signal1', True],
    ['opt_sync1_3_0.mp4', '37 seconds',  '@Refer to signal8', False]    
])
#widgets are groped in blocks (complex widgets with logic)
block = Block('X Block',
    [           
        Button('Clean table', icon = 'swipe'),
        Select('Select', value='All', options=['All','Based','Group'])
    ], table, icon = 'api')
```

| Screen global variables |	Status | Type | Description |
| :---: | :---: | :---: | :---: | 
| name  | Has to be defined | str | Unique screen name |
| blocks | Has to be defined | list |which blocks to show on the screen |
| user   | Always defined, read-only | User+ | Access to User(inherited) class which associated with a current user |
| header | Optional | str | show it instead of app name |
| toolbar | Optional | list | Gui elements to show in the screen toolbar |
| order | Optional | int | order in the program menu |
| icon  | Optional | str | MD icon of screen to show in the screen menu |
| prepare | Optional | def prepare() | Syncronizes GUI elements one to another and with the program/system data. If defined then is called before screen appearing. |


### Server start ###
tests/template/run.py
```
import unigui
unigui.start('Test app') 
```
Unigui builds the interactive app for the code above.
Connect a browser to localhast:8000 which are by default and will see:

![image](https://github.com/Claus1/unigui/assets/1247062/aca4db13-df32-4c16-8fff-e6a1a74bf640)

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
clean_button = Button('Clean the table’, clean_table)
```

| Handler returns |	Description |
| :---: | :---: | 
| Gui object |  Object to update |
| Gui object array or tuple |  Objects to update |
| None | Nothing to update, Ok |
| Error(...), Warning(...), Info(...) | Show to user info about a problem. |
| UpdateScreen, True | Redraw whole screen |
| Dialog(..) | Open a dialog with parameters |
| user.set_screen(screen_name) | switch to another screen |


Unigui	synchronizes GUI state on frontend-end automatically after calling a handler.

If a Gui object doesn't have 'changed' handler the object accepts incoming value automatically to the 'value' variable of gui object.

If 'value' is not acceptable instead of returning an object possible to return Error or Warning or Info. That functions can update a object list passed after the message argument.

```
def changed_range(_, value):
   if value < 0.5 and value > 1.0:
       #or Error(message, _) if we want to return the previous visible value to the field, return gui object _ also.
       return Error(f‘The value of {_.name} has to be > 0.5 and < 1.0!', _) 
    #accept value othewise
    _.value = value

edit = Edit('Range of involving', 0.6, changed_range, type = 'number')
```

### Block details ###
The width and height of blocks is calculated automatically depending on their children. It is possible to set the block width, or make it scrollable , for example for images list. Possible to add MD icon to the header, if required. width, scroll, height, icon are optional.
```
#Block(name, *children, **options)
block = Block(‘Pictures’,add_button, *images, width = 500, scroll = True,icon = 'api')
```
 
The first Block child is a widget(s) which are drawn in the block header just after its name.
Blocks can be shared between the user screens with its states. Such a block has to be located in the 'blocks' folder .
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
If some elements are enumerated inside an array, Unigui will display them on a line one after another, otherwise everyone will be displayed on a new own line(s).
 
Using a shared block in some screen:
```
from blocks.tblock import concept_block
...
blocks = [.., concept_block]
```

#### Events interception of shared elements ####
Interception handlers have the same in/out format as usual handlers.
#### They are called before the inner element handler call. They cancel the call of inner element handler but you can call it as shown below.
For example above interception of select_mode changed event will be:
```
@handle(select_mode, 'changed')
def do_not_select_mode_x(selector, value):
    if value == 'Mode X':
        return Error('Do not select Mode X in this context', selector) # send old value for update select_mode to the previous state
    return _.accept(value) #otherwise accept the value
```

#### Layout of blocks. #### 
If the blocks are simply listed Unigui draws them from left to right or from top to bottom depending on the orientation setting. If a different layout is needed, it can be set according to the following rule: if the vertical area must contain more than one block, then the enumeration in the array will arrange the elements vertically one after another. If such an element enumeration is an array of blocks, then they will be drawn horizontally in the corresponding area.

#### Example ####
blocks = [ [b1,b2], [b3, [b4, b5]]]
#[b1,b2] - the first vertical area, [b3, [b4, b5]] - the second one.

![image](https://github.com/Claus1/unigui/assets/1247062/75d0f64c-d457-43c6-a909-0c97f4b4ab0f)

### Basic gui elements ###
Normally they have type property which says unigui what data it contains and optionally how to draw the element. 
#### If the element name starts from _ , unigui will hide its name on the screen. ####
if we need to paint an icon in an element, add 'icon': 'any MD icon name' to the element constructor.

#### Most constructor parameters are optional for Gui elements except the first one which is the element name. ####

Common form for element constructors:
```
Gui('Name', value = some_value, changed = changed_handler)
#It is possible to use short form, that is equal:
Gui('Name', some_value, changed_handler)
```
calling the method 
def accept(self, value) 
causes  a call changed handler if it defined, otherwise just save value to self.value

### Button ###
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

### Load to server Button ###
Special button provides file loading from user device or computer to the Unigui server.
```
UploadButton('Load', handler_when_loading_finish, icon='photo_library')
```
handler_when_loading_finish(button_, the_loaded_file_filename) where the_loaded_file_filename is a file name in upload server folder. This folder name is defined in config.py .

### Camera Button ###
Special button provides to make a photo on the user mobile device. 
```
CameraButton('Make a photo', handler_when_shooting_finish, icon='camera_alt')
```
handler_when_loading_finish(button_, name_of_loaded_file) where name_of_loaded_file is the made photo name in the server folder. This folder name is defined in config.py .

### Edit and Text field. ###
```
Edit('Some field', '') #for string value
Edit('Number field', 0.9, type = 'number') #changed handler will get a number
```
If set edit = false it will be readonly field or text label.
```
Edit('Some field', '', edit = false) 
#is equal to
Text('Some field')
```
complete handler is optional function which accepts the current edit value and returns a string list for autocomplete.

```
def get_complete_list(gui_element, current_value):
    return [s for s in vocab if current_value in s]    

Edit('Edit me', 'value', complete = get_complete_list) #value has to be string or number
```

Optional 'update' handler is called when the user press Enter in the field.
It can return None if OK or objects for updating as usual 'changed' handler.

Optional selection property with parameters (start, end) is called when selection is happened.
Optional autogrow property uses for serving multiline fileds.


### Radio button ###
```
Switch('Radio button', value = True[,changed = .., type = ...])

Optional type can be 'check' for a status button or 'switch' for a switcher . 
```

### Select group. Contains options field. ###
```
Select('Select something', "choice1", selection_is_changed, options = ["choice1","choice2", "choice3"]) 
```
Optional type parameter can be 'toggles','list','dropdown'. Unigui automatically chooses between toogles and dropdown, if type is omitted,
if type = 'list' then Unigui build it as vertical select list.


### Image. ###
width,changed,height,header are optional, changed is called if the user select or touch the image.
When the user click the image, a check mark is appearing on the image, showning select status of the image.
It is usefull for image list, gallery, e.t.c
```
Image(image_url, header = 'description', changed = selecting_changed, width = .., height = ..)
```


### Video. ###
width and height are optional.
```
Video(video_url, width = .., height = ..)
```

### Tree. The element for tree-like data. ###
```
Tree(name, selected_item_name, changed_handler, options = {name1: parent1, name2 : None, .})
```
options is a tree structure, a dictionary {item_name:parent_name}. 
parent_name is None for root items. changed_handler gets item key (name) as value. 

### Table. ###
Tables is common structure for presenting 2D data and charts. 
Optional append, delete, update handlers are called for adding, deleting and updating rows.


Assigning a handler for such action causes Unigui to draw and activate an appropriate action icon button in the table header automatically.
```
table = Table('Videos', [0], row_changed, headers = ['Video', 'Duration', 'Owner', 'Status'],  
  rows = [
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed']
  ], 
  multimode = false, update = update)
```
Unigui counts rows id as an index in a rows array. If table does not contain append, delete arguments, then it will be drawn without add and remove icons.  
value = [0] means 0 row is selected in multiselect mode (in array). multimode is False so switch icon for single select mode will be not drawn and switching to single select mode is not allowed.

| Table option parameter |	Description |
| :---: | :---: | 
| changed  | table handler accept the selected row number |
| complete |  Autocomplete handler as with value type (string value, (row index, column index)) that returns a string list of possible complitions |
| append |  A handler gets new row index and return filled row with proposed values, has system append_table_row by default |
| delete | A handler gets list or index of selected rows and remove them. system delete_table_row by default |
| update | called when the user presses the Enter in a table cell |
| modify | default = accept_rowvalue(table, value). called when the cell value is changed by the user |
| edit   | default True. if true user can edit table, using standart or overloaded table methods |
| tools  | default True, then  Table has toolbar with search field and icon action buttons. |
| show   | default False, the table scrolls to (the first) selected row, if True and it is not visible |
| multimode | default True, allows to select single or multi selection mode |


### Table handlers. ###
complete, modify and update have the same format as the others handlers, but value is consisted from the cell value and its position in the table.


```
def table_updated(table_, tabval):
    value, position = tabval
    #check value
    ...
    if error_found:
        return Error('Can not accept the value!')
    accept_rowvalue(table_, tabval)
```

### Chart ###
Chart is a table with additional Table constructor parameter 'view' which explaines unigui how to draw a chart. The format is '{x index}-{y index1},{y index2}[,..]'. '0-1,2,3' means that x axis values will be taken from 0 column, and y values from 1,2,3 columns of row data.
'i-3,5' means that x axis values will be equal the row indexes in rows, and y values from 3,5 columns of rows data. If a table constructor got view = '..' parameter then unigui displays a chart icon at the table header, pushing it switches table mode to the chart mode. If a table constructor got type = 'linechart' in addition to view parameter the table will be displayed as a chart on start. In the chart mode pushing the icon button on the top right switches back to table view mode.

### Graph ###
Graph supports an interactive graph with optional draw methods.
```
graph = Graph('X graph', graph_value, graph_selection, 
    nodes = [
     { 'id' : 'node1', 'label': "Node 1" },
     { 'id' : 'node2', 'label': "Node 2" },
     { 'id' : 'node3', 'label': "Node 3" }    
  ], edges = [
     { 'id' : 'edge1', 'source': "node1", 'target': "node2", 'label' : 'extending' },
     { 'id' :'edge2' , 'source': "node2", 'target': "node3" , 'label' : 'extending'}     
  ])
```
where graph_value is a dictionary like {'nodes' : ["node1"], 'edges' : ['edge3']}, where enumerations are selected nodes and edges.
Constant graph_default_value == {'nodes' : [], 'edges' : []} i.e. nothing to select.

'changed' method graph_selector called when user (de)selected nodes or edges:
```
def graph_selection(_, val):
    _.value = val
    if 'nodes' in val:        
        return Info(f'Nodes {val["nodes"]}') 
    if 'edges' in val:
        return Info(f"Edges {val['edges']}") 
```
With pressed 'Shift' multi select works for nodes and edges.

Has optional draw 'method' with options 'random', 'circle', 'breadthfirst', by default 'random'.

### Dialog ###
```
Dialog(name, text, callback, buttons, content = None)
```
where buttons is a list of the dialog buttons like ['Yes','No', 'Cancel'].
Dialog callback has the signature as other with a pushed button name value
```
def dicallback(current_dialog, bname):
    if bname == 'Yes':
        do_this()
    elif ..
```
content can be filled with Gui elements for additional dialog functionality.


### Popup windows ###
They are intended for non-blocking displaying of error messages and informing about some events, for example, incorrect user input and the completion of a long process on the server.
```
Info(info_message, *someGUIforUpdades)
Warning(warning_message, *someGUIforUpdades)
Error(error_message, *someGUIforUpdades)
```
They are returned by handlers and cause appearing on the top screen colored rectangles window for 3 second. someGUIforUpdades is optional GUI enumeration for updating.

For long time processes it is possible to create Progress window. It is just call user.progress in any place.
Open window 
```
user.progress("Analyze .. Wait..")
```
Update window message 
```
user.progress(" 1% is done..")
```
Close window user.progress(None) or automatically when the handler returns something.

### Other subtle benefits of a Unigui protocol and technology. ###
1. Possible to work with any set of unigui resources as with a single system, within the same GUI user space, carries out any available operations, including crossing, on the fly.
2. Reproduces and saves sequences of the user interaction with the system without programming. It can be used for complex testing, supporting of security protocols and more.
3. Possible to mirror a session to other users, works simultaneously in one session for many users.


### Milti-user programming? You don't need it! ###
Unigui automatically creates and serves an environment for every user.
The management class is User contains all required methods for processing and handling the user activity. A programmer can redefine methods in the inherited class, point it as system user class and that is all. Such methods suit for history navigation, undo/redo and initial operations. The screen folder contains screens which are recreated for every user. The same about blocks. The code and modules outside that folders are common for all users as usual. By default Unigui use the system User class and you do not need to point it. 
```
class Hello_user(unigui.User):
    def __init__(self):
        super().__init__()
        print('New Hello user connected and created!')

unigui.start('Hello app', user_type = Hello_user)
```
In screens and blocks sources we can access the user by 'user' variable
```
print(isinstance(user, Hello_user))
```

More info about User class methods you can find in user.py in the souce dir.

Examples are in tests folder.

Unigui protocol messages from/to server you can see in a browser console (F12).
