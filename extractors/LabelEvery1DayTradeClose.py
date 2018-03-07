from BaseLabelEveryNDayTrade import BaseLabelEveryNDayTrade;

class LabelEvery1DayTradeClose(BaseLabelEveryNDayTrade):
    def __init__(self):
        super(LabelEvery1DayTradeClose, self).__init__(nday=1,buy_price='closePrice',sell_price='closePrice');
        pass;
    pass;
