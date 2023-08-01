

class FactorManager(object):
    def __init__(self):
        self._factors = None
        pass


    def load_factors(self, strategies: list):
        self._factors = {f for s in strategies for f in s.depended_factors()}
        self._all_symbols = {f._symbol for f in self._factors}
        pass


    def get_symbols(self) -> set:
        return self._all_symbols


    def update_factor_values(self):
        pass

    def get_strategy_factor_values(self, strategy_index: int):
        
        pass
    pass
