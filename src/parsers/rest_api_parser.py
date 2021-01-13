import json
import urllib.request
import pandas as pd
# download raw json object
from datetime import datetime
from pprint import pprint

from src.controllers.connections.SQLConnectionManager import SQLConnectionManager
from src.models import Scheme, SchemeCache

sql_mgr = SQLConnectionManager()


def download_schemes(scheme_source):
    scheme_meta = get_json_data(scheme_source)
    for this_info in scheme_meta:
        scheme_url = str(scheme_source) + "/" + str(this_info["schemeCode"])
        scheme_data = get_json_data(scheme_url)
        scheme = get_scheme_from_data(scheme_data)
        SchemeCache().add(scheme)
        break
    return SchemeCache()


def insert_scheme_historical_in_db(scheme):
    sql_mgr.insert_or_update(scheme.historical_data, "Schemes")


def get_json_data(scheme_source):
    url = scheme_source
    data = urllib.request.urlopen(url).read().decode()
    # parse json object
    data = json.loads(data)
    return data


def get_scheme_from_data(data):
    scheme = Scheme()
    scheme.name = data["meta"]["scheme_name"]
    scheme.category = data["meta"]["scheme_category"]
    scheme.historical_data = pd.DataFrame.from_dict(data=data["data"])
    scheme.historical_data["Scheme"] = scheme.name
    return scheme
