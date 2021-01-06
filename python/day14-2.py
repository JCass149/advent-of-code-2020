input = open("../input/day14.txt").read().splitlines()


def decimalTo36bit(decimal):
    bit = str(bin(decimal))[2:]
    zerosToAdd = "0" * (36-len(bit))
    bit = zerosToAdd + bit
    return bit


def applyMask(mask, decimal):
    # apply mask
    bit = decimalTo36bit(decimal)
    newBit = []
    floatingNumbers = 0
    for idx, val in enumerate(mask):
        if val == 'X':
            newBit.append('X')
        elif val == '1':
            newBit.append('1')
        else:
            newBit.append(bit[idx])
    newBit = ''.join(newBit)
    return newBit


def addressesDecoder(mask, decimal):
    result = applyMask(mask, decimal)
    addresses = generate_floating_addresses(result, [[]], 0)
    return addresses


def generate_floating_addresses(result, addresses, index):
    addressesBefore = len(addresses)
    if result[index] == 'X':
        for i in range(addressesBefore):
            # add a new address with 0 at the end
            toAdd = addresses[i].copy()
            toAdd.append('0')
            addresses.append(toAdd)
            # add a 1 to the end of the existing address
            addresses[i].append('1')
    else:
        for i in range(addressesBefore):
            addresses[i].append(result[index])
    # if at the last address
    if index == (36-1):
        return addresses
    else:
        return generate_floating_addresses(result, addresses, index+1)


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
        addresses = addressesDecoder(currentMask, memoryAddress)
        for address in addresses:
            decimalAddress = int(''.join(address), 2)
            memory[decimalAddress] = value


#print("memory: "+str(memory))

total = 0
for i in memory:
    total += memory[i]

print("total: "+str(total))
