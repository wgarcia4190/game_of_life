import pygame
import numpy as np
import time

pygame.init()

width, height = 1000, 1000
backgroundColor = 25, 25, 25
xAxisTotalCells, yAxisTotalCells = 50, 50
cellsWidth = width / xAxisTotalCells
cellsHeight = height / yAxisTotalCells

gameState = np.zeros((xAxisTotalCells, yAxisTotalCells))

gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

screen = pygame.display.set_mode((width, height))
screen.fill(backgroundColor)

pause = False

while True:

    newGameState = np.copy(gameState)

    screen.fill(backgroundColor)
    time.sleep(0.1)

    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pause = not pause

        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / cellsWidth)), int(np.floor(posY / cellsHeight))
            newGameState[celX, celY] = not mouseClick[2]

    for yAxis in range(0, yAxisTotalCells):
        for xAxis in range(0, xAxisTotalCells):

            if not pause:
                neighbourCell = gameState[(xAxis - 1) % xAxisTotalCells, (yAxis - 1) % yAxisTotalCells] + \
                                gameState[xAxis % xAxisTotalCells, (yAxis - 1) % yAxisTotalCells] + \
                                gameState[(xAxis + 1) % xAxisTotalCells, (yAxis - 1) % yAxisTotalCells] + \
                                gameState[(xAxis - 1) % xAxisTotalCells, yAxis % yAxisTotalCells] + \
                                gameState[(xAxis + 1) % xAxisTotalCells, yAxis % yAxisTotalCells] + \
                                gameState[(xAxis - 1) % xAxisTotalCells, (yAxis + 1) % yAxisTotalCells] + \
                                gameState[xAxis % xAxisTotalCells, (yAxis + 1) % yAxisTotalCells] + \
                                gameState[(xAxis + 1) % xAxisTotalCells, (yAxis + 1) % yAxisTotalCells]

                # Rule 1
                if gameState[xAxis, yAxis] == 0 and neighbourCell == 3:
                    newGameState[xAxis, yAxis] = 1

                # Rule 2
                elif gameState[xAxis, yAxis] == 1 and (neighbourCell < 2 or neighbourCell > 3):
                    newGameState[xAxis, yAxis] = 0

            polygon = [(xAxis * cellsWidth, yAxis * cellsHeight),
                       ((xAxis + 1) * cellsWidth, yAxis * cellsHeight),
                       ((xAxis + 1) * cellsWidth, (yAxis + 1) * cellsHeight),
                       (xAxis * cellsWidth, (yAxis + 1) * cellsHeight)]

            if newGameState[xAxis, yAxis] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), polygon, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), polygon, 0)

    gameState = np.copy(newGameState)
    pygame.display.flip()
