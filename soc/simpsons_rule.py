import time
import numpy as np
from scipy import integrate


# Use np.array for better performance with scipy
nparray_x = np.array([], dtype="f")
nparray_y = np.array([], dtype="f")
result = 0


# https://en.wikipedia.org/wiki/Simpson%27s_rule
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.simpson.html
def simpsons_rule(x, y):
    global nparray_x, nparray_y, result
    nparray_x = np.append(nparray_x, x)
    nparray_y = np.append(nparray_y, y)
    result = integrate.simpson(nparray_y, nparray_x)
    return result


if __name__ == "__main__":
    # This code is for performance testing and making sure code is correct
    arr_len = 1000
    sin_x = np.linspace(0, np.pi / 2, arr_len)
    sin_y = np.sin(np.linspace(0, np.pi / 2, arr_len))

    start = time.time()
    for i in range(arr_len):
        simpsons_rule(sin_x[i], sin_y[i])

    # Compute time (Forcing it to stress test with n function calls)
    print("Time", time.time() - start)
    # Result should be around 1 (Integrated sin from 0 to pi/2)
    print("Result", result)
