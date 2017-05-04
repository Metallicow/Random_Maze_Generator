#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description:
============

Random Maze Generators

Adapted from this base activestate code recipe by FB36:
http://code.activestate.com/recipes/578356-random-maze-generator/


License:
========
Licensed under the <MIT License https://opensource.org/licenses/MIT>

The MIT License (MIT)
Copyright (c) FB - 20121214
Copyright (c) FB36 - 20130106
Copyright (c) Edward Greig - 20160131

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Requirements:
=============

  Depending on the function desired, these additional libraries may be needed:
    * PIL/Pillow - for rendering/making a image.
    * wxPython - for dc rendering/making a bitmap.


"""

#-Imports----------------------------------------------------------------------

#--Python Imports.
import random

#--PIL/Pillow Imports.
from PIL import Image


def GetRandomZigZaggyMaze(mazeWidth, mazeHeight):
    """
    Random Maze Generator using Depth-first Search
    http://en.wikipedia.org/wiki/Maze_generation_algorithm
    FB - 20121214
    """
    # local optimizations.
    randint = random.randint

    # Make the maze matrix/grid.
    maze = [[0 for x in range(mazeWidth)] for y in range(mazeHeight)]
    # 4 directions to move in the maze.
    dirX = [0, 1, 0, -1]
    dirY = [-1, 0, 1, 0]

    # Start the maze from a random cell.
    stack = [(randint(0, mazeWidth - 1), randint(0, mazeHeight - 1))]

    while len(stack) > 0:
        (cellX, cellY) = stack[-1]
        maze[cellY][cellX] = 1
        # Find a new cell to add.
        neighborList = []  # List of available neighbors.
        for i in range(4):
            neighborX = cellX + dirX[i]
            neighborY = cellY + dirY[i]
            if neighborX >= 0 and neighborX < mazeWidth and neighborY >= 0 and neighborY < mazeHeight:
                if maze[neighborY][neighborX] == 0:
                    # of occupied neighbors must be 1.
                    ctr = 0
                    for j in range(4):
                        ex = neighborX + dirX[j]
                        ey = neighborY + dirY[j]
                        if ex >= 0 and ex < mazeWidth and ey >= 0 and ey < mazeHeight:
                            if maze[ey][ex] == 1:
                                ctr += 1
                    if ctr == 1:
                        neighborList.append(i)
        # If 1 or more neighbors available then randomly select one and move.
        if len(neighborList) > 0:
            ir = neighborList[randint(0, len(neighborList) - 1)]
            cellX += dirX[ir]
            cellY += dirY[ir]
            stack.append((cellX, cellY))
        else:
            stack.pop()

    return maze

def GetRandomTraditionalMaze(mazeWidth, mazeHeight):
    """
    Random Maze Generator using Depth-first Search
    http://en.wikipedia.org/wiki/Maze_generation_algorithm
    FB36 - 20130106
    """
    # local optimizations.
    randint = random.randint

    # Make the maze matrix/grid.
    maze = [[0 for x in range(mazeWidth)] for y in range(mazeHeight)]
    # 4 directions to move in the maze.
    dirX = [0, 1, 0, -1]
    dirY = [-1, 0, 1, 0]

    # Start the maze from a random cell.
    cellX = randint(0, mazeWidth - 1)
    cellY = randint(0, mazeHeight - 1)
    # stack element: (x, y, direction).
    maze[cellY][cellX] = 1
    stack = [(cellX, cellY, 0)]

    while len(stack) > 0:
        (cellX, cellY, cellDir) = stack[-1]
        # To prevent zigzags:
        # If changed direction in the last move then cannot change again.
        if len(stack) > 2:
            if cellDir != stack[-2][2]:
                dirRange = [cellDir]
            else:
                dirRange = range(4)
        else:
            dirRange = range(4)

        # Find a new cell to add.
        neighborList = []  # List of available neighbors.
        for i in dirRange:
            neighborX = cellX + dirX[i]
            neighborY = cellY + dirY[i]
            if neighborX >= 0 and neighborX < mazeWidth and neighborY >= 0 and neighborY < mazeHeight:
                if maze[neighborY][neighborX] == 0:
                    ctr = 0  # of occupied neighbors must be 1.
                    for j in range(4):
                        ex = neighborX + dirX[j]
                        ey = neighborY + dirY[j]
                        if ex >= 0 and ex < mazeWidth and ey >= 0 and ey < mazeHeight:
                            if maze[ey][ex] == 1:
                                ctr += 1
                    if ctr == 1:
                        neighborList.append(i)

        # If 1 or more neighbors available then randomly select one and move.
        if len(neighborList) > 0:
            ir = neighborList[randint(0, len(neighborList) - 1)]
            cellX += dirX[ir]
            cellY += dirY[ir]
            maze[cellY][cellX] = 1
            stack.append((cellX, cellY, ir))
        else:
            stack.pop()

    return maze

class Maze(object):
    """
    Maze object
    """
    def __init__(self, mazeStyle='ZigZaggy',
                 mazeWidth=256, mazeHeight=256,
                 color1=(0, 0, 0), color2=(255, 255, 255)):
        """
        Default class constructor.

        :param `mazeStyle`: 'ZigZaggy' or 'Traditional'
        :type `mazeStyle`: str
        :param `mazeWidth`: Width of the maze in pixels.
        :type `mazeWidth`: int
        :param `mazeHeight`: Height of the maze in pixels.
        :type `mazeHeight`: int
        :type `color1`: 3 or 4 RGB or RGBA tuple color
         Ex: (0, 0, 0) or (0, 0, 0, 255)
        :type `color1`: tuple
        :type `color2`: 3 or 4 RGB or RGBA tuple color
         Ex: (255, 255, 255) or (255, 255, 255, 255)
        :type `color2`: tuple
        """
        # Attributes.
        self.maze = None
        self.mazeStyle = mazeStyle
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight
        self.color1 = color1
        self.color2 = color2

    def GetMazeStyles(self):
        """
        Get the supported/implemented maze styles available for generation.

        :returns: A list of string of all implemented maze styles.
        :rtype: tuple
        """
        return ('ZigZaggy', 'Traditional')

    def GetMazeStyle(self):
        """
        Get the maze style attribute.

        :returns: The maze style.
        :rtype: str
        """
        return self.mazeStyle

    def SetMazeStyle(self, mazeStyle):
        """
        Set the maze style attribute.

        :param `mazeStyle`: The maze style to set.
        :type `mazeStyle`: str
        :seealso: :meth:`GetMazeStyles`
        """
        assert mazeStyle in self.GetMazeStyles()
        self.mazeStyle = mazeStyle

    def GetSize(self):
        """
        Get the maze size.

        :returns: The maze size (width, height)
        :rtype: tuple
        """
        size = (self.mazeWidth, self.mazeHeight)
        return size

    def SetSize(self, size):
        """
        Set the maze size.

        :param `size`: The maze size to set (width, height).
        :type `size`: tuple/list
        """
        self.mazeWidth = size[0]
        self.mazeHeight = size[1]

    def GetWidth(self):
        """
        Get the maze width.

        :returns: The maze size width.
        :rtype: int
        """
        return self.mazeWidth

    def SetWidth(self, width):
        """
        Set the maze width.

        :param `width`: The maze width to set.
        :type `width`: int
        """
        self.mazeWidth = width

    def GetHeight(self):
        """
        Get the maze height.

        :returns: The maze size height.
        :rtype: int
        """
        return self.mazeHeight

    def SetHeight(self, height):
        """
        Set the maze height.

        :param `height`: The maze height to set.
        :type `height`: int
        """
        self.mazeHeight = height

    def GetColor1(self):
        """
        Get the 1st maze color.

        :returns: A 3 or 4 color tuple. Ex: (0, 0, 0)
        :rtype: tuple
        """
        return self.color1

    def SetColor1(self, color1):
        """
        Set the 1st maze color.

        :param `color1`: The 1st maze color to set.  Ex: (0, 0, 0)
        :type `color1`: tuple
        """
        self.color1 = color1

    def GetColor2(self):
        """
        Get the 2nd maze color.

        :returns: A 3 or 4 color tuple. Ex: (255, 255, 255)
        :rtype: tuple
        """
        return self.color2

    def SetColor2(self, color2):
        """
        Set the 2nd maze color.

        :param `color2`: The 2nd maze color to set.  Ex: (255, 255, 255)
        :type `color2`: tuple
        """
        self.color2 = color2

    def GetColors(self):
        """
        Get the 2 maze colors.

        :returns: A 2-list or 3 or 4 color tuples. Ex: [(0, 0, 0), (255, 255, 255)]
        :rtype: list
        """
        colors = [self.color1, self.color2]
        return colors

    def SetColors(self, color1, color2):
        """
        Set the 2 maze colors.

        :param `color1`: The 1st maze color to set.  Ex: (0, 0, 0)
        :type `color1`: tuple
        :param `color2`: The 2nd maze color to set.  Ex: (255, 255, 255)
        :type `color2`: tuple
        """
        self.color1 = color1
        self.color2 = color2

    def GetMaze(self):
        """
        Get the maze data matrix.

        :returns: A list of lists.
        :rtype: list
        """
        return self.maze

    ## def SetMaze(self, maze):
    ##     self.maze = maze

    def GenerateRandomMaze(self):
        """
        Generate a random maze from the current :attr:`mazeStyle`.
        """
        mazeStyle = self.GetMazeStyle()
        if mazeStyle == 'ZigZaggy':
            self.GenerateRandomZigZaggyMaze()
        elif mazeStyle == 'Traditional':
            self.GenerateRandomTraditionalMaze()

    def GenerateRandomZigZaggyMaze(self):
        """
        Generate a random zigzaggy style maze.
        """
        self.maze = GetRandomZigZaggyMaze(self.mazeWidth, self.mazeHeight)

    def GenerateRandomTraditionalMaze(self):
        """
        Generate a random traditional style maze.
        """
        self.maze = GetRandomTraditionalMaze(self.mazeWidth, self.mazeHeight)

    def GetAsPILImage(self, imgMode, imgWidth, imgHeight):
        """
        Get the maze data matrix as a PIL.Image.

        :param `imgMode`: One of the PIL.Image.MODES
        :type `imgMode`: str
        :param `imgWidth`: Desired width of the PIL.Image
        :type `imgWidth`: int
        :param `imgHeight`: Desired height of the PIL.Image
        :type `imgHeight`: int
        :returns: A PIL/Pillow image constructed from the maze data matrix.
        :rtype: PIL.Image
        """
        maze = self.maze
        mazeWidth, mazeHeight = self.mazeWidth, self.mazeHeight
        # unittest: Make sure passed args/kwargs/everything is valid.
        assert (maze is not None
            and mazeWidth <= imgWidth
            and mazeHeight <= imgHeight
            and imgWidth >= 0
            and imgHeight >= 0
            and imgMode in Image.MODES)
        # imgWidth, imgHeight = self.imgWidth, self.imgHeight
        # PIL/Pillow Image.
        mode = imgMode
        size = (imgWidth, imgHeight)
        image = Image.new(mode, size)
        imagePixels = image.load()

        colors = self.GetColors()

        # Paint the maze, from top to bottom; left to right.
        for y in range(imgHeight):
            for x in range(imgWidth):
                imagePixels[x, y] = colors[maze[mazeHeight * y / imgHeight][mazeWidth * x / imgWidth]]
        return image

    def GetAswxBitmap(self, imgWidth, imgHeight):
        """
        Get the maze data matrix as a wxPython Bitmap.

        :param `imgWidth`: Desired width of the `wx.Bitmap`.
        :type `imgWidth`: int
        :param `imgHeight`: Desired height of the `wx.Bitmap`.
        :type `imgHeight`: int
        :returns: A wxPython Bitmap constructed from the maze data matrix.
        :rtype: wx.Bitmap
        """
        maze = self.maze
        mazeWidth, mazeHeight = self.mazeWidth, self.mazeHeight
        # unittest: Make sure passed args/kwargs/everything is valid.
        assert (maze is not None
            and mazeWidth <= imgWidth
            and mazeHeight <= imgHeight
            and imgWidth >= 0
            and imgHeight >= 0)

        if 'phoenix' in wx.version():
            bmp = wx.Bitmap(imgWidth, imgHeight)
        else:
            bmp = wx.EmptyBitmap(imgWidth, imgHeight)
        dc = wx.MemoryDC(bmp)
        colors = color1, color2 = self.GetColors()

        dc_SetPen = dc.SetPen
        dc_DrawPoint = dc.DrawPoint
        wxPen = wx.Pen
        dc.SetBrush(wx.Brush(color1))
        dc.SetPen(wx.Pen(color1))
        dc.Clear()
        dc.DrawRectangle(0, 0, mazeWidth, mazeHeight)
        dc.SetBrush(wx.Brush(color2))
        dc.SetPen(wx.Pen(color2))
        # Paint the maze, from top to bottom; left to right.
        for y in range(imgHeight):
            for x in range(imgWidth):
                if colors[maze[mazeHeight * y / mazeHeight][mazeWidth * x / mazeWidth]] == color2:
                    dc_DrawPoint(x, y)

        return dc.GetAsBitmap()

    def PaintOnwxPythonDC(self, dc):
        """
        Paint the maze data matrix on a wxPython device context object.

        :param `dc`: The device context to draw on.
        :type `dc`: wx.DC
        """
        maze = self.maze
        mazeWidth, mazeHeight = self.mazeWidth, self.mazeHeight
        colors = color1, color2 = self.GetColors()
        dc_SetPen = dc.SetPen
        dc_DrawPoint = dc.DrawPoint
        wxPen = wx.Pen
        dc.SetBrush(wx.Brush(color1))
        dc.SetPen(wx.Pen(color1))
        dc.Clear()
        dc.DrawRectangle(0, 0, mazeWidth, mazeHeight)
        dc.SetBrush(wx.Brush(color2))
        dc.SetPen(wx.Pen(color2))
        # Paint the maze, from top to bottom; left to right.
        for y in range(mazeHeight):
            for x in range(mazeWidth):
                if colors[maze[mazeHeight * y / mazeHeight][mazeWidth * x / mazeWidth]] == color2:
                    dc_DrawPoint(x, y)

    def PrettyFormatMaze(self):
        """
        Pretty format the maze
        so print will look like a grid.

        Example:
        >>> print(mazeObj.PrettyFormatMaze())
        [1, 1, 1, 0, 1, 1]
        [0, 0, 1, 1, 1, 0]
        [1, 0, 1, 0, 1, 1]
        [1, 0, 1, 0, 1, 0]
        [1, 0, 0, 1, 1, 1]
        [1, 1, 1, 1, 0, 1]

        :returns: A pretty formated representation of the maze.
        :rtype: str
        """
        mazeStr = '\n'.join([str(row) for row in self.maze])
        return mazeStr


if __name__ == '__main__':
    # Sample app.
    mazeStyle = 'ZigZaggy'
    # mazeStyle = 'Traditional'
    imgMode = "RGBA"
    width, height = 256, 256
    imgWidth, imgHeight, mazeWidth, mazeHeight = (
        width, height, width, height)
    color1 = (0, 0, 0)
    color2 = (255, 255, 255)

    mazeObj = Maze(mazeStyle, mazeWidth, mazeHeight, color1, color2)
    mazeObj.SetMazeStyle(mazeStyle)
    mazeObj.GenerateRandomMaze()
    # img = mazeObj.GetAsPILImage(imgMode, imgWidth, imgHeight)
    # print(mazeObj.PrettyFormatMaze())
    # img.show()
    # img.save("Maze_" + str(mazeWidth) + "x" + str(mazeWidth) + ".png", "PNG")

    import wx
    app = wx.App()
    frame = wx.Frame(None)
    panel = wx.Panel(frame, size=(256, 256))
    panel.SetSizeHints(256, 256, 256, 256)
    def OnPaint(event):
        evtObj = event.GetEventObject()
        dc = wx.PaintDC(evtObj)
        dc.GradientFillLinear(rect=evtObj.GetClientRect(),
                              initialColour='#FFFFFF',
                              destColour='#4444FF',
                              nDirection=wx.SOUTH)
        evtObj.bmp.SetMaskColour(color2)
        dc.DrawBitmap(evtObj.bmp, x=0, y=0, useMask=True)
        ## mazeObj.PaintOnwxPythonDC(dc)
    panel.bmp = mazeObj.GetAswxBitmap(width, height)
    panel.Bind(wx.EVT_PAINT, OnPaint)
    frame.Center()
    frame.Fit()
    w, h = frame.GetSize()
    frame.SetSizeHints(w, h, w, h)
    frame.Show()
    app.MainLoop()
