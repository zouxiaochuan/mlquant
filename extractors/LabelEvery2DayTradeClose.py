from BaseLabelEveryNDayTrade import BaseLabelEveryNDayTrade;

class LabelEvery2DayTradeClose(BaseLabelEveryNDayTrade):
    def __init__(self):
        super(LabelEvery2DayTradeClose, self).__init__(nday=2,buy_price='closePrice',sell_price='closePrice');
        pass;
    pass;
