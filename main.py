import glob
import os

from src.models import SchemeCache, Analytics
from src.parsers import xlsx, rest_api_parser


def load_schemes():
    #read_schemes_from_rest()
    read_schemes_from_cache()

def read_schemes_from_rest():
    cache = rest_api_parser.download_schemes("https://api.mfapi.in/mf")
    cache.save()

def read_schemes_from_cache():
    SchemeCache().load()
    for scheme_name, scheme in SchemeCache().schemes.items():

        analytica = Analytics()
        analytica.perform_analytics(scheme)
        print(analytica.df.to_clipboard())
        #print(analytica.df.to_csv(float_format='%.3f'))


def read_schemes_from_db():
    cache = rest_api_parser.download_schemes("https://api.mfapi.in/mf")
    cache.save()


def read_schemes_from_files():
    list_of_files = glob.glob('data/latest_nav/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    xlsx.load_schemes(latest_file)


if __name__ == "__main__":
    load_schemes()
