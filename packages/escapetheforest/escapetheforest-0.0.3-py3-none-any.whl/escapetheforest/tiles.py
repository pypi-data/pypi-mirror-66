
import items, enemies, actions, world


class mapTile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tile_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        # Returns all move actions from adjacent tiles
        moves = []

        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.moveEast())

        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.moveWest())

        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.moveNorth())

        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.moveSouth())
        return moves

    def available_actions(self, pl):
        # Returns all possible actions from current tile
        moves = self.adjacent_moves()
        moves.append(actions.viewInventory())
     #   moves.append(actions.viewHP())
        moves.append(actions.viewStats())

        for i in range(0, len(pl.inventory)):
            if pl.inventory[i].name == "Wooden stick":
                moves.append(actions.sharpenStick())
                break

        for j in range(0, len(pl.inventory)):
            if pl.inventory[j].name == "Mushroom":
                moves.append(actions.eatMushroom())
                break

        moves.append(actions.killSelf())

        return moves


class startingRoom(mapTile):

    def run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)
            else:
                return """You are in an unremarkable part of the forest. You should keep going and find your way out of this murky forest."""
        wrapper.has_run = False
        return wrapper
    @run_once

    def tile_text(self):
        return "\n" "\n" """Suddenly you wake up and find yourself in a dark forest... You look around, wondering how you got there. 
It's damp and cold, so you decide to get moving. """

    def modify_player(self, player):
        # "Room has no action on player"
        pass

class emptyForrestTile(mapTile):
    def tile_text(self):
        return """Another unremarkable part of the forrest. You must forge onwards.
        """
    def modify_player(self, player):
        # Room has no action on player
        pass

class lootRoom(mapTile):
    def __init__(self, x, y, item):
        self.taken = False
        self.item = item
        super(lootRoom, self).__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        if (self.taken == False):
            self.add_loot(player)
            self.taken = True

class NPCtile(mapTile):
    def __init__(self, x, y, NPC):
        self.NPC=NPC
        self.metNPC = False
        super(NPCtile, self).__init__(x, y)



class traderTile(NPCtile):
    def __init__(self, x, y):
        super(traderTile, self).__init__(x, y, enemies.trader())

    def tile_text(self):
        if (self.NPC.is_alive()) and (self.metNPC == False):
            self.metNPC = True
            print("A small figure with a big ears suddenly stands in front of you on a stump. \n'Howdy! I'm a forest elf and I wanna buy mushrooms, I love them! You are welcome to sell them to me if you have any!'")
        elif (self.NPC.is_alive()) and (self.metNPC == True):
            return "The mushroom-loving elf stands there on the stump looking at you, " \
                   "waiting for you to sell him some mushrooms."
        else:
            return """The corpse of a dead elf rots on the ground.
            """

    def modify_player(self, the_player):
        # "Room has no action on player"
        pass

    def available_actions(self, pl):

        moves = self.adjacent_moves()
        moves.append(actions.viewInventory())
        moves.append(actions.viewStats())

        for i in range(0, len(pl.inventory)):
            if pl.inventory[i].name == "Wooden stick":
                moves.append(actions.sharpenStick())
                break

        for j in range(0, len(pl.inventory)):
            if pl.inventory[j].name == "Mushroom":
                moves.append(actions.eatMushroom())
                break

        for j in range(0, len(pl.inventory)):
            if (actions.sellMushroom() not in moves):
                #print("The action was not found")
                if pl.inventory[j].name == "Mushroom":
                   # print("Mushroom exists, adding the action")
                    moves.append(actions.sellMushroom())
                    break
        moves.append(actions.killSelf())
        return moves



class enemyRoom(mapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        self.hasAttacked = False
        self.metEnemy = False
        super(enemyRoom, self).__init__(x, y)

    def modify_player(self, the_player):
        if (self.enemy.is_alive()) and (self.enemy.isaggressive):
            the_player.hp = the_player.hp - self.enemy.damage
            if the_player.hp <= 0:
                print("The enemy does {} damage. You have {} hp remaining.".format(self.enemy.damage, the_player.hp))
                print("You fall to the ground, trying to crawl away from the enemy, but the enemy strikes one last blow leaving you dead on the ground...")

            else:
                print("The enemy does {} damage. You have {} hp remaining.".format(self.enemy.damage, the_player.hp))


    def available_actions(self, pl):
        if self.enemy.is_alive():
            return [actions.flee(tile=self), actions.attack(enemy=self.enemy)]
        else:
            moves = self.adjacent_moves()
            moves.append(actions.viewInventory())
            moves.append(actions.viewStats())

            for i in range(0, len(pl.inventory)):
                if pl.inventory[i].name == "Wooden stick":
                    moves.append(actions.sharpenStick())
                    break

            for j in range(0, len(pl.inventory)):
                if pl.inventory[j].name == "Mushroom":
                    moves.append(actions.eatMushroom())
                    break

            moves.append(actions.killSelf())
            return moves

class bigSpiderTile(enemyRoom):
    def __init__(self, x,y):
        #self.hasAttacked = False
        super(bigSpiderTile, self).__init__(x,y, enemies.bigSpider())

    def tile_text(self):
        if self.enemy.is_alive() and self.hasAttacked == False:
            self.hasAttacked = True
            return """A big spider comes to bite you!""""\n"

        elif self.hasAttacked == True:
            return """The big spider attacks again!"""
        else:
            return """A big dead spider lies on the ground here"""

class oldManTile(enemyRoom):
    def __init__(self, x, y):
        #self.metOldman= False
        super(oldManTile, self).__init__(x, y, enemies.crazyOldMan())

    def tile_text(self):
        if (self.enemy.is_alive()) and (self.metEnemy == False):
            self.metEnemy = True
            return """A crazy old man with red eyes and a big bears suddenly stands before you. He has an axe in his hand and runs towards you to hit you!
            """
        elif (self.enemy.is_alive()) and (self.metEnemy == True):
            return "The old man hits you with his axe."
        else:
            return """The corpse of an old dead man rots on the ground.
            """

class banditTile(enemyRoom):
    def __init__(self, x, y):
        super(banditTile, self).__init__(x, y, enemies.bandit())


    def tile_text(self):
        if (self.enemy.is_alive() and self.enemy.isaggressive == True):
            self.metEnemy = True
            return """The gives out a roar and strikes you, 'RRAAAAAHH!!'
            """

        elif (self.enemy.is_alive() and self.enemy.isaggressive == False and self.metEnemy == False):
            self.metEnemy = True
            return ("""A bandit approaches you! Hey hey, who do we have here... Don't you know that there is a fee of 10G to pass through here? Pay up, or die!
            """)

        elif (self.metEnemy == True) and (self.enemy.is_alive()) and (self.enemy.isaggressive == False):
            return """The bandit just stands and looks at you with an evil grin on his face"""

        else:
            return """The corpse of a dead man rots on the ground.
                        """

    def available_actions(self, pl):
        if (self.enemy.isaggressive == False) and self.enemy.is_alive():
            return [actions.giveTenG(enemy=self.enemy), actions.flee(tile=self), actions.attack(enemy=self.enemy)]

        elif (self.enemy.isaggressive==True) and self.enemy.is_alive():
            return [actions.flee(tile=self), actions.attack(enemy=self.enemy)]

        elif (self.enemy.isaggressive==True) and (self.enemy.is_alive()) and (self.metBandit == True):
            return mapTile.available_actions(self, pl)

        elif not self.enemy.is_alive():
            #This mf returns only the available actions from the maptile class, fuk yaaaaah!!
            return mapTile.available_actions(self, pl)


class ringleaderTile(enemyRoom):
    def __init__(self, x, y):
        super(ringleaderTile, self).__init__(x, y, enemies.ringLeader())

    def tile_text(self):
        if (self.enemy.is_alive()) and (self.enemy.isaggressive == True) and (self.hasAttacked == False):
            self.hasAttacked = True
            return """'RRAAAAAHH!!'
            """
        elif self.hasAttacked == True:
            return """The bandit ringleader attacks again!"""

        elif (self.enemy.is_alive()) and (self.enemy.isaggressive == False):
            return ("""The bandit ringleader approaches you!
'So, you have come to visit our dark forest? We dont want people snooping around here. Pay up 30 gold or die!'
            """)

        else:
            pass


    def available_actions(self, pl):
        if (self.enemy.isaggressive == False) and self.enemy.is_alive():
            return [actions.giveAllMoney(enemy=self.enemy), actions.flee(tile=self), actions.attack(enemy=self.enemy)]
        elif (self.enemy.isaggressive==True) and self.enemy.is_alive():
            return [actions.flee(tile=self), actions.attack(enemy=self.enemy)]

        elif not self.enemy.is_alive():
            #This returns only the available actions from the maptile class:
            return mapTile.available_actions(self, pl)



class findKnifeTile(lootRoom):
    def __init__(self, x, y):
        super(findKnifeTile, self).__init__(x, y, items.knife())

    def tile_text(self):
        if self.taken == False:
            return """Your notice something on the ground. It's a knife! You pick it up.
        """
        else:
            return """
        Another unremarkable part of the forrest. You must forge onwards.
        """


###Create more rooms for finding gold and stumbling upon the ringleader!

class leaveForrestTile(mapTile):

    def tile_text(self):
        return """You see a field crossed by a road glimpsing between the trees.
    You are outside of the forest!"""

    def modify_player(self, player):
        player.victory = True


class findStickTile(lootRoom):

    def __init__(self, x, y):
        super(findStickTile, self).__init__(x, y, items.stick())

    def tile_text(self):
        if self.taken == False:
            return """You see a piece of wood, it might make a decent weapon and you pick it up. """
        else:
            return """Another unremarkable part of the forrest. You must forge onwards."""


class findMushRoomTile(lootRoom):
    token = 0
    def __init__(self, x, y):
        super(findMushRoomTile, self).__init__(x, y, items.mushRoom())

    def tile_text(self):
        if self.taken == False:
            return """Your notice something on the ground. It's a strange looking mushroom! You pick it up."""

        elif self.token == 0:
            self.token = 1
            return """Another unremarkable part of the forrest. You must forge onwards."""

        else:
            return """Another unremarkable part of the forrest. You must forge onwards."""





