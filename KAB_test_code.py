import time
import datetime as dt
import requests
import pandas             as pd
import numpy               as np
import matplotlib.pyplot   as plt
from   matplotlib.gridspec import GridSpec

# ===== 設定値 =====================

# kabuステーションAPI パスワード（kabuステーションのAPIタブで設定したもの）
API_PASSWORD = "SetYourPassword"

# 本番 / 検証 両対応
ENV = "prod"   # "prod" or "dev"

BASE_URLS = {
    "prod": "http://localhost:18080/kabusapi",
    "dev":  "http://localhost:18081/kabusapi",
}

BASE_URL = BASE_URLS[ENV]

# 取得対象銘柄と市場
# 例: 8306 三菱UFJ（東証プライム） -> "8306@1"
SYMBOL = "8306"
EXCHANGE = 1   # 1: 東証など。詳細はリファレンス参照 ([kabucom.github.io](https://kabucom.github.io/kabusapi/reference/index.html?utm_source=openai))
SYMBOL_FULL = f"{SYMBOL}@{EXCHANGE}"

# ティック取得時間（秒）: 簡易テスト用に 120秒
TICK_COLLECT_SECONDS = 120
POLL_INTERVAL_SECONDS = 3   # 3秒ごとに /board を叩く（秒間10件制限に配慮）([kabucom.github.io](https://kabucom.github.io/kabusapi/ptal/faq.html?utm_source=openai))

# =================================


class KabuApiClient:
    def __init__(self, base_url: str, api_password: str):
        self.base_url = base_url
        self.api_password = api_password
        self.token = None

    def login(self):
        url = f"{self.base_url}/token"
        payload = {"APIPassword": self.api_password}
        print(f"[LOGIN] POST {url}")
        r = requests.post(url, json=payload)
        print(f"[LOGIN] status={r.status_code}, body={r.text}")
        r.raise_for_status()
        data = r.json()
        # {"ResultCode":0, "Token":"..."} を想定 ([kabucom.github.io](https://kabucom.github.io/kabusapi/reference/index.html?utm_source=openai))
        if data.get("ResultCode") != 0:
            raise RuntimeError(f"Token error: {data}")
        self.token = data["Token"]
        print(f"[LOGIN] token acquired: {self.token[:8]}...")

    def _headers(self):
        if not self.token:
            raise RuntimeError("Token not set. Call login() first.")
        return {"X-API-KEY": self.token}

    def get_board(self, symbol_full: str):
        url = f"{self.base_url}/board/{symbol_full}"
        r = requests.get(url, headers=self._headers())
        # デバッグ用ログ
        print(f"[BOARD] {symbol_full} status={r.status_code}")
        r.raise_for_status()
        return r.json()


def collect_ticks(client: KabuApiClient,
                  symbol_full: str,
                  duration_sec: int,
                  interval_sec: int) -> pd.DataFrame:
    """board APIを一定間隔で叩き、簡易ティックを集める"""
    records = []
    start = time.time()
    while time.time() - start < duration_sec:
        try:
            data = client.get_board(symbol_full)
            now = dt.datetime.now()
            price = data.get("CurrentPrice")
            volume = data.get("TradingVolume")  # 累計出来高（銘柄による）([kabucom.github.io](https://kabucom.github.io/kabusapi/reference/index.html?utm_source=openai))
            if price is not None:
                records.append({
                    "time": now,
                    "price": float(price),
                    "volume_total": float(volume) if volume is not None else np.nan,
                })
                print(f"[TICK] {now} price={price}, volume_total={volume}")
        except Exception as e:
            print(f"[ERROR] get_board failed: {e}")
        time.sleep(interval_sec)

    if not records:
        raise RuntimeError("No tick data collected. Check symbol, API, or market session.")

    df = pd.DataFrame(records)
    df.set_index("time", inplace=True)
    # volume_total から1本ごとの出来高を差分で推定
    df["volume"] = df["volume_total"].diff().fillna(0).clip(lower=0)
    return df


# ===== インジケータ計算 =====

def calc_macd(series: pd.Series,
              fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return macd, signal_line, hist


def calc_williams_r(high: pd.Series,
                    low: pd.Series,
                    close: pd.Series,
                    period=14):
    highest_high = high.rolling(window=period, min_periods=1).max()
    lowest_low = low.rolling(window=period, min_periods=1).min()
    wr = -100 * (highest_high - close) / (highest_high - lowest_low)
    return wr


def resample_to_ohlc(df_tick: pd.DataFrame,
                     freq: str = "1T") -> pd.DataFrame:
    """
    ティックからOHLCVを作る。
    freq: "1T"で1分足。必要なら "5T" などに変更可能。
    """
    ohlc = df_tick["price"].resample(freq).ohlc()
    vol = df_tick["volume"].resample(freq).sum()
    ohlc["volume"] = vol
    # 欠損の削りなど、必要に応じて
    ohlc.dropna(subset=["open", "high", "low", "close"], inplace=True)
    return ohlc


# ===== プロット処理 =====

def plot_price_macd_wr_volume(df_ohlc: pd.DataFrame, title: str = ""):
    plt.style.use("seaborn-v0_8-darkgrid")

    fig = plt.figure(figsize=(12, 8))
    gs = GridSpec(4, 1, height_ratios=[3, 1, 1, 1], hspace=0.1)

    ax_price = fig.add_subplot(gs[0])
    ax_macd = fig.add_subplot(gs[1], sharex=ax_price)
    ax_wr = fig.add_subplot(gs[2], sharex=ax_price)
    ax_vol = fig.add_subplot(gs[3], sharex=ax_price)

    # Price
    ax_price.plot(df_ohlc.index, df_ohlc["close"], color="white", linewidth=1.0)
    ax_price.set_ylabel("Price")
    if title:
        ax_price.set_title(title)

    # MACD
    macd, signal, hist = calc_macd(df_ohlc["close"])
    ax_macd.plot(df_ohlc.index, macd, label="MACD", color="cyan", linewidth=1.0)
    ax_macd.plot(df_ohlc.index, signal, label="Signal", color="orange", linewidth=1.0)
    ax_macd.bar(df_ohlc.index, hist, label="Hist", color="gray", alpha=0.5, width=0.0008)
    ax_macd.legend(loc="upper left", fontsize=8)
    ax_macd.set_ylabel("MACD")

    # WBR
    wr = calc_williams_r(df_ohlc["high"], df_ohlc["low"], df_ohlc["close"])
    ax_wr.plot(df_ohlc.index, wr, label="W%R", color="magenta", linewidth=1.0)
    ax_wr.axhline(-20, color="yellow", linestyle="--", linewidth=0.8)
    ax_wr.axhline(-80, color="yellow", linestyle="--", linewidth=0.8)
    ax_wr.set_ylabel("W%R")
    ax_wr.set_ylim(-100, 0)

    # Volume
    ax_vol.bar(df_ohlc.index, df_ohlc["volume"], color="lightblue", width=0.0008)
    ax_vol.set_ylabel("Volume")

    for ax in [ax_price, ax_macd, ax_wr, ax_vol]:
        ax.tick_params(axis="x", rotation=30)

    plt.show()


def main():
    print(f"ENV={ENV}, BASE_URL={BASE_URL}")
    client = KabuApiClient(BASE_URL, API_PASSWORD)
    client.login()

    # ティック収集
    print("[INFO] collecting ticks...")
    df_tick = collect_ticks(
        client,
        SYMBOL_FULL,
        duration_sec=TICK_COLLECT_SECONDS,
        interval_sec=POLL_INTERVAL_SECONDS,
    )
    print(df_tick.head())

    # 1分足にリサンプル
    df_ohlc = resample_to_ohlc(df_tick, freq="1T")
    print(df_ohlc.tail())

    if len(df_ohlc) < 5:
        print("[WARN] 足の本数が少ないため、MACD/WBRの形はあまり参考になりません。")
    title = f"{SYMBOL_FULL} 1-min OHLC via /board ({ENV})"
    plot_price_macd_wr_volume(df_ohlc, title=title)


if __name__ == "__main__":
    main()


#------------------------------------------------------------------------------
#
#
#
#
#
#
#
#