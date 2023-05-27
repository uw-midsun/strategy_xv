from convertData import convertMultipleData, scoreRankLoops

file_list = [r"data\SegmentBLoop.csv", r"data\SegmentDLoop.csv", r"data\SegmentELoop.csv", r"data\CombinedTest.csv"]
combined = convertMultipleData(file_list)
scored = scoreRankLoops(combined)

print(combined)
print(scored)