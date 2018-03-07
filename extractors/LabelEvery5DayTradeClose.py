from BaseLabelEveryNDayTrade import BaseLabelEveryNDayTrade;

class LabelEvery5DayTradeClose(BaseLabelEveryNDayTrade):
    def __init__(self):
        super(LabelEvery5DayTradeClose, self).__init__(nday=5,buy_price='closePrice',sell_price='closePrice');
        pass;
    pass;
