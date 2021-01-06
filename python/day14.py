input = open("../input/day14.txt").read().splitlines()


def decimalTo36bit(decimal):
    bit = str(bin(decimal))[2:]
    zerosToAdd = "0" * (36-len(bit))
    bit = zerosToAdd + bit
    return bit


def applyMaks(mask, decimal):
    # apply mask
    bit = decimalTo36bit(decimal)
    newBit = []
    for idx, val in enumerate(mask):
        if val == 'X':
            newBit.append(bit[idx])
        else:
            # ^ => XOR. Therefor, flip bit only if bit in decimal and mask differ
            if int(val) ^ int(bit[idx]):
                newBit.append(val)
            else:
                newBit.append(bit[idx])
    newBit = ''.join(newBit)
    return int(newBit, 2)


currentMask = ""
memory = {}
for inx, line in enumerate(input):
    if line[:4] == "mask":
        currentMask = line[7:]
        print("")
        print("currentMask: "+str(currentMask))
    else:
        print("line: "+str(line))
        splitLine = line.split()
        memoryAddress, value = int(splitLine[0][4:-1]), int(splitLine[2])
        maskedValue = applyMaks(currentMask, value)
        memory[memoryAddress] = maskedValue

#print("memory: "+str(memory))

total = 0
for i in memory:
    total += memory[i]

print("total: "+str(total))
