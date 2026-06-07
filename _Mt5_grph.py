# ! python
# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
#
# Spyder Editor
# Name          : _Cyg_grph.py
# Purpose       : **
# Comment Lang  : JP
# Author        : Blve Bird
# Created Date  : 01/03/2026
# Version       : 0.0.0.1
#
#------------------------------------------------------------------------------
#==============================================================================

#------------------------------------------------------------------------------
import ttkbootstrap            as     ttk
from   ttkbootstrap            import Style
from   ttkbootstrap.dialogs    import Messagebox
#from   ttkbootstrap.widgets.scrolled import ScrolledText
from   ttkbootstrap.scrolled   import ScrolledText
from   ttkbootstrap.constants  import *
from   ttkbootstrap.constants  import END
import tkinter
from   tkinter.filedialog      import askopenfilename
#------------------------------------------------------------------------------
import io
import cv2
import PIL
from   PIL                     import Image, ImageTk, ImageOps
import seaborn                 as sns
import statsmodels.api         as sm
import pandas                  as pd
import numpy                   as np
import configparser
from   datetime                import datetime
import pytz
import mplfinance              as mpf

import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot       as plt
from   matplotlib.patches      import Rectangle
from   matplotlib.dates        import DateFormatter, AutoDateLocator
from   matplotlib.dates        import MinuteLocator, HourLocator, DayLocator, WeekdayLocator, MonthLocator
import matplotlib.ticker       as mticker
#------------------------------------------------------------------------------
import math
import sys
import time
import subprocess
import asyncio
import MetaTrader5             as mt5
#------------------------------------------------------------------------------
import _Cyg_conf
#------------------------------------------------------------------------------

my_style = { 'base_mpl_style': 'fast',
             'marketcolors': {'candle': {'up': '#5383c3', 'down': '#d7003a'},
                              'edge'  : {'up': '#5383c3', 'down': '#d7003a'},
                              'wick'  : {'up': '#ffffff', 'down': '#ffffff'},
                              'ohlc'  : {'up': '#5383c3', 'down': '#d7003a'},
                              'volume': {'up': '#5383c3', 'down': '#d7003a'},
                              'vcedge': {'up': '#5383c3', 'down': '#d7003a'},
                              'vcdopcod': False,
                              'alpha'   : 0.9},
             'mavcolors': None,
             'facecolor': '#1f1f1f',
             'gridcolor': '#808080',
             'gridstyle': None,
             'y_on_right': False,
             'rc': {'axes.edgecolor': '#f8f8ff',
                    'axes.grid'     :  True,
                    'axes.grid.axis': 'y',
                    'grid.color'    : '#000000',
                    'grid.linestyle': '--'
                   },
             'base_mpf_style': 'None'
           }

timeframe_dict = {
    mt5.TIMEFRAME_M1:      60,
    mt5.TIMEFRAME_M2:     120,
    mt5.TIMEFRAME_M3:     180,
    mt5.TIMEFRAME_M4:     240,
    mt5.TIMEFRAME_M5:     300,
    mt5.TIMEFRAME_M6:     360,
    mt5.TIMEFRAME_M10:    600,
    mt5.TIMEFRAME_M12:    720,
    mt5.TIMEFRAME_M15:    900,
    mt5.TIMEFRAME_M20:   1200,
    mt5.TIMEFRAME_M30:   1800,
    mt5.TIMEFRAME_H1:    3600,
    mt5.TIMEFRAME_H2:    7200,
    mt5.TIMEFRAME_H3:   10800,
    mt5.TIMEFRAME_H4:   14400,
    mt5.TIMEFRAME_H6:   21600,
    mt5.TIMEFRAME_H8:   28800,
    mt5.TIMEFRAME_H12:  43200,
    mt5.TIMEFRAME_D1:   86400,
    mt5.TIMEFRAME_W1:  604800,
    mt5.TIMEFRAME_MN1:2592000,
}

def get_time_axis_style(timeframe):
    if   timeframe == mt5.TIMEFRAME_M1 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M2 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M3 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M4 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M5 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M6 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M10: return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M12: return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M15: return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M20: return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_M30: return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_H1 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_H2 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars=104,160
    elif timeframe == mt5.TIMEFRAME_H3 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars=112,208
    elif timeframe == mt5.TIMEFRAME_H4 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars=104,224
    elif timeframe == mt5.TIMEFRAME_H6 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars=112,224
    elif timeframe == mt5.TIMEFRAME_H8 : return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars=110,224
    elif timeframe == mt5.TIMEFRAME_H12: return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars=112,224
    elif timeframe == mt5.TIMEFRAME_D1 : return dict( grid_step=4, label_step=2, fmt='%d %b %Y'    ) # bars=107,214
    elif timeframe == mt5.TIMEFRAME_W1 : return dict( grid_step=4, label_step=2, fmt='%d %b %Y'    ) # bars= 80,160
    elif timeframe == mt5.TIMEFRAME_MN1: return dict( grid_step=4, label_step=2, fmt='%d %b %Y'    ) # bars= 82,164
    else:                                return dict( grid_step=4, label_step=2, fmt='%d %b %H:%M' ) # bars= 80,160

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Make Dataframe (not used)
# MT5 から指定本数ぶんのOHLCVを取得し、
# mpf.plot で使える DataFrame を返す。
#
#
#------------------------------------------------------------------------------
#==============================================================================
def prepare_df_for_plot( symbol, timeframe, bars=150 ):
    # 最新バーの time を取得
    rates_last      = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)
    if rates_last is None or len(rates_last) == 0:
        raise RuntimeError("No rates from MT5")
    tNm             = timeframe_dict[timeframe] * bars  # 秒数×本数
    tSx             = pd.to_datetime(rates_last['time'][0] - tNm, unit='s')
    tEx             = pd.to_datetime(rates_last['time'][0],       unit='s')
    timezone        = pytz.timezone("Etc/UTC")
    date_from       = datetime(tSx.year, tSx.month, tSx.day, tSx.hour, tSx.minute, tSx.second, 0, tzinfo=timezone)
    date_to         = datetime(tEx.year, tEx.month, tEx.day, tEx.hour, tEx.minute, tEx.second, 0, tzinfo=timezone)
    ticks           = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)
    if ticks is None or len(ticks) == 0:
        raise RuntimeError("No ticks in range")
    df              = pd.DataFrame(ticks)
    df['time']      = pd.to_datetime(df['time'], unit='s')
    df.drop(columns=['spread', 'real_volume'], inplace=True)
    df.rename(columns={'tick_volume': 'volume'}, inplace=True)
    df.set_index('time', inplace=True)
    #--------------------------------------------------------------------------
    # ここは index を変えない
    # compress_tfs の場合も datetime index のまま使う
    return  df

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Add Indicators
#
#
#------------------------------------------------------------------------------
#==============================================================================
def add_indicators  ( df ):
    df              = df.copy()
    close           = df['close']
    # --- MACD（12,26,9） ---
    fast_ema        = close.ewm(span=12, adjust=False).mean()
    slow_ema        = close.ewm(span=26, adjust=False).mean()
    macd            = fast_ema - slow_ema
    signal          = macd.ewm(span=9, adjust=False).mean()
    macd_hist       = macd - signal
    df['macd'     ] = macd
    df['macd_sig' ] = signal
    df['macd_hist'] = macd_hist
    # --- RSI（14） ---
    delta           = close.diff()
    gain            = np.where(delta > 0, delta, 0.0)
    loss            = np.where(delta < 0, -delta, 0.0)
    roll_up         = pd.Series(gain, index=df.index).rolling(window=14).mean()
    roll_down       = pd.Series(loss, index=df.index).rolling(window=14).mean()
    rs              = roll_up / roll_down
    rsi             = 100.0 - (100.0 / (1.0 + rs))
    df['rsi']       = rsi
    # --- ボリンジャーバンド（20, ±2σ） ---
    bb_mid          = close.rolling(window=20).mean()
    bb_std          = close.rolling(window=20).std()
    bb_upper        = bb_mid + 2 * bb_std
    bb_lower        = bb_mid - 2 * bb_std
    df['bb_mid'  ]  = bb_mid
    df['bb_upper']  = bb_upper
    df['bb_lower']  = bb_lower
    # --- WBR(Win-Bollin-RSI) の一例 ---
    # バンド内の相対位置 + RSI成分を合成
    bb_width        = (bb_upper - bb_lower).replace(0, np.nan)
    pos_in_band     = (close - bb_mid) / bb_width   # -0.5〜+0.5 付近になる想定
    wbr             = pos_in_band * 50 + (rsi - 50)
    df['wbr']       = wbr
    return  df

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Plot Candles
# シンプルなローソク足描画
# df.index: datetime
#
#------------------------------------------------------------------------------
#==============================================================================
def plot_candles    ( ax, df, width_ratio=0.6,up_color='blue',down_color='red',grid_color='#555555' ):
    xs              = df.index
    # ローソク足の横幅をインデックス型に応じて決定
    # 時間軸から幅を推定（等間隔前提）
    if  len(xs) > 1:
        dx          = xs[1] - xs[0]
        # datetime64 のとき（Timedelta 型）
        if  hasattr(dx, "total_seconds"):
            width   = dx * width_ratio
        # 整数やfloatのとき（時間を詰めた連番インデックスなど）
        else:
            width   = float(dx) * width_ratio
    else:
        # データ1本だけの場合のデフォルト幅
        if np.issubdtype(xs.dtype, np.number):
            width   = 1.0
        else:
            width   = pd.Timedelta(seconds=30)
    for t, row in df.iterrows():
        o, h, l, c  = row['open'], row['high'], row['low'], row['close']
        color       = up_color if c >= o else down_color
        # ヒゲ
        ax.vlines(t, l, h, color=color, linewidth=1)
        # 実体
        body_bottom = min(o, c)
        body_height = abs(c - o)
        if body_height == 0:
            body_height = (df['high'] - df['low']).mean() * 0.05
        rect = Rectangle((t - width / 2, body_bottom),width,body_height,facecolor=color,edgecolor=color)
        ax.add_patch(rect)
    # X軸範囲
    if  np.issubdtype(xs.dtype, np.number):
        ax.set_xlim(xs.min() - 0.5, xs.max() + 0.5)
    else:
        ax.set_xlim(xs.min(), xs.max())
    ax.grid(True, linestyle='-', color=grid_color, linewidth=0.5, alpha=0.4)
    
#==============================================================================
#------------------------------------------------------------------------------
#
#
# Apply Time-axes
#
#
#------------------------------------------------------------------------------
#==============================================================================
def apply_time_axis ( ax, df, original_index, timeframe, xrot=90, xsiz=8 ):
    style           = get_time_axis_style(timeframe)
    grid_step       = style['grid_step' ]   # 何本おきに tick を打つか
    label_step      = style['label_step']   # 何個おきにラベルを付けるか
    fmt             = style['fmt'       ]   # 日付フォーマット
    n               = df.shape[0]
    if n == 0:      return
    # x 範囲は 0〜n-1 の連番
    ax.set_xlim(0, n-1)
    # 本数ベースで等間隔に tick を選ぶ
    xticks          = list(range(0, n, grid_step))
    xlabels         = []
    for i, x in enumerate(xticks):
        if i % label_step == 0 and x < n:
            # ラベルの中身だけ元の datetime index から取る
            xlabels.append(original_index[x].strftime(fmt))
        else:
            xlabels.append('')
    ax.set_xticks       (xticks)
    ax.set_xticklabels  (xlabels, rotation=xrot, ha='center')
    for label in ax.get_xticklabels():
        label.set_fontsize( xsiz )          # Font Size Setting
        
#==============================================================================
#------------------------------------------------------------------------------
#
#
# Create Figure (test)
#
#
#------------------------------------------------------------------------------
#==============================================================================
def create_fig_test ( df_all, timeframe, bars=81, xrot=90, xsiz=0.69 ):
    df = df_all
    target          = bars
    if len(df) >= target: # df_all
        df_draw     = df.iloc[-target:].copy()
    else:
        df_draw     = df.copy() # 足りないときはあるだけ描画
    df              = df_draw
    # 元の日時 index を保持しておく
    original_index  = df.index.copy()
    fig, axes       = mpf.plot( df,type='candle',mav=(5,25),volume=True,figratio=(10,5),figscale=1.1,style=my_style,tight_layout=True,figsize=(8.01,6.01),returnfig=True,xrotation=xrot,fontscale=xsiz ) # show=False にしておいてもよい
    ax_price        = axes[0]   # ローソク足
    ax_vol          = axes[1]   # 出来高
    # ここを追加：価格軸のフォーマット調整
    ax_price.ticklabel_format(style='plain', axis='y', useOffset=False)
    ax_price.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
    apply_time_axis(ax_price, df, original_index, timeframe, xrot, xsiz)
    apply_time_axis(ax_vol  , df, original_index, timeframe, xrot, xsiz) # 出来高側も同じX軸に揃える
    return fig, axes

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Create Figure
#
#
#------------------------------------------------------------------------------
#==============================================================================

#------------------------------------------------------------------------------
# Color Settings
#------------------------------------------------------------------------------
COLOR_BKGR          = '#2B3E50' # ほんのり青みのある濃紺（ベース）
COLOR_SPIN          = '#808080' # 枠線（灰色） #4C5C7A でもOK
COLOR_TEXT          = '#f5f5f5' # 軸ラベル・目盛り #E5E9F0
COLOR_GRID          = '#555555' # グリッド（濃いめの灰色）
#------------------------------------------------------------------------------
COLOR_CAN_UPUP      = '#66aaff' # 明るい赤
COLOR_CAN_DOWN      = '#ff6666' # 明るい青
COLOR_CAN_BAND      = '#888888' # BB 中心線（明るい灰色）
COLOR_CAN_UPER      = 'green'   # BB 上側
COLOR_CAN_LOWR      = 'green'   # BB 下側
COLOR_CAN_LEGF      = 'white'   # legend Front
COLOR_CAN_LEGB      = 'black'   # legend Back
COLOR_CAN_LEGE      = '#cccccc' # legend Edge
#------------------------------------------------------------------------------
COLOR_MAC_MACD      = 'blue'    # MACD
COLOR_MAC_SIGN      = 'orange'  # SIGNAL
COLOR_MAC_BARS      = 'gray'    # MAC BAR
#------------------------------------------------------------------------------
COLOR_WBR_PLOT      = 'purple'  # WBR Line
COLOR_WBR_BAND      = '#888888' # WBR Line
COLOR_WBR_UPER      = 'green'   # WBR 上側
COLOR_WBR_LOWR      = 'green'   # WBR 下側
#------------------------------------------------------------------------------
COLOR_VOL_BARS      = 'gray'    # VOL BAR
#------------------------------------------------------------------------------
BAR_WIDTH           = 0.6       # bar_width は連番なので固定でOK
#------------------------------------------------------------------------------

def create_fig      ( df_all, timeframe, bars=81, xrot=90, xsiz=8 ):
    #--------------------------------------------------------------------------
    df              = add_indicators(df_all)
    target          = bars # 81
    if len(df) >= target:
        df_draw     = df.iloc[-target:].copy()
    else:
        df_draw     = df.copy()                 # 足りないときはあるだけ描画
    df              = df_draw
    original_index  = df.index.copy()           # 元の日時 index を保持しておく
    df              = df.copy()
    df.reset_index  (drop=True, inplace=True)   # 描画用に index を 0〜n-1 の連番にする
    plt.style.use   ('default')
    n               = df.shape[0]
    x               = np.arange(n)              # 0,1,...,n-1
    fig, axes       = plt.subplots( 4,1,sharex=True,figsize=(10,8),gridspec_kw={'height_ratios':[3,2,2,1]} )
    ax_price, ax_macd, ax_wbr, ax_vol = axes
    #--------------------------------------------------------------------------
    # ---- ダークテーマ風のベース色 ----
    #--------------------------------------------------------------------------
    for ax in axes:
        ax.set_facecolor        (COLOR_BKGR)
        for spine in ax.spines.values():
            spine.set_color     (COLOR_SPIN)
        ax.tick_params          (colors=COLOR_TEXT)
        ax.yaxis.label.set_color(COLOR_TEXT)
    fig.patch.set_facecolor     (COLOR_BKGR)
    #--------------------------------------------------------------------------
    # 軸1: ローソク足 + BB
    #--------------------------------------------------------------------------
    plot_candles        (ax_price, df, up_color=COLOR_CAN_UPUP, down_color=COLOR_CAN_DOWN)
    ax_price.plot       (x, df['bb_mid'    ], color=COLOR_CAN_BAND, linewidth=1.0,   label='BB Mid')
    ax_price.plot       (x, df['bb_upper'  ], color=COLOR_CAN_UPER, linewidth=0.8,   label='+2σ')
    ax_price.plot       (x, df['bb_lower'  ], color=COLOR_CAN_LOWR, linewidth=0.8,   label='--2σ')
    ax_price.set_ylabel ('PRICE')
    leg_price       = ax_price.legend(loc='upper left', facecolor=COLOR_CAN_LEGF, framealpha=0.8, edgecolor=COLOR_CAN_LEGB)
    for text in leg_price.get_texts():
        text.set_color  (COLOR_CAN_LEGB)    # 凡例の文字は黒で
    ax_price.ticklabel_format           (style='plain', axis='y', useOffset=False)
    ax_price.yaxis.set_major_formatter  (mticker.FormatStrFormatter('%.2f'))
    ax_price.grid       (True, linestyle='-', color=COLOR_GRID,     linewidth=1.0,   alpha=0.4)
    #--------------------------------------------------------------------------
    # 軸2: MACD
    #--------------------------------------------------------------------------
    ax_macd.bar         (x, df['macd_hist' ], color=COLOR_MAC_BARS, width=BAR_WIDTH, label='Hist', alpha=0.5)
    ax_macd.plot        (x, df['macd'      ], color=COLOR_MAC_MACD, linewidth=1.5,   label='MACD')
    ax_macd.plot        (x, df['macd_sig'  ], color=COLOR_MAC_SIGN, linewidth=1.5,   label='Signal')
    ax_macd.axhline     (0, color=COLOR_GRID,                       linewidth=0.8)
    ax_macd.set_ylabel  ('MACD')
    ax_macd.legend      (loc='upper left', framealpha=0.8)
    ax_macd.grid        (True, linestyle='-', color=COLOR_GRID,     linewidth=1.0,   alpha=0.4)
    #--------------------------------------------------------------------------
    # 軸3: WBR + BB(補助)
    #--------------------------------------------------------------------------
    ax_wbr.plot         (x, df['wbr'       ], color=COLOR_WBR_PLOT, linewidth=2.0,   label='WBR')
    ax_wbr.axhline      (0, color=COLOR_GRID, linewidth=0.8)
    ax_wbr.set_ylabel   ('WBR')
    ax_wbr.grid         (True, linestyle='-', color=COLOR_GRID,     linewidth=1.0,   alpha=0.4)
    ax_wbr2             = ax_wbr.twinx()
    ax_wbr2.set_facecolor('none')
    for spine in ax_wbr2.spines.values():
        spine.set_color (COLOR_SPIN)   # ここで枠を揃える
    ax_wbr2.tick_params (colors=COLOR_TEXT)
    ax_wbr2.plot        (x, df['bb_mid'    ], color=COLOR_WBR_BAND, linewidth=1.5,   alpha=0.3)
    ax_wbr2.plot        (x, df['bb_upper'  ], color=COLOR_WBR_UPER, linewidth=1.0,   alpha=0.3)
    ax_wbr2.plot        (x, df['bb_lower'  ], color=COLOR_WBR_LOWR, linewidth=1.0,   alpha=0.3)
    #--------------------------------------------------------------------------
    # 軸4: Volume
    #--------------------------------------------------------------------------
    ax_vol.bar          (x, df['volume'    ], color=COLOR_VOL_BARS, width=BAR_WIDTH)
    ax_vol.set_ylabel   ('VOLUME')
    ax_vol.grid         (True, linestyle='-', color=COLOR_GRID    , linewidth=1.0,   alpha=0.4)
    #--------------------------------------------------------------------------
    # X軸スタイル適用（0〜n-1 前提、ラベルだけ original_index を参照）
    #--------------------------------------------------------------------------
    for ax in (ax_price, ax_macd, ax_wbr, ax_vol):
        apply_time_axis(ax, df, original_index, timeframe, xrot, xsiz)
    for ax in (ax_price, ax_macd, ax_wbr):
        for label in ax.get_xticklabels():
            label.set_visible(False)
    #--------------------------------------------------------------------------
    plt.tight_layout()
    return fig, (ax_price, ax_macd, ax_wbr, ax_vol)    

#------------------------------------------------------------------------------
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

# End of File -----------------------------------------------------------------
