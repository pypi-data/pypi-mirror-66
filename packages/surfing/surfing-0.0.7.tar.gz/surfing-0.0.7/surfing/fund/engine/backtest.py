import datetime
import copy
import json
import numpy as np
import pandas as pd
import os

from .asset_helper import SAAHelper, TAAHelper
from .trader import AssetTrader, FundTrader
from .report import ReportHelper
from ...data.manager.manager_fund import FundDataManager
from ...data.struct import AssetWeight, AssetPrice, AssetPosition, AssetValue
from ...data.struct import FundPosition, TAAParam, AssetTradeParam, FundTradeParam


class FundBacktestEngine:

    DEFAULT_CASH_VALUE = 1e8

    def __init__(self, data_manager: FundDataManager, trader, taa_params:TAAParam=None):
        self._dm = data_manager
        self._saa_helper = SAAHelper() # 战略目标
        self._taa_helper = TAAHelper(taa_params=taa_params) if taa_params else None
        self._report_helper = ReportHelper()
        self._trader = trader

    @property
    def is_fund_backtest(self):
        return isinstance(self._trader, FundTrader)

    def init(self):
        if not self._dm.inited:
            self._dm.init()
        self._saa_helper.init()
        if self._taa_helper:
            self._taa_helper.init()
        self._report_helper.init()
        self._trader.init()

    def run(self, saa: AssetWeight, start_date: datetime.date=None, end_date: datetime.date=None, cash: float=None):
        cash = cash or self.DEFAULT_CASH_VALUE
        # init position
        self.cur_asset_position = AssetPosition(cash=cash)
        self.cur_fund_position = FundPosition(cash=cash)
        cur_asset_mv = AssetValue(prices=AssetPrice(cash=1), positions=self.cur_asset_position)
        #print(cur_asset_mv)
        self._pending_trades = []

        # init days
        start_date = start_date or self._dm.start_date
        end_date = end_date or self._dm.end_date

        # setup helpers
        self._saa_helper.setup(saa)
        if self._taa_helper:
            self._taa_helper.setup(saa)
        self._report_helper.setup(saa)
        self._trader.setup(saa)

        # loop trading days
        _dts = self._dm.get_trading_days()
        dts = _dts[(_dts.datetime >= start_date) & (_dts.datetime <= end_date)].datetime # df with datetime.date
        for t in dts:
            self._run_on(t)
        # init report data
        self._report_helper.plot_init(self._dm)

    def _run_on(self, dt):
        # current asset price
        cur_asset_price = self._dm.get_index_price_data(dt)
        if self.is_fund_backtest:
            # prep fund data
            fund_nav = self._dm.get_fund_nav(dt)
            fund_score = {index_id: self._dm.get_fund_score(dt, index_id) for index_id in self.cur_asset_position.__dict__.keys()}
            # finalize trades
            self._pending_trades, traded_list = self._trader.finalize_trade(dt, self._pending_trades, cur_asset_price, self.cur_asset_position, self.cur_fund_position, fund_nav)
            target_asset_allocation = self.calc_asset_allocation(dt, cur_asset_price)
            virtual_position, trade_list = self._trader.calc_fund_trade(dt, self.cur_asset_position, cur_asset_price, target_asset_allocation, self.cur_fund_position, fund_nav, fund_score)
            self.book_trades(trade_list)
            self._report_helper.update(dt, self.cur_asset_position.copy(), cur_asset_price, self._pending_trades, self.cur_fund_position.copy(), fund_nav, traded_list, fund_score)
        else:
            # finalize trades
            self._pending_trades, traded_list = self._trader.finalize_trade(dt, self._pending_trades, cur_asset_price, self.cur_asset_position)
            target_asset_allocation = self.calc_asset_allocation(dt, cur_asset_price)
            virtual_position, trade_list = self._trader.calc_asset_trade(dt, self.cur_asset_position, cur_asset_price, target_asset_allocation)
            self.book_trades(trade_list)
            self._report_helper.update(dt, self.cur_asset_position.copy(), cur_asset_price, self._pending_trades, self.cur_fund_position.copy(), {}, traded_list, {})

    def calc_asset_allocation(self, dt, cur_asset_price: AssetPrice):
        cur_saa = self._saa_helper.on_price(dt, cur_asset_price)
        if self._taa_helper:
            asset_pct = self._dm.get_index_pcts(dt)
            cur_taa = self._taa_helper.on_price(dt, cur_asset_price, cur_saa, asset_pct)
        else:
            cur_taa = cur_saa
        return cur_taa

    def book_trades(self, trade_list: list):
        if trade_list and len(trade_list) > 0:
            self._pending_trades += trade_list

    def get_asset_result(self):
        return self._report_helper.get_asset_stat()

    def get_fund_result(self):
        return self._report_helper.get_fund_stat()

    def get_asset_trade(self):
        return self._report_helper.get_asset_trade()

    def get_fund_trade(self):
        return self._report_helper.get_fund_trade()
        
    def plot(self, is_asset:bool=True, is_fund:bool=True, is_choose:bool=False):
        if not is_choose:
            if is_asset:
                self._report_helper.backtest_asset_plot()
            if is_fund:
                self._report_helper.backtest_fund_plot()
        else:
            pass
    
    def plot_score(self, index_id):
        #['csi500', 'gem', 'gold', 'hs300', 'national_debt', 'sp500rmb']
        self._report_helper._plot_fund_score(index_id)

def saa_backtest(m: FundDataManager, saa: AssetWeight):
    asset_param = AssetTradeParam() # type in here
    t = AssetTrader(asset_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=None)
    b.init()
    b.run(saa=saa)

def taa_backtest(m: FundDataManager, saa: AssetWeight):
    taa_param = TAAParam()  # type in here
    asset_param = AssetTradeParam() # type in here
    t = AssetTrader(asset_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=taa_param)
    b.init()
    b.run(saa=saa)

def fund_backtest_without_taa(m: FundDataManager, saa: AssetWeight):
    asset_param = AssetTradeParam() # type in here
    fund_param = FundTradeParam() # type in here
    t = FundTrader(asset_param, fund_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=None)
    b.init()
    b.run(saa=saa)

def fund_backtest(m: FundDataManager, saa: AssetWeight):
    taa_param = TAAParam()  # type in here
    asset_param = AssetTradeParam() # type in here
    fund_param = FundTradeParam() # type in here
    t = FundTrader(asset_param, fund_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=taa_param)
    b.init()
    b.run(saa=saa)


def profile(file_name='/tmp/test.txt', func=fund_backtest):
    import cProfile, pstats, io
    from pstats import SortKey
    print('---start---')
    from ...data.manager.score import FundScoreManager
    m = FundDataManager('20150101', '20160101', score_manager=FundScoreManager())
    m.init()

    saa = AssetWeight(
        hs300=15/100,
        csi500=5/100,
        gem=3/100,
        sp500rmb=7/100,
        national_debt=60/100,
        gold=10/100,
        cash=5/100
    )
    print('---inited---')
    
    pr = cProfile.Profile()
    pr.enable()
    
    func(m, saa)
    
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    open(file_name, 'w').write(s.getvalue())

def test():
    from ...data.manager.score import FundScoreManager
    m = FundDataManager('20150101', '20160101', score_manager=FundScoreManager())
    m.init()

    saa = AssetWeight(
        hs300=15/100,
        csi500=5/100,
        gem=3/100,
        sp500rmb=7/100,
        national_debt=60/100,
        gold=10/100,
        cash=5/100
    )
    
    #saa_backtest(m, saa)
    #taa_backtest(m, saa)
    #fund_backtest_without_taa(m, saa)
    fund_backtest(m, saa)



if __name__ == '__main__':
    profile(file_name='/Users/cjiang/taa_perf1.txt', func=fund_backtest)