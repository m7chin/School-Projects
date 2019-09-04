"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Nathan Stack (nts28) and Michael Chin (msc288)
12/4/2017
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship or None]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _Adirection:    whether the aliens are moving right or left
                        [string, either 'left' or 'right']
        _numstep:       the number of steps the alien wave has taken since
                        last bolt fired [int >= 0]
        _rand:          a random integer in range [1,BOLT_RATE]
                        [1<= int <= BOLT_RATE]
        _waveNum:       The wave number that the player is on [1 <= int <= 3]
        _speed:         the number of seconds (0 < float <= 1) between alien steps
                        (copied from consts.py written by CS 1110 instructors)
        _score:         the current player score [int >= 0]
        _scorelabel:    the GLabel that displays current player score
                        [GLabel]
        _liveslabel:    the GLabel that displays the number of lives left
                        [GLabel]
        _mute:          a Boolean value indicating whether or not the sounds for
                        the game are muted [True or False]
        _shipPew:       the sound that plays every time the ship fires a bolt (unless
                        _mute==True) [a Sound object]
        _alienPew:      the sound that plays every time an alien fires a bolt (unless
                        _mute==True) [a Sound object]
        _alienBoom:     the sound that plays every time a ship bolt collides with an
                        alien (unless _mute==True) [a Sound object]
        _shipBoom:      the sound that plays every time an alien bolt collides with
                        the ship (unless _mute==True) [a Sound object]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getScore(self):
        """
        Returns: the current player score"""
        return self._score
    
    def getLives(self):
        """
        Returns: the number of lives left [int >= 0]
        """
        return self._lives
    
    def setLives(self,lives):
        """
        Sets the number of lives left
        
        Precondition: parameter lives is an int >= 0
        """
        assert type(lives)==int and lives >= 0
        self._lives = lives
    
    def getShip(self):
        """
        Returns: the player ship to control [either Ship or None]
        """
        return self._ship
    
    def setShip(self,ship):
        """
        Sets the player ship to control
        
        Precondition: parameter ship is a Ship object
        """
        assert isinstance(ship,Ship)
        self._ship = ship
        
    def getAliens(self):
        """
        Returns: the 2d list of aliens in the wave [each position in each row contains
                 either Alien or none]
        """
        return self._aliens
    
    def setBolts(self,bolts):
        """
        Sets the laser bolts currently on screen
        
        Precondition: parameter bolts is a list of Bolt, possibly empty
        """
        assert type(bolts)==list
        for bolt in bolts:
            assert isinstance(bolt,Bolt)
        self._bolts = bolts
        
    def getWavesNum(self):
        """
        Returns the number of waves the player has seen
        """
        return self._waveNum
    
    def setWavesNum(self, wave):
        """
        Sets the number of waves the player has seen to wave
        """
        self._waveNum = wave
    
    def getSpeed(self):
        """
        Returns the speed of the aliens
        """
        return self._speed
    
    def setSpeed(self, speed):
        """
        Sets the speed of the aliens to speed
        
        Parameter speed: the number of seconds between alien steps.
        Precondition: speed = (0 < float <= 1)
        """
        assert type(speed) is float and speed > 0 and speed <=1
        self._speed = speed
    
    def getMute(self):
        """
        Returns: a Boolean value indicating whether or not the sounds for
                        the game are muted
        """
        return self._mute
    
    def setMute(self,mute):
        """
        Sets the _mute attribute to the parameter mute
        
        Parameter mute: a Boolean value that indicates whether or not the sounds
        for the game should be muted
        """
        assert type(mute) is bool
        self._mute = mute
        
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self,wave,speed,score):
        """
        Creates a new instance of Wave, the subcontroller for a single wave,
        which manages the ships and aliens.
        
        Creates the ship, aliens, and the defense line while also creating a list of bolts,
        setting the attribute _time to zero, and setting the initial direction of the aliens.
        It also sets the attribute _numstep to zero, sets the attribute _rand which is used
        to determine when the aliens need to fire bolts, sets the number of
        lives to SHIP_LIVES, and sets the attribute _waveNum.
        """
        self._aliens = self._startAlienWave(ALIEN_H_SEP+ALIEN_WIDTH/2,GAME_HEIGHT-\
                                       ALIEN_CEILING-ALIEN_HEIGHT/2-\
                                       (ALIEN_V_SEP+ALIEN_HEIGHT)*(ALIEN_ROWS-1))
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
                            linewidth=1,linecolor='black')
        self._ship = Ship(GAME_WIDTH/2)
        self._bolts = []
        self._time = 0
        self._Adirection = 'right'
        self._numstep = 0
        self._rand = random.randint(1,BOLT_RATE)
        self._lives = SHIP_LIVES
        self._waveNum = wave
        self._speed = speed
        self._shipPew = Sound('pew1.wav')
        self._alienPew = Sound('pew2.wav')
        self._alienBoom = Sound('blast2.wav')
        self._shipBoom = Sound('blast1.wav')
        self._mute = False
        self._score = score
        self._scorelabel = GLabel(text='Score : '+str(score),font_size=30.0,\
                                  y=GAME_HEIGHT*.97,left=GAME_WIDTH*0.02)
        self._liveslabel = GLabel(text='Lives: '+str(self._lives),font_size=30.0,\
                                  y=GAME_HEIGHT*.97,left=GAME_WIDTH*.85)
        
    
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Updates the game to move the ships, aliens and laser bolts for every change in time dt
        
        Parameter input: The key input
        Precondition: input is an instance of GInput
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if not self._ship is None:
            x = self._ship.moveShip(input)
            self._ship = Ship(x)
        
        self._updateShipBolts(input)
        
        self._moveAliens(input,dt)
        self._updateAlienBolts()
        self._detectCollisions()
        self._scorelabel.text = 'Score: ' + str(self._score)
        self._liveslabel.text = 'Lives: ' + str(self._lives)
        
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the Ship, Aliens, Defensive Line and Bolts
        
        Precondition: parameter view is an instance of GView
        """
        for row in self._aliens:
            for alien in row:
                if not alien is None: 
                    alien.draw(view)
        self._dline.draw(view)
        if not self._ship is None:
            self._ship.draw(view)
        if len(self._bolts)!=0:
            for bolt in self._bolts:
                bolt.draw(view)
        self._scorelabel.draw(view)
        self._liveslabel.draw(view)
        
    
    # HELPER METHODS
    def _startAlienWave(self,x,y):
        """
        Returns: a 2d list of aliens at starting positions x and y.
        
        Parameter x: the starting x coordinate for the center of the bottom left most alien
        Precondition: x is an int or float
        
        Parameter y: the starting y coordinate for the center of the bottom left most alien
        Precondition: y is an int or float
        """
        result = []
        
        for row in range(ALIEN_ROWS):
            result.append([])
            y1 = y + (ALIEN_V_SEP+ALIEN_HEIGHT)*row
            if row % 2 !=0:
                row_num = row - 1
            else:
                row_num = row
            image = ALIEN_IMAGES[row_num % len(ALIEN_IMAGES)]
                
            for col in range(ALIENS_IN_ROW):
                x1 = x + (ALIEN_H_SEP+ALIEN_WIDTH)*col
                result[row].append(Alien(x1,y1,image))
        
        return result
    
    def _updateAlienWave(self,x,y):
        """
        Updates the Aliens to their new position x and y and returns the new list of aliens
        
        Parameter x: the new x coordinate for the bottom left most alien
        Precondition: x is an int or float
        
        Parameter y: the new y coordinate for the bottom left most alien
        Precondition: y is an int or float
        """
        result = []
        
        for row in range(ALIEN_ROWS):
            result.append([])
            y1 = y + (ALIEN_V_SEP+ALIEN_HEIGHT)*row
            if row % 2 !=0:
                row_num = row - 1
            else:
                row_num = row
            image = ALIEN_IMAGES[row_num % len(ALIEN_IMAGES)]
                
            for col in range(ALIENS_IN_ROW):
                x1 = x + (ALIEN_H_SEP+ALIEN_WIDTH)*col
                if self._aliens[row][col]:
                    result[row].append(Alien(x1,y1,image))
                else:
                    result[row].append(None)
        
        return result

    def _moveAliens(self,input,dt):
        """
        Moves the aliens if the instance attribute _time is >= ALIEN_SPEED
        
        Parameter input: the key input, an instance of GInput
        Parameter dt: the change in time, a float
        """
        self._time += dt
        if self._time >= self._speed and self._Adirection=='right':
            blcorner = self._findblcorner()
            x = blcorner[0]
            y = blcorner[1]
            alien_right = self._rightmostAlien()
            x1 = alien_right.getX()
            right_edge = (x1+ALIEN_WIDTH/2)
            if GAME_WIDTH-right_edge < ALIEN_H_SEP:
                y -= ALIEN_V_WALK
                self._aliens = self._updateAlienWave(x,y)
                self._Adirection = 'left'
            else:
                x += ALIEN_H_WALK
                self._aliens = self._updateAlienWave(x,y)
            self._time = 0
            self._numstep += 1
       
        elif self._time >= self._speed and self._Adirection=='left':
            blcorner = self._findblcorner()
            x = blcorner[0]
            y = blcorner[1]
            alien_left = self._leftmostAlien()
            x1 = alien_left.getX()
            left_edge = (x1-ALIEN_WIDTH/2)
            if left_edge < ALIEN_H_SEP:
                y -= ALIEN_V_WALK
                self._aliens = self._updateAlienWave(x,y)
                self._Adirection = 'right'
            else:
                x -= ALIEN_H_WALK
                self._aliens = self._updateAlienWave(x,y)
            self._time = 0
            self._numstep += 1
    
    def _findblcorner(self):
        """
        Returns: the y coordinate bottom left corner of the alien wave.
                 The y coordinate refers to the alien that was in that position
                 when the alien wave was originally created.
        """
        for row in self._aliens:
            row1 = self._aliens.index(row)
            for alien in row:
                col = row.index(alien)
                if not alien is None:
                    x = alien.getX() - col*(ALIEN_H_SEP+ALIEN_WIDTH)
                    y  = alien.getY() - row1*(ALIEN_V_SEP+ALIEN_HEIGHT)
                    return (x,y)
    
    def _rightmostAlien(self):
        """
        Returns: (one of) the rightmost alien(s) in the current alien wave.
        """
        for col in range(ALIENS_IN_ROW):
            col = ALIENS_IN_ROW - 1 - col
            for row in range(ALIEN_ROWS):
                if not self._aliens[row][col] is None:
                    return self._aliens[row][col]

        
    def _updateShipBolts(self,input):
        """
        Creates a ship bolt if there is no prexisting ship bolt and moves the
        ship bolt if there is an existing one and appends the newly created bolt to _bolts.
        
        Parameter input: the user input, used to control the ship and change state
                  [instance of GInput]
        """
        space = input.is_key_down('spacebar')
        numShipBolts = 0
        # update existing ship bolt
        if len(self._bolts)!=0:    
            for bolt in self._bolts:
                if bolt.getVelocity()>0:
                    numShipBolts = 1
                    pos = self._bolts.index(bolt)
                    x = bolt.getX()
                    y = bolt.moveBolt('ship')
                    y1 = y - BOLT_HEIGHT/2
                    if y1 >= GAME_HEIGHT:
                        del self._bolts[pos]
                        numShipBolts=0
                    else:
                        self._bolts[pos] = Bolt(x,y,'ship')
                        
        if space and numShipBolts==0 and not self._ship is None:
            x = self._ship.getX()
            bolt = Bolt(x,SHIP_BOTTOM+SHIP_HEIGHT+BOLT_HEIGHT/2,'ship')
            if self._mute==False:
                self._shipPew.play()
            self._bolts.append(bolt)
    
    def _updateAlienBolts(self):
        """
        Creates an alien bolt if the criteria are met for an alien to fire
        one and moves the existing alien bolts
        """
        #update existing alien bolts
        if len(self._bolts)!=0:
            for bolt in self._bolts:
                if bolt.getVelocity()<0:
                    pos = self._bolts.index(bolt)
                    x = bolt.getX()
                    y = bolt.moveBolt('alien')
                    y1 = y + BOLT_HEIGHT/2
                    if y1 < 0:
                        del self._bolts[pos]
                    else:
                        self._bolts[pos] = Bolt(x,y,'alien')
        
        if self._rand == self._numstep:
            alien = self._findRandBottomAlien()
            x = alien.getX()
            y = alien.getY()
            bolt = Bolt(x,y,'alien')
            self._bolts.append(bolt)
            self._rand = random.randint(1,BOLT_RATE)
            self._numstep = 0
            if self._mute==False:
                self._alienPew.play()
        
    
    def _isColEmpty(self, col):
        """
        Checks if the given column in the instance attribute _aliens is empty and
        returns True if it is and False if it is not.
        
        Parameter col: the column in the instance attribute _aliens to check
        Precondition: col is an int
        """
        for row in range(ALIEN_ROWS):
            if not self._aliens[row][col] is None:
                return False
        return True


    def _findRandBottomAlien(self):
        """
        Returns: the bottommost alien in a random column 
        """
        randCol = random.randint(0, ALIENS_IN_ROW-1)
        while self._isColEmpty(randCol):
            randCol = random.randint(0, ALIENS_IN_ROW-1)
        
        alien = None
        i = ALIEN_ROWS
        for row in range(ALIEN_ROWS):
            if self._aliens[row][randCol] != None and i > row:
                alien = self._aliens[row][randCol]
                i = row
        
        return alien
    
    def _detectCollisions(self):
        """
        Detects if an alien's bolt collides with the ship and if the ship's bolt
        collides with an alien. Also deletes the bolt and the alien or ship if there
        is a collision. Also, when a ship bolt collides with an alien bolt, the
        alien wave speeds up.
        """
        if self._bolts != 0:    
            for bolt in self._bolts:
                pos_bolt = self._bolts.index(bolt)
            
            # Deal with alien collisions
                for row in self._aliens:
                    row1 = self._aliens.index(row)
                    for alien in row:
                        col_alien = row.index(alien)
                        if not alien is None:
                            collision = alien.collides(bolt)
                            if collision:
                                if self._mute==False:
                                    self._alienBoom.play()
                                self._updateScore(alien,row1)
                                self._aliens[row1][col_alien] = None
                                del self._bolts[pos_bolt]
                                self.setSpeed(self.getSpeed()*.9875)
            # Deal with ship collisions
                if not self._ship is None:
                    collision = self._ship.collides(bolt)
                    if collision:
                        if self._mute==False:
                            self._shipBoom.play()
                        self._ship = None
                        del self._bolts[pos_bolt]
    
    def _leftmostAlien(self):
        """
        Returns: (one of) the leftmost alien(s) in the current alien wave.       
        """
        for col in range(ALIENS_IN_ROW):
            for row in range(ALIEN_ROWS):
                if not self._aliens[row][col] is None:
                    return self._aliens[row][col]
    
    def _updateScore(self,alien,row1):
        """
        Updates the current player score depending on the row and column in the alien wave
        where the alien (parameter) 'alien' exists (at row,col). Aliens in the front
        of the wave are worth less points than aliens in the back of the wave.
        """
        for row in range(ALIEN_ROWS):
            if row % 2 !=0: # if the row is odd
                row_num = row - 1
            else:
                row_num = row
            points = 10 + 10*(row_num)
            if row==row1:
                self._score += points
                    