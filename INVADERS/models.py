"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

Nathan Stack (nts28) and Michael Chin (msc288)
12/4/17
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
            _x: the x coordinate of the ship [int or float >= 0]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        put specification here
        """
        return self._x
    
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x):
        """
        Creates a new ship object by calling the initializer of GImage, where the
        x coordinate of the center of the Ship object to be created is given by
        the parameter x.
        
        Parameter x: the x coordinate of the center of the Ship object
        Precondition: x must be an int or float >= (0 + SHIP_WIDTH / 2) and <= (GAME_WIDTH - SHIP_WIDTH/2)
        """
        assert type(x) in [int,float]
        assert x >= SHIP_WIDTH/2
        assert x <= GAME_WIDTH - SHIP_WIDTH/2
        self._x = x
        GImage.__init__(self,x=x,y=SHIP_BOTTOM+SHIP_HEIGHT/2,width=SHIP_WIDTH,\
                        height=SHIP_HEIGHT,source='ship.png')
        
    def moveShip(self,input):
        """
        Returns: new x coordinate of ship, which changes in response to key presses
        """
        x = self._x
        if input.is_key_down('left'):
            x -= SHIP_MOVEMENT
        if input.is_key_down('right'):
            x += SHIP_MOVEMENT
        if x > GAME_WIDTH-SHIP_WIDTH/2:
            x = GAME_WIDTH-SHIP_WIDTH/2
        if x < SHIP_WIDTH/2:
            x = SHIP_WIDTH/2
        return x
        
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by an alien and collides with this
                 instance of ship
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        
        [this specification was copied nearly verbatim from the CS 1110 website.
        This specification was written by the CS 1110 instructors.]
        """
        if bolt.getVelocity() < 0: #bolt fired by an alien
            corner1 = (bolt.getX() - BOLT_WIDTH/2,bolt.getY() + BOLT_HEIGHT/2)
            corner2 = (bolt.getX() - BOLT_WIDTH/2,bolt.getY() - BOLT_HEIGHT/2)
            corner3 = (bolt.getX() + BOLT_WIDTH/2,bolt.getY() + BOLT_HEIGHT/2)
            corner4 = (bolt.getX() + BOLT_WIDTH/2,bolt.getY() - BOLT_HEIGHT/2)
            corners = [corner1,corner2,corner3,corner4]
            for corner in corners:
                if self.contains(corner):
                    return True
        return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _x: the x coordinate of the center of the Alien object
            [ALIEN_WIDTH/2 <= int or float <= GAME_WIDTH-ALIEN_WIDTH/2]
        _y: the y coordinate of the center of the Alien object
            [DEFENSE_LINE <= int or float <= GAME_HEIGHT-ALIEN_HEIGHT/2]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns: the x coordinate of the center of the Alien object
        """
        return self._x
    
    def getY(self):
        """
        Returns: the y coordinate of the center of the Alien object
        """
        return self._y
        
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,source):
        """
        Creates a new alien object using the initializer of GImage where the
        parameters x and y refer to the x and y coordinates of the center of the
        Alien object, respectively.
        
        Parameter x: the x coordinate of the center of the Alien object
        Precondition: x must be an int or float >= (ALIEN_WIDTH/2) and <= (GAME_WIDTH-ALIEN_WIDTH/2)
        
        Parameter y: the y coordinate of the center of the Alien object
        Precondition: y must be an int or float >= (DEFENSE_LINE) and <= (GAME_HEIGHT-ALIEN_HEIGHT/2)
        
        Parameter source: The image that represents the Alien object
        Precondition: source is a string that refers to an Alien image(.png) existing in
                      the global variable ALIEN_IMAGES (in consts.py)
        """
        assert source in ALIEN_IMAGES
        assert type(x) in [int,float] and type(y) in [int,float]
        assert x >= ALIEN_WIDTH/2 and x <= GAME_WIDTH-ALIEN_WIDTH/2
        assert y >= DEFENSE_LINE and y <= GAME_WIDTH - ALIEN_HEIGHT/2
        
        self._x = x
        self._y = y
        GImage.__init__(self,x=x,y=y,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source=source)
        
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this
                 instance of alien
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        
        [this specification was copied verbatim from the CS 1110 website. This specification
        was written by the CS 1110 instructors.]
        """
        if bolt.getVelocity() > 0: #bolt fired by a ship
            corner1 = (bolt.getX() - BOLT_WIDTH/2,bolt.getY() + BOLT_HEIGHT/2)
            corner2 = (bolt.getX() - BOLT_WIDTH/2,bolt.getY() - BOLT_HEIGHT/2)
            corner3 = (bolt.getX() + BOLT_WIDTH/2,bolt.getY() + BOLT_HEIGHT/2)
            corner4 = (bolt.getX() + BOLT_WIDTH/2,bolt.getY() - BOLT_HEIGHT/2)
            corners = [corner1,corner2,corner3,corner4]
            for corner in corners:
                if self.contains(corner):
                    return True
        return False
            
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _object: A string indicating whether this bolt was fired by the ship or an alien
                    [string, == to either 'ship' or 'alien']
        _y: The vertical (y) coordinate of the Bolt object's center
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getVelocity(self):
        """Returns: the velocity of this bolt"""
        return self._velocity
    
    def getX(self):
        """Returns: the x coordinate of this bolt object's center"""
        return self._x
    
    def getY(self):
        """Returns: the y coordinate of this bolt object's center"""
        return self._y
    
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,object):
        """
        Creates a bolt object using the __init__ of GRectangle
        
        Parameter x: The x coordinate of the center of the bolt
        Precondition: x is an int or float >= BOLT_WIDTH/2 and <= GAME_WIDTH-BOLT_WIDTH/2
        
        Parameter y: The y coordinate of the center of the bolt
        Precondition: y is an int or float >= -BOLT_HEIGHT/2 and <= GAME_WIDTH+BOLT_HEIGHT/2
                      and <= GAME_WIDTH + BOLT_HEIGHT/2
        
        Parameter object: The object that the bolt is being shot from
        Precondition: parameter object is a string, either 'ship' or 'alien'
        
        Precondition: parameter object is a string, either 'ship' or 'alien'
        """
        assert type(object) is str and (object == 'ship' or object == 'alien')
        assert type(x) in [int,float] and type(y) in [int,float]
        assert y >= -BOLT_HEIGHT/2 and y <= GAME_WIDTH+BOLT_HEIGHT/2
        assert x >= BOLT_WIDTH/2 and x <= GAME_WIDTH-BOLT_WIDTH/2
        
        self._x = x
        self._y = y
        
        if object=='ship':
            self._velocity = BOLT_SPEED
            GRectangle.__init__(self, x = x , y = y, width = BOLT_WIDTH,height = BOLT_HEIGHT, \
                                fillcolor = 'black')
        else: # object=='alien'
            self._velocity = -BOLT_SPEED
            GRectangle.__init__(self, x = x , y = y, width = BOLT_WIDTH,height = BOLT_HEIGHT, \
                                fillcolor = 'red')
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def moveBolt(self,object):
        """
        Returns: new y coordinate of bolt, which changes in response to key presses
        """
        y = self._y
        if object=='ship':
            y += self._velocity
        else:
            y += self._velocity
        
        return y
    
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE