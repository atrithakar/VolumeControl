def linMap(var, loVar, hiVar,loOut,hiOut):
    if var<loVar:
        return loOut
    if var>hiVar:
        return hiOut
    slope = (hiOut-loOut)/(hiVar-loVar)
    offset = loOut - (slope*loVar)
    result = (slope*var) + offset
    return result
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
def main():
    x = int(input("x = "))
    print(linMap(x,50,200,0,100))

if __name__ == "__main__":
    main()