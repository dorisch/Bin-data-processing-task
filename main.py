from data_processing import BinFileReader, DataRecord, DataToCsv
import sys

file = BinFileReader(sys.argv[1])
data = file.read_data()
nf = DataToCsv(data)
nf.write_to_csv()
