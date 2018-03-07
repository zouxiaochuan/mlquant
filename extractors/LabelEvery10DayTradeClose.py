from BaseLabelEveryNDayTrade import BaseLabelEveryNDayTrade;

class LabelEvery10DayTradeClose(BaseLabelEveryNDayTrade):
    def __init__(self):
        super(LabelEvery10DayTradeClose, self).__init__(nday=10,buy_price='closePrice',sell_price='closePrice');
        pass;
    pass;
