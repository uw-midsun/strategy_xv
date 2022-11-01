import pytest
import pandas as pd
from ..convertData import convertData

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
