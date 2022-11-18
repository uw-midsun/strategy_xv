import pytest
import pandas as pd
from ..convertData import convertData, numOfTurns, numOfStops, totalTimeAndSpeed

def test_loops():
    column = ["Cumulative Distance(Miles)", "Major Turns", "Number of stops", "Level 1 Turns (Easy)", "Level 2 Turns (Medium)"
            "Level 2 turns (Medium)", "Level 3 Turns (Hard)", "Average Speed", "Estimated Completion Time", "Current Status"]
    
    loopOne = [21.9, 10, 3, 'N/A', 'N/A', 'N/A', 45.76204315565586, 0.4785625485625485, 'N/A']
    loopTwo = [40.7, 8, 2, 'N/A', 'N/A', 'N/A', 56.830527323240716, 0.7161643911643915, 'N/A']
    loopThree = [16.4, 5, 4, 'N/A', 'N/A', 'N/A', 52.44186046511628, 0.3127272727272727, 'N/A']
    combined = [79.0, 23, 9, 'N/A', 'N/A', 'N/A', 52.36763616791372, 1.5085653235653254, 'N/A']


    pd.testing.assert_frame_equal(convertData(r".\data\SegmentBLoop.csv"), pd.DataFrame([loopOne], columns=column))
    pd.testing.assert_frame_equal(convertData(r".\data\SegmentDLoop.csv"), pd.DataFrame([loopTwo], columns=column))
    pd.testing.assert_frame_equal(convertData(r".\data\SegmentELoop.csv"), pd.DataFrame([loopThree], columns=column))
    pd.testing.assert_frame_equal(convertData(r".\data\CombinedTest.csv"), pd.DataFrame([combined], columns=column))

loopB = pd.read_csv(r".\data\SegmentBLoop.csv")
# Clean speed data 
loopB.at[0, "Int"] = 0
prev = 0
for speed in loopB['Spd']:
	if speed != "  ":
		prev = int(speed)

for i, row in loopB.iterrows():
	if row["Spd"] == "  ":
		loopB.at[i, "Spd"] = prev
	elif int(row["Spd"]) > 65:
		loopB.at[i, "Spd"] = 65
		prev = 65
	else:
		prev = row["Spd"]

loopD = pd.read_csv(r".\data\SegmentDLoop.csv")
# Clean speed data 
loopD.at[0, "Int"] = 0
prev = 0
for speed in loopD['Spd']:
	if speed != "  ":
		prev = int(speed)

for i, row in loopD.iterrows():
	if row["Spd"] == "  ":
		loopD.at[i, "Spd"] = prev
	elif int(row["Spd"]) > 65:
		loopD.at[i, "Spd"] = 65
		prev = 65
	else:
		prev = row["Spd"]

loopE = pd.read_csv(r".\data\SegmentELoop.csv")
# Clean speed data 
loopE.at[0, "Int"] = 0
prev = 0
for speed in loopE['Spd']:
	if speed != "  ":
		prev = int(speed)

for i, row in loopE.iterrows():
	if row["Spd"] == "  ":
		loopE.at[i, "Spd"] = prev
	elif int(row["Spd"]) > 65:
		loopE.at[i, "Spd"] = 65
		prev = 65
	else:
		prev = row["Spd"]


def testNumOfTurns():
	assert(numOfTurns(loopB) == 10)
	assert(numOfTurns(loopD) == 8)
	assert(numOfTurns(loopE) == 5)

def testNumOfStops():
	assert(numOfStops(loopB) == 3)
	assert(numOfStops(loopD) == 2)
	assert(numOfStops(loopE) == 4)

def testTotalTimeAndSpeed():
	assert(totalTimeAndSpeed(loopB, 21.9) == (0.4785625485625485, 45.76204315565586))
	assert(totalTimeAndSpeed(loopD, 40.7) == (0.7161643911643915, 56.830527323240716))
	assert(totalTimeAndSpeed(loopE, 16.4) == (0.3127272727272727, 52.44186046511628))