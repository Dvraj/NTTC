
import scipy.io as sci
import numpy as np
import math

N_FRAMES = 100
N_LDPC = 16200
N_CELLS = 2700
N_SUBSTREAMS = 12
N_MOD = 6

all_data = sci.loadmat("demux_64_16200_allCR.mat")
input_data = np.array(all_data['v'])[0][0]
k = np.array (input_data[0])


print(k)
print(len(k))
a=0
output_data_check = np.array(all_data['y'])[0][0]
print("hello world")

rateRest = {
		0: 11, 1: 7, 2: 3, 3: 10, 4: 6, 5: 2, 6: 9, 7: 5, 
		8: 1, 9: 8, 10: 4, 11: 0					
	}

#output_data = np.zeros((N_FRAMES, N_CELLS, N_SUBSTREAMS))
output_data = np.zeros((int(N_LDPC/N_SUBSTREAMS), N_SUBSTREAMS, N_FRAMES), dtype = np.uint8)
for frameIndex in range(N_FRAMES):
			for bitIndex in range(N_LDPC):
				nStream = rateRest[bitIndex%N_SUBSTREAMS]
				mBitIndex = int(math.floor(bitIndex/N_SUBSTREAMS))
				bit = input_data[bitIndex][frameIndex]
				output_data[mBitIndex][nStream][frameIndex] = bit
output_data = np.reshape(output_data, (int(N_LDPC/N_MOD), N_MOD, N_FRAMES))
match = np.all(output_data_check == output_data)
print(f"Match: {match}")
print("koniec")