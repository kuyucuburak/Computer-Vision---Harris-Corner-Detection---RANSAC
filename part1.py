from PIL import Image

import numpy


row = 0
column = 0


def main():
    numpy.set_printoptions(suppress=True, precision=False, threshold=numpy.inf)

    image = Image.open('image.jpg')
    imageMatrix1, imageMatrix2 = harrisDetect(image)

    resultImage1 = Image.fromarray(imageMatrix1)
    resultImage1.save("result_1.png")

    resultImage1 = Image.fromarray(imageMatrix2)
    resultImage1.save("result_2.png")


def harrisDetect(image):
    global row, column

    grayImage = image.convert('L')
    matrix = numpy.array(grayImage)

    row = len(matrix)
    column = len(matrix[0])


    imageMatrix = numpy.array(image)

    cornerMatrix1 = getMc(matrix, 3)
    imageMatrix = compare(imageMatrix, cornerMatrix1, (255, 0, 0), 0.003)

    cornerMatrix2 = getMc(matrix, 5)
    imageMatrix = compare(imageMatrix, cornerMatrix2, (0, 255, 0), 0.004)

    cornerMatrix3 = getMc(matrix, 7)
    imageMatrix = compare(imageMatrix, cornerMatrix3, (0, 0, 255), 0.005)

    imageMatrix1 = imageMatrix.astype(numpy.uint8)


    imageMatrix = compareAllFilters(numpy.array(image), cornerMatrix1, cornerMatrix2, cornerMatrix3, (255, 0, 0))
    imageMatrix2 = imageMatrix.astype(numpy.uint8)


    return imageMatrix1, imageMatrix2


def getM(Ix, Iy, loopCount):
    Mc = numpy.zeros((row, column))
    for i in range(5, row-4):
        for j in range(5, column-4):
            M_all = numpy.zeros((2, 2))
            for m in range(-loopCount, loopCount+1):
                for n in range(-loopCount, loopCount+1):
                    x = Ix[i + m][j + n]
                    y = Iy[i + m][j + n]
                    M = numpy.zeros((2, 2))
                    M[0][0] = x * x
                    M[0][1] = x * y
                    M[1][0] = x * y
                    M[1][1] = y * y
                    M_all = M_all + M
            detM = (M_all[0][0] * M_all[1][1]) - (M_all[0][1] * M_all[1][0])
            traceM = M_all[0][0] + M_all[1][1]
            K = 0.15
            Mc[i][j] = detM - (K * (traceM ** 2))
    return Mc


def getMc(matrix, size):
    loopCount = int(size/2)


    sumIx = numpy.zeros(matrix.shape)

    Ix = numpy.copy(matrix)
    for i in range(-loopCount, 0):
        Ix = numpy.c_[numpy.zeros(row), Ix]
        Ix = numpy.delete(Ix, -1, axis=1)
        sumIx = sumIx + Ix * i

    Ix = numpy.copy(matrix)
    for i in range(1, loopCount+1):
        Ix = numpy.c_[Ix, numpy.zeros(row)]
        Ix = numpy.delete(Ix, 0, axis=1)
        sumIx = sumIx + Ix * i


    sumIy = numpy.zeros(matrix.shape)

    Iy = numpy.copy(matrix)
    for j in range(-loopCount, 0):
        Iy = numpy.r_[numpy.zeros((1, column)), Iy]
        Iy = numpy.delete(Iy, -1, axis=0)
        sumIy = sumIy + Iy * j

    Iy = numpy.copy(matrix)
    for j in range(1, loopCount+1):
        Iy = numpy.r_[Iy, numpy.zeros((1, column))]
        Iy = numpy.delete(Iy, 0, axis=0)
        sumIy = sumIy + Ix * j


    return getM(sumIx, sumIy, loopCount)


def compare(imageMatrix, cornerMatrix, color, thresholdMultiplier):
    threshold = thresholdMultiplier * numpy.max(cornerMatrix)
    for i in range(5, row-4):
        for j in range(5, column-4):
            if cornerMatrix[i][j] > threshold:
                isCorner = True
                for m in range(-1, 2):
                    for n in range(-1, 2):
                        if cornerMatrix[i][j] < cornerMatrix[i + m][j + n]:
                            isCorner = False
                            break
                    if not isCorner:
                        break
                if isCorner:
                    imageMatrix[i+1][j+1] = color
                    imageMatrix[i+1][j] = color
                    imageMatrix[i+1][j-1] = color
                    imageMatrix[i][j+1] = color
                    imageMatrix[i][j-1] = color
                    imageMatrix[i-1][j+1] = color
                    imageMatrix[i-1][j] = color
                    imageMatrix[i-1][j-1] = color
    return imageMatrix


def compareAllFilters(imageMatrix, cornerMatrix1,  cornerMatrix2, cornerMatrix3, color):
    threshold1 = 0.003 * numpy.max(cornerMatrix1)
    threshold2 = 0.004 * numpy.max(cornerMatrix2)
    threshold3 = 0.005 * numpy.max(cornerMatrix3)
    for i in range(5, row-4):
        for j in range(5, column-4):
            if cornerMatrix1[i][j] > threshold1:
                isCorner = True
                for m in range(-1, 2):
                    for n in range(-1, 2):
                        value = cornerMatrix1[i][j]
                        if value < cornerMatrix1[i + m][j + n]:
                            isCorner = False
                            break
                        if value < cornerMatrix2[i + m][j + n]:
                            isCorner = False
                            break
                    if not isCorner:
                        break
                if isCorner:
                    imageMatrix[i+1][j+1] = color
                    imageMatrix[i+1][j] = color
                    imageMatrix[i+1][j-1] = color
                    imageMatrix[i][j+1] = color
                    imageMatrix[i][j-1] = color
                    imageMatrix[i-1][j+1] = color
                    imageMatrix[i-1][j] = color
                    imageMatrix[i-1][j-1] = color
            if cornerMatrix2[i][j] > threshold2:
                isCorner = True
                for m in range(-1, 2):
                    for n in range(-1, 2):
                        value = cornerMatrix2[i][j]
                        if value < cornerMatrix1[i + m][j + n]:
                            isCorner = False
                            break
                        if value < cornerMatrix2[i + m][j + n]:
                            isCorner = False
                            break
                        if value < cornerMatrix3[i + m][j + n]:
                            isCorner = False
                            break
                    if not isCorner:
                        break
                if isCorner:
                    imageMatrix[i+1][j+1] = color
                    imageMatrix[i+1][j] = color
                    imageMatrix[i+1][j-1] = color
                    imageMatrix[i][j+1] = color
                    imageMatrix[i][j-1] = color
                    imageMatrix[i-1][j+1] = color
                    imageMatrix[i-1][j] = color
                    imageMatrix[i-1][j-1] = color
            if cornerMatrix3[i][j] > threshold3:
                isCorner = True
                for m in range(-1, 2):
                    for n in range(-1, 2):
                        value = cornerMatrix3[i][j]
                        if value < cornerMatrix2[i + m][j + n]:
                            isCorner = False
                            break
                        if value < cornerMatrix3[i + m][j + n]:
                            isCorner = False
                            break
                    if not isCorner:
                        break
                if isCorner:
                    imageMatrix[i+1][j+1] = color
                    imageMatrix[i+1][j] = color
                    imageMatrix[i+1][j-1] = color
                    imageMatrix[i][j+1] = color
                    imageMatrix[i][j-1] = color
                    imageMatrix[i-1][j+1] = color
                    imageMatrix[i-1][j] = color
                    imageMatrix[i-1][j-1] = color
    return imageMatrix


if __name__ == "__main__":
    main()
