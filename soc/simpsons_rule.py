import time
import numpy as np
from scipy import integrate


# https://en.wikipedia.org/wiki/Simpson%27s_rule
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.simpson.html
def simpsons_rule(x, y):
    if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
        x = np.array(x, dtype="f")
        y = np.array(y, dtype="f")
    result = integrate.simpson(y=y, x=x)
    return result


if __name__ == "__main__":
    # This code is for performance testing and making sure code is correct
    arr_len = 500
    sin_x = np.linspace(0, 2 * np.pi, arr_len)
    sin_y = np.sin(np.linspace(0, 2 * np.pi, arr_len))

    start = time.time()
    for i in range(1, arr_len):
        res = simpsons_rule(sin_x[:i], sin_y[:i])
        print(f"Sin(x), [0, {sin_x[i]}] = {res}")

    # Compute time (Forcing it to stress test with n function calls)
    print("Time", time.time() - start)
    # Result should be around 1 (Integrated sin from 0 to pi/2)
    print("Result", res)
