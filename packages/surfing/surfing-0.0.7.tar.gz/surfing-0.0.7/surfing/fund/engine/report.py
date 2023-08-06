import pandas as pd
import numpy as np
import datetime
import copy
from pprint import pprint 
import matplotlib as mpl
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
mpl.rcParams['font.family'] = ['Heiti TC']

from ...data.manager.manager_fund import FundDataManager
from ...data.struct import AssetWeight, AssetPosition, AssetPrice, AssetValue
from ...data.struct import FundPosition, FundPosItem, FundTrade
from ...data.manager.score import FundScoreManager

class ReportHelper:
    
    '''
    save backtest history
    '''
    TRADING_DAYS_PER_YEAR = 242

    def __init__(self):
        pass

    def init(self): 
        pass

    def plot_init(self, dm):
        self.index_price = dm.get_index_price()
        self.fund_info = dm.get_fund_info()
        self.fund_nav = dm.dts.fund_nav
        self.fund_indicator = dm.dts.fund_indicator
        
    def setup(self, saa:AssetWeight):
        self.saa_weight = saa.__dict__
        self.asset_cash_history = {}
        self.asset_position_history = {}
        self.asset_market_price_history = {}
        self.pending_trade_history = {}
        self.asset_weights_history = {}
        self.tactic_history = {}
        self.fund_position_history = {}
        self.trade_history = {}
        self.rebalance_date = []
        self.fund_cash_history = {}
        self.fund_marktet_price_history = {}
        self.fund_weights_history = {}
        self.fund_score = {}

    def update(self,dt:datetime, asset_cur_position:AssetPosition, asset_cur_price:AssetPrice, pend_trades:list, fund_cur_position:FundPosition, fund_nav:dict, traded_list:list, fund_score:dict):   
        # 检查回测时使用
        #self.asset_cash_history[dt] = asset_cur_position.cash##
        #self.asset_position_history[dt] = asset_cur_position.__dict__##
        #self.pending_trade_history[dt] = pend_trades##
        # dic = {f : f_info.__dict__  for f, f_info in fund_cur_position.funds.items()}
        # for f, f_info in dic.items():
        #     f_info['price'] =  fund_nav[f]
        # self.fund_position_history[dt] = dic##
        #self.fund_cash_history[dt] = fund_cur_position.cash##
        self.asset_market_price_history[dt] = AssetValue(prices=asset_cur_price, positions=asset_cur_position).sum() 
        self.asset_weights_history[dt] = AssetValue(prices=asset_cur_price, positions=asset_cur_position).get_weight()
        mv, w = fund_cur_position.calc_mv_n_w(fund_navs=fund_nav)
        self.fund_marktet_price_history[dt] = mv
        self.fund_weights_history[dt] = w
        if len(traded_list) > 0:
            self.trade_history[dt] = traded_list
        self.fund_score[dt] = fund_score
        
    def _calc_stat(self, df):
        year = df.shape[0]/self.TRADING_DAYS_PER_YEAR
        total_return = df['mv'][-1] / df['mv'][0]
        try:
            five_year_return = (df['mv'][-1] / df['mv'][-(5 * self.TRADING_DAYS_PER_YEAR)] - 1)
        except:
            five_year_return = five_year_return = (df['mv'][-1] / df['mv'][0] - 1)
        annualized_return = np.exp(np.log(total_return)/year) - 1
        annualized_volatiltity = (df['mv'].shift(1) / df['mv']).std() * np.sqrt((df.shape[0] - 1) / year)
        sharpe = annualized_return / annualized_volatiltity
        mdd = 1 - (df.loc[:, 'mv'] / df.loc[:, 'mv'].rolling(10000, min_periods=1).max()).min()
        mdd_part1 = (df.loc[:, 'mv'] / df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        mdd_date1 = df.loc[:mdd_part1.idxmin(),'mv'].idxmax()
        mdd_date2 = mdd_part1.idxmin()
        r = {}
        w = copy.deepcopy(self.saa_weight)
        w['mdd'] = mdd
        w['annual_ret'] = annualized_return
        w['sharpe'] = sharpe
        w['5_year_ret'] = five_year_return
        w['annual_vol'] = annualized_volatiltity
        w['mdd_d1'] = mdd_date1
        w['mdd_d2'] = mdd_date2
        return w

    def get_asset_stat(self):
        self.asset_mv = pd.DataFrame([ {'date':k, 'mv':v} for k,v in self.asset_market_price_history.items()]).set_index('date')
        w = self._calc_stat(self.asset_mv.copy())
        return w
    
    def get_fund_stat(self):
        self.fund_mv = pd.DataFrame([ {'date':k, 'mv':v} for k,v in self.fund_marktet_price_history.items()]).set_index('date')
        w = self._calc_stat(self.fund_mv.copy())
        return w

    def get_fund_trade(self):
        fsdf = self.fund_score.copy()
        fund_info_df = self.fund_info.copy().set_index('fund_id')
        fund_trade = []
        for d in self.trade_history:
            f_t = [ i.__dict__  for i in self.trade_history[d] if isinstance(i, FundTrade)]
            fund_trade.extend(f_t)
        if len(fund_trade) < 1:
            return pd.DataFrame()
        ft_res = []
        for ft in fund_trade:
            ft['desc_name'] = fund_info_df.loc[ft['fund_id'], 'desc_name']
            index_id = fund_info_df.loc[ft['fund_id'], 'index_id']
            try:
                s = fsdf[ft['submit_date']][index_id][ft['fund_id']]
            except:
                s = np.nan
            ft['submit_d_score'] = s
            fund_id = ft['fund_id']
            submit_d = ft['submit_date']
            traded_d = ft['trade_date']
            ft['before_w']  = self.fund_weights_history[submit_d].get(fund_id,0)
            ft['after_w'] = self.fund_weights_history[traded_d].get(fund_id,0)
            ft_res.append(ft)
        fund_trade_df = pd.DataFrame(ft_res)
        return fund_trade_df

    def get_asset_trade(self):
        asset_trade = []
        for d in self.trade_history:
            a_t = [ i.__dict__  for i in self.trade_history[d] if not isinstance(i, FundTrade)]
            asset_trade.extend(a_t) 
        res = []
        for dic in asset_trade: 
            index_id = dic['index_id']
            submit_d = dic['submit_date']
            traded_d = dic['trade_date']
            dic['before_w'] = self.asset_weights_history[submit_d].__dict__[index_id]
            dic['after_w'] = self.asset_weights_history[traded_d].__dict__[index_id]
            res.append(dic)
        return pd.DataFrame(res)

    def backtest_asset_plot(self):
        bt_type = 'asset'
        print(f'{bt_type} report')
        w = self.get_asset_stat()
        pprint(w)
        self._plot_asset_weights()
        self._plot_market_value(self.asset_mv, bt_type)
        self._plot_mdd_period_assets()

    def backtest_fund_plot(self):
        bt_type = 'fund'
        print(f'{bt_type} report')
        w = self.get_fund_stat()
        pprint(w)
        self._plot_fund_weights()
        self._plot_market_value(self.fund_mv, bt_type)
        self._plot_mdd_period_funds()
        self._plot_asset_fund_diff()

    def plot_whole(self):
        bt_type = 'asset'
        print(f'{bt_type} report')
        w = self.get_asset_stat()
        pprint(w)
        self._plot_asset_weights()
        self._plot_market_value(self.asset_mv,bt_type)
        self._plot_mdd_period_assets()

        bt_type = 'fund'
        print(f'{bt_type} report')
        w = self.get_fund_stat()
        pprint(w)
        self._plot_fund_weights()
        self._plot_market_value(self.fund_mv,bt_type)
        self._plot_mdd_period_funds()
        self._plot_asset_fund_diff()

    def _plot_asset_weights(self):
        res = []
        for k,v in self.asset_weights_history.items():
            v = v.__dict__
            v['date'] = k
            res.append(v)
        weights_df = pd.DataFrame(res).set_index('date')
        weights_df = weights_df.drop(['cash'], axis = 1).dropna()[1:]
        res = []
        for dic, s in zip(weights_df.to_dict('records'), weights_df.sum(axis = 1).values):
            res.append({ k: v/ s for k, v in dic.items()})
        df = pd.DataFrame(res)
        cols = df.columns.tolist()
        cols = [col for col in cols if df[col].sum() != 0]
        df = df[cols]
        df.index = weights_df.index
        df.plot.area(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 9)
        s = pl.title('asset weights history', fontsize=20)

    def _plot_fund_weights(self):
        res = []
        for k,v in self.fund_weights_history.items():
            v = v
            v['date'] = k
            res.append(v)
        weights_df = pd.DataFrame(res).set_index('date')
        weights_df = weights_df.div(weights_df.sum(axis=1), axis=0)
        weights_df.fillna(0)[1:].plot.area(figsize=(18,9),legend=False,fontsize = 13)
        s = pl.title('fund weights history', fontsize=20)

    def _plot_market_value(self, mv_df, bt_type):    
        index_df_raw = self.index_price.copy().loc[mv_df.index[0]:mv_df.index[-1],]
        index_df = index_df_raw.copy().fillna(method='bfill')
        index_df = index_df/index_df.iloc[0]
        w_l = []
        for idx, r in index_df_raw.iterrows():
            nan_asset = [k for k,v in r.to_dict().items() if np.isnan(v)]
            wgts = self.saa_weight.copy()
            wgts['cash'] = 0
            for k in nan_asset:
                wgts[k] = 0
            s = sum([v  for k,v in wgts.items()])
            wgts = {k :v /s for k, v in wgts.items()}
            wgts['datetime'] = idx
            w_l.append(wgts)
        wgts_df = pd.DataFrame(w_l).set_index('datetime').drop(['cash'], axis = 1)
        mv_df['benchmark'] = (wgts_df * index_df).sum(axis = 1)
        mv_df =mv_df /mv_df.iloc[0]
        mv_df.plot.line(figsize=(20,12),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 10)
        s = pl.title(f'{bt_type} market value', fontsize=20)

    def _plot_mdd_period_assets(self): 
        df = self.asset_mv
        mdd_part1 = (df.loc[:, 'mv'] / df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        mdd_date1 = df.loc[:mdd_part1.idxmin(),'mv'].idxmax()
        mdd_date2 = mdd_part1.idxmin()
        l = [k for k, v in self.saa_weight.items() if v > 0]
        l.remove('cash')
        df = self.index_price.copy()[l].loc[mdd_date1:mdd_date2].fillna(method='bfill')
        df = df / df.iloc[0]
        
        df.plot.line(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 13)
        s = pl.title('asset bt during mdd period  price of holding assets', fontsize=20)    

    def _plot_mdd_period_funds(self):
        df = self.fund_mv
        mdd_part1 = (df.loc[:, 'mv'] / df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        mdd_date1 = df.loc[:mdd_part1.idxmin(),'mv'].idxmax()
        mdd_date2 = mdd_part1.idxmin()
        date_list = np.array(list(self.fund_weights_history.keys()))
        date_list = date_list[(date_list >= mdd_date1) & (date_list <= mdd_date2)]
        fund_list = []
        for d in date_list:
            fund_list.extend([k for k,v in self.fund_weights_history[d].items() if isinstance(v, float) and (round(v,3) > 0)])
        fund_list = list(set(fund_list)) 
        df = self.fund_nav[fund_list].loc[mdd_date1:mdd_date2,:] 
        fig, ax = plt.subplots(figsize= [18,9])
        df = df/df.iloc[0]
        table_df = self.fund_info.set_index('fund_id').loc[fund_list,:].reset_index()[['fund_id','desc_name','index_id']].sort_values(['index_id'])
        df_mdd = pd.DataFrame(((1-df.iloc[-1])*100).round(2))
        df_mdd.columns = ['max draw down %']
        table_df = table_df.set_index('fund_id').join(df_mdd).reset_index()
        fund_list = table_df.fund_id.tolist()
        
        for col in df.columns:
            plt.plot(df.index, df[[col]], linewidth=1.0, label = col)
        plt.legend(fontsize=13 ,loc = 'lower left')
        plt.title('fund bt during mdd period  nav of all funds', fontsize=20)
        ax.xaxis.set_ticks_position('top')
        t = plt.table(cellText=table_df.values.tolist(),
          colLabels=table_df.columns,
          colWidths= [0.25,0.45,0.15,0.15],  
          loc='bottom',
          )
        t.auto_set_font_size(False)
        t.auto_set_font_size(False)
        t.set_fontsize(15)
        t.auto_set_column_width('fund_id')
        t.AXESPAD = 0.1
        t.scale(1, 2)
        plt.show()
        
    def _plot_asset_fund_diff(self):
        asset_mv = self.asset_mv[['mv']]
        fund_mv = self.fund_mv[['mv']]
        asset_mv.columns = ['asset_mv']
        fund_mv.columns = ['fund_mv']

        check_diff = fund_mv.join(asset_mv)
        check_diff = check_diff / check_diff.iloc[0]
        check_diff['diff'] = 100 * (check_diff['fund_mv']  - check_diff['asset_mv']) / check_diff['asset_mv'] 
        check_diff[['fund_mv','asset_mv']].plot.line(figsize=(20,12),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 10)
        s = pl.title('asset and fund market value ', fontsize=20)
        check_diff[['diff']].plot.line(figsize=(20,12),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 10)
        s = pl.title('asset and fund market value diff % ', fontsize=20)

    def _plot_fund_score(self, asset):
        mv_df = self.fund_mv
        fund_w = self.fund_weights_history
        trade_dic = self.trade_history
        index_price = self.index_price
        end_date = mv_df.index.tolist()[-1]
        date_list = list(trade_dic.keys()) + [end_date]
        asset_weight = self.asset_weights_history
        fund_info = self.fund_info
        fund_asset_df = fund_info[['fund_id','index_id']].set_index('fund_id')
        fund_mv = self.fund_nav
        fund_score = self.fund_score
        fund_indicator = self.fund_indicator.pivot_table(index = ['fund_id','datetime'])
        traded_to_submit_date = {}
        for d in trade_dic:
            dic = trade_dic[d][0]
            traded_to_submit_date[dic.trade_date] = dic.submit_date
        res = []
        for k,v in asset_weight.items():
            v = v.__dict__
            v['date'] = k
            res.append(v)
        weights_df = pd.DataFrame(res).set_index('date')
        weights_df = weights_df.drop(['cash'], axis = 1).dropna()[1:]
        res = []
        for dic, s in zip(weights_df.to_dict('records'), weights_df.sum(axis = 1).values):
            res.append({ k: v/ s for k, v in dic.items()})
        df = pd.DataFrame(res)
        cols = df.columns.tolist()
        name_dic = fund_info[['fund_id','desc_name']].set_index('fund_id')
        b_d = mv_df.index[0]
        e_d = mv_df.index[-1]
        bench_df = index_price.loc[b_d:e_d,[asset]]
        bench_df = bench_df/bench_df.iloc[0]
        for i in range(len(date_list) - 1):   
            b_d = date_list[i]
            e_d = date_list[i+1]
            if b_d == e_d:
                break
            bench_df_tmp = bench_df.loc[b_d:e_d,:]
            f_l = [k  for k ,v in fund_w[b_d].items() if isinstance(v, float) and round(v ,3 ) > 0]
            f_l = [f for f in f_l if fund_asset_df.loc[f,'index_id'] == asset]
            mv_b = bench_df.loc[b_d,asset]
            fund_tmp = fund_mv.loc[b_d:e_d,f_l].copy()
            fund_tmp = fund_tmp/fund_tmp.iloc[0]
            fund_tmp = fund_tmp*mv_b
            res = []
            submit_d = traded_to_submit_date[b_d]
            if len(f_l) < 1:
                continue
            fig, ax = plt.subplots(figsize= [16,12])
            plt.plot(bench_df_tmp.index, bench_df_tmp[asset], label=asset,linewidth=5.0)
            for f in f_l:
                desc = name_dic.loc[f,'desc_name']
                f_i_dict= fund_indicator.loc[f,submit_d].to_dict()
                dic = {
                    'fund_id' : f,
                    'desc_name' : desc,
                    'score' : round(fund_score[submit_d][asset][f],4),
                    'weight': round(fund_w[b_d][f], 4)
                }
                for s in ['alpha','beta','fee_rate','track_err']:
                    dic[s] = round(f_i_dict[s],4)
                res.append(dic)    
                plt.plot(fund_tmp.index, fund_tmp[f], label=f+'_'+desc,linestyle='--',linewidth=3.0)    
            plt.legend(fontsize=15 ,loc = 'lower right')
            plt.title(f'{asset} {b_d} {e_d}', fontsize=25)
            plt.suptitle(FundScoreManager().funcs[asset].__dict__, y=0.87, fontsize=18)
            ax.xaxis.set_ticks_position('top')
            fund_df = pd.DataFrame(res)
            fund_df['ir'] = (fund_df['alpha'] / fund_df['track_err']).round(4)
            fund_df = fund_df[['desc_name','fund_id','weight','alpha','beta','track_err','fee_rate','ir','score']]
            t = plt.table(
                cellText=fund_df.values.tolist(),
                colLabels=fund_df.columns,
                loc='bottom',
                colWidths= [0.25,0.12,0.09,0.09,0.09,0.09,0.09,0.09,0.09]          
            )
            t.auto_set_font_size(False)
            t.set_fontsize(15)
            t.auto_set_column_width('fund_id')
            t.AXESPAD = 0.1
            t.scale(1, 4)
            plt.show()

