#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datareaders.base import DataReaderBase
from datareaders.tools import COL, _get_dates
import pandas as pd
from StringIO import StringIO
import logging
import traceback

class DataReaderYahooFinanceDaily(DataReaderBase):
    """
    DataReader to fetch data from Yahoo Finance Daily
    """

    def init(self, *args, **kwargs):
        self._get_multi = self._get_multi_topanel

    def _get_one(self, name, *args, **kwargs):
        start_date, end_date = _get_dates(0, *args, **kwargs)

        url = 'http://ichart.finance.yahoo.com/table.csv'
        params = {
            's': name,
            'a': start_date.month - 1,
            'b': start_date.day,
            'c': start_date.year,
            'd': end_date.month - 1,
            'e': end_date.day,
            'f': end_date.year,
            'g': 'd',
            'ignore': '.csv',
        }

        response = self.session.get(url, params=params)
        data = response.text

        df = pd.read_csv(StringIO(data), sep=',', index_col=0, parse_dates=True)

        return(df)