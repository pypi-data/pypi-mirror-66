
import tiles

"""This is the actual world """
import random

_world = {}
starting_position = (0, 0)

#Now, this function goes through the map tile and creates a dictionary that contains the coordinates and the tile name


def load_tiles():
    """Parses a file that describes the world space into the _world object"""
    with open('resources/map.txt', 'r') as f:
        rows = f.readlines()
        row=[]

        # the following lines takes each row of the map.txt file and appends them to a long list. Then it shuffles the list randomly and then it
        # creates a new list with all the tiles randomly shuffled.

  #      for i in range(len(rows)):
  #          row.extend(rows[i].replace('\n','').split('\t'))
  #          #print(rows[i])
  #          #print(row)
  #          random.shuffle(row)
  #          val=0
  #          row2=[]
  #          while val<len(row):
  #              row2.append('\t'.join(row[val:val+4])+'\n')
  #              #print(row2)
  #              val+=4

  #  rows=row2
    x_max = len(rows[0].split('\t')) # Assumes all rows contain the same number of tabs

    for y in range(len(rows)):
        cols = rows[y].split('\t')

        for x in range(x_max):
            tile_name = cols[x].replace('\n', '') # Windows users may need to replace '\r\n'

            #This just says that if the tile_name is startingroom, that should be our starting position.
            if tile_name == 'startingRoom':
                global starting_position
                starting_position = (x, y)

            #The variable _world is a dictionary that maps a coordinate pair to a tile. So the code _world[(x, y)]=....
            #creates the key (i.e. the coordinate pair) of the dictionary. If the cell is
            #an empty string, we don’t want to store a tile in it’s place which is why we have the code None if tile_name == ''.
            #However, if the cell does contain a name, we want to actually create a tile of that type. The getattr method is
            #built into Python and lets us reflect into the tile module and find the class whose name matches tile_name.
            #Finally the (x, y) passes the coordinates to the constructor of the tile.

            _world[(x, y)] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)

            if tile_name == '':
                _world[(x,y)] = None

            else:
                _world[(x, y)] = getattr(__import__('tiles'), tile_name)(x, y)



"""
    rlist=[0, len(rows)-1]
    print(rlist)

    print(rows)
    for key, value in _world.items():
        if(isinstance(value, tiles.leaveForrestTile)):
            print(key,value)
            print(key[0])
            if (key[1] != 0) and (key[1] != len(rows)-1):
                print("boo")
                nkey = (random.randint(0,3),random.choice(rlist))
                print(nkey)
                _world[key]= _world[nkey]
                print(_world[key])
                print(_world[nkey])
                print(_world)
                """








def emptify_tile(x,y):
    _world[(x, y)] = tiles.emptyForrestTile(x, y)
    return _world[(x, y)]


def tile_exists(x,y):
    """Returns the tile at the given coordinates or None if there is no tile.
    :param x: the x-coordinate in the worldspace
    :param y: the y-coordinate in the worldspace
    :return: the tile at the given coordinates or None if there is no tile
    """
    return _world.get((x,y))
