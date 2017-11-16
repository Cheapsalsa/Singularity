#Copyright 2004 - 2009 Yost Engineering Inc.

##Permission is hereby granted, free of charge, to any person
##obtaining a copy of this software and associated documentation
##files (the "Software"), to deal in the Software without
##restriction, including without limitation the rights to use,
##copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the
##Software is furnished to do so, subject to the following
##conditions:
##
##The above copyright notice and this permission notice shall be
##included in all copies or substantial portions of the Software.
##
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
##EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
##OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
##NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
##HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
##WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
##FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
##OTHER DEALINGS IN THE SOFTWARE.

import math

backend = ""
backends = []
errors = []
try:
   import pyglet
   from pyglet.window import key as keyboard
   from pyglet.gl import *
   backends.append("pyglet")
except ImportError:
    errors.append("Could not load pyglet: module is not installed.")

try:
   import pygame
   backends.append("pygame-basic")
except ImportError:
   errors.append("Could not load pygame-basic: module is not installed.")
   
try:
   import pygame.gfxdraw as gfx
   backends.append("pygame")
except ImportError:
   errors.append("Could not load pygame with gfxdraw: module is not installed.")

if not len(backends):
   print("ERROR: There are no available backends.")
   for error in errors:
      print(error)
   
#Define these here in case 'from * import ...' is used

def unloadScreen():
   """UnloadScreen() - Destroy the window and resources"""
   if backend == "pygame" or backend == "pygame-basic": UnloadScreen_Pygame()
   elif backend == "pyglet": UnloadScreen_Pyglet()
def updateScreen():
   """UpdateScreen() - Update the contents of the screen: should be at the end of the game loop"""
   if backend == "pygame" or backend == "pygame-basic": UpdateScreen_Pygame()
   elif backend == "pyglet": UpdateScreen_Pyglet()
def clearScreen(color=(255, 255, 255, 255)):
   """ClearScreen(color=(255, 255, 255, 255)) - Clear the contents of the screen: should be at the beginning of the game loop"""
   if backend == "pygame" or backend == "pygame-basic": ClearScreen_Pygame(color)
   elif backend == "pyglet": ClearScreen_Pyglet(color)

def pixelSet(x, y, color=(255, 255, 255, 255)):
   """Set the pixel at (x, y) to the given color"""
   x=int(x)
   y=int(y)
   
   if backend == "pygame-basic":
      PixelSet_Pygame(x, y, color)
   elif backend == "pygame":
      PixelSetGFX_Pygame(x, y, color)
   elif backend == "pyglet": PixelSet_Pyglet(x, y, color)
   
def pixelGet(x, y):
   """Return a tuple indicating the color at the given position"""
   x=int(x)
   y=int(y)
   
   if backend == "pygame" or backend == "pygame-basic": return PixelGet_Pygame(x, y)
   elif backend == "pyglet": return PixelGet_Pyglet(x, y)

def line(x1, y1, x2, y2, color=(255, 255, 255, 255), width=1):
   """Draw a line from (x1, y1) to (x2, y2)"""
   x1=int(x1)
   y1=int(y1)
   x2=int(x2)
   y2=int(y2)
   
   if backend == "pygame-basic":
      Line_Pygame(x1, y1, x2, y2, color, width)
   elif backend == "pygame":
      LineGFX_Pygame(x1, y1, x2, y2, color, width)
   elif backend == "pyglet": Line_Pyglet(x1, y1, x2, y2, color, width)

def rectangle(x1, y1, x2, y2, color=(255, 255, 255, 255), width=1):
   """Draw a rectangle using the two points as the corners"""
   x1=int(x1)
   y1=int(y1)
   x2=int(x2)
   y2=int(y2)
   
   if backend == "pygame-basic":
      Rectangle_Pygame(x1, y1, x2, y2, color, width)
   elif backend == "pygame":
      RectangleGFX_Pygame(x1, y1, x2, y2, color, width)
   elif backend == "pyglet": Rectangle_Pyglet(x1, y1, x2, y2, color, width)

def triangle(x1, y1, x2, y2, x3, y3, color=(255, 255, 255, 255), width=1):
   """Draw a triangle using the three points as corners"""
   x1=int(x1)
   y1=int(y1)
   x2=int(x2)
   y2=int(y2)
   x3=int(x3)
   y3=int(y3)
   
   if backend == "pygame-basic":
      Triangle_Pygame(x1, y1, x2, y2, x3, y3, color, width)
   elif backend == "pygame":
      TriangleGFX_Pygame(x1, y1, x2, y2, x3, y3, color, width)
   elif backend == "pyglet": Triangle_Pyglet(x1, y1, x2, y2, x3, y3, color, width)

def circle(x, y, r, color=(255, 255, 255, 255), width=1):
   """Draw a circle at (x, y) with radius r"""
   x=int(x)
   y=int(y)
   r=int(r)
   if backend == "pygame-basic":
      Circle_Pygame(x,y,r, color, width)
   elif backend == "pygame":
      CircleGFX_Pygame(x,y,r, color, width)
   elif backend == "pyglet": Circle_Pyglet(x, y, r, color, width)

def ellipse(x, y, w, h, color=(255, 255, 255, 255), width=1):
   """Draw an ellipse at (x, y) bounded by the rectangle with width w and height h"""
   x=int(x)
   y=int(y)
   h=int(h)
   w=int(w)
   if backend == "pygame-basic":
      Ellipse_Pygame(x, y, w, h, color, width)
   elif backend == "pygame":
         EllipseGFX_Pygame(x, y, w, h, color, width)   
   elif backend == "pyglet": Ellipse_Pyglet(x, y, w, h, color, width)

def keyIsPressed(key):
   """Return True if the string key is currently pressed"""
   if backend == "pygame" or backend == "pygame-basic": return KeyIsPressed_Pygame(key)
   elif backend == "pyglet": return KeyIsPressed_Pyglet(key)
def keyIsNotPressed(key):
   """Return True if the string key is currently not pressed"""
   if backend == "pygame" or backend == "pygame-basic": return KeyIsNotPressed_Pygame(key)
   elif backend == "pyglet": return KeyIsNotPressed_Pyglet(key)
def keyGetPressedList():
   """Returns a list of currently pressed keys as strings"""
   if backend == "pygame" or backend == "pygame-basic": return KeyGetPressedList_Pygame()
   elif backend == "pyglet": return KeyGetPressedList_Pyglet()

def mouseGetButtonL():
   """Returns True if the left mouse button is clicked and False otherwise"""
   if backend == "pygame" or backend == "pygame-basic": return MouseGetButtonL_Pygame()
   elif backend == "pyglet": return MouseGetButtonL_Pyglet()
def mouseGetButtonR():
   """Returns True if the right mouse button is clicked and False otherwise"""
   if backend == "pygame" or backend == "pygame-basic": return MouseGetButtonR_Pygame()
   elif backend == "pyglet": return MouseGetButtonR_Pyglet()
def mouseGetButtonM():
   """Returns True if the middle mouse button is clicked and False otherwise"""
   if backend == "pygame" or backend == "pygame-basic": return MouseGetButtonM_Pygame()
   elif backend == "pyglet": return MouseGetButtonM_Pyglet()
def mouseGetX():
   """Returns the x coordinate of the mouse cursor"""
   if backend == "pygame" or backend == "pygame-basic": return MouseGetX_Pygame()
   elif backend == "pyglet": return MouseGetX_Pyglet()
def mouseGetY():
   """Returns the y coordinate of the mouse cursor"""
   if backend == "pygame" or backend == "pygame-basic": return MouseGetY_Pygame()
   elif backend == "pyglet": return MouseGetY_Pyglet()
def mouseGetPosition():
   """Returns a tuple containing the x and y coordinates of the mouse cursor"""
   if backend == "pygame" or backend == "pygame-basic": return MouseGetPosition_Pygame()
   elif backend == "pyglet": return MouseGetPosition_Pyglet()
def mouseGetButtons():
   """Returns a 3-tuple describing the state of each mouse button"""
   if backend == "pygame" or backend == "pygame-basic": return MouseGetButtons_Pygame()
   elif backend == "pyglet": return MouseGetButtons_Pyglet()

def fontSelect(fontname="Arial", fontsize=24):
   """Initialize the font object; should be called prior to rendering text"""
   if backend == "pygame" or backend == "pygame-basic": FontSelect_Pygame(fontname, fontsize)
   elif backend == "pyglet": FontSelect_Pyglet(fontname, fontsize)
def fontWrite(x, y, text, color=(255, 255, 255, 255)):
   """Draw the string text at position (x, y)"""
   if backend == "pygame" or backend == "pygame-basic": FontWrite_Pygame(x, y, text, color)
   elif backend == "pyglet": FontWrite_Pyglet(x, y, text, color)

def musicLoad(filename):
   """Load filename as the current background music"""
   if backend == "pygame" or backend == "pygame-basic": MusicLoad_Pygame(filename)
   elif backend == "pyglet": MusicLoad_Pyglet(filename)
def musicPlay():
   """Play the currently loaded background music"""
   if backend == "pygame" or backend == "pygame-basic": MusicPlay_Pygame()
   elif backend == "pyglet": MusicPlay_Pyglet()
def musicPause():
   """Pause the currently playing background music"""
   if backend == "pygame" or backend == "pygame-basic": MusicPause_Pygame()
   elif backend == "pyglet": MusicPause_Pyglet()
def musicUnPause():
   """Unpause the currently loaded background music"""
   if backend == "pygame" or backend == "pygame-basic": MusicUnPause_Pygame()
   elif backend == "pyglet": MusicUnPause_Pyglet()
def musicFade(seconds):
   """Fade out the currently playing background music over the given time"""
   if backend == "pygame" or backend == "pygame-basic": MusicFade_Pygame(seconds)
   elif backend == "pyglet": MusicFade_Pyglet(seconds)
def musicSetVolume(volumePercent=40):
   """Set the volume of the currently loaded background music"""
   if backend == "pygame" or backend == "pygame-basic": MusicSetVolume_Pygame(volumePercent)
   elif backend == "pyglet": MusicSetVolume_Pyglet(volumePercent)
def musicGetVolume():
   """Get the volume of the currently loaded background music"""
   if backend == "pygame" or backend == "pygame-basic": MusicGetVolume_Pygame()
   elif backend == "pyglet": MusicGetVolume_Pyglet()
def musicStop():
   """Stop the currently playing background music"""
   if backend == "pygame" or backend == "pygame-basic": MusicStop_Pygame()
   elif backend == "pyglet": MusicStop_Pyglet()

def soundLoad(filename, slot):
   """Load the sound given in filename and store it in the given slot"""
   if backend == "pygame" or backend == "pygame-basic": SoundLoad_Pygame(filename, slot)
   elif backend == "pyglet": SoundLoad_Pyglet(filename, slot)
def soundPlay(slot):
   """Play the sound stored in the given slot"""
   if backend == "pygame" or backend == "pygame-basic": SoundPlay_Pygame(slot)
   elif backend == "pyglet": SoundPlay_Pyglet(slot)
def soundStop(slot):
   """Stop the sound stored in the given slot"""
   if backend == "pygame" or backend == "pygame-basic": SoundStop_Pygame(slot)
   elif backend == "pyglet": SoundStop_Pyglet(slot)
def soundSetVolume(slot, volumePercent=40):
   """Set the volume of the sound stored in the given slot"""
   if backend == "pygame" or backend == "pygame-basic": SoundSetVolume_Pygame(slot, volumePercent)
   elif backend == "pyglet": SoundSetVolume_Pyglet(slot, volumePercent)

def spriteLoad(filename, slot):
   """Load the sprite given in filename and store it in the given slot"""
   if backend == "pygame" or backend == "pygame-basic": SpriteLoad_Pygame(filename, slot)
   elif backend == "pyglet": SpriteLoad_Pyglet(filename, slot)
def spriteRender(x, y, slot, rotation=0, scale=1, flipH=False, flipV=False, alpha=255):
   """Alpha parameter not currently supported in pygame"""
   if backend == "pygame" or backend == "pygame-basic": SpriteRender_Pygame(x, y, slot, rotation, scale, flipH, flipV, alpha)
   elif backend == "pyglet": SpriteRender_Pyglet(x, y, slot, rotation, scale, flipH, flipV, alpha)
def spriteSimpleRender(x, y, slot):
   """Render sprite in slot at position x, y"""
   if backend == "pygame" or backend == "pygame-basic": SpriteSimpleRender_Pygame(x, y, slot)
   elif backend == "pyglet": SpriteSimpleRender_Pyglet(x, y, slot)
def spriteWidth(slot):
   """Return the width of the sprite in the given slot"""
   if backend == "pygame" or backend == "pygame-basic": SpriteWidth_Pygame(slot)
   elif backend == "pyglet": SpriteWidth_Pyglet(slot)
def spriteHeight(slot):
   """Return the height of the sprite in the given slot"""
   if backend == "pygame" or backend == "pygame-basic": SpriteHeight_Pygame(slot)
   elif backend == "pyglet": SpriteHeight_Pyglet(slot)

def frameGetLimit():
   """Return the current frames per second"""
   if backend == "pygame" or backend == "pygame-basic": return FrameGetLimit_Pygame()
   elif backend == "pyglet": return FrameGetLimit_Pyglet()
def frameSetLimit(fps):
   """Set a limit on the frame refresh rate given by fps"""
   if backend == "pygame" or backend == "pygame-basic": FrameSetLimit_Pygame(fps)
   elif backend == "pyglet": FrameSetLimit_Pyglet(fps)
def frameDelay():
   """Ticks the clock; should be called during every game loop--returns a value that indicates the amount of time elapsed since last update"""
   if backend == "pygame" or backend == "pygame-basic": FrameDelay_Pygame()
   elif backend == "pyglet": FrameDelay_Pyglet()

############################################################# PYGAME CODE ##################################################################################

#########  sprites Functions

def SpriteLoad_Pygame(Filename,spriteSlot,size=None):
   """spritesLoad(Filename,spritesSlot,size=None)"""
   if size==None :
       sprites_Pygame[spriteSlot]=pygame.image.load(Filename)
   else:
       if len(size)==2:
           sprites_Pygame[spriteSlot]=pygame.transform.scale(pygame.image.load(Filename),size)

def SpriteRender_Pygame(centerx, centery, spriteSlot, rotationAngle=0, scaleFactor=1, flipH=False, flipV=False, alpha=255):
   """spritesRender(centerx, centery, spritesSlot, rotationAngle=0, scaleFactor=1, flipH=False, flipV=False, alpha=255) - Alpha parameter is not currently supported in pygame"""
   if sprites_Pygame[spriteSlot] != None:
       #newsurf=pygame.transform.rotate(sprites[spritesSlot],rotationAngle)
       newsurf=pygame.transform.flip(sprites_Pygame[spriteSlot],flipH,flipV)
       newsurf2=pygame.transform.rotozoom(newsurf, rotationAngle, scaleFactor) 
       (x1,y1)=newsurf2.get_size()
       x=x1/2
       y=y1/2
       rectangle=screenbuffer_Pygame.blit(newsurf2,(centerx-x,centery-y))
       return rectangle 
       #screenbuffer_Pygame.blit(pygame.transform.rotate(pygame.transform.flip(self.frames[self.frame],self.flipH,self.flipV),self.angle),(float(self.col)*32,float(self.row)*32))

def SpriteSimpleRender_Pygame(upperleftx, upperlefty, spriteSlot):
   """spritesSimpleRender(upperleftx, upperlefty, spritesSlot)"""
   if sprites_Pygame[spriteSlot] != None:
       rectangle=screenbuffer_Pygame.blit(sprites_Pygame[spriteSlot],(upperleftx,upperlefty))
       return rectangle 
        
def SpriteHeight_Pygame(spriteSlot):
   return sprites_Pygame[spriteSlot].get_height()

def SpriteWidth_Pygame(spriteSlot):
   return sprites_Pygame[spriteSlot].get_width()

#########  Music/sounds Functions
def MusicLoad_Pygame( filename ):
    """ MusicLoad( Filename ) - loads the background music file."""
    pygame.mixer.music.load( filename )

def MusicPlay_Pygame():
    """MusicPlay() - plays the loaded background music file."""
    pygame.mixer.music.play(-1)

def MusicPause_Pygame():
    """MusicPause() - pauses the background music."""
    pygame.mixer.music.pause()

def MusicUnPause_Pygame():
    """MusicUnPause() - resumes the background music."""
    pygame.mixer.music.unpause()

def MusicFade_Pygame(seconds):
    """MusicFade( seconds ) - fades out the background music over the specified number of seconds."""
    pygame.mixer.music.fadeout(seconds*1000)

def MusicSetVolume_Pygame(volumePercent):
    """MusicSetVolume(Percent) - sets the music volume to a percentage 0-100."""
    pygame.mixer.music.set_volume(volumePercent/100.0)

def MusicGetVolume_Pygame():
    """MusicGetVolume() - returns the music volume percentage."""
    return pygame.mixer.music.get_volume()*100
    
def MusicStop_Pygame():
    """MusicStop() - Stops the background music."""
    pygame.mixer.music.stop()
    
def SoundLoad_Pygame(filename, soundsSlot):
    """soundsLoad(filename, soundsSlot) - loads sounds file data into one of the 256 sounds slots."""
    global sounds_Pygame
    #sounds_Pygame[soundsSlot] = pygame.mixer.sounds(filename)
    sounds_Pygame[soundsSlot] = pygame.mixer.Sound(filename)

def SoundSetVolume_Pygame(soundsSlot, volumePercent=40):
    """soundsSetVolume(soundsSlot,volumePercent=40) - sets the playback volume for the sounds slot
    to the the specified volume(0-100)"""
    global sounds_Pygame
    sounds_Pygame[soundsSlot].set_volume(volumePercent/100.0)

def SoundGetVolume_Pygame(soundsSlot):
    """MusicGetVolume() - returns the music volume percentage."""
    return sounds_Pygame[soundsSlot].get_volume()*100

def SoundPlay_Pygame(soundsSlot):
    """soundsPlay(soundsSlot) - plays a loaded sounds slot(0-255)."""
    global sounds_Pygame
    sounds_Pygame[soundsSlot].play()
    
def SoundStop_Pygame():
    """soundsStop() - stops all playing soundss."""
    pygame.mixer.stop()
    pygame.mixer.music.stop()

#########  General Functions
def ClearScreen_Pygame(color=(255, 255, 255, 255)):
    screenbuffer_Pygame.fill(color)
        
def UnloadScreen_Pygame():
    pygame.quit()
    """UnLoadScreen() - closes the pscreen window"""
    
def UpdateScreen_Pygame():
    """UpdateScreen() -  move the display buffer to the screen and display it."""
    pygame.display.flip()

############ key input functions
def KeyGetPressedList_Pygame():
    """Returns a list of the pressed keys as a sequence of strings."""
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    result=[]
    for i in range(0,len(pressed)):
        if pressed[i]!=0:
            result.append(pygame.key.name(i))
    return result        

def KeyIsPressed_Pygame(KeySymbol):
    """Return a 1 if the specified key is pressed 0 if it isn't"""
    if KeySymbol in KeyGetPressedList_Pygame():
        return 1
    else:
        return 0
    
def KeyIsNotPressed_Pygame(KeySymbol):
    """Return a 1 if the specified key is not pressed 0 if it is"""
    if KeySymbol not in KeyGetPressedList_Pygame():
        return 1
    else:
        return 0

#####Mouse Functions
def MouseGetPosition_Pygame():
    """MouseGetPosition() - returns the mouse position as and (x,y) pair."""
    (x,y)=pygame.mouse.get_pos()
    return (x,y)

def MouseGetButtons_Pygame():
    """MouseGetButtons() - returns the button state as a three element boolean tuple (l,m,r)."""
    return pygame.mouse.get_pressed() 

def MouseGetButtonL_Pygame():
    """MouseGetButtonL() - returns the state of the left mouse button. True when pressed , False when not pressed. """
    return pygame.mouse.get_pressed()[0] 

def MouseGetButtonM_Pygame():
    """MouseGetButtonM() - returns the state of the middle mouse button. True when pressed , False when not pressed. """
    return pygame.mouse.get_pressed()[1] 

def MouseGetButtonR_Pygame():
    """MouseGetButtonR() - returns the state of the right mouse button. True when pressed , False when not pressed. """
    return pygame.mouse.get_pressed()[2] 

def MouseGetX_Pygame():
    """MouseGetX() - returns the mouse x-coordinate."""
    (x,y)=pygame.mouse.get_pos()
    return x

def MouseGetY_Pygame():
    """MouseGetY() - returns the mouse y-coordinate."""    
    (x,y)=pygame.mouse.get_pos()
    return y

###### Font Functions
def FontSelect_Pygame(fontName="Arial",fontSize=24):
    """FontSelect(fontName="Arial",fontSize=24) - sets the current font and font size."""
    global font_Pygame
    font_Pygame=pygame.font.SysFont(fontName,fontSize)

def FontWrite_Pygame(x,y,string,color=(255,255,255)):
    """FontWrite(x,y,string,color=(255,255,255)) - writes the text to the screen using the current font. """
    screenbuffer_Pygame.blit(font_Pygame.render(string,True,color),(x,y))        

###### Drawing Functions

def PixelSet_Pygame(x,y,color=(255,255,255)):
    """PixelSet(x,y,color=(255,255,255)) - turn on the pixel at the specified location. """
    screenbuffer_Pygame.set_at((x,y),color)

def PixelGet_Pygame(x,y):
    """PixelGet(x,y) - get and return the color of the pixel at the specified location. """
    return screenbuffer_Pygame.get_at((x,y))

def Line_Pygame(x1,y1,x2,y2,color=(255,255,255),width=1):
    """Line(x1,y1,x2,y2,color=(255,255,255),width=1) - draw a line between the two specified points. """
    pygame.draw.line(screenbuffer_Pygame,color,(x1,y1),(x2,y2),width)

def Circle_Pygame(x,y,radius,color=(255,255,255),width=1):

   if len(color) == 4:
      color = color[:3]
   
   if width < 2:
      pygame.draw.circle(screenbuffer_Pygame, color, (x, y), radius, width)
      return
   
   inner = []
   outer = []

   for i in range(0, SEGMENTS):
      dx = radius * math.cos(i*2*math.pi/SEGMENTS)
      dy = radius * math.sin(i*2*math.pi/SEGMENTS)

      inner.append( (int(dx + x), int(dy + y)) )

      x_outer = (radius + width) * math.cos(i*2*math.pi/SEGMENTS)
      y_outer = (radius + width) * math.sin(i*2*math.pi/SEGMENTS)
      #Build outer list backwards 
      outer.insert(0, (int(x + x_outer), int(y + y_outer)))

   pygame.draw.polygon(screenbuffer_Pygame, color, inner + [inner[0]] + outer + [outer[0]])
      
def Ellipse_Pygame(x,y,width,height,color=(255,255,255),linewidth=1):
   if len(color) == 4:
      color = color[:3]
   
   if linewidth < 2:
      pygame.draw.ellipse(screenbuffer_Pygame, color, [x, y, width, height], linewidth)
      return
   
   inner = []
   outer = []

   for i in range(0, SEGMENTS):
      dx = width * math.cos(i*2*math.pi/SEGMENTS)
      dy = height * math.sin(i*2*math.pi/SEGMENTS)

      inner.append( (int(dx + x), int(dy + y)) )

      x_outer = (width + linewidth) * math.cos(i*2*math.pi/SEGMENTS)
      y_outer = (height + linewidth) * math.sin(i*2*math.pi/SEGMENTS)
      #Build outer list backwards 
      outer.insert(0, (int(x + x_outer), int(y + y_outer)))

   pygame.draw.polygon(screenbuffer_Pygame, color, inner + [inner[0]] + outer + [outer[0]])
   
def Rectangle_Pygame(x1,y1,x2,y2,color=(255,255,255),width=1):
    if len(color) == 4:
       color = color[:3]
      
    if x1<x2:
        x=x1
    else:
        x=x2
    if y1<y2:
        y=y1
    else:
        y=y2
    w=abs(x2-x1)
    h=abs(y2-y1)
    pygame.draw.rect(screenbuffer_Pygame,color,(x,y,w+1,h+1),width)

def Triangle_Pygame(x1,y1,x2,y2,x3,y3,color=(255,255,255),width=1):
    if len(color) == 4:
       color = color[:3]
    """Triangle(x1,y1,x2,y2,x3,y3,color=(255,255,255),width=1) - draw a triangle using the three points specified"""
    pygame.draw.polygon(screenbuffer_Pygame, color, [(x1,y1),(x2,y2),(x3,y3)], width)

######### GFX Drawing functions

def PixelSetGFX_Pygame(x, y, color=(255, 255, 255, 255)):
   gfx.pixel(screenbuffer_Pygame, x, y, color)

def LineGFX_Pygame(x1, y1, x2, y2, color=(255, 255, 255, 255), width=1):

   if width == 1:
      gfx.line(screenbuffer_Pygame, x1, y1, x2, y2, color)
      return 
      
   width-=1
   #Invert y coordinates because screen y is inverted
   angle = math.atan2((x2 - x1), -(y2 - y1))

   dy = round((math.sin(angle)))
   dx = round((math.cos(angle)))

   rx1 = x1
   ry1 = y1

   rx2 = x2
   ry2 = y2

   lx1 = x1
   ly1 = y1

   lx2 = x2
   ly2 = y2

   for i in range(int(width/2)):
      rx1 += dx
      ry1 += dy
      rx2 += dx
      ry2 += dy

   for i in range(int(width - width/2)):
      lx1 -= dx
      ly1 -= dy
      lx2 -= dx
      ly2 -= dy
  
   gfx.filled_polygon(screenbuffer_Pygame, [(rx1, ry1), (lx1, ly1), (lx2, ly2), (rx2, ry2)], color)
   
def CircleGFX_Pygame(x1, y1, r, color=(255, 255, 255, 255), width=1):
   if len(color) == 3:
       color += (255,)
   if not width:
      gfx.filled_circle(screenbuffer_Pygame, x1, y1, r, color)
   elif width == 1:
      gfx.circle(screenbuffer_Pygame, x1, y1, r, color)
   else:
      
      inner = []
      outer = []

      for i in range(0, SEGMENTS):
         x = r * math.cos(i*2*math.pi/SEGMENTS)
         y = r * math.sin(i*2*math.pi/SEGMENTS)

         inner.append( (int(x + x1), int(y + y1)) )
         
         x_outer = (r + width) * math.cos(i*2*math.pi/SEGMENTS)
         y_outer = (r + width) * math.sin(i*2*math.pi/SEGMENTS)
         #Build outer list backwards 
         outer.insert(0, (int(x1 + x_outer), int(y1 + y_outer)))
         
      
      #Otherwise, drawing a circle with a width

      #midpoint = [(inner[0][0], inner[0][1]+1)]
      #midpoint2 = [(outer[0][0], outer[0][1]+1)]
      gfx.filled_polygon(screenbuffer_Pygame, inner + [inner[0]] + outer + [outer[0]], color)
      #gfx.filled_polygon(screenbuffer_Pygame, inner + [inner[0]] + [outer[0]] + outer, color)
      #gfx.line(screenbuffer_Pygame, inner[0][0], inner[0][1], outer[0][0], outer[0][1], (color[0], color[1], color[2], 32)) 
      #gfx.filled_trigon(screenbuffer_Pygame, inner[-1][0], inner[-1][1], outer[0][0], outer[0][1], outer[-1][0], outer[-1][1], color)
      #gfx.filled_polygon(screenbuffer_Pygame, outer, color)


def RectangleGFX_Pygame(x1, y1, x2, y2, color=(255, 255, 255, 255), width=1):
   if x1<x2:
      x=x1
   else:
      x=x2
   if y1<y2:
      y=y1
   else:
      y=y2
   w=abs(x2-x1)
   h=abs(y2-y1)
   #Box is filled, rectangle is not... wow--nice function names, pygame
   if not width:
      gfx.box(screenbuffer_Pygame, pygame.Rect(x, y, w, h), color)
   else:
      for i in range(0, width):
         gfx.rectangle(screenbuffer_Pygame, pygame.Rect(x-i, y-i, w+(i*2), h+(i*2)), color)

def EllipseGFX_Pygame(x1, y1, w, h, color=(255, 255, 255, 255), width=1):
   if len(color) == 3:
       color += (255,)
   if not width:
      gfx.filled_ellipse(screenbuffer_Pygame, x1, y1, w, h, color)
   elif width == 1:
      gfx.ellipse(screenbuffer_Pygame, x1, y1, w, h, color)
   else:
      
      inner = []
      outer = []

      for i in range(0, SEGMENTS):
         x = w * math.cos(i*2*math.pi/SEGMENTS)
         y = h * math.sin(i*2*math.pi/SEGMENTS)

         inner.append( (int(x + x1), int(y + y1)) )

         x_outer = (w + width) * math.cos(i*2*math.pi/SEGMENTS)
         y_outer = (h + width) * math.sin(i*2*math.pi/SEGMENTS)
         
         outer.insert(0, (int(x1 + x_outer), int(y1 + y_outer)))

      #Otherwise, drawing a circle with a width
      gfx.filled_polygon(screenbuffer_Pygame, inner + [inner[0]] + outer + [outer[0]], color)
      

def TriangleGFX_Pygame(x1, y1, x2, y2, x3, y3, color=(255, 255, 255, 255), width=1):
   if not width:
      gfx.filled_trigon(screenbuffer_Pygame, x1, y1, x2, y2, x3, y3, color)
   else:
      for i in range(0, width):
         LineGFX_Pygame(x1, y1, x2, y2, color, width)
         LineGFX_Pygame(x2, y2, x3, y3, color, width)
         LineGFX_Pygame(x3, y3, x1, y1, color, width)  
   
########    Clock/Framerate Functions

def FrameDelay_Pygame():
   if limitFPS_Pygame:
      clock_Pygame.tick(limitFPS_Pygame)
   else:
      clock_Pygame.tick()

def FrameSetLimit_Pygame(fps):
   global limitFPS_Pygame
   limitFPS_Pygame = fps

def FrameGetLimit_Pygame():
   return clock_Pygame.get_fps()
   
############################################################# PYGLET CODE ##################################################################################

#Utility class for allowing horizontal/vertical image-flipping--and then I went ahead and put everything else in here too
class PygletSprite():

   def __init__(self, imageName):

      image = pyglet.image.load(imageName)

      self.sprite = pyglet.sprite.Sprite(image)

      self.sprite.image.anchor_x = self.sprite.width / 2
      self.sprite.image.anchor_y = self.sprite.height / 2
      
      self.flipH = False
      self.flipV = False

   def transform(self, rotationAngle, scaleFactor, flipV, flipH):
      if self.flipH != flipH or self.flipV != flipV:
         #print "Transforming" 
         self.sprite.image = self.sprite.image.get_texture().get_transform(flipV, flipH)
      self.flipV = flipV
      self.flipH = flipH

      self.rotation = rotationAngle
      self.scale = scaleFactor
      
         
      

def __SetPolygonFillMode_Pyglet(width):
    if width != 0:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(width)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

######## Sprite Functions

def SpriteLoad_Pyglet(filename, spriteSlot, size=None):
    sprites_Pyglet[spriteSlot] = PygletSprite(filename)
        

def SpriteRender_Pyglet(centerx, centery, spriteSlot, rotationAngle = 0, scaleFactor = 1, flipV = False, flipH = False, alpha=255):
    __SetPolygonFillMode_Pyglet(0)

    currSprite = sprites_Pyglet[spriteSlot]
    currSprite.sprite.position = (centerx, window_Pyglet.height - centery)

    currSprite.transform(rotationAngle, scaleFactor, flipV, flipH)
    
    currSprite.sprite.opacity = alpha
    currSprite.sprite.draw()

def SpriteSimpleRender_Pyglet(centerx, centery, spriteSlot):
    SpriteRender_Pyglet(centerx, window_Pyglet.height - centery, spriteSlot)

def SpriteHeight_Pyglet(spriteSlot):
   return sprites_Pyglet[spriteSlot].sprite.height

def SpriteWidth_Pyglet(spriteSlot):
   return sprites_Pyglet[spriteSlot].sprite.width


######## Drawing Functions

def PixelSet_Pyglet(x1, y1, color=(255, 255, 255, 255)):
    if len(color) == 3:
       color += (255,)

    pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
        ('v2i', (x1, window_Pyglet.height - y1)),
        ('c4B', (color[0], color[1], color[2], color[3]))
    )

def PixelGet_Pyglet(x1, y1):
    #This just needs to be four unsigned bytes
    p = " " * 4
    glReadPixels(x1, window_Pyglet.height - y1, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, p)
    return (ord(p[0]), ord(p[1]), ord(p[2]), ord(p[3]))

def Line_Pyglet(x1, y1, x2, y2, color=(255, 255, 255, 255), width=1):
    if len(color) == 3:
       color += (255,)
    if not width:
      width = 1
    glLineWidth(width)
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        ('v2i', (x1, window_Pyglet.height - y1, x2, window_Pyglet.height - y2)),
        ('c4B', (color * 2))
    )

def Rectangle_Pyglet(x1, y1, x2, y2, color=(255, 255, 255, 255), width=1):
    if len(color) == 3:
       color += (255,)

    __SetPolygonFillMode_Pyglet(width)
    

    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
        ('v2i', (x1, window_Pyglet.height - y1,
                 x2, window_Pyglet.height - y1,
                 x2, window_Pyglet.height - y2,
                 x1, window_Pyglet.height - y2)),
        ('c4B', (color * 4))
    )

def Triangle_Pyglet(x1, y1, x2, y2, x3, y3, color=(255, 255, 255, 255), width=1):
    if len(color) == 3:
       color += (255,)
       
    __SetPolygonFillMode_Pyglet(width)
    pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES,
        ('v2i', (x1, window_Pyglet.height - y1,
                 x2, window_Pyglet.height - y2,
                 x3, window_Pyglet.height - y3)),
        ('c4B', (color * 3))
    )

def Circle_Pyglet(x1, y1, r, color=(255, 255, 255, 255), width=1):
    
   if len(color) == 3:
      color += (255,)
   inner = []
   #outer = []

   for i in range(0, SEGMENTS):
      x = r * math.cos(i*2*math.pi/SEGMENTS)
      y = r * math.sin(i*2*math.pi/SEGMENTS)

      inner.extend((int(x + x1), int(window_Pyglet.height - (y + y1))))

      if width > 1:
         x_outer = (r + width) * math.cos(i*2*math.pi/SEGMENTS)
         y_outer = (r + width) * math.sin(i*2*math.pi/SEGMENTS)
         inner.extend((int(x1 + x_outer), int(window_Pyglet.height - (y1 + y_outer))))
         
    #Drawing a circle with a width of one, or a filled circle
   __SetPolygonFillMode_Pyglet(0)
   if width <= 1:
       
      if width == 1:
         __SetPolygonFillMode_Pyglet(1)
          
      pyglet.graphics.draw(len(inner)/2, pyglet.gl.GL_POLYGON,
         ('v2i', inner),
         ('c4B', color*(len(inner)/2)))

      return

   inner += inner[0:4]
   
   pyglet.graphics.draw( len(inner)/2, pyglet.gl.GL_QUAD_STRIP,
        ('v2i', inner),
        ('c4B', color*(len(inner)/2)))


def Ellipse_Pyglet(x1, y1, w, h, color=(255, 255, 255, 255), width=1):
   if len(color) == 3:
      color += (255,)
   inner = []
   #outer = []

   for i in range(0, SEGMENTS):
      x = w * math.cos(i*2*math.pi/SEGMENTS)
      y = h * math.sin(i*2*math.pi/SEGMENTS)

      inner.extend((int(x + x1), int(window_Pyglet.height - (y + y1))))

      if width > 1:
         x_outer = (w + width) * math.cos(i*2*math.pi/SEGMENTS)
         y_outer = (h + width) * math.sin(i*2*math.pi/SEGMENTS)
         inner.extend((int(x1 + x_outer), int(window_Pyglet.height - (y1 + y_outer))))
         
    #Drawing a circle with a width of one, or a filled circle
   __SetPolygonFillMode_Pyglet(0)
   if width <= 1:
       
      if width == 1:
         __SetPolygonFillMode_Pyglet(1)
          
      pyglet.graphics.draw(len(inner)/2, pyglet.gl.GL_POLYGON,
         ('v2i', inner),
         ('c4B', color*(len(inner)/2)))

      return

   inner += inner[0:4]
   
   pyglet.graphics.draw( len(inner)/2, pyglet.gl.GL_QUAD_STRIP,
        ('v2i', inner),
        ('c4B', color*(len(inner)/2)))
    
######## Music Functions

def MusicLoad_Pyglet(filename):
    global player_Pyglet
    player_Pyglet.queue(pyglet.media.load(filename))
    
def MusicPlay_Pyglet():
    player_Pyglet.play()

def MusicPause_Pyglet():
    player_Pyglet.pause()

def MusicUnPause_Pyglet():
    player_Pyglet.play()
    
def MusicStop_Pyglet():
    player_Pyglet.seek(0)
    player_Pyglet.pause()

def MusicSetVolume_Pyglet(percent):
    percent /= float(100)
    player_Pyglet.volume = percent

def MusicGetVolume_Pyglet():
    return player_Pyglet.volume * 100

def MusicFade_Pyglet(seconds):
    global musicFading_Pyglet
    if musicFading_Pyglet:
       return

    vol = MusicGetVolume_Pyglet()    
    decrement = vol / seconds

    def __Fader(dt, amount):
       
       cVol = MusicGetVolume_Pyglet()

       if not cVol:
          pyglet.clock.unschedule(__Fader)
          musicFading_Pyglet = False
          MusicStop()
       
       MusicSetVolume_Pyglet(max(0, cVol - amount))
    
    musicFading_Pyglet = True

    pyglet.clock.schedule_interval(__Fader, 1, amount=decrement)
    
######## Sound Functions

def SoundLoad_Pyglet(filename, soundSlot):
    source = pyglet.media.load(filename)
    
    player = pyglet.media.Player()
    player.queue(source)
    
    sounds_Pyglet[soundSlot] = player

def SoundPlay_Pyglet(soundSlot):
    player = sounds_Pyglet[soundSlot]
    player.play()

def SoundStop_Pyglet(soundSlot):
    sounds_Pyglet[soundSlot].seek(0)
    sounds_Pyglet[soundSlot].pause()

def SoundSetVolume_Pyglet(soundSlot, volumePercent=40):
    percent /= float(100)
    sounds_Pyglet[soundSlot].volume = percent
    
######## Font Functions

def FontSelect_Pyglet(fontName = "Arial", fontSize = 24, bold = False, italic = False):
    global font
    font = pyglet.font.load(fontName, fontSize, bold, italic)

def FontWrite_Pyglet(x, y, string, color=(255, 255, 255, 255)):
    __SetPolygonFillMode_Pyglet(0)
    color = map(lambda x: float(x) / 255, color)        #Contrary to every other function, rgb values are received in range 0...1
    text = pyglet.font.Text(font, string, x, window_Pyglet.height - y, 0, color)
    text.draw()

######## Mouse Functions

def MouseGetButtonL_Pyglet():
    return mouseButtonState_Pyglet[pyglet.window.mouse.LEFT]

def MouseGetButtonM_Pyglet():
    return mouseButtonState_Pyglet[pyglet.window.mouse.MIDDLE]

def MouseGetButtonR_Pyglet():
    return mouseButtonState_Pyglet[pyglet.window.mouse.RIGHT]

def MouseGetX_Pyglet():
    return mousePositions_Pyglet[0]

def MouseGetY_Pyglet():
    return mousePositions_Pyglet[1]

def MouseGetPosition_Pyglet():
    return mousePositions_Pyglet

def MouseGetButtons_Pyglet():
    return (MouseGetButtonL_Pyglet(), MouseGetButtonM_Pyglet(), MouseGetButtonR_Pyglet())

######## Keyboard Functions

def KeyGetPressedList_Pyglet():
    return keysPressed_Pyglet.keys()

def KeyIsPressed_Pyglet(key):
    if keysPressed_Pyglet.has_key(key):
        return True
    return False

def KeyIsNotPressed_Pyglet(key):
    return not KeyIsPressed_Pyglet(key)

#Utility function to match these keys with ones returned through pygame
def __KeyConvert_Pyglet(key):
    key = keyboard.symbol_string(key).lower()

    if key == "quoteleft":
       key = '`'

    elif key == "lshift":
       key = 'left shift'

    elif key == 'lctrl':
       key = 'left ctrl'

    elif key == 'lalt':
       key = 'left alt'

    elif key == 'semicolon':
       key = ';'

    elif key == 'apostraphe':
       key = "'"

    elif key == 'backslash':
       key = '\\'

    elif key == 'slash':
       key = '/'

    elif key == 'minus':
       key = '-'

    elif key == 'equal':
       key = '='

    elif key[0:3] == 'num' and len(key) == 5:
       key = key[4:]

    elif key == 'capslock':
       key = 'caps lock'

    elif key[0] == '_' and key[-1:] >= '0' and key[-1:] <= '9':
        key = key[-1:]

    return key

#######     Clock/Framerate Functions
def FrameDelay_Pyglet():
    return pyglet.clock.tick()

def FrameSetLimit_Pyglet(fps):
    pyglet.clock.set_fps_limit(fps)

def FrameGetLimit_Pyglet():
    return pyglet.clock.get_fps()

######## Screen Functions
        
def UnloadScreen_Pyglet():
    MusicStop()
    window_Pyglet.close()

def ClearScreen_Pyglet(color=(255, 255, 255)):
    glClearColor(color[0]/float(255), color[1]/float(255), color[2]/float(255), 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_ACCUM_BUFFER_BIT)
   
    #window_Pyglet.clear()

def UpdateScreen_Pyglet():
    window_Pyglet.dispatch_events()
    window_Pyglet.flip()

#Call this function only after the window has been created
def __InitEvents_Pyglet():

    if not window_Pyglet:
        return

    #Handlers to store information
    @window_Pyglet.event
    def on_mouse_press(x, y, button, modifiers):
        mouseButtonState_Pyglet[button] = True
        
    @window_Pyglet.event
    def on_mouse_release(x, y, button, modifiers):
        mouseButtonState_Pyglet[button] = False

    @window_Pyglet.event
    def on_key_press(symbol, modifier):
        keysPressed_Pyglet[__KeyConvert_Pyglet(symbol)] = True

    @window_Pyglet.event
    def on_key_release(symbol, modifier):
        del keysPressed_Pyglet[__KeyConvert_Pyglet(symbol)]

    @window_Pyglet.event
    def on_mouse_motion(x, y, dx, dy):
        mousePositions_Pyglet[0] = x
        mousePositions_Pyglet[1] = window_Pyglet.height - y

    @window_Pyglet.event
    def on_mouse_press(x, y, button, modifiers):
        mouseButtonState_Pyglet[button] = True
        
    @window_Pyglet.event
    def on_mouse_release(x, y, button, modifiers):
        mouseButtonState_Pyglet[button] = False

    @window_Pyglet.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        mousePositions_Pyglet[0] = x
        mousePositions_Pyglet[1] = window_Pyglet.height - y
       
        if buttons & pyglet.window.mouse.LEFT:
           mouseButtonState_Pyglet[pyglet.window.mouse.LEFT] =  True
        if buttons & pyglet.window.mouse.MIDDLE:
           mouseButtonState_Pyglet[pyglet.window.mouse.MIDDLE] =  True
        if buttons & pyglet.window.mouse.RIGHT:
           mouseButtonState_Pyglet[pyglet.window.mouse.RIGHT] =  True
       

############### Common Functions

def loadScreen(resolution=(800, 600), fullscreen=False, selectedBackend="pygame"):
    """LoadScreen(resolution=800, 600), fullscreen=False, selectedBackend="pygame" """
       
    global backend


    if selectedBackend == "pygame" and "pygame" not in backends:
       print("WARNING: Could not load pygame. Faling back to pygame-basic...")
       selectedBackend = "pygame-basic"   
    if selectedBackend in backends:
       backend = selectedBackend
      
    else:
       print("ERROR: Trying to pass " + selectedBackend + " as an argument to LoadScreen(), but it could not be loaded.")
       return
   
    global UnloadScreen, UpdateScreen, ClearScreen, PixelSet, PixelGet, Line, Circle, Rectangle, Ellipse, Triangle, KeyIsPressed, KeyIsNotPressed,\
           KeyGetPressedList, MouseGetButtonL, MouseGetButtonM, MouseGetButtonR, MouseGetX, MouseGetY, MouseGetPosition, MouseGetButtons, FontSelect,\
           FontWrite, MusicLoad, MusicPlay, MusicPause, MusicUnPause, MusicFade, MusicSetVolume, MusicGetVolume, MusicStop, SoundLoad, SoundPlay,\
           SoundStop, SoundSetVolume, SpriteLoad, SpriteRender, SpriteSimpleRender, SpriteHeight, SpriteWidth, ClockSetFPS, ClockGetFPS, ClockTick
    
    if backend == "pyglet":

        global window_Pyglet
        if fullscreen:
            window_Pyglet = pyglet.window.Window(None, None, "PScreen Module (Pyglet)", False, None, True)
        else:
            window_Pyglet = pyglet.window.Window(resolution[0], resolution[1], "PScreen Module (Pyglet)", False, None, False)

        global player_Pyglet 
        player_Pyglet = pyglet.media.ManagedSoundPlayer()
 
        #Internal function to initialize events system
        __InitEvents_Pyglet()
        
        #Necessary for proper alpha-blending and back-to-front rendering
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        #Necessary for alpha-blending in sprites
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

         #bind all functions to their pygame versions
        UnloadScreen = UnloadScreen_Pyglet
        UpdateScreen = UpdateScreen_Pyglet
        ClearScreen = ClearScreen_Pyglet
        
        PixelSet = PixelSet_Pyglet
        PixelGet = PixelGet_Pyglet
        Line = Line_Pyglet
        Circle = Circle_Pyglet
        Rectangle = Rectangle_Pyglet
        Ellipse = Ellipse_Pyglet
        Triangle = Triangle_Pyglet

        KeyIsPressed = KeyIsPressed_Pyglet
        KeyIsNotPressed = KeyIsNotPressed_Pyglet
        KeyGetPressedList = KeyGetPressedList_Pyglet

        MouseGetButtonL = MouseGetButtonL_Pyglet
        MouseGetButtonM = MouseGetButtonM_Pyglet
        MouseGetButtonR = MouseGetButtonR_Pyglet
        MouseGetX = MouseGetX_Pyglet
        MouseGetY = MouseGetY_Pyglet
        MouseGetPosition = MouseGetPosition_Pyglet
        MouseGetButtons = MouseGetButtons_Pyglet

        FontSelect = FontSelect_Pyglet
        FontWrite = FontWrite_Pyglet

        MusicLoad = MusicLoad_Pyglet
        MusicPlay = MusicPlay_Pyglet
        MusicPause = MusicPause_Pyglet
        MusicUnPause = MusicUnPause_Pyglet
        MusicFade = MusicFade_Pyglet
        MusicSetVolume = MusicSetVolume_Pyglet
        MusicGetVolume = MusicGetVolume_Pyglet
        MusicStop = MusicStop_Pyglet

        SoundLoad = SoundLoad_Pyglet
        SoundPlay = SoundPlay_Pyglet
        SoundStop = SoundStop_Pyglet
        SoundSetVolume = SoundSetVolume_Pyglet

        SpriteLoad = SpriteLoad_Pyglet
        SpriteRender = SpriteRender_Pyglet
        SpriteSimpleRender = SpriteSimpleRender_Pyglet
        SpriteHeight = SpriteHeight_Pyglet
        SpriteWidth = SpriteWidth_Pyglet

        FrameSetLimit = FrameSetLimit_Pyglet
        FrameGetLimit = FrameGetLimit_Pyglet
        FrameDelay = FrameDelay_Pyglet

    elif backend == "pygame":
         global PixelSet_Pygame, Line_Pygame, Circle_Pygame, Rectangle_Pygame, Ellipse_Pygame, Triangle_Pygame
         PixelSet_Pygame = PixelSetGFX_Pygame
         Line_Pygame = LineGFX_Pygame
         Circle_Pygame = CircleGFX_Pygame
         Rectangle_Pygame = RectangleGFX_Pygame
         Ellipse_Pygame = EllipseGFX_Pygame
         Triangle_Pygame = TriangleGFX_Pygame
      
    if backend == "pygame" or backend == "pygame-basic":

        #setup the display
        pygame.display.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)
        pygame.font.init()
 
        global screenbuffer_Pygame
        if fullscreen:
            screenbuffer_Pygame=pygame.display.set_mode(resolution,pygame.SWSURFACE+pygame.FULLSCREEN,24)
        else:    
            screenbuffer_Pygame=pygame.display.set_mode(resolution,pygame.SWSURFACE,24)
        pygame.display.set_caption("PScreen Module (" + backend.title() + ")")
        pygame.display.set_icon(pygame.Surface((10,10)))

        #setup the clock for framerate control
        global clock_Pygame
        clock_Pygame = pygame.time.Clock()

        #bind all functions to their pygame versions
        UnloadScreen = UnloadScreen_Pygame
        UpdateScreen = UpdateScreen_Pygame
        ClearScreen = ClearScreen_Pygame
        
        PixelSet = PixelSet_Pygame
        PixelGet = PixelGet_Pygame
        Line = Line_Pygame
        Circle = Circle_Pygame
        Rectangle = Rectangle_Pygame
        Ellipse = Ellipse_Pygame
        Triangle = Triangle_Pygame

        KeyIsPressed = KeyIsPressed_Pygame
        KeyIsNotPressed = KeyIsNotPressed_Pygame
        KeyGetPressedList = KeyGetPressedList_Pygame

        MouseGetButtonL = MouseGetButtonL_Pygame
        MouseGetButtonM = MouseGetButtonM_Pygame
        MouseGetButtonR = MouseGetButtonR_Pygame
        MouseGetX = MouseGetX_Pygame
        MouseGetY = MouseGetY_Pygame
        MouseGetPosition = MouseGetPosition_Pygame
        MouseGetButtons = MouseGetButtons_Pygame

        FontSelect = FontSelect_Pygame
        FontWrite = FontWrite_Pygame

        MusicLoad = MusicLoad_Pygame
        MusicPlay = MusicPlay_Pygame
        MusicPause = MusicPause_Pygame
        MusicUnPause = MusicUnPause_Pygame
        MusicFade = MusicFade_Pygame
        MusicSetVolume = MusicSetVolume_Pygame
        MusicGetVolume = MusicGetVolume_Pygame
        MusicStop = MusicStop_Pygame

        SoundLoad = SoundLoad_Pygame
        SoundPlay = SoundPlay_Pygame
        SoundStop = SoundStop_Pygame
        SoundSetVolume = SoundSetVolume_Pygame

        SpriteLoad = SpriteLoad_Pygame
        SpriteRender = SpriteRender_Pygame
        SpriteSimpleRender = SpriteSimpleRender_Pygame
        SpriteHeight = SpriteHeight_Pygame
        SpriteWidth = SpriteWidth_Pygame

        FrameSetLimit = FrameSetLimit_Pygame
        FrameGetLimit = FrameGetLimit_Pygame
        FrameDelay = FrameDelay_Pygame

######### backend functions

def getBackends():
    return backends

######### collision functions
def collideCircles(circle1_x,circle1_y,circle1_radius,circle2_x,circle2_y,circle2_radius):
    """CollideCircles(circle1_x,circle1_y,circle1_radius,circle2_x,circle2_y,circle2_radius) - Returns True if the two circles collide, False otherwise."""
    if ((circle2_x-circle1_x)**2 + (circle2_y-circle1_y)**2)**0.5  <= (circle1_radius+circle2_radius):
        return True
    else:
        return False
          
def collidePointCircle(point_x,point_y,circle_x,circle_y,circle_radius):
    """CollidePointCircle(point_x,point_y,circle_x,circle_y,circle_radius) - Returns True if the point collides with the circle, False otherwise."""
    if ((point_x-circle_x)**2 + (point_y-circle_y)**2)**0.5  <= circle_radius:
        return True
    else:
        return False
    
def collidePointRectangle(point_x,point_y,rect_x1,rect_y1,rect_x2,rect_y2):
    """CollidePointRectangle(point_x,point_y,rect_x1,rect_y1,rect_x2,rect_y2) - returns True if the point collides with the rectangle, False otherwise."""
    if (rect_x1<point_x<rect_x2  or rect_x2<point_x<rect_x1) and (rect_y1<point_y<rect_y2 or rect_y2<point_y<rect_y1):
        return True
    else:
        return False

def collideRectangles(rect1_x1,rect1_y1,rect1_x2,rect1_y2, rect2_x1,rect2_y1,rect2_x2,rect2_y2  ):
    """CollideRectangles(rect1_x1,rect1_y1,rect1_x2,rect1_y2, rect2_x1,rect2_y1,rect2_x2,rect2_y2  ) - Returns True if the two orthogonal rectangles collide, False otherwise. """
    r1 = pygame.Rect(rect1_x1,rect1_y1,rect1_x2-rect1_x1,rect1_y2-rect1_y1)
    r2 = pygame.Rect(rect2_x1,rect2_y1,rect2_x2-rect2_x1,rect2_y2-rect2_y1)
    return r1.colliderect(r2)    

def collideCircleRectangle(circle_x,circle_y,circle_radius,rect_x1,rect_y1,rect_x2,rect_y2):
    """CollideCircleRectangle(circle_x,circle_y,circle_radius,rect_x1,rect_y1,rect_x2,rect_y2) - Returns True if the circle collides with the rectangle, False otherwise """
    if((rect_x1-circle_radius<circle_x<rect_x2+circle_radius  or rect_x2-circle_radius<circle_x<rect_x1+circle_radius) and  (rect_y1<circle_y<rect_y2  or rect_y2<circle_y<rect_y1)) or ((rect_x1<circle_x<rect_x2  or rect_x2<circle_x<rect_x1) and  (rect_y1-circle_radius<circle_y<rect_y2+circle_radius  or rect_y2-circle_radius<circle_y<rect_y1+circle_radius)):
        return True
    else:
        if CollidePointCircle(rect_x1,rect_y1,circle_x,circle_y,circle_radius):
            return True
        elif CollidePointCircle(rect_x2,rect_y2,circle_x,circle_y,circle_radius):
            return True
        elif CollidePointCircle(rect_x1,rect_y2,circle_x,circle_y,circle_radius):
            return True
        elif CollidePointCircle(rect_x2,rect_y1,circle_x,circle_y,circle_radius):
            return True
        else:
            return False

def collideLineCircle(line_x1,line_y1,line_x2,line_y2,circle_x,circle_y,circle_radius):
   """CollideCircleLine(line_x1,line_y1,line_x2,line_y2,circle_x,circle_y,circlie_radius)"""
   # vector from end point 1 to circle center
   dx1 = circle_x-line_x1
   dy1 = circle_y-line_y1
   # vector from line end to end
   dx2 = line_x2 - line_x1
   dy2 = line_y2 - line_y1

   #dot product of two vectors
   dotprod = float(dx1*dx2 + dy1*dy2)

   dist = (dx2**2 + dy2**2)**0.5  # note, could optimize out the square root here

   param_point = dotprod / dist**2

   if(param_point < 0):
      closest_x = line_x1
      closest_y = line_y1
   elif(param_point > 1):
      closest_x = line_x2
      closest_y = line_y2
   else:
      closest_x = line_x1 + param_point * dx2
      closest_y = line_y1 + param_point * dy2

   dist = ((circle_x-closest_x)**2 + (circle_y-closest_y)**2) ** 0.5
   if dist<=circle_radius:
      return True
   return False

#Used to render circles/ellipses
SEGMENTS = 50
#setup the variables for this class
sounds_Pygame = [None]*256
sprites_Pygame = [None]*256

clock_Pygame = None
limitFPS_Pygame = None

sounds_Pyglet = [None]*256
#Second slot is for loaded flag
sprites_Pyglet = [None]*256

screenbuffer_Pygame=None
window_Pyglet = None

mouseButtonState_Pyglet = [False]*5
mousePositions_Pyglet = [-1, -1] #x, y

keysPressed_Pyglet = {}

soundPlayer_Pyglet = None
player_pyglet = None

musicFading_Pyglet = False
#Main handle to our display 

alphaEnabled_Pygame = True

#Global font
font_Pyglet = None
font_Pygame = None
