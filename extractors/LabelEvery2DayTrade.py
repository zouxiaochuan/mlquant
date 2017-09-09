from BaseLabelEveryNDayTrade import BaseLabelEveryNDayTrade;

class LabelEvery2DayTrade(BaseLabelEveryNDayTrade):
    def __init__(self):
        super(LabelEvery2DayTrade, self).__init__(nday=2,sell_price='openPrice');
        pass;
    pass;
