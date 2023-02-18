def costBenefit(cumDistance: int, majorTurns: int, stops: int, level1: int, level2: int, level3: int, avgSpeed: int, compTime: int, Status: int):
    """
    params:
      @Cumulative Distance(Miles) (+)
      @Major turns (+)
      @Number of stops (+)
      @Level 1 Turns (Easy) (+)
      @Level 2 turns (Medium) (++)
      @Level 3 Turns (Hard) (+++)
      @Average Speed  | Nothing
      @Estimated Completion Time
      @Current Status | Nothing
    Write a program to calculate the benefit cost score based 
    on the details mentioned in the benefit cost score page.
    returns:
      benefitScore: int
    """
    # loss = time + weight avg of turns + no. of stops 
    # Softmax 
    turnSigma = level1*1 + level2*2 + level3*3
    totalTurns = level1 + level2 + level3
    cul = compTime + (turnSigma/totalTurns)  + stops + majorTurns
    return (cumDistance/cul)
