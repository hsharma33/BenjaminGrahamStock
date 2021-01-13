from datetime import date

multiplier: int = 16
base_qty: int = 100
sell_qty_delta: int = 10
buy_controller: int = 2

buy_qry_delta: int = multiplier * sell_qty_delta / buy_controller
scrips: dict = {
    "example_scrip_name": {
        "url": "xyz",
        "data_format": "xml",
        "start_date": "",
        "end_date": "",

        # optional keys
        "user": "bogus",
        "pass": "bugus",

    }

}
DATABASE_CONFIG = {
    "server": '127.0.0.1',
    "database": 'BGEnterprise',
    "username": 'sa',
    "password": 'Try@12345',
}
