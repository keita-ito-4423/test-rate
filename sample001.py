# -*- coding: utf-8 -*-
import requests
from decimal import *


def get_low_n_pairs(n):
    sorted_pairs = sorted(data["pairs"], key=lambda x: float(x["priceUsd"]))
    return sorted_pairs[:n]


def get_high_n_pairs(n):
    sorted_pairs = sorted(
        data["pairs"], key=lambda x: float(x["priceUsd"]), reverse=True
    )
    return sorted_pairs[:n]


url = "https://api.dexscreener.com/latest/dex/search?q=USDT/USDC"
response = requests.get(url)
data = response.json()


print("count all pairs:")
print(len(data["pairs"]))
nth = 5
print("high value pairs:")
for pair in get_high_n_pairs(nth):
    print(
        pair["priceUsd"],
        pair["baseToken"]["symbol"],
        pair["quoteToken"]["symbol"],
        "chainId:",
        pair["chainId"],
        "dexId:",
        pair["dexId"],
        "url:",
        pair["url"],
    )

print("low value pairs:")
for pair in get_low_n_pairs(nth):
    print(
        pair["priceUsd"],
        pair["baseToken"]["symbol"],
        pair["quoteToken"]["symbol"],
        "chainId:",
        pair["chainId"],
        "dexId:",
        pair["dexId"],
        "url:",
        pair["url"],
    )

print("spread:")
spread = Decimal(get_high_n_pairs(nth)[0]["priceUsd"]) - Decimal(
    get_low_n_pairs(nth)[0]["priceUsd"]
)
print(spread)
print("spread_pct:")
spread_pct = (
    abs(
        Decimal(get_high_n_pairs(nth)[0]["priceUsd"])
        - Decimal(get_low_n_pairs(nth)[0]["priceUsd"])
    )
    / Decimal(get_low_n_pairs(nth)[0]["priceUsd"])
    * 100
)
print(spread_pct)
