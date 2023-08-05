import numpy as np
import ta

print(ta.RSI(np.array(range(20), dtype=np.double)*2.1, 5))