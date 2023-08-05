import io
import os
import json
import pickle
import codecs
import inspect
import requests
import pandas as pd
from io import BytesIO
from finlab import report


def backtest(strategy):

    code = inspect.getsource(strategy)

    url = "https://rkatitawci.execute-api.ap-northeast-1.amazonaws.com/default/backtest"

    payload = code.encode('utf-8')
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.20.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "rkatitawci.execute-api.ap-northeast-1.amazonaws.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    pickled = json.loads(response.text)['message']
    return report.Report(pickle.loads(codecs.decode(pickled.encode(), 'base64')))

class FinlabDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return FinlabDataFrame

    @staticmethod
    def reshape(df1, df2):

        if isinstance(df2, pd.Series):
            df2 = pd.DataFrame({c:df2 for c in df1.columns})

        if isinstance(df2, FinlabDataFrame) or isinstance(df2, pd.DataFrame):
            index = df1.index | df2.index
            columns = df1.columns & df2.columns
            return df1.reindex(index=index,columns=columns, method='ffill'), \
            df2.reindex(index=index,columns=columns, method='ffill')
        else:
            return df1, df2

    def __lt__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__lt__(df1, df2)

    def __gt__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__gt__(df1, df2)

    def __le__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__le__(df1, df2)

    def __ge__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__ge__(df1, df2)

    def __eq__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__eq__(df1, df2)

    def __ne__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__ne__(df1, df2)

    def __sub__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__sub__(df1, df2)

    def __add__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__add__(df1, df2)

    def __mul__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__mul__(df1, df2)

    def __truediv__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__truediv__(df1, df2)

    def __rshift__(self, other):
        return self.shift(-other)

    def __lshift__(self, other):
        return self.shift(other)

    def __and__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__and__(df1, df2)

    def __or__(self, other):
        df1, df2 = self.reshape(self, other)
        return pd.DataFrame.__or__(df1, df2)

    def average(self, n):
        return self.rolling(n, min_periods=int(n/2)).mean()

    def largest(self, n):
        return (self.fillna(self.min().min()).transpose().apply(lambda s:s.nlargest(n)).transpose().notna())

    def smallest(self, n):
        return (self.fillna(self.max().max()).transpose().apply(lambda s:s.nsmallest(n)).transpose().notna())

    def rise(self, n=1):
        return self > self.shift(n)

    def fall(self, n=1):
        return self < self.shift(n)

    def sustain(self, n):
        return self.rolling(n).sum() > 0


class Data():


    def __init__(self, path=os.path.join("history", "items")):

        self.date = datetime.datetime.now().date()
        self.warrning = False

        self.col2table = {}
        tnames = os.listdir(path)
        self.path = path


        for tname in tnames:

            path = os.path.join(self.path, tname)

            if not os.path.isdir(os.path.join(self.path, tname)):
                continue

            items = [f[:-4] for f in os.listdir(path)]

            for item in items:
                if item not in self.col2table:
                    self.col2table[item] = []
                self.col2table[item].append(tname)

    def get(self, name, amount=0, table=None, convert_to_numeric=True):
        if table is None:
            candidates = self.col2table[name]
            if len(candidates) > 1 and self.warrning:
                print('**WARRN there are tables have the same item', name, ':', candidates)
                print('**      take', candidates[0])
                print('**      please specify the table name as an argument if you need the file from another table')
                for c in candidates:
                    print('**      data.get(', name, ',',amount, ', table=', c, ')')

            table = candidates[0]

        df = pd.read_pickle(os.path.join(self.path, table, name + '.pkl'))

        return FinlabDataFrame(df.loc[:self.date.strftime("%Y-%m-%d")].iloc[-amount:])


    def talib(self, func_name, amount=0, freq="d", **args):


        from talib import abstract

        func = getattr(abstract, func_name)

        isSeries = True if len(func.output_names) == 1 else False
        names = func.output_names
        if isSeries:
            dic = {}
        else:
            dics = {n:{} for n in names}

        close = self.get('收盤價', amount)
        open_ = self.get('開盤價', amount)
        high  = self.get('最高價', amount)
        low   = self.get('最低價', amount)
        volume= self.get('成交量', amount)

        if freq == 'W':
            close = close.resample("W").last()
            open_ = open_.resample("W").first()
            high = high.resample("W").max()
            low = low.resample("W").min()
            volume = volume.resample("W").sum()

        sids = close.columns & open_.columns & high.columns & low.columns & volume.columns

        for key in sids:
            #try:
            s = func({
                'open':open_[key].ffill(),
                'high':high[key].ffill(),
                'low':low[key].ffill(),
                'close':close[key].ffill(),
                'volume':volume[key].ffill()
            }, **args)

            if isSeries:
                dic[key] = s
            else:
                for colname, si in zip(names, s):
                    dics[colname][key] = si

        if isSeries:
            ret = pd.DataFrame(dic, index=close.index)
            ret = FinlabDataFrame(ret.apply(lambda s:pd.to_numeric(s, errors='coerce')))
        else:
            newdic = {}
            for key, dic in dics.items():
                newdic[key] = pd.DataFrame(dic, close.index).loc[:self.date]
            ret = [newdic[n] for n in names]#pd.Panel(newdic)
            ret = [FinlabDataFrame(d.apply(lambda s:pd.to_numeric(s, errors='coerce'))) for d in ret]


        return ret

class Data(Data):
    def __init__(self, repo_name = 'https://www.finlab.tw'):
        self.repo_name = repo_name
        self.english_to_chinese = {
            'open': '開盤價',
            'close': '收盤價',
            'return': '報酬率',
            'high': '最高價',
            'low': '最低價',
            'volume': '成交張數',
            'benchmark': '發行量加權股價報酬指數',
        }
        self.cache = {}

    def get(self, name, folder='fdata'):

        if name in self.english_to_chinese:
            name = self.english_to_chinese[name]

        key = '/'.join([self.repo_name, folder, name + '.pkl'])


        if key not in self.cache:
            res = requests.get(key)
            f = open('temp.pkl', 'wb')
            f.write(res.content)
            df = pd.read_pickle('temp.pkl')
            self.cache[key] = df

        return FinlabDataFrame(self.cache[key])
