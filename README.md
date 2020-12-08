/README.md>
# unigui #
Universal App Browser

### Purpose ###
Provide programming technology that does not require client programming, for a server written in any language, for displaying on any device, in any resolution, without any turning.

### How to ###
The exchange protocol for the solution is JSON as the most universally accessible, comprehensible, readable, and popular format compatible with all programming languages.  The server sends JSON data to App Browser which has built-in tools (autodesigner) that allows you to easily generate a beautiful GUI that conforms to Google’s Material Design standard.


### Programming ###
The program directory has to contain a folder screens. The folder contains all screens which the Unigui has to show.
Example.

screens/main.py
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
block = Block('Groups', 
    [   Select('Select', value='All', options=['All','Based','Group']),
        Select('Group', value='Group1', options=['Group 1','Group 2', 'Group 3'])
    ], table)
#what to show on the screen
blocks = [block] 
```

### Server start ###
```
import unigui
unigui.start('Test app', 8080) #app name to show in Unigui and port for initial connection
```
Unigui builds the interactive app on client side for the code above:
![alt text](https://github.com/Claus1/unigui/blob/main/tests/scrshoot1.png?raw=true)





