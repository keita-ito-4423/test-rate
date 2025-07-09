import requests, json

URL = "https://apiv5.paraswap.io/prices"
params = {
    "srcToken": "ETH",  # シンボルで OK
    "destToken": "USDC",
    "amount": str(int(0.10 * 1e18)),  # 0.1 ETH → wei
    "side": "SELL",
    "network": 1,
}

res = requests.get(URL, params=params, timeout=10)
print(res.status_code, res.text)  # ← ここでレスポンス本文を必ず確認
res.raise_for_status()  # 2xx なら通過

price_route = res.json()["priceRoute"]
# print("srcAmount :", price_route["srcAmount"])
# print("destAmount:", price_route["destAmount"])

# どこから何を取るか
# 欲しい値	取得元
# 受取／支払数量	destAmount, srcAmount
# 実質価格	destAmount ÷ srcAmount（単位調整後）
# 理論レート	srcUSD ÷ (srcAmount/1e18) または destUSD ÷ (destAmount/1e6)
# 価格インパクト	(理論 − 実質) ÷ 理論 × 100
# ガス代	gasCostUSD（USD 換算）

from decimal import Decimal

wei = Decimal("1e18")
usdc = Decimal("1e6")

src_amount = Decimal(price_route["srcAmount"])  # wei
dest_amount = Decimal(price_route["destAmount"])  # 6-dec USDC

eth_in = src_amount / wei
usdc_out = dest_amount / usdc

exec_price = usdc_out / eth_in  # 受取 ÷ 支払: USDC/ETH

# 理論値めやす: srcUSD / (src_amount/wei) でも算出できる
fair_price = Decimal(price_route["srcUSD"]) / eth_in

price_impact_pct = (fair_price - exec_price) / fair_price * 100

print(f"支払        : {eth_in:.4f} ETH")
print(f"受取        : {usdc_out:.2f} USDC")
print(f"実質レート  : {exec_price:.2f} USDC / ETH")
print(f"理論レート  : {fair_price:.2f} USDC / ETH")
print(f"価格インパクト: {price_impact_pct:.2f} %")
print(f"ガスコストUSD: {price_route['gasCostUSD']}")
