import pytest
import pandas as pd
from ..convertData import convertData, convertMultipleData, scoreRankLoops, numOfTurns, numOfStops, totalTimeAndSpeed, cleanSpeedData, costBenefit

def test_cost_benefit():
        assert(costBenefit(11, 8, 9, 5, 4, 3, 2, 1, 0) == 0.5546218487394958)


def test_loops():
    column = ["Loop Name", "Cumulative Distance (Miles)", "Major Turns", "Number of stops", "Level 1 Turns (Easy)", "Level 2 Turns (Medium)", 
                "Level 3 Turns (Hard)", "Average Speed", "Estimated Completion Time", "Current Status"]
    
    loopOne = ["benefitCostScore/data/SegmentBLoop.csv", 21.9, 10, 3, 'N/A', 'N/A', 'N/A', 45.76204315565586, 0.4785625485625485, 'N/A']
    loopTwo = ["benefitCostScore/data/SegmentDLoop.csv", 40.7, 8, 2, 'N/A', 'N/A', 'N/A', 56.830527323240716, 0.7161643911643915, 'N/A']
    loopThree = ["benefitCostScore/data/SegmentELoop.csv", 16.4, 5, 4, 'N/A', 'N/A', 'N/A', 52.44186046511628, 0.3127272727272727, 'N/A']
    combined = ["benefitCostScore/data/CombinedTest.csv", 79.0, 23, 9, 'N/A', 'N/A', 'N/A', 52.36763616791372, 1.5085653235653254, 'N/A']

    pd.testing.assert_frame_equal(convertData(r"benefitCostScore/data/SegmentBLoop.csv"), pd.DataFrame([loopOne], columns=column))
    pd.testing.assert_frame_equal(convertData(r"benefitCostScore/data/SegmentDLoop.csv"), pd.DataFrame([loopTwo], columns=column))
    pd.testing.assert_frame_equal(convertData(r"benefitCostScore/data/SegmentELoop.csv"), pd.DataFrame([loopThree], columns=column))
    pd.testing.assert_frame_equal(convertData(r"benefitCostScore/data/CombinedTest.csv"), pd.DataFrame([combined], columns=column))


def test_combined_ranked_loops():
    column = ["Loop Name", "Cumulative Distance (Miles)", "Major Turns", "Number of stops", "Level 1 Turns (Easy)", "Level 2 Turns (Medium)", 
                "Level 3 Turns (Hard)", "Average Speed", "Estimated Completion Time", "Current Status"]
    
    loopOne = ["benefitCostScore/data/SegmentBLoop.csv", 21.9, 10, 3, 'N/A', 'N/A', 'N/A', 45.76204315565586, 0.4785625485625485, 'N/A']
    loopOne = pd.DataFrame([loopOne], columns=column)
    loopTwo = ["benefitCostScore/data/SegmentDLoop.csv", 40.7, 8, 2, 'N/A', 'N/A', 'N/A', 56.830527323240716, 0.7161643911643915, 'N/A']
    loopTwo = pd.DataFrame([loopTwo], columns=column)
    loopThree = ["benefitCostScore/data/SegmentELoop.csv", 16.4, 5, 4, 'N/A', 'N/A', 'N/A', 52.44186046511628, 0.3127272727272727, 'N/A']
    loopThree = pd.DataFrame([loopThree], columns=column)
    combined = ["benefitCostScore/data/CombinedTest.csv", 79.0, 23, 9, 'N/A', 'N/A', 'N/A', 52.36763616791372, 1.5085653235653254, 'N/A']
    combined = pd.DataFrame([combined], columns=column)

    combinedDF = convertMultipleData(["benefitCostScore/data/SegmentBLoop.csv", "benefitCostScore/data/SegmentDLoop.csv", 
                                    "benefitCostScore/data/SegmentELoop.csv", "benefitCostScore/data/CombinedTest.csv"])
    pd.testing.assert_frame_equal(combinedDF, pd.concat([loopOne, loopTwo, loopThree, combined], ignore_index=True))
    
    ranked = scoreRankLoops(combinedDF)
    scores = [1.414860, 3.200651, 1.449695, 2.224815]
    combinedDF["Benefit Cost Score"] = scores
    combinedDF = combinedDF.sort_values(by=["Benefit Cost Score"], ascending=False, kind="mergesort").reset_index(drop=True)
    pd.testing.assert_frame_equal(ranked, combinedDF)


def test_stats():
    loopB = pd.read_csv(r"benefitCostScore/data/SegmentBLoop.csv")
    cleanSpeedData(loopB)

    loopD = pd.read_csv(r"benefitCostScore/data/SegmentDLoop.csv")
    cleanSpeedData(loopD)

    loopE = pd.read_csv(r"benefitCostScore/data/SegmentELoop.csv")
    cleanSpeedData(loopE)

    ## number of turns
    assert(numOfTurns(loopB) == 10)
    assert(numOfTurns(loopD) == 8)
    assert(numOfTurns(loopE) == 5)

    ## number of stops
    assert(numOfStops(loopB) == 3)
    assert(numOfStops(loopD) == 2)
    assert(numOfStops(loopE) == 4)

    ## total time and speed
    assert(totalTimeAndSpeed(loopB, 21.9) == (0.4785625485625485, 45.76204315565586))
    assert(totalTimeAndSpeed(loopD, 40.7) == (0.7161643911643915, 56.830527323240716))
    assert(totalTimeAndSpeed(loopE, 16.4) == (0.3127272727272727, 52.44186046511628))
