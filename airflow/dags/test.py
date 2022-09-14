import sys
from data_extraction.caselaw.cellar import cellar_extraction

# sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
print(sys.path)
cellar_extraction.cellar_extract(['local','--amount','50'])