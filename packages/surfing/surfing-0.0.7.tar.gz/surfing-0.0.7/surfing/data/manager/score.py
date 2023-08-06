from ..struct import FundScoreParam
from .data_tables import FundDataTables
import dataclasses

@dataclasses.dataclass
class ScoreFunc:

    alpha: float=0 # weight of alpha
    beta: float=0  # weight of abs(1-beta), or beta's deviation from 1
    track_err: float=0 # weight of track_err
    fee_rate: float=0 # weight of fee_rate
    ir: float=0 # weight of ir

    def get(self, data):
        return self.alpha * data.alpha + self.beta * abs(1-data.beta) + self.track_err * data.track_err + self.fee_rate * data.fee_rate + self.ir * data.ir


class FundScoreManager:

    def __init__(self):
        self.params = None
        self.dts = None
        self.funcs = {
            'hs300': ScoreFunc(alpha=0.3, beta=-0.1, fee_rate=-0.1, ir=0.5),
            'csi500': ScoreFunc(alpha=0.3, beta=-0.1, fee_rate=-0.1, ir=0.5),
            'gem': ScoreFunc(alpha=0.3, beta=-0.1, fee_rate=-0.1, ir=0.5),

            'national_debt': ScoreFunc(alpha=0.2, fee_rate=-0.2, track_err=-0.6),
            'credit_debt': ScoreFunc(alpha=0.2, fee_rate=-0.2, track_err=-0.8),

            'sp500rmb': ScoreFunc(fee_rate=-0.2, track_err=-0.8),
            'dax30rmb': ScoreFunc(fee_rate=-0.2, track_err=-0.8),
            'n225rmb': ScoreFunc(fee_rate=-0.2, track_err=-0.8),

            'gold': ScoreFunc(alpha=0.2, fee_rate=-0.2, track_err=-0.8),
            'oil': ScoreFunc(alpha=0.2, fee_rate=-0.2, track_err=-0.8),
            'real_state': ScoreFunc(alpha=0.2, fee_rate=-0.2, track_err=-0.8),
        }

    def set_param(self, score_param: FundScoreParam):
        self.params = score_param

    def set_dts(self, dts: FundDataTables):
        self.dts = dts

    def get_fund_score(self, dt, index_id) -> dict:
        func = self.funcs.get(index_id)
        assert self.params and self.dts, 'cannot provide fund_score without params or data tables'
        try:
            cur_d = self.dts.index_fund_indicator_pack.loc[dt, index_id]
        except:
            return {}
        if len(cur_d) == 0:
            return {}
        elif len(cur_d) == 1:
            return {cur_d.index[0]: 1}
        else:
            assert func, f'score function does not implemented {index_id}'
            cur_d['ir'] = cur_d['alpha'] / cur_d['track_err']
            cur_d_sta = cur_d.apply(lambda x: (x - x.mean() + 1e-6)/ (x.std() + 1e-6), axis=0)
            cur_d_sta['beta'] = cur_d['beta']
            score_raw = cur_d_sta.apply(lambda x: func.get(x), axis=1)
            score = (score_raw - score_raw.min()) / (score_raw.max() - score_raw.min())
            return { fund_id: s for fund_id, s in score.iteritems() }
    