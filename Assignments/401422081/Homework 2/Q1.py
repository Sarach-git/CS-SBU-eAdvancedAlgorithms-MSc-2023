

def play(nums):
    print (nums)
    numsCount = len(nums)
    playerTurn = False
    sequence = ""
    maxScore = 0

    for i in range(0, numsCount):
        playerTurn = not playerTurn
        print(len(nums))
        # 1 ball is left, select it and put L 
        if(len(nums)==1):
            sequence = sequence + "L"
            maxScore = maxScore + (nums[0] if playerTurn else 0)
            nums.pop(0)
            continue
        # 3 ball is left, select the max one from right or left 
        if(len(nums)==3):
            if(nums[0]<=nums[2]):
                sequence = sequence + "R"
                maxScore = maxScore + (nums[len(nums) - 1] if playerTurn else 0)
                nums.pop(len(nums) - 1)
            else:
                sequence = sequence + "L"
                maxScore = maxScore + (nums[0] if playerTurn else 0)
                nums.pop(0)
            continue
        # 2 ball is left, select the maximum one  
        if(len(nums)==2):
            if(nums[0]<=nums[1]):
                sequence = sequence + "R"
                maxScore = maxScore + (nums[len(nums) - 1] if playerTurn else 0)
                nums.pop(len(nums) - 1)
            else:
                sequence = sequence + "L"
                maxScore = maxScore + (nums[0] if playerTurn else 0)
                nums.pop(0)
            continue

        # Select the one which if we select it, we lose the minimum 
        if(nums[0] - max(nums[1], nums[len(nums) - 1]) <= nums[len(nums) - 1] - max(nums[0],nums[len(nums) - 2])):
            sequence = sequence + "R"
            maxScore = maxScore + (nums[len(nums) - 1] if playerTurn else 0)
            nums.pop(len(nums) - 1)
        else:
            sequence = sequence + "L"
            maxScore = maxScore + (nums[0] if playerTurn else 0)
            nums.pop(0)

    return maxScore, sequence


input = "10 80 90 30"
nums = list(map(int, input.split()))
maxScore, sequence = play(nums)
print(maxScore)
print(sequence)

