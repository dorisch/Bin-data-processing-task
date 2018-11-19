from struct import unpack, calcsize
import csv
import datetime

class DataRecord:

    def __init__(self, time, pos_1, pos_2, pos_3, att_1, att_2, att_3, att_4):
        self.time = time
        self.pos_1 = pos_1
        self.pos_2 = pos_2
        self.pos_3 = pos_3
        self.att_1 = att_1
        self.att_2 = att_2
        self.att_3 = att_3
        self.att_4 = att_4


class TimeConverter:
    def __init__(self, time):
        self.time = time

    def conversion (self):
        dif = 943920000  ##the elapsed time from 1978 to 2000 in sec
        t = datetime.datetime.utcfromtimestamp(self.time + dif).strftime("%A, %B %d, %Y %I:%M:%S")
        
        return t


class BinFileReader:
    data = []
    
    def __init__(self, filename):
        self.filename = filename
        
    def read_data (self):
        struct_fmt = '>64xL43x3l82x4l1847x'
        size = calcsize(struct_fmt)

        with open(self.filename, "rb") as f:
            i = 0
            reader = f.read()
            while i < 7510976:
                t = (unpack('>L', reader[(65+i):(69+i)]))[0]
                p = unpack('>3l', reader[(112+i):(124+i)])
                a = unpack('>4l', reader[(206+i):(222+i)])
                
                self.data.append(DataRecord(t*0.2, p[0]*0.0002, p[1]*0.0002, p[2]*0.0002, a[0]*0.0000000005, a[1]*0.0000000005, a[2]*0.0000000005, a[3]*0.0000000005))
                i = i + size

        return self.data


class DataToCsv:
    def __init__(self, data):
        self.data = data

    def write_to_csv(self):
        with open("data.csv", 'w') as csvfile:
            new_file = csv.writer(csvfile, lineterminator = '\n')
            list = []
            new_file.writerow(["time [s]", "date and time" , "Pos_ECI_1 [km]" , "Pos_ECI_2 [km]" , "Pos_ECI_3 [km]" , "Att_ECI_1", "Att_ECI_2", "Att_ECI_3", "Att_ECI_4"])
            for row in self.data:
                list.append(row.time)
                list.append(TimeConverter(row.time).conversion())
                list.append(row.pos_1)
                list.append(row.pos_2)
                list.append(row.pos_3)
                list.append(row.att_1)
                list.append(row.att_2)
                list.append(row.att_3)
                list.append(row.att_4)
                new_file.writerow(list)
                list = []

        return new_file
            
        
            
            

