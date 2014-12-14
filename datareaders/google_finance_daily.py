#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datareaders.base import DataReaderBase
from datareaders.tools import COL, _get_dates
#from datareaders.tools import to_float, to_int
import pandas as pd
from StringIO import StringIO
import logging
import traceback

class DataReaderGoogleFinanceDaily(DataReaderBase):
    """
    DataReader to fetch data from Google Finance Daily
    """

    def init(self, *args, **kwargs):
        self._get_multi = self._get_multi_topanel

    def _get_one(self, name, *args, **kwargs):
        start_date, end_date = _get_dates(0, *args, **kwargs)

        url = 'http://www.google.com/finance/historical'
        params = {
            "q": name,
            "startdate": start_date.strftime('%b %d, ' '%Y'),
            "enddate": end_date.strftime('%b %d, %Y'),
            "output": "csv"
        }

        response = self.session.get(url, params=params)
        data = response.text

        df = pd.read_csv(StringIO(data), sep=',', index_col=0, parse_dates=True, na_values='-')
        df.index.name = COL.DATE

        df = df[::-1] # reverse order

        #for col in COL.LST_PRICE():
        #    df[col] = df[col].map(to_float)

        #df[COL.VOLUME] = df[COL.VOLUME].map(to_int)

        return(df)

