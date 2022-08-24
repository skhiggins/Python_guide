import datetime

def time_stamp():
    ct = str(datetime.datetime.now())
    datestamp = ct[:10].replace('-','')
    timestamp = ct[11:19].replace(':','')
    return datestamp + '_' + timestamp