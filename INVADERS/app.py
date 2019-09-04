"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There 
is no need for any additional classes in this module.  If you need more classes, 99% of 
the time they belong in either the wave module or the models module. If you are unsure 
about where a new class should go, post a question on Piazza.

Nathan Stack (nts28) and Michael Chin (msc288)
Completed: 12/4/2017
"""
import cornell
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.
    
    The primary purpose of this class is to manage the game state: which is when the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS: 
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.
    
    For a complete description of how the states work, see the specification for the
    method update.
    
    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be 
    documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    Extra attributes (and their invariants):
        _spress: whether or not s was pressed last frame
                [Bool]
        _mpress: whether or not m was pressed last frame 
                [Bool]
    """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = STATE_INACTIVE
        if self._state==STATE_INACTIVE:
            self._text = GLabel(text="Press 'S' to Play",font_size=50.0,x=GAME_WIDTH/2,\
                                y=GAME_HEIGHT/2,halign='center',valign='middle')
        else:
            self._text = None
        self._spress = False
        self._mpress = False
        self._wave = None  
    
    def update(self,dt):
        """
        Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.
        
        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these 
        does its own thing and might even needs its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the 
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).
        
        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen. 
        The application switches to this state if the state was STATE_INACTIVE in the 
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        STATE_CONTINUE: This state restores the ship after it was destroyed. The 
        application switches to this state if the state was STATE_PAUSED in the 
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_COMPLETE: The wave is over, and is either won or lost.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Some code in this method was copied from the state.py demo from class, created
        by the CS 1110 instructors.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        S = self.input.is_key_down('s')
        if S and not self._spress and self._state==STATE_INACTIVE:
            self._spress = True
            self._text = None
            self._state = STATE_NEWWAVE
        if self._state == STATE_NEWWAVE:
            self._wave = Wave(1, ALIEN_SPEED,0)
            self._state = STATE_ACTIVE
        self._checkGameOver()                  
        if self._state == STATE_ACTIVE:
            self._wave.update(self.input,dt)
            self._checkMute()
        if not self._wave is None:
            if self._wave.getShip() is None and self._wave.getLives() > 0 and self._state!=STATE_PAUSED:
                self._state = STATE_PAUSED
                self._wave.setLives(self._wave.getLives()-1)
                self._wave.setBolts([])
        self._checkStatePaused()
        self._checkBetweenWaves()
        
    def draw(self):
        """
        Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in 
        Wave. In order to draw them, you either need to add getters for these attributes 
        or you need to add a draw method to class Wave.  We suggest the latter.  See 
        the example subcontroller.py from class.
        """
        # IMPLEMENT ME
        if not self._text is None:
            self._text.draw(self.view)
        if self._state == STATE_ACTIVE:
            self._wave.draw(self.view)
    
    # HELPER METHODS GO HERE
    def _checkMute(self):
        """
        This function responds to key presses, based upon which it either mutes
        the sound or unmutes the sound. If the sound is currently muted, pressing
        the 'M' key will unmute the sound. If the sound is currently unmuted, pressing
        the 'M' key will mute the sound
        """
        M = self.input.is_key_down('m')
        if M and not self._mpress and self._wave.getMute() == False:
            self._wave.setMute(True)
            self._mpress = True
        if not M:
           self._mpress = False
        if M and not self._mpress and self._wave.getMute() == True:
            self._wave.setMute(False)
            self._mpress = True
            
    def _noAliens(self,aliens):
        """
        Returns True if all elements in every row of aliens are None.
        
        Precondition: parameter aliens is a 2d list of aliens in the wave
                      [rectangular 2d list of Alien or None]
        """
        for row in aliens:
            for alien in row:
                if isinstance(alien,Alien):
                    return False
        return True
    
    def _belowdefenseline(self,aliens):
        """
        Returns True if any alien in any row of (parameter) aliens dips below the defense line.
        
        Precondition: parameter aliens is a 2d list of aliens in the wave
                      [rectangular 2d list of Alien or None]
        """
        for row in aliens:
            for alien in row:
                if not alien is None:
                    y = alien.getY() - ALIEN_HEIGHT/2
                    if y <= DEFENSE_LINE:
                        return True
        return False
    
    def _checkStatePaused(self):
        """
        If the current state of the game is STATE_PAUSED, this function responds accordingly.
        If the current state is not STATE_PAUSED, this function does nothing.
        
        If the state is STATE_PAUSED, this function changes the currently active message
        to be displayed on the screen and responds to key presses (based upon which it changes
        the state to STATE_ACTIVE and creates a new player ship to be displayed on the screen).
        """
        S = self.input.is_key_down('s')
        if self._state == STATE_PAUSED:
            self._text = GLabel(text="Press 'S' to Continue",font_size=50.0,\
                                x=GAME_WIDTH//2,y=GAME_HEIGHT//2,halign='center',\
                                valign='middle')
            self._spress = False
        if S and not self._spress and self._state == STATE_PAUSED:
            self._wave.setShip(Ship(GAME_WIDTH/2))
            self._text = None
            self._spress = True
            self._state = STATE_ACTIVE
            
    def _checkGameOver(self):
        """
        Checks if the game is over by determining if the player is out of lives,
        if the aliens have reached the defensive line, or if the player has beaten
        all of the waves (and responds accordingly)
        """
        if not self._wave is None:    
            aliens = self._wave.getAliens()
            if self._belowdefenseline(aliens) or self._wave.getLives()==0:
                self._state = STATE_COMPLETE
                self._text = GLabel(text="GAME OVER",font_size=50.0,\
                                x=GAME_WIDTH//2,y=GAME_HEIGHT//2,halign='center',\
                                valign='middle')
            if self._noAliens(aliens) and self._wave.getWavesNum() == 3:
                self._state = STATE_COMPLETE
                self._text = GLabel(text="YOU WIN!!!",font_size=50.0,\
                                x=GAME_WIDTH//2,y=GAME_HEIGHT//2,halign='center',\
                                valign='middle')
    
    def _checkBetweenWaves(self):
        """
        If there are no aliens in the current alien wave and there are still more
        alien waves for the player to beat, this function creates a message to be
        drawn on the window that tells the player to press the 'S' key to continue onto
        the next wave.
        
        A new wave is then created. This function also increases the speed of the aliens
        in this newly created alien wave so that the alien wave gets progressively faster
        after each wave is complete. Also, when a new wave is created, the number of
        ship lives left (_lives in wave.py) gets reset to SHIP_LIVES
        """
        S = self.input.is_key_down('s')
        if not self._wave is None:
            aliens = self._wave.getAliens()
            speed = self._wave.getSpeed() * .90
            if self._noAliens(aliens) and self._wave.getWavesNum() < 3:
                self._state = STATE_BETWEEN_WAVES
                self._spress = False
                text = 'Wave ' + str(self._wave.getWavesNum()) + \
                " complete. Press 'S' to start Wave " + str(self._wave.getWavesNum()+1)
                self._text = GLabel(text=text,font_size=40.0,x=GAME_WIDTH/2,\
                                y=GAME_HEIGHT/2,halign='center',valign='middle')
                if S and not self._spress:
                    self._wave = Wave(self._wave.getWavesNum() + 1, speed,self._wave.getScore())
                    score = 'Score: ' + str(self._wave.getScore())
                    self._score = GLabel(text=score,font_size=20.0,x=GAME_WIDTH*.2,\
                                         y=GAME_HEIGHT*.9,halign='center',valign='middle')
                    self._state = STATE_ACTIVE
                    self._text = None