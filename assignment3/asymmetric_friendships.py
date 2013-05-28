import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = tuple(sorted(record))
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: friendID
    # value: counter
    if len(list_of_values)==1:
    	pf = tuple(list_of_values[0])
    	fp = tuple(pf[::-1])
        mr.emit(pf)
        mr.emit(fp)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
