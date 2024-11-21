from numba import jit
import numpy as np
import time

@jit(nopython=True, cache=True)
def test_func_njit():
    size = 1000
    arr = np.random.rand(size)
    result = 0
    
    for _ in range(1000):
        result += np.sum(np.sin(arr) * np.cos(arr))
        result = np.sqrt(result)
    
    return result


if __name__ == "__main__":
    st = time.time()
    temp = test_func_njit()
    et = time.time()

    ans = et - st

    print(f"Comp time for njit: {ans} seconds")

