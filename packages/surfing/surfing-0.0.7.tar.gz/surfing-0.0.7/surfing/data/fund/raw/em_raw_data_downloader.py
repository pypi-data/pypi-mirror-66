#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import rqdatac as rq
import pickle as pkl
from .EMQuantAPI_Python.python3.EmQuantAPI import *
import datetime
import json
import csv
from ...wrapper.mysql import RawDatabaseConnector
from ...view.raw_models import *
from ...api.basic import BasicDataApi

class EmRawDataDownloader(object):

    def __init__(self):
        # ForceLogin
        # 取值0，当线上已存在该账户时，不强制登录
        # 取值1，当线上已存在该账户时，强制登录，将前一位在线用户踢下线
        options = 'ForceLogin=1'
        loginResult = c.start(options, mainCallBack=self._main_callback)
        if(loginResult.ErrorCode != 0):
            print('EM login failed')
            exit()

        self._scale_change_dates = ['0331', '0630', '0930', '1231']

    def _upload_raw(self, df, table_name, if_exists='append'):
        print(table_name)
        df.to_sql(table_name, RawDatabaseConnector().get_engine(), index=False, if_exists=if_exists)

    def _main_callback(self, quantdata):
        '''
        mainCallback 是主回调函数，可捕捉连接错误
        该函数只有一个为c.EmQuantData类型的参数quantdata
        :param quantdata: c.EmQuantData
        '''
        print(f'MainCallback: {quantdata}')

    def _get_date_list(self, start_date, end_date):
        start_datetime = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_datetime = datetime.datetime.strptime(end_date, '%Y%m%d')
        date_list = []
        while start_datetime <= end_datetime:
            date_list.append(start_datetime.strftime('%Y%m%d'))
            start_datetime += datetime.timedelta(days=1)
        return date_list

    def em_fund_nav_history(self, nav_file_dir):
        import os
        index = 1
        for filename in os.listdir(nav_file_dir):
            if filename.endswith(".xls"):
                print(f'{index}: {filename}')
                index += 1
                fund_nav = pd.concat(pd.read_excel(os.path.join(nav_file_dir, filename), sheet_name=None), 
                    ignore_index=True)
                fund_nav = fund_nav.drop(['简称'], axis = 1)
                fund_nav = fund_nav.rename(columns={
                        '代码': 'CODES',
                        '时间': 'DATES',
                        '单位净值(元)': 'ORIGINALUNIT',
                        '累计净值(元)': 'ORIGINALNAVACCUM',
                        '复权净值(元)': 'ADJUSTEDNAV',
                        '万份基金单位收益(元)': 'UNITYIELD10K',
                        '7日年化收益率(%)': 'YIELDOF7DAYS'
                    })

                fund_nav = fund_nav[(fund_nav['DATES'] != '--') & (~fund_nav['DATES'].isnull())]
                fund_nav = fund_nav[(fund_nav['DATES'] != '--') & (~fund_nav['DATES'].isnull())]
                fund_nav = fund_nav.replace('--', np.nan)
                self._upload_raw(fund_nav, EmFundNav.__table__.name)
            else:
                continue

    def em_fund_scale_history(self):
        from sqlalchemy import distinct
        date_funds = {}
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                dates = db_session.query(
                    distinct(EmFundNav.DATES)
                ).all()

                dates = [d for d, in dates]
                dates.sort()
                start_date = dates[0]
                for i in range(1, 100):
                    dates.insert(0, start_date - datetime.timedelta(days=i))

                for d in dates:
                    month_day = d.strftime('%m%d')
                    if month_day not in self._scale_change_dates:
                        continue

                    print(d)

                    fund_ids = db_session.query(
                        distinct(EmFundNav.CODES)
                    ).filter(
                        EmFundNav.DATES >= d,
                        EmFundNav.DATES <= d + datetime.timedelta(days=100)
                    ).all()

                    fund_ids = [f for f, in fund_ids]
                    fund_id_str = ','.join(fund_ids) 

                    df=c.css(fund_id_str,"FUNDSCALE",f"EndDate={d},Ispandas=1").reset_index()
                    df['DATES'] = d

                    self._upload_raw(df, EmFundScale.__table__.name)
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def em_fund_nav(self, start_date, end_date):
        # Get all fund ids, 功能函数-板块成分
        # http://quantapi.eastmoney.com/Cmd/Sector?from=web
        fund_id_result = c.sector('507013', end_date)
        if fund_id_result.ErrorCode != 0:
            print(f'Failed to get fund id list: {fund_id_result.ErrorMsg}')
            return

        fund_id_list = fund_id_result.Data[0::2]
        fund_id_str = ','.join(fund_id_list)

        df = c.csd(fund_id_str, 'ORIGINALUNIT,ORIGINALNAVACCUM,ADJUSTEDNAV,10KUNITYIELD,YIELDOF7DAYS', 
            start_date, end_date, 'AdjustFlag=2,Ispandas=1')

        # print(df)
        df.reset_index(inplace=True)
        df['UNITYIELD10K'] = df['10KUNITYIELD']
        df = df.drop(['10KUNITYIELD'], axis = 1)
        self._upload_raw(df, EmFundNav.__table__.name)

    def em_fund_scale(self, start_date, end_date):
        # Get all fund ids, 功能函数-板块成分
        # http://quantapi.eastmoney.com/Cmd/Sector?from=web
        fund_id_result = c.sector('507013', end_date)
        if fund_id_result.ErrorCode != 0:
            print(f'Failed to get fund id list: {fund_id_result.ErrorMsg}')
            return

        fund_id_list = fund_id_result.Data[0::2]
        fund_id_str = ','.join(fund_id_list)

        for d in self._get_date_list(start_date, end_date):
            month_day = d.strftime('%m%d')
            if month_day not in self._scale_change_dates:
                continue

            print(d)

            df = c.css(fund_id_str, 'FUNDSCALE', f'EndDate={end_date},Ispandas=1').reset_index()
            df['DATES'] = d
            self._upload_raw(df, EmFundScale.__table__.name)

    def em_index(self, start_date, end_date):
        # ----------------------
        # H11073.CSI,信用债
        # SPX.GI,标普500
        # GDAXI.GI,德国DAX
        # N225.GI,日经225
        # 000012.SH,利率债
        # 000300.SH,沪深300
        # 000905.SH,中证500
        # 399006.SZ,创业板
        # 801181.SWI,房地产开发申万
        # ----------------------
        # USDCNY.IB,美元兑人民币市询价,TODO: '''ErrorCode=10001012, ErrorMsg=insufficient user access, Data={}'''
        # JPYCNY.IB,日元兑人民币市询价,TODO: '''ErrorCode=10001012, ErrorMsg=insufficient user access, Data={}'''
        # EURCNY.IB,欧元兑人民币市询价,TODO: '''ErrorCode=10001012, ErrorMsg=insufficient user access, Data={}'''
        # ----------------------
        # AU0.SHF,沪金主力连续
        # BC.ICE,布伦特原油当月连续,TODO: always get None
        # ----------------------
        codes = ('H11073.CSI,SPX.GI,GDAXI.GI,N225.GI,000012.SH,000300.SH,000905.SH,399006.SZ,801181.SWI,'
            'USDCNY.IB,JPYCNY.IB,EURCNY.IB,'
            'AU0.SHF,BC.ICE')
        df = c.csd(codes, 'CLOSE', start_date, end_date, 'Ispandas=1')
        # self._upload_raw(df, EmIndexPrice.__table__.name)

    def download_all(self, start_date, end_date):
        self.em_fund_nav(start_date, end_date)

if __name__ == '__main__':
    em = EmRawDataDownloader()
    em.em_fund_scale_history()
