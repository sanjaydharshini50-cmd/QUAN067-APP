ASSETS={
"Gold":{"ticker":"GC=F","asset_class":"Commodity","currency":"USD"},
"Bitcoin":{"ticker":"BTC-USD","asset_class":"Cryptocurrency","currency":"USD"},
"NVIDIA":{"ticker":"NVDA","asset_class":"Equity","currency":"USD"},
"Apple":{"ticker":"AAPL","asset_class":"Equity","currency":"USD"},
"Microsoft":{"ticker":"MSFT","asset_class":"Equity","currency":"USD"},
"Amazon":{"ticker":"AMZN","asset_class":"Equity","currency":"USD"},
"Tesla":{"ticker":"TSLA","asset_class":"Equity","currency":"USD"},
"Alphabet":{"ticker":"GOOGL","asset_class":"Equity","currency":"USD"},
"Meta":{"ticker":"META","asset_class":"Equity","currency":"USD"},
"Ethereum":{"ticker":"ETH-USD","asset_class":"Cryptocurrency","currency":"USD"}}
def get_asset(name):
    if name not in ASSETS: raise KeyError(f"Unsupported asset: {name}")
    return ASSETS[name]
