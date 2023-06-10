import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from simpsons_rule import simpsons_rule

# time is x, current is y

here = Path(__file__).parent
pathlist = (here / "data").glob("**/*.csv")

results = []

for path in pathlist:
    path_in_str = str(path)
    df = pd.read_csv(path_in_str)

    # Account for time offset
    time_offset = df["Data_Timestamp"].iloc[0]
    df["Data_Timestamp"] = df["Data_Timestamp"] - time_offset
    current = df["Current"].to_numpy()
    time = df["Data_Timestamp"].to_numpy()

    plt.plot(time, current)
    plt.savefig(f"data/{path.name}.png")
    plt.close()

    res = simpsons_rule(x=time, y=current)
    print(path.name, res)
