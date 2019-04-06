from warnings import simplefilter
from matplotlib import pyplot, MatplotlibDeprecationWarning

import numpy
import random


randomIntegerLimit = 2000
numberOfPoints = 750
margin = 25

maxNumberOfIteration = 5000
numberOfIteration = 0
minNumberOfSuitablePoints = 30


def main():
    global numberOfIteration

    numpy.set_printoptions(suppress=True, precision=False, threshold=numpy.inf)
    simplefilter(action='ignore', category=MatplotlibDeprecationWarning)

    index1_1 = 0
    index1_2 = 0
    index2_1 = 0
    index2_2 = 0
    index3_1 = 0
    index3_2 = 0
    max1 = 0
    max2 = 0
    max3 = 0
    pointsX, pointsY = produceRandomPoints()
    for i in range(0, maxNumberOfIteration):
        numberOfIteration = numberOfIteration + 1

        index1, index2 = produceRandomIndexes()

        x1 = pointsX[index1]
        x2 = pointsX[index2]
        y1 = pointsY[index1]
        y2 = pointsY[index2]

        if x2 == x1:
            continue

        m = round((y2 - y1) / (x2 - x1), 2)
        n = round((y2 - m * x2), 2)

        counter = getSuitablePoints(pointsX, pointsY, m, n,)
        if counter > max1:
            max3 = max2
            max2 = max1
            max1 = counter

            index3_1 = index2_1
            index3_2 = index2_2

            index2_1 = index1_1
            index2_2 = index1_2

            index1_1 = index1
            index1_2 = index2
        elif counter > max2 and not((index2_1 == index1 and index2_2 == index2) or (index2_1 == index2 and index2_2 == index1)) and not((index1_1 == index1 and index1_2 == index2) or (index1_1 == index2 and index1_2 == index1)):
            max3 = max2
            max2 = counter

            index3_1 = index2_1
            index3_2 = index2_2

            index2_1 = index1
            index2_2 = index2
        elif counter > max3 and not((index3_1 == index1 and index3_2 == index2) or (index3_1 == index2 and index3_2 == index1)) and not((index2_1 == index1 and index2_2 == index2) or (index2_1 == index2 and index2_2 == index1)):
            max3 = counter

            index3_1 = index1
            index3_2 = index2

            if max3 > minNumberOfSuitablePoints:
                break

    drawGraphic(pointsX, pointsY, index1_1, index1_2, 1, max1)
    drawGraphic(pointsX, pointsY, index2_1, index2_2, 2, max2)
    drawGraphic(pointsX, pointsY, index3_1, index3_2, 3, max3)

    pyplot.show()


def produceRandomPoints():
    randomPointsX = []
    randomPointsY = []
    for i in range(0, numberOfPoints):
        valueX = random.randint(0, randomIntegerLimit)
        valueY = random.randint(0, randomIntegerLimit)
        while randomPointsX.__contains__(valueX) and randomPointsY.__contains__(valueY):
            valueX = random.randint(0, randomIntegerLimit)
            valueY = random.randint(0, randomIntegerLimit)

        randomPointsX.append(valueX)
        randomPointsY.append(valueY)

    return numpy.array(randomPointsX), numpy.array(randomPointsY)


def produceRandomIndexes():
    index1 = random.randint(0, numberOfPoints-1)
    index2 = random.randint(0, numberOfPoints-1)
    while index1 == index2:
        index1 = random.randint(0, numberOfPoints-1)
        index2 = random.randint(0, numberOfPoints-1)

    return index1, index2


def getSuitablePoints(pointsX, pointsY, m, n):
    counter = 0
    for i in range(0, numberOfPoints):
        x = pointsX[i]
        y = pointsY[i]

        tempN = y - m*x
        if (n - margin) < tempN < (n + margin):
            counter = counter + 1

    return counter


def drawGraphic(pointsX, pointsY, index1, index2, number, numberOfData):
    def getX(nP, Y):
        return (Y - nP) / m

    def getY(nP, X):
        return m*X + nP

    if number == 1:
        pyplot.scatter(pointsX, pointsY, color='#004A7F')

    pyplot.subplot(int("22" + str(number)))
    pyplot.scatter(pointsX, pointsY, color='#004A7F')

    x1 = pointsX[index1]
    x2 = pointsX[index2]
    y1 = pointsY[index1]
    y2 = pointsY[index2]

    m = round((y2 - y1) / (x2 - x1), 2)
    n = round((y2 - m * x2), 2)

    if m < 1:
        pyplot.plot([0, randomIntegerLimit], [getY(n, 0), getY(n, randomIntegerLimit)], 'r-', lw=2)
        pyplot.plot([0, randomIntegerLimit], [getY(n-margin, 0), getY(n-margin, randomIntegerLimit)], 'g-', lw=2)
        pyplot.plot([0, randomIntegerLimit], [getY(n+margin, 0), getY(n+margin, randomIntegerLimit)], 'g-', lw=2)
    else:
        pyplot.plot([getX(n, 0), getX(n, randomIntegerLimit)], [0, randomIntegerLimit], 'r-', lw=2)
        pyplot.plot([getX(n-margin, 0), getX(n-margin, randomIntegerLimit)], [0, randomIntegerLimit], 'g-', lw=2)
        pyplot.plot([getX(n+margin, 0), getX(n+margin, randomIntegerLimit)], [0, randomIntegerLimit], 'g-', lw=2)
    pyplot.title("slope: " + str(m) + "\nnumber of data: " + str(numberOfData))


    pyplot.subplot(int("224"))
    pyplot.scatter(pointsX, pointsY, color='#004A7F')
    if m < 1:
        pyplot.plot([0, randomIntegerLimit], [getY(n, 0), getY(n, randomIntegerLimit)], 'r-', lw=2)
        pyplot.plot([0, randomIntegerLimit], [getY(n-margin, 0), getY(n-margin, randomIntegerLimit)], 'g-', lw=2)
        pyplot.plot([0, randomIntegerLimit], [getY(n+margin, 0), getY(n+margin, randomIntegerLimit)], 'g-', lw=2)
    else:
        pyplot.plot([getX(n, 0), getX(n, randomIntegerLimit)], [0, randomIntegerLimit], 'r-', lw=2)
        pyplot.plot([getX(n-margin, 0), getX(n-margin, randomIntegerLimit)], [0, randomIntegerLimit], 'g-', lw=2)
        pyplot.plot([getX(n+margin, 0), getX(n+margin, randomIntegerLimit)], [0, randomIntegerLimit], 'g-', lw=2)
    pyplot.title("number of iteration: " + str(numberOfIteration))


if __name__ == "__main__":
    main()
