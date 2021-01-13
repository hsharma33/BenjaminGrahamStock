import pickle
from datetime import datetime

import numpy as np
import pandas as pd

from config import buy_qry_delta, sell_qty_delta


class SchemeCache:
    __instance = None
    has_changed = False

    schemes: dict = {}
    scheme_analytics: dict = {}

    scheme_of_max_prev_date: str = ""
    scheme_of_max_prev_price: str = ""
    scheme_of_max_latest_price: str = ""
    scheme_of_max_latest_date: str = ""
    scheme_of_max_change_percentage: str = ""

    def __new__(cls):
        if SchemeCache.__instance is None:
            SchemeCache.__instance = object.__new__(cls)

        return SchemeCache.__instance

    def __init__(self):
        pass

    def add(self, scheme):
        if self.in_cache(scheme):
            pass
        else:
            self.schemes[scheme.name] = scheme
            self.has_changed = True

    def save(self):

        with open('schemes.pickle', 'wb') as handle:
            pickle.dump(self.schemes, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):

        with open('schemes.pickle', 'rb') as handle:
            self.schemes = pickle.load(handle)

    def in_cache(self, scheme):
        return scheme.name in self.schemes


class Scheme:

    def __init__(self):
        self.name: str = ""
        self.category: str = ""
        self.latest_nav_date: str = None
        self.latest_nav: float = ""
        self.previous_nav: float = ""
        self.previous_nav_date: str = ""
        self.change_percentage: str = ""
        self.historical_data = ""

    def __hash__(self):
        pass


class Analytics:

    def __init__(self):
        self.df = pd.DataFrame()
        self.action_price_delta = 0.01

    def perform_analytics(self, scheme, date_filter_tuple=None):
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        self.df["nav_date"] = pd.to_datetime(scheme.historical_data.iloc[:, 0], format="%d-%m-%Y").sort_values()
        self.df["nav_value(rs)"] = scheme.historical_data.iloc[:, 1].astype(float)
        self.df.reset_index(inplace=True, drop=True)
        if date_filter_tuple:
            self.filter_dates(date_filter_tuple())
        self.df["rate_diff"] = (self.df["nav_value(rs)"] - self.df["nav_value(rs)"].shift(1))

        self.action_price_delta = np.absolute(self.df["nav_value(rs)"].diff()).mean()
        self.df["avg_rate_diff"] = self.action_price_delta
        self.df["action"] = np.where(np.absolute(self.df["nav_value(rs)"] - self.df["nav_value(rs)"].shift(1,
                                      fill_value=self.action_price_delta) < self.action_price_delta),
                                     "HOLD", np.where(self.df["rate_diff"] < 0, "BUY", "SELL"))
        self.df["qty"] = np.where((self.df["action"] == "HOLD"), 0,
                                  np.where((self.df["action"] == "BUY"), buy_qry_delta, sell_qty_delta))

        self.df['cost_of_deal'] = self.df['qty'] * self.df['nav_value(rs)']
        self.df["total_qty"] = 0

        self.df["invested_money"] = 0
        self.df["total_asset_value"] = 0
        self.df["total_earnings"] = 0
        self.df["profit_percent"] = 0

    def filter_dates(self):
        pass
