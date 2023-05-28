# Benefit Cost Score
## Criteria
Given the information in the routebook (as an excel file), create a new excel file that includes:
* Cumulative Distance(Miles)
* Major turns
* Number of stops
* Level 1 Turns (Easy)
* Level 2 turns (Medium)
* Level 3 Turns (Hard)
* Average Speed
* Estimated Completion Time
* Current Status

## How to get the data as an excel file
1. Open the Routebook PDF as a Word document
2. Copy the desired loop into an excel sheet

*Copying from PDF to Excel does not work*

## What could not be done with just the excel file
1. Determining the level of the turns is not possibel with just the excel file
    * This is a metric that the team came up with and is not measured in the routebook **This is possible; the turning angle is calculated in `get_coordinates`**
2. Current status - how far off we are from the leader
    * This depends on conditions during the race which is not possible to calculate just with the excel file **Theortically possible if we know the approx coordinate of leader and if the route path never overlaps on itself**