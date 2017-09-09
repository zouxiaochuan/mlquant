from BaseLabelEveryNDayTrade import BaseLabelEveryNDayTrade;

class LabelEvery1DayTradeOpen(BaseLabelEveryNDayTrade):
    def __init__(self):
        super(LabelEvery1DayTradeOpen, self).__init__(nday=1,sell_price='openPrice');
        pass;
    pass;
