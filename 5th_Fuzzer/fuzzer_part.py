# -*- coding: utf-8 -*-

import random
import math
import os, sys
import threading
import glob
import time
#import utils
import shutil
from datetime import datetime
import gc
import subprocess
# for email
import smtplib
import signal


FUZZ_DELAY = 6
USE_WINDBG = False 
EXPLOITABLE_FRE = 6

class File_Fuzzer:
    def __init__(self,target ,ext):
    
        self.base_path = os.getcwd() + "/"
        self.target =target
        self.target_path = self.base_path + os.path.basename(target) + "/"
        self.sample_path = self.base_path + "samples/"
        self.test_path = self.target_path + "test/"
        self.crash_path = self.target_path +  "crash/"
        self.exploitable_path = self.target_path + "crash/exploitable/"
        self.sample_ext = ext
        self.sample_stream = None
        self.case_name = None
        self.crash_fname = ''
        self.iter = 0
        self.running = False
        self.crash_count = 0
        self.dbg = None
        self.mutate_method = ""
        self.mutate_byte = ""
        self.mutate_offset = 0
        self.mutate_len = 0
        self.orig_bytes = ""
        self.exploitable_count = 0
        self.exploitable_hashset = []
        self.title_exploitable_count = 0
        self.title_probably_exploitable_count = 0

        
        if not os.path.exists(self.target_path):
            os.mkdir(self.target_path)
        if not os.path.exists(self.sample_path):
            os.mkdir(self.sample_path)
        if not os.path.exists(self.test_path):
            os.mkdir(self.test_path)
        if not os.path.exists(self.crash_path):
            os.mkdir(self.crash_path)
        if not os.path.exists(self.exploitable_path):
            os.mkdir(self.exploitable_path)
            
    def File_Picker(self):
        sample_list = glob.glob(self.sample_path + self.sample_ext + '/*')
        if len(sample_list) < 1:
            print (" [-] 샘플이 존재하지 않습니다. sample 폴더를 확인해 주세요.")
        while 1:
            sample = random.choice(sample_list)
            self.sample_stream = open(sample,"rb").read()
            print(self.sample_stream[0:10])
            if len(self.sample_stream) > 1:
                break
        return

      # case 0 : 값을 랜덤하게 변경한다.
      # case 1 : 값을 랜덤하게 삽입한다.

    def Mutate(self):
        global mutated_stream 
        global mutate_byte
        test_cases = [ "\x00", "\xff", "\x41", "%%s"]
        #case = random.randint(0, 1)
        case = 1
      #mutate_count = int(random.randint(1, len(self.sample_stream)) * 0.005)+1 # 전체 변경 바이트 수
        mutate_count = random.randint(1,2)
      #test_cases.append(str(random.randint(0,255)))
        mutate_byte = random.choice(test_cases)
        self.mutate_byte = mutate_byte
        if case == 0:   # replace
            print (" [+] Case 1. Byte Replace  ")
            self.mutate_case = 0
            for i in range(mutate_count):
                mutate_offset = random.randint(1, len(self.sample_stream)) # 변경 offset 
                mutate_len = random.randint(1,4)   # 변경 바이트 길이
                mutated_stream = self.sample_stream[0:mutate_offset]
                
                temp = []
                for i in range (mutate_len):
                    temp.append(self.mutate_byte)
                print(temp)
                temp = "".join(temp)
                print(temp)
                ms = bytearray(mutated_stream)
                ms += temp.encode()
                print(ms[-10:])
                ms += self.sample_stream[mutate_offset + mutate_len:]
                print(ms[-10:])

            print (" [+] Mutated %d counts(replace %d bytes)" % (mutate_count, mutate_len))

        else:         # add
            print (" [+] Case 2. Byte Insertion ")
            self.mutate_case = 1
            mutate_offset = random.randint(1, len(self.sample_stream)) # 변경 offset 
            mutate_len = random.randint(1,30000)   # 변경 바이트 길이
            mutated_stream = self.sample_stream[0:mutate_offset]
            
            #print (mutated_stream)
            #mutated_stream += mutate_byte * mutate_len
            temp = []
            for i in range (mutate_len):
                temp.append(self.mutate_byte)
            print(temp)
            temp = "".join(temp)
            print(temp)
            ms = bytearray(mutated_stream)
            ms += temp.encode()
            print(ms[-10:])
            ms += self.sample_stream[mutate_offset:]
            print ("  [+] Mutated %d bytes(add)" % (mutate_len) )

        self.mutate_offset = mutate_offset
        self.case_name = self.test_path + "case-%s.%s" % (str(self.iter),self.sample_ext)
        f = open(self.case_name ,"wb")
        f.write(bytes(ms))
        f.close()
        return 

    def Fuzzing(self, count):
        self.count = count
        print (self.count)
        self.File_Picker()
        self.Mutate()

if __name__ == '__main__':
    print ("Usage example : C:/Users/5ddish/Desktop/fuzzer/reader/reader.exe , zip")

    if len(sys.argv) !=3:
        print ("[SYSTEM] Error .... Please Chqeck Usage")
        sys.exit()

    print ("[SYSTEM] Fuzzer Start ")

    fuzzer = File_Fuzzer(sys.argv[1], sys.argv[2])
    fuzzer.Fuzzing(5000)