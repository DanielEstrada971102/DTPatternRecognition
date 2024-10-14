import math

class pyshower(object):
    "shower object building in python with digi information by SL"
    def __init__(self, wh, sc, st, info_df):
        self.wh = wh
        self.sc = sc
        self.st = st
        self.BX = None
        self.nDigis = len(info_df)
        self.avg_pos = info_df["w"].mean()
        self.avg_time = info_df["time"].mean()
        self.eq2Emulator = False
        return
