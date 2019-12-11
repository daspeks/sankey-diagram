import sys

from SimpleGraphics import *
import math

def loadData(inf):
    
    # Read input in a list
    dlist = inf.readlines()

    # Create an empty dictionary to store data destination and values
    data = {}
    for i, value in enumerate(dlist):
        
        # Add the title separately
        if i == 0:
            data[value] = []
        
        # Add source title and its colors, if they exist
        elif i == 1:
            buf = value.rstrip().split(",")
            if len(buf) == 1: # no colors exist
                data[buf[0]] = []
            else: # colors exist
                data[buf[0]] = [int(buf[1]), int(buf[2]), int(buf[3])]
    
        # Add destinations, their values and colors, if they exist
        else:
            buf = value.rstrip().split(",")
            if len(buf) == 2: # no colors exist
                data[buf[0]] = [float(buf[1])]
            else: # colors exist
                data[buf[0]] = [float(buf[1]), int(buf[2]), int(buf[3]), int(buf[4])]

    return data



def drawSankey(data):

    # Find total flow
    totalFlow = 0
    nod = 0
    for i, value in enumerate(data.values()):
        if i >= 2: # iterating only through destination values
            totalFlow += value[0]
            nod = i-1

    # Calculate available pixels
    availP = 450 - (nod - 1) * 10

    # Calculate pixels per unit of flow
    ppuf = availP / totalFlow

    # Calculate height of destination bars
    height = []
    for i, value in enumerate(data.values()):
        if i >= 2 : # iterating only through destination values
            height.append(value[0] * ppuf)
    sh = totalFlow * ppuf

    # Get a colors list from the mentioned website
    colors = [[230, 25, 75], [60, 180, 75], [255, 225, 25], [0, 130, 200],
              [245, 130, 48], [145, 30, 180], [128, 128, 128], [240, 50, 230],
              [210, 245, 60], [250, 190, 190], [0, 128, 128], [230, 190, 255],
              [170, 110, 40], [255, 250, 200], [128, 0, 0], [170, 255, 195],
              [128, 128, 0], [255, 215, 180], [128, 128, 128]]

    # Set colors of the source and destination bars
    ucolors = [] # used_colors
    sr, sg, sb = 0, 0, 0 # set source to black (default)
    cc = 0 # color counter to iterate throught 'colors' from start (optional)
    for i, value in enumerate(data.values()):
        
        # retrieve source color, if it exists, for later use
        if i == 1 and len(value) == 3:
            sr, sg, sb = value[0], value[1], value[2]
        
        if i >= 2 : # iterating only through destination values
            # check if r,g,b values are available for the particular destination
            if len(value) == 4:
                ucolors.append([value[1], value[2], value[3]])
            
            # add color from 'colors' if no colors exist
            else:
                ucolors.append(colors[cc]) # to start from first position in colors
                cc += 1 # update color counter after you use it


    # At the end of the above loop, ucolors will be of the same length as the number of destinations.

    # Draw destination bars
    dstartx = 700
    dstarty = 100
    y = dstarty
    gap = 60
    width = 20
    dc = 2 # dictionary_counter for labels
    for c, h in enumerate(height):
        setOutline('black')
        setFill(ucolors[c][0], ucolors[c][1], ucolors[c][2])
        rect(dstartx, y, width, h)
        setFont("Times", "10")
        text(dstartx + gap, y + (h/2), list(data.keys())[dc])
        y = y + h + 10
        dc = dc + 1

    # Get the last y pixel of the last destination
    dendy = y - 10

    # Get total height of destinations
    dh = dendy - dstarty

    # Set source color to a color not present in 'colors' list, if source color is still black (checking only red component)
    if sr == 0:
        sr, sg, sb = 70, 70, 240

    # Draw source
    sstartx = 100
    sstarty = dstarty + (dh/2) - (sh/2)
    swidth = 40
    setOutline('black')
    setFill(sr, sg, sb)
    rect(sstartx, sstarty, swidth, sh)
    line_width = dstartx - (sstartx + swidth)

    # Connecting source to destinations
    for i, h in enumerate(height):
        # set destination colors
        red, green, blue = ucolors[i][0], ucolors[i][1], ucolors[i][2]
        for col in range(line_width + 2): # 2 because you need +1 to color over the black left border of the destination; another +1 because you also need to color over the black right border of the source which we start from swidth - 1. Since we do swidth-1 below we add +1 to 1 and hence +2
            m = col / (line_width)
            
            r = (sr * (1 - m)) + (m * red)
            g = (sg * (1 - m)) + (m * green)
            b = (sb * (1 - m)) + (m * blue)
            
            m = m * math.pi - math.pi / 2
            m = (math.sin(m) + 1) / 2
            
            # Draw black border
            setColor(0, 0, 0)
            line(sstartx + (swidth - 1) + col, sstarty - (m * (sstarty - dstarty)),
                 sstartx + (swidth - 1) + col, sstarty - (m * (sstarty - dstarty)))
            
            # Draw box color
            setColor(r, g, b)
            line(sstartx + (swidth - 1) + col, sstarty + 1 - (m * (sstarty - dstarty)),
                 sstartx + (swidth - 1) + col, sstarty + h - 1 - (m * (sstarty - dstarty))) # -1 to smooth out the end
            
            # Draw black border
            setColor(0, 0, 0)
            line(sstartx + (swidth - 1) + col, sstarty + h - 1 - (m * (sstarty - dstarty)),
                 sstartx + (swidth - 1) + col, sstarty + h - 1 - (m * (sstarty - dstarty))) # -1 to smooth out the end
        
        sstarty = sstarty + h
        dstarty = dstarty + h + 10




def main():
    
    # Part 1: Handle inputs
    if (len(sys.argv) == 1):
        filename = input("Enter file name: ")
        
    elif (len(sys.argv) == 2):
        filename = sys.argv[1]
        
    else:
        print("Error: Invalid arguments")
        close()
        sys.exit()

    try:
        inf = open(filename, "r")
    except:
        print ('Error: File not found or invalid file name')
        close()
        sys.exit()


    # Part 2: Load data
    data = loadData(inf)
    inf.close()
    
    # Display information on SimpleGraphics window as required
    setFont("Times", "24", "bold")
    text(400, 50, list(data.keys())[0])
    setFont("Times", "10")
    text(35, 300, list(data.keys())[1])

    # Part 3: Draw a Sankey diagram from data
    drawSankey(data)

    
main()
