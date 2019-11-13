
import scipy.io as sci
import numpy as np
import math



class qam64_all:
    
    St_Rest = {
		    0: 11, 1: 7, 2: 3, 3: 10, 4: 6, 5: 2, 6: 9, 7: 5, 
		    8: 1, 9: 8, 10: 4, 11: 0					
	    }
    St_35 = {
		    0: 2, 1: 7, 2: 6, 3: 9, 4: 0, 5: 3, 6: 1, 7: 8, 
		    8: 4, 9: 11, 10: 5, 11: 10					
	    }
    St_23 = {
		    0: 11, 1: 7, 2: 3, 3: 10, 4: 6, 5: 2, 6: 9, 7: 5, 
		    8: 1, 9: 8, 10: 4, 11: 0					
	    }
    rates = {
		    "2/3": St_23,
		    "3/5": St_35,
		    "rest": St_Rest
	    }
    paths = {
		    "2/3": 'demux_64_64800_without35.mat',
		    "3/5": 'demux_64_64800_35.mat',
		    "rest": 'demux_64_16200_allCR.mat'
	    }
    N_FRAMES = 100
    N_MOD = 6        
    N_SUBSTREAMS = 12
    N_LDPC = 64800
    N_CELLS = N_LDPC/N_MOD
   
   

    def __init__(self, rate):
        if(rate == "rest"):
            self.N_LDPC = 16200
        else:
            self.N_LDPC = 64800
        self.N_CELLS = self.N_LDPC/self.N_MOD

        self.path = self.paths[rate]
        all_data = sci.loadmat(self.path)
        self.rate = self.rates[rate]
        self.inputData = np.array(all_data['v'])[0][0]
        self.output_data_check = np.array(all_data['y'])[0][0]
        self.output_data = np.zeros((int(self.N_LDPC/self.N_SUBSTREAMS), self.N_SUBSTREAMS, self.N_FRAMES), dtype = np.uint8)
    

    
    def demultiplex(self):
        for frameIndex in range(self.N_FRAMES):
            for bitIndex in range(self.N_LDPC):
                nStream = self.rate[bitIndex%self.N_SUBSTREAMS]
                mBitIndex = int(math.floor(bitIndex/self.N_SUBSTREAMS))
                bit = self.inputData[bitIndex][frameIndex]
                self.output_data[mBitIndex][nStream][frameIndex] = bit
        self.output_data = np.reshape(self.output_data, (int(self.N_LDPC/self.N_MOD), self.N_MOD, self.N_FRAMES))

    def checkResult(self):
        match = np.all(self.output_data_check == self.output_data)
        print(f"Match_{self.path}: {match}")

    def save(self):
        mat = {"y": self.output_data}
        sci.savemat(f"out_{self.path}", mat)


print("QAM64_16200_allCR")
qam_rest = qam64_all("rest")
qam_rest.demultiplex()
qam_rest.checkResult()
#qam_rest.save()
print("koniec_REST\n")
print("QAM64_64800_35")
qam_35 = qam64_all("3/5")
qam_35.demultiplex()
qam_35.checkResult()
#qam_35.save()
print("koniec_3/5")
print("QAM64_64800_without35")
qam_23 = qam64_all("2/3")
qam_23.demultiplex()
qam_23.checkResult()
#qam_23.save()
print("koniec_2/3\n")



    
    
    