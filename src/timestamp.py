import math
from datetime import datetime

def getTimestamp():
    ts = datetime.timestamp(datetime.now())
    return math.floor(ts * 1000)
