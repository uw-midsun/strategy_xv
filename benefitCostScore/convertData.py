from email import header
import pandas as pd


def convertData(file):
    '''
    This function takes in a csv file in the format of route descriptions on the route book and
    creates a csv file with the following properties calculate:
        Cumulative Distance(Miles)
        Major turns
        Number of stops
        Level 1 Turns (Easy)
        Level 2 turns (Medium)
        Level 3 Turns (Hard)
        Average Speed
        Estimated Completion Time
        Current Status
    It will also return a pandas dataframe with the same information
    '''

    data = pd.read_csv(file)
    column = ["Cumulative Distance(Miles)", "Major Turns", "Number of stops", "Level 1 Turns (Easy)", "Level 2 Turns (Medium)"
            "Level 2 turns (Medium)", "Level 3 Turns (Hard)", "Average Speed", "Estimated Completion Time", "Current Status"]
    
    loopData = []

    data.at[0, "Int"] = 0

    # Clean speed data 
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


    # Total distance
    totalDistance = float(data["Trip"][len(data["Trip"])-1])
    loopData.append(totalDistance)

    # Major Turns
    turnCount = 0
    for instructions in data["Major Turns/Instructions"]:
        if "left" in instructions.lower() or "right" in instructions.lower() or "turn" in instructions.lower():
            turnCount += 1
    loopData.append(turnCount)

    # Number of Stops
    stopCount = 0
    for instructions in data["Major Turns/Instructions"]:
        if "stop" in instructions.lower() and "***" not in instructions.lower() and "stage stop" not in instructions.lower():
            stopCount += 1
    for notes in data["Landmarks/Notes"]:
        if "stop" in notes.lower() and "***" not in notes.lower() and "not" not in notes.lower():
            stopCount += 1
    loopData.append(stopCount)

    loopData.append("N/A")
    loopData.append("N/A")
    loopData.append("N/A")

    # Calculate time and speed
    totalTime = 0
    for index, row in data.iterrows():
        totalTime += float(row["Int"]) / float(row["Spd"])

    averageSpeed = totalDistance / totalTime
    loopData.append(averageSpeed)
    loopData.append(totalTime)
    loopData.append("N/A")

    print(loopData)
    df = pd.DataFrame([loopData], columns=column)
    df.to_csv(file.split(".")[0] + "Converted" + ".csv")
    return df