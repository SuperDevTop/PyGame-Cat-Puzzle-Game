# Current program operates with the cat moving to the adjacent boxes, now need to randomize the boxes it can go to. 
# Using pygame for the animation 

import pygame
import random

SCREENHEIGHT = 800
SCREENWIDTH = 600

pygame.init()

# creating the screen and setting title bar
screen = pygame.display.set_mode((SCREENHEIGHT, SCREENWIDTH))
pygame.display.set_caption("Andrey's Math IA - Find the Cat")

icon = pygame.image.load('cat-icon.png')
pygame.display.set_icon(icon)

# loading images
# icons courtesy of flaticon
background = pygame.image.load('backyard_800x600.jpg')
boxClosedImg = pygame.image.load('box-closed.png')
boxOpenedImg = pygame.image.load('box-open.png')
catImg = pygame.image.load('cat.png')
catSuperImg = pygame.image.load('cat-super.png')

# declaring variables
guess = []
randPathStart = [0, 1, 2, 3]
boxXLoc = []
boxYLoc = []
numBoxes = 4
boxesYCoord = 400
boxesXStartCoord = 50
boxesXSpacing = 100
clsBtnXStartCoord = 100
clsBtnYStartCoord = 500
clsBtnWidth = 100
clsBtnHeight = 50
clsBtnEnabled = False
showBtnXStartCoord = 300
showBtnYStartCoord = 500
showBtnWidth = 170
showBtnHeight = 50
showBtnEnabled = False
awaitingReset = False

for x in range(0, numBoxes):
    boxXLoc.append(boxesXStartCoord + (x * boxesXSpacing))
    boxYLoc.append(boxesYCoord)

font = pygame.font.SysFont('arial', 20)
currentDay = 0
evasivePath = []


def loadBoxImages(opened=False, openedBox=-1):
    for x in range(0, numBoxes):
        if opened and x == openedBox:
            drawOpenBox(boxesXStartCoord + (x * boxesXSpacing), boxesYCoord)
        else:
            drawClosedBox(boxesXStartCoord + (x * boxesXSpacing), boxesYCoord)


def drawClosedBox(x, y):
    screen.blit(boxClosedImg, (x, y))


def loadCat(day):
    screen.blit(catImg, (boxXLoc[evasivePath[day]], boxesYCoord - 30))


def attemptAnimation(day):
    screen.blit(background, (0, 0))
    loadCat(day)
    loadBoxImages()
    for x in range(0, day + 1):
        displayGuess(x)
    pygame.display.update()
    pygame.time.delay(500)

    screen.blit(background, (0, 0))
    loadCat(day)
    loadBoxImages(True, guess[day])
    for x in range(0, day + 1):
        displayGuess(x)
    pygame.display.update()
    pygame.time.delay(500)

    if day < len(evasivePath) - 2:
        positionXFrom = boxXLoc[evasivePath[day]]
        positionXTo = boxXLoc[evasivePath[day + 1]]

        if positionXFrom <= positionXTo:
            change = 0.5
        else:
            change = -0.5

        currentX = positionXFrom
        while currentX != positionXTo + change:
            screen.blit(background, (0, 0))
            screen.blit(catImg, (currentX, boxesYCoord - 30))
            currentX += change
            loadBoxImages()
            for x in range(0, day + 1):
                displayGuess(x)
            pygame.display.update()


# animate the cat on the last day ie. currentDay
def foundCatAnimation():
    currentX = boxXLoc[guess[currentDay]]
    currentY = boxesYCoord

    while currentY >= 300:
        screen.blit(background, (0, 0))
        screen.blit(catSuperImg, (currentX, currentY))
        loadBoxImages(True, guess[currentDay])
        for x in range(0, currentDay + 1):
            displayGuess(x)
        currentY -= 1
        displayMessage("CONGRATS! YOU HAVE FOUND THE CAT!", 100, 250)
        displayMessage("Reset to play again.", 100, 275)
        pygame.display.update()
        pygame.time.delay(10)


def drawOpenBox(x, y):
    screen.blit(boxOpenedImg, (x, y))


def clickedBox(clickedX, clickedY):
    boxWidth = boxClosedImg.get_width()
    boxHeight = boxClosedImg.get_height()
    for x in range(0, numBoxes):
        if boxXLoc[x] <= clickedX <= (boxXLoc[x] + boxWidth):
            if boxYLoc[x] <= clickedY <= (boxYLoc[x] + boxHeight):
                return x
    return -1


def displayRules():
    messages = ["Try to find the cat hiding in one of the boxes.",
                "  1. Every day you are only allowed to check one box.",
                "  2. Every night the cat will move to an adjacent box.",
                "      example:  move from box 2 to box 1 or 3",
                "Click on a box to check it."]
    pygame.draw.rect(screen, (255, 255, 255), (5, 5, 500, 30 * len(messages)), 0)
    for x in range(len(messages)):
        # x coordinate always at 10, with 30 pixels in between the top of each line (30 * x)
        displayMessage(messages[x], 10, 10 + 30 * x)


# reset game values and reload starting images
def restartGame():
    screen.blit(background, (0, 0))
    loadBoxImages()
    # to specify that you're accessing the global variables
    global currentDay
    global guess
    global evasivePath
    global clsBtnEnabled
    global showBtnEnabled
    global awaitingReset
    currentDay = 0
    guess = []
    evasivePath = []
    displayRules()
    clsBtnEnabled = False
    showBtnEnabled = False
    awaitingReset = False


def displayGuess(dayNum):
    # rgb(128, 128, 128) is grey, (0, 0, 0) is black, (255, 255, 255) is white
    display = font.render("Day " + str(dayNum + 1) + ":  checked box " + str(guess[dayNum] + 1), True, (0, 0, 0))
    # x coordinate is 10 pixels away from the edge
    screen.blit(display, (SCREENHEIGHT - display.get_width() - 10, display.get_height() * dayNum + 10))


def displayMessage(text, x, y):
    # rgb(128, 128, 128) is grey, (0, 0, 0) is black, (255, 255, 255) is white, rgb(0, 0, 255) is blue
    # pygame.draw.rect(screen, (255, 255, 255), (x, y, 50, 50), 0)
    display = font.render(text, True, (0, 0, 0))
    screen.blit(display, (x, y))


def displayButton(colour, outlineColour, x, y, width, height, text):
    outlineThickness = 2
    pygame.draw.rect(screen, outlineColour, (x, y, width + outlineThickness, height + outlineThickness), 0)
    pygame.draw.rect(screen, colour, (x, y, width, height), 0)
    displayText = font.render(text, True, (255, 255, 255))
    screen.blit(displayText,
                (x + (width / 2 - displayText.get_width() / 2), y + (height / 2 - displayText.get_height() / 2)))


# to get plus minus 1 do -1 ^ randomint(1, 2) or something like this
# searches for a evasive path in a random way
def randPath(day, currentBox):
    if guess[day] != currentBox:
        if day + 1 == len(guess):
            evasivePath.append(currentBox)
            return True
        else:
            if currentBox == 0:
                if randPath(day + 1, currentBox + 1):
                    # consider list.insert(index, value) to add to front
                    evasivePath.append(currentBox)
                    return True
                else:
                    return False
            elif currentBox == 4:
                if randPath(day + 1, currentBox - 1):
                    evasivePath.append(currentBox)
                    return True
                else:
                    return False
            else:
                randTemp = random.randint(1, 2)
                if randPath(day + 1, currentBox + ((-1) ** randTemp)):
                    evasivePath.append(currentBox)
                    return True
                elif randPath(day + 1, currentBox + ((-1) ** (randTemp + 1))):
                    evasivePath.append(currentBox)
                    return True
                else:
                    return False
    else:
        return False


def path(day, currentBox):
    if guess[day] != currentBox:
        if day + 1 == len(guess):
            evasivePath.append(currentBox)
        else:
            if currentBox == 0:
                if path(day + 1, currentBox + 1):
                    # consider list.insert(index, value) to add to front
                    evasivePath.append(currentBox)
                    return True
                else:
                    return False
            elif currentBox == 4:
                if path(day + 1, currentBox - 1):
                    evasivePath.append(currentBox)
                    return True
                else:
                    return False
                # return path(day + 1, currentBox - 1)
            else:
                # return path(day + 1, currentBox - 1) or path(day + 1, currentBox + 1)
                if path(day + 1, currentBox - 1):
                    evasivePath.append(currentBox)
                    return True
                elif path(day + 1, currentBox + 1):
                    evasivePath.append(currentBox)
                    return True
                else:
                    return False
    else:
        return False


def pathExist(day, currentBox):
    if guess[day] != currentBox:
        if day + 1 == len(guess):
            return True
        else:
            if currentBox == 0:
                if pathExist(day + 1, currentBox + 1):
                    return True
                else:
                    return False
            elif currentBox == 4:
                if pathExist(day + 1, currentBox - 1):
                    return True
                else:
                    return False
            else:
                if pathExist(day + 1, currentBox - 1):
                    return True
                elif pathExist(day + 1, currentBox + 1):
                    return True
                else:
                    return False
    else:
        return False


running = True
restartGame()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # mousePos = pygame.mouse.get_pos()
            x, y = event.pos
            if not awaitingReset:
                loadBoxImages()
                boxSelection = clickedBox(x, y)
                if boxSelection != -1:
                    # openBox(boxSelection)
                    clsBtnEnabled = True
                    showBtnEnabled = True
                    screen.blit(background, (0, 0))
                    loadBoxImages(True, boxSelection)
                    guess.append(boxSelection)
                    for x in range(0, currentDay + 1):
                        displayGuess(x)
                    pathExistTemp = False
                    for x in randPathStart:
                        if pathExist(0, x):
                            pathExistTemp = True
                            break

                    # cycled through all starting positions boxes and no path is found, ie. cat is found
                    if not pathExistTemp:
                        foundCatAnimation()
                        showBtnEnabled = False
                    currentDay += 1
                    if currentDay >= 1000:#gives the amount of days the user has to try 
                        displayMessage("You failed to find the cat.  Reset to try again", 100, 250)
                        awaitingReset = True

            if clsBtnEnabled and clsBtnXStartCoord <= x <= clsBtnXStartCoord + clsBtnWidth and \
                    clsBtnYStartCoord <= y <= clsBtnYStartCoord + clsBtnHeight:
                restartGame()

            if showBtnEnabled and showBtnXStartCoord <= x <= showBtnXStartCoord + showBtnWidth and \
                    showBtnYStartCoord <= y <= showBtnYStartCoord + showBtnHeight:
                showBtnEnabled = False
                awaitingReset = True
                pathExistTemp2 = False

                # search for an evasive path in a random way via testing for a solution at a random starting point
                random.shuffle(randPathStart)
                for x in randPathStart:  # loops through the random starting positions
                    if randPath(0, x):  # if a path is found via testing random paths. Here you need to change so it starts at middle 
                        pathExistTemp2 = True
                        evasivePath.reverse()
                        break
                for x in range(len(evasivePath)):
                    attemptAnimation(x)
                displayMessage("You failed to find the cat.  Reset to try again", 100, 250)

    if clsBtnEnabled:
        displayButton((105, 105, 105), (211, 211, 211), clsBtnXStartCoord, clsBtnYStartCoord, clsBtnWidth, clsBtnHeight,
                      "Reset")

    if showBtnEnabled:
        displayButton((105, 105, 105), (211, 211, 211), showBtnXStartCoord, showBtnYStartCoord, showBtnWidth,
                      showBtnHeight, "Show Animation")

    pygame.display.update()