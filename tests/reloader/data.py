remote_image ="https://bestfriends.org/sites/default/files/styles/hero_mobile/public/hero-dash/Asana3808_Dashboard_Standard.jpg?h=ebad9ecf&itok=cWevo33k"


local_video = "web/sad cat.mp4"
local_image = "C:/Users/georg/Desktop/Projects/save/animals/bear/039b2ae790.jpg"
public_dir = "C:/Users/georg/Desktop/Projects/save/animals"


tree_options = {
    'Animals' : None,
    'Brushtail Possum' : 'Animals',
    'Genet' : 'Animals',
    'Silky Anteater' : 'Animals',
    'Greater Glider' : 'Animals',
    'Tarsier' : 'Animals',
    'Kinkajou' : 'Animals',
    'Tree Kangaroo' : 'Animals',
    'Sunda Flying Lemur' : 'Animals',
    'Green Tree Python' : 'Animals',
    'Fruit Bat' : 'Animals',
    'Tree Porcupines' : 'Animals',
    'Small Tarsier' : 'Tarsier',
    'Very small Tarsier': 'Small Tarsier'
}


nodes = [
     { 'label': "Node 1" },
     { 'label': "Node 2" },
     { 'label': "Node 3" },
     { 'label': "Node 4" }
  ]
edges = [
     { 'source': 0, 'target': 1, 'label' : 'extending' },
     { 'source': 1, 'target': 2 , 'label' : 'extending'},
     { 'source': 2, 'target': 3  },
     { 'source': 3, 'target': 1  },
     { 'source': 3, 'target': 0  }
  ]
import random, pandas as pd
headers = ['Audio', 'Duration,sec', 'Stars']
rows =  [[f'sync{i}.mp3', round(random.random() * 15000) / 100, random.randint(1,50)] for i in range(50)]
view = 'i-1,2'  


panda_table = pd.read_csv('../blocks/class.csv')
