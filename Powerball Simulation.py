import random

winningNums = []
for i in range(5):
    num = random.randrange(1,70)
    while num in winningNums:
        num = random.randrange(1,70)
    winningNums.append(num)

powerballNum = random.randrange(1,27)

winningList = winningNums.copy()
winningList.append(powerballNum)
print(winningList)

for i in range(10000):
    ticketNums = []
    for j in range(5):
        num = random.randrange(1,70)
        while num in ticketNums:
            num = random.randrange(1,70)
        ticketNums.append(num)
    
    ticketPowerball = random.randrange(1,27)

    match = 0
    for num in winningNums:
        if num in ticketNums:
            match += 1

    powerball = 0
    if powerballNum == ticketPowerball:
        powerball = 1

    winnings = 0
    if powerball == 1:
        if match == 4:
            winnings = 50000
        elif match == 3:
            winnings = 100
        elif match == 2:
            winnings = 7
        else:
            winnings = 4
    else:
        if match == 5:
            winnings = 1000000
        elif match == 4:
            winnings = 100
        elif match == 3:
            winnings = 7

    # Commented out code allows for easy transference to .csv file
    # format: [ticket num, n1, n2, n3, n4, n5, pb num, num regular matches, pb match, money earned]
    '''ticketList = ticketNums.copy()
    ticketList.insert(0, i+1)
    ticketList.append(ticketPowerball)
    ticketList.append(match)
    ticketList.append(powerball)
    if powerball == 1 and match == 5:
        ticketList.append("jackpot")
    else:
        ticketList.append(winnings)

    print(ticketList)'''
    
    print(winnings)
