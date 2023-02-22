import pandas as pd

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

def numOfTurns(data):
    '''
    Number of major turns
    @param data: Pandas dataframe containing entire loop data
    '''
    turnCount = 0
    for instructions in data["Major Turns/Instructions"]:
        if "left" in instructions.lower() or "right" in instructions.lower() or "turn" in instructions.lower():
            turnCount += 1
    return turnCount

def numOfStops(data):
    '''
    Determines the number of stops
    @param data: Pandas dataframe containing entire loop data
    '''
    stopCount = 0
    for instructions in data["Major Turns/Instructions"]:
        if "stop" in instructions.lower() and "***" not in instructions.lower() and "stage stop" not in instructions.lower():
            stopCount += 1
    for notes in data["Landmarks/Notes"]:
        if "stop" in notes.lower() and "***" not in notes.lower() and "not" not in notes.lower():
            stopCount += 1
    return stopCount

def totalTimeAndSpeed(data, totalDistance):
    '''
    Calculates the total time and average speed of the loop
    @param data: Pandas dataframe containing entire loop data
    @param totalDistance: float representing the total distance of the loop
    '''
    totalTime = 0
    for index, row in data.iterrows():
        totalTime += float(row["Int"]) / float(row["Spd"])

    averageSpeed = totalDistance / totalTime
    return totalTime, averageSpeed

def cleanSpeedData(data):
    data.at[0, "Int"] = 0
    prev = 0
    for speed in data['Spd']:
        if speed != "  ":
            prev = int(speed)

    for i, row in data.iterrows():
        if row["Spd"] == "  ":
            data.at[i, "Spd"] = prev
        elif int(row["Spd"]) > 65:
            data.at[i, "Spd"] = 65
            prev = 65
        else:
            prev = row["Spd"]

def convertData(file):
    '''
    This function takes in a csv file in the format of route descriptions on the route book and
    creates a csv file with the following properties calculate:
        Cumulative Distance (Miles)
        Major turns
        Number of stops
        Level 1 Turns (Easy)
        Level 2 Turns (Medium)
        Level 3 Turns (Hard)
        Average Speedw
        Estimated Completion Time
        Current Status
    It will also return a pandas dataframe with the same information
    '''
    data = pd.read_csv(file)
    columns = ["Loop Name", "Cumulative Distance (Miles)", "Major Turns", "Number of stops", "Level 1 Turns (Easy)", "Level 2 Turns (Medium)", 
                "Level 3 Turns (Hard)", "Average Speed", "Estimated Completion Time", "Current Status"]
    
    loopData = []
    loopData.append(file)

    # Total distance
    totalDistance = float(data["Trip"][len(data["Trip"])-1])
    loopData.append(totalDistance)

    # Number of turns
    turnCount = numOfTurns(data)
    loopData.append(turnCount)

    # Number of Stops
    stopCount = numOfStops(data)
    loopData.append(stopCount)

    # Placeholder for level of turn
    loopData.append("N/A")
    loopData.append("N/A")
    loopData.append("N/A")

    # Calculate time and speed
    cleanSpeedData(data) # Clean speed data
    totalTime, averageSpeed = totalTimeAndSpeed(data, totalDistance)
    loopData.append(averageSpeed)
    loopData.append(totalTime)
    loopData.append("N/A")

    # print(loopData)
    df = pd.DataFrame([loopData], columns=columns)
    df.to_csv(file.split(".")[0] + "Converted" + ".csv")
    return df


def convertMultipleData(files):
    '''
    Takes in a list of file paths to CSVs in the format of route descriptions on the route book,
    converts the data using convertData, and THEN combines the result into a single
    CSV and returns a dataframe with the same information
    
    @params files: List of strings representing files paths to CSVs
    '''
    dfs = [convertData(file) for file in files]
    combined = pd.concat(dfs, ignore_index=True)
    combined.to_csv(r"data\CombinedConverted.csv")
    return combined

def scoreRankLoops(loopData):
    '''
    Takes in a combined dataframe of converted data for each loop, scores each loop,
    and returns a dataframe with each loop sorted from highest benefit cost score to least

    @params loopData: pandas dataframe of converted loop data
    '''
    scored = loopData.copy()

    # THe number of turns at each level is still being filled with "N/A" so I've put in dummy values for now
    '''
    scores = [costBenefit(loop["Cumulative Distance (Miles)"], loop["Major Turns"], loop["Number of stops"], loop["Level 1 Turns (Easy)"], 
                            loop["Level 2 Turns (Medium)"], loop["Level 3 Turns (Hard)"], loop["Average Speed"], loop["Estimated Completion Time"], loop["Current Status"]) 
                for idx, loop in loopData.iterrows()]
    '''
            
    scores = [costBenefit(loop["Cumulative Distance (Miles)"], loop["Major Turns"], loop["Number of stops"], 1, 
                            1, 1, loop["Average Speed"], loop["Estimated Completion Time"], loop["Current Status"]) 
                for idx, loop in loopData.iterrows()]

    scored["Benefit Cost Score"] = scores
    scored = scored.sort_values(by=["Benefit Cost Score"], ascending=False, kind="mergesort").reset_index(drop=True)
    scored.to_csv(r"data\CombinedConvertedScored.csv")
    return scored
