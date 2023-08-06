from . import DataManager
import pandas as pd
import dataclasses
import datetime
from ..wrapper.mysql import RawDatabaseConnector, BasicDatabaseConnector, DerivedDatabaseConnector
from ..struct import AssetWeight, AssetPrice, FundScoreParam, FundScoreHelper
from .score import FundScoreManager
from .data_tables import FundDataTables
from ..view.raw_models import *
from ..view.basic_models import *
from ..view.derived_models import *

 

class FundDataManager(DataManager):

    def __init__(self, start_time=None, end_time=None, fund_score_param: FundScoreParam=None, score_manager: FundScoreManager=None):
        DataManager.__init__(self, 
            start_time or datetime.datetime(2005, 1, 1), 
            end_time or datetime.datetime.now()
        )
        self._fund_score_param = fund_score_param or FundScoreParam(tag_type=1, score_method=1, is_full=1)
        self.dts = FundDataTables()
        self._is_inited = False
        self._score_manager = score_manager or FundScoreManager()
        self.set_score_param(self._fund_score_param)
    
    @property
    def inited(self):
        return self._is_inited

    def init(self, index_list=None):
        index_list = index_list or list(AssetWeight.__dataclass_fields__.keys())
        
        def fetch_table(view):
            query = quant_session.query(view)
            return pd.read_sql(query.statement, query.session.bind)

        # info is necessary
        with BasicDatabaseConnector().managed_session() as quant_session:
            self.dts.fund_info = fetch_table(FundInfo)
            _filter_fund_info = self.dts.fund_info[self.dts.fund_info.index_id.isin(index_list)]
            self.dts.fund_list = set(_filter_fund_info.fund_id)
            self.dts.fund_index_map = {cur.fund_id: cur.index_id for idx, cur in _filter_fund_info.iterrows()}
            self.dts.trading_days = fetch_table(TradingDayList)
            # index
            self.dts.index_info = fetch_table(IndexInfo)
            _index_query = quant_session.query(IndexPrice.index_id, IndexPrice.datetime, IndexPrice.close).filter(IndexPrice.index_id.in_(index_list))
            self.dts.index_price = pd.read_sql(_index_query.statement, _index_query.session.bind).pivot_table(index='datetime', columns='index_id', values='close').fillna(method= 'ffill')
            # fund nav
            _fund_nav_query = quant_session.query(
                    FundNav.fund_id,
                    FundNav.adjusted_net_value,
                    FundNav.subscribe_status, 
                    FundNav.redeem_status, 
                    FundNav.datetime
                ).filter(
                    FundNav.fund_id.in_(self.dts.fund_list),
                    FundNav.datetime >= self.start_date,
                    FundNav.datetime <= self.end_date,
                )
            self.dts.fund_nav = pd.read_sql(_fund_nav_query.statement, _fund_nav_query.session.bind).pivot_table(index='datetime', columns='fund_id', values='adjusted_net_value').fillna(method='ffill')
            
        # get derived data first
        with DerivedDatabaseConnector().managed_session() as derived_session:
            # fund indicator
            _fund_indicator_query = derived_session.query(
                    FundIndicator.fund_id,
                    FundIndicator.datetime,
                    FundIndicator.alpha,
                    FundIndicator.beta,
                    FundIndicator.fee_rate,
                    FundIndicator.track_err,
                ).filter(
                    FundIndicator.fund_id.in_(self.dts.fund_list),
                )
            self.dts.fund_indicator = pd.read_sql(_fund_indicator_query.statement, _fund_indicator_query.session.bind)
            self.dts.fund_indicator['index_id'] = self.dts.fund_indicator.fund_id.apply(lambda x: self.dts.fund_index_map[x])
        
        # raw index val pct, only used in tactic asset allocation
        with RawDatabaseConnector().managed_session() as quant_session:
            query = quant_session.query(IndexValPct)
            df = pd.read_sql(query.statement, query.session.bind).pivot_table(index='datetime', columns='index_id', values='pe_pct').fillna(method='ffill')
            self.dts.index_pct = df.rename(columns=FundScoreHelper.TACTIC_ASSET_CONVERT)

        self.dts.fix_data()

        self._is_inited = True
        self._score_manager.set_dts(self.dts)
        print(self.dts)

    def set_score_param(self, score_param: FundScoreParam):
        self._score_manager.set_param(score_param)

    def get_index_pcts(self, dt):
        # jch: only pct within 7 days take effect
        INDEX_PCT_EFFECTIVE_DELAY_DAY_NUM = 7
        res = {}
        for index_id in self.dts.index_pct.columns:
            df = self.dts.index_pct[index_id]
            _filtered = df[(df.index <= dt) & (df.index >= dt - datetime.timedelta(days=INDEX_PCT_EFFECTIVE_DELAY_DAY_NUM))]
            if len(_filtered) > 0:
                res[index_id] = _filtered.iloc[-1]
        return res

    def get_fund_score(self, dt, index_id) -> dict: 
        return self._score_manager.get_fund_score(dt, index_id)

    def get_fund_nav(self, dt):
        df = self.dts.fund_nav
        return df.loc[dt].to_dict()

    def get_fund_info(self, fund_id=None):
        '''
        fund_id                                                   000001!0
        wind_id                                                  000001.OF
        transition                                                       0
        order_book_id                                               000001
        desc_name                                                     华夏成长
        start_date                                              2001-12-18
        end_date                                                2040-12-31
        wind_class_1                                                 混合型基金
        wind_class_2                                               偏股混合型基金
        manager_id       王亚伟(20011218-20050412)\r\n田擎(20040227-20051029...
        company_id                                                    华夏基金
        benchmark                                                        0
        full_name                                               华夏成长证券投资基金
        currency                                                       CNY
        base_fund_id                                                     0
        is_structured                                                    0
        is_open                                                          0
        asset_type                                                    null
        update_time                                             2020-03-24
        manage_fee                                                     1.5
        trustee_fee                                                   0.25
        purchase_fee                                                   NaN
        redeem_fee                                                     NaN
        note                                                          None
        track_index                                                   none
        '''
        if fund_id:
            df = self.dts.fund_info
            _filtered = df[df['fund_id']=='000001!0']
            return None if len(_filtered) == 0 else _filtered.iloc[0]
        else:
            return self.dts.fund_info.copy()

    def get_trading_days(self):
        return self.dts.trading_days.copy()

    def get_index_price(self, dt=None):
        if dt:
            return self.dts.index_price.loc[dt]
        else:
            return self.dts.index_price.copy()
    
    def get_index_price_data(self, dt):
        _index_price = self.get_index_price(dt)
        return AssetPrice(**_index_price.to_dict())

def profile(file_name='/tmp/test.txt'):
    import cProfile, pstats, io
    from pstats import SortKey
    pr = cProfile.Profile()
    pr.enable()
    m = FundDataManager('20190101', '20200101', score_manager=FundScoreManager())
    m.init()
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    open(file_name, 'w').write(s.getvalue())


def test():
    #m = FundDataManager('20190101', '20200101', score_manager=FundScoreManager())
    m = FundDataManager('20190101', '20200101')
    m.init()
    print(m.get_fund_info(fund_id=None))
    print(m.get_fund_info(fund_id='000001!0'))
    print(m.get_trading_days())
    print(m.get_fund_score(datetime.date(2019,1,3), 'hs300'))

if __name__ == '__main__':
    profile()