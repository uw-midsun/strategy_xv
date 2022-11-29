from convertData import convertData
import pandas as pd

loopOne = convertData(r"strategy_xv\benefitCostScore\data\SegmentBLoop.csv")
loopTwo = convertData(r"strategy_xv\benefitCostScore\data\SegmentDLoop.csv")
loopThree = convertData(r"strategy_xv\benefitCostScore\data\SegmentELoop.csv")
combined = convertData(r"strategy_xv\benefitCostScore\data\CombinedTest.csv")

print(loopOne)
print(loopTwo)
print(loopThree)
print(combined)