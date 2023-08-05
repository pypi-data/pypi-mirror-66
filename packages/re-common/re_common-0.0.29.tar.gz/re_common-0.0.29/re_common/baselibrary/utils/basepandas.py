import pandas as pd
import numpy as np
from pandas import DatetimeIndex, DataFrame

"""
https://www.pypandas.cn/docs/getting_started/10min.html#%E6%9F%A5%E7%9C%8B%E6%95%B0%E6%8D%AE
 Series（一维数据）;带标签的一维同构数组
 DataFrame（二维数据）;带标签的，大小可变的，二维异构表格;index（行）或 columns（列）
 DataFrame 是 Series 的容器，Series 则是标量的容器
 NumPy 数组只有一种数据类型，DataFrame 每列的数据类型各不相同
"""


class BasePandas(object):

    def __init__(self):
        pass

    def create_null_dataframe(self):
        """
        创建空的dataframe
        :return: type:DataFrame
        """
        df = pd.DataFrame()
        return df

    def create_series_for_list(self, list):
        """
        用值列表生成 Series 时，Pandas 默认自动生成整数索引
        pd.Series([1, 3, 5, np.nan, 6, 8])
        :return: type:Series
        """
        s = pd.Series(list)
        print(type(s))
        return s

    def create_time_index(self, datastring, periods):
        """
        创建行标
        含日期时间索引与标签的 NumPy 的数组
        :param datastring: '20130101'
        :param periods: 6
        :return: type:DatetimeIndex
        """
        dates = pd.date_range(datastring, periods=periods)
        return dates

    def create_ndarray(self, index, columns):
        """
        产生指定行列的随机数据
        :param index: 行  6
        :param columns: 列 4
        :return:  type:ndarray
        """
        return np.random.randn(index, columns)

    def create_time_dataform(self, data, dates: DatetimeIndex, columns=list('ABCD')):
        return pd.DataFrame(data, index=dates, columns=columns)

    def dicts_to_dataform(self, dicts):
        """
        字典转二维数据
        {'A': 1.,
        'B': pd.Timestamp('20130102'),
        'C': pd.Series(1, index=list(range(4)), dtype='float32'),
        'D': np.array([3] * 4, dtype='int32'),
        'E': pd.Categorical(["test", "train", "test", "train"]),
        'F': 'foo'}
        :param dicts:
        :return:
        """
        df = pd.DataFrame(dicts)
        return df

    def dtypes(self, df: DataFrame):
        """
        DataFrame 的列的数据类型
        :return:
        """
        return df.dtypes

    def head(self, df, num=5):
        """
        查看前几条数据
        :param num:
        :return:
        """
        return df.head(num)

    def tail(self, df, num=5):
        """
        查看后几条数据
        :param num:
        :return:
        """
        return df.tail(num)

    def index(self, df):
        """
        显示索引
        :param df:
        :return:
        """
        return df.index

    def columns(self, df):
        """
        显示列名
        :param df:
        :return:
        """
        return df.columns

    def dataform_to_numpy(self, df):
        """
        输出底层数据的 NumPy 对象。
        注意，DataFrame 的列由多种数据类型组成时，该操作耗费系统资源较大，
        输出不包含行索引和列标签
        :return:
        """
        return df.to_numpy()

