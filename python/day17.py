import copy

initialCube = open("../input/day17.txt").read().splitlines()
dimensions = 4
print("initialCube: "+str(initialCube))

# A dict of tuples of size D (dimensions)
# e.g. {(x1, y1, ..., D):'.', ..., (xN, yN, ..., D):'#'}
pocketDimension = {}
for y in range(len(initialCube)):
    for x in range(len(initialCube[y])):
        pocketDimension[tuple([x, y] + [0]*(dimensions-2))] = initialCube[y][x]
print("pocketDimension: "+str(pocketDimension))

# Each dimnsion has a range of values, e.g D1= -3 -> 6, D2= -1->4
smallestValuePerDimension = [0] * dimensions
largestValuePerDimension = [len(initialCube[0])-1, len(initialCube)-1] + \
    ([0] * (dimensions-2))
print("smallestValuePerDimension: "+str(smallestValuePerDimension))
print("largestValuePerDimension: "+str(largestValuePerDimension))


def expected_size():
    #  What size the pocketDimension "should" be (just a check)
    totalSize = 1
    for i in range(dimensions):
        totalSize = totalSize * \
            (largestValuePerDimension[i]-smallestValuePerDimension[i]+1)
    return totalSize


print("expected size of pocket dimension: "+str(expected_size()))
print("actual size of pocket dimension: "+str(len(pocketDimension)))


def generate_expansion(d, targetD, newValue, currentList):
    # Generate the empty values that should be added when expanding the pocket dimension
    # this is a slightly compilicatedrecursive function, but is basically a top-down method of generating all necessary value
    # e.g for 3 dimensions, growing "up" (increasing the largest value in D2) in the second dimension:
    # iteration 1: (D1min), ... ,  (D1max)
    # iteration 2: (D1min, D2max+1), ... ,  (D1max, D2max+1)
    # iteration 3: (D1min, D2max+1, D3min), ... ,  (D1max, D2max+1, D3max)

    newList = []

    # d = dimensionsRemaining
    # currentD = dimension currently working on
    currentD = dimensions - d

    if currentD == targetD:
        if len(currentList) == 0:
            newList.append([newValue])
        else:
            for i in currentList:
                newList.append(i+[newValue])
        return generate_expansion(d-1, targetD, newValue, newList)

    elif d > 0:
        if len(currentList) == 0:
            for i in range(smallestValuePerDimension[currentD], largestValuePerDimension[currentD]+1):
                newList.append([i])
        else:
            for i in currentList:
                for j in range(smallestValuePerDimension[currentD], largestValuePerDimension[currentD]+1):
                    newList.append(i+[j])
        return generate_expansion(d-1, targetD, newValue, newList)

    else:
        return currentList


def grow_X_Dimension(dimension, newMinMax):
    # expand the pocket Dimension if any dimesnsion has a value ('#') on it's edge

    global pocketDimension

    # generate an extra "layer" for dimension D
    sliceToAdd = generate_expansion(dimensions, dimension, newMinMax, [])
    for coord in sliceToAdd:
        pocketDimension[tuple(coord)] = '.'

    # update smallest/largest values
    if newMinMax < smallestValuePerDimension[dimension]:
        smallestValuePerDimension[dimension] = newMinMax
    else:
        largestValuePerDimension[dimension] = newMinMax


def expand_pocket_dimension():
    global pocketDimension
    # if there exists a value on the edge
    expanding = True
    while(expanding):
        expanding = False
        for coordinate in pocketDimension:

            # if the coordinate is active, check each dimension to see if it is on the "edge"
            if pocketDimension[coordinate] == '#':
                for dimension in range(dimensions):
                    if coordinate[dimension] == smallestValuePerDimension[dimension]:
                        grow_X_Dimension(
                            dimension, smallestValuePerDimension[dimension]-1)
                        expanding = True
                    elif coordinate[dimension] == largestValuePerDimension[dimension]:
                        grow_X_Dimension(
                            dimension, largestValuePerDimension[dimension]+1)
                        expanding = True

                    if expanding:
                        break

            if expanding:
                break


# 3^n - 1 = number of neighbours
neighbourTranslations = [[] for i in range(3**dimensions)]


def generate_neighbour_translations(dimensions):
    # this is horrible, but generates a set of translation/shift matrices for each neighbour for any input dimension
    global neighbourTranslations
    for i in range(len(neighbourTranslations)):
        for d in range(dimensions):
            value = ((i//3**d) % 3)-1
            neighbourTranslations[i].append(value)


generate_neighbour_translations(dimensions)

# remove identity translation, e.g. (0, 0, 0, 0)
identityTranslation = [0]*dimensions
neighbourTranslations.remove(identityTranslation)

print("neighbour translations: "+str(neighbourTranslations))


def get_neighbour(coordinate, neighbourShift):
    neighbourCoordinate = neighbourShift.copy()
    for i, val in enumerate(coordinate):
        neighbourCoordinate[i] = neighbourShift[i]+val
    return neighbourCoordinate


def apply_rules():
    global pocketDimension
    pocketDimensionCopy = pocketDimension.copy()
    for coordinate in pocketDimensionCopy:
        totalActiveNeighbours = 0
        for neighbourShift in neighbourTranslations:
            neighbourCoordinate = tuple(
                get_neighbour(coordinate, neighbourShift))
            try:
                if pocketDimensionCopy[neighbourCoordinate] == '#':
                    totalActiveNeighbours += 1
                    if totalActiveNeighbours > 3:
                        break
            except KeyError:
                # If neighbour is outside of pocketDimension
                continue

        if pocketDimensionCopy[coordinate] == '#' and not (totalActiveNeighbours == 2 or totalActiveNeighbours == 3):
            pocketDimension[coordinate] = '.'
        elif pocketDimensionCopy[coordinate] == '.' and totalActiveNeighbours == 3:
            pocketDimension[coordinate] = '#'


def count_active():
    total = 0
    for coordinate in pocketDimension:
        if pocketDimension[coordinate] == '#':
            total += 1
    return total


iterations = 6
for i in range(iterations):
    print("iteration i: "+str(i))
    expand_pocket_dimension()
    #print("pocketDimension after expanding: " + str(pocketDimension))
    print("size of pocketDimension after expanding: " + str(len(pocketDimension)))
    print("expected size of pocketDimension: " + str(expected_size()))

    apply_rules()
    #print("pocketDimension after applying rules: " + str(pocketDimension))
    print("total active: "+str(count_active()))
    print("")

print("total active: "+str(count_active()))
