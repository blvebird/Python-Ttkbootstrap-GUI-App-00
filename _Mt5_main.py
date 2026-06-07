# ! python
# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
#
# Spyder Editor
# Name          : _Mt5_main.py
# Purpose       : **
# Comment Lang  : JP
# Author        : Blve Bird
# Created Date  : 01/03/2026
# Version       : 0.0.0.1
#
#------------------------------------------------------------------------------
#==============================================================================
# Reference Sites
# [Mplfinance]
# https://note.nkmk.me/python-pandas-matplotlib-candlestick-chart/
# https://zenn.dev/arafipro/books/python-plotly-chart/viewer/python-plotly-chart-03
# https://plotly.com/python/candlestick-charts/
# https://stackoverflow.com/questions/69328751/how-to-display-a-mplfinance-chart-in-tkinter
# https://tzmi.hatenablog.com/entry/2020/01/25/131021
# https://qiita.com/code0327/items/c27472af808397bcd42b
# https://zenn.dev/neku/articles/46caa74515e605

#------------------------------------------------------------------------------
from   tkinter                 import filedialog
import tkinter                 as     tk
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
import seaborn                 as     sns
import statsmodels.api         as     sm
import pandas                  as     pd
import numpy                   as     np
import configparser
#------------------------------------------------------------------------------
import math
import sys
import time
import subprocess
import asyncio
import MetaTrader5             as     mt5
#------------------------------------------------------------------------------
from   sklearn.model_selection import train_test_split
from   sklearn.model_selection import GridSearchCV
from   sklearn.model_selection import StratifiedKFold
from   sklearn.model_selection import KFold
#------------------------------------------------------------------------------
import sklearn
from   sklearn.ensemble        import RandomForestRegressor
from   matplotlib              import rcParams
import matplotlib.pyplot       as     plt
from   matplotlib              import ticker
from   matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#------------------------------------------------------------------------------
import gc
import requests
import json
import time
import datetime
from   datetime                import datetime
import subprocess
import pytz
import mplfinance              as     mpf
#------------------------------------------------------------------------------
import plotly.graph_objects    as     go
import plotly.io               as     pio
from   datetime                import datetime
#------------------------------------------------------------------------------
from   _Mt5_grph               import create_fig, prepare_df_for_plot
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Global Variables
#------------------------------------------------------------------------------

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Global Variables
#
#
#------------------------------------------------------------------------------
#==============================================================================
timeframe_dict = {			
	mt5.TIMEFRAME_M1 :	60	, #
	mt5.TIMEFRAME_M2 :	120	,
	mt5.TIMEFRAME_M3 :	180	,
	mt5.TIMEFRAME_M4 :	240	,
	mt5.TIMEFRAME_M5 :	300	, #
	mt5.TIMEFRAME_M6 :	360	,
	mt5.TIMEFRAME_M10:	600	,
	mt5.TIMEFRAME_M12:	720	,
	mt5.TIMEFRAME_M15:	900	, #
	mt5.TIMEFRAME_M20:	1200	,
	mt5.TIMEFRAME_M30:	1800	, #
	mt5.TIMEFRAME_H1 :	3600	, #
	mt5.TIMEFRAME_H2 :	7200	,
	mt5.TIMEFRAME_H3 :	16200	,
	mt5.TIMEFRAME_H4 :	20160	, #
	mt5.TIMEFRAME_H6 :	32400	,
	mt5.TIMEFRAME_H8 :	43200	,
	mt5.TIMEFRAME_H12:	64800	,
	mt5.TIMEFRAME_D1 :	129600	, #
	mt5.TIMEFRAME_W1 :	604800	, #
	mt5.TIMEFRAME_MN1:	2592000	, #
}			

timeframe_numA = [
    mt5.TIMEFRAME_M1 , #  0#
    mt5.TIMEFRAME_M2 , #  1
    mt5.TIMEFRAME_M3 , #  2
    mt5.TIMEFRAME_M4 , #  3
    mt5.TIMEFRAME_M5 , #  4#
    mt5.TIMEFRAME_M6 , #  5
    mt5.TIMEFRAME_M10, #  6
    mt5.TIMEFRAME_M12, #  7
    mt5.TIMEFRAME_M15, #  8#
    mt5.TIMEFRAME_M20, #  9
    mt5.TIMEFRAME_M30, # 10#
    mt5.TIMEFRAME_H1 , # 11#
    mt5.TIMEFRAME_H2 , # 12
    mt5.TIMEFRAME_H3 , # 13
    mt5.TIMEFRAME_H4 , # 14#
    mt5.TIMEFRAME_H6 , # 15
    mt5.TIMEFRAME_H8 , # 16
    mt5.TIMEFRAME_H12, # 17
    mt5.TIMEFRAME_D1 , # 18#
    mt5.TIMEFRAME_W1 , # 19#
    mt5.TIMEFRAME_MN1, # 20#
]

timeframe_numB = [
     0,#mt5.TIMEFRAME_M1 , #  0#
    -1,#mt5.TIMEFRAME_M2 , #  1
    -1,#mt5.TIMEFRAME_M3 , #  2
    -1,#mt5.TIMEFRAME_M4 , #  3
     1,#mt5.TIMEFRAME_M5 , #  4#
    -1,#mt5.TIMEFRAME_M6 , #  5
    -1,#mt5.TIMEFRAME_M10, #  6
    -1,#mt5.TIMEFRAME_M12, #  7
     2,#mt5.TIMEFRAME_M15, #  8#
    -1,#mt5.TIMEFRAME_M20, #  9
     3,#mt5.TIMEFRAME_M30, # 10#
     4,#mt5.TIMEFRAME_H1 , # 11#
    -1,#mt5.TIMEFRAME_H2 , # 12
    -1,#mt5.TIMEFRAME_H3 , # 13
     5,#mt5.TIMEFRAME_H4 , # 14#
    -1,#mt5.TIMEFRAME_H6 , # 15
    -1,#mt5.TIMEFRAME_H8 , # 16
    -1,#mt5.TIMEFRAME_H12, # 17
     6,#mt5.TIMEFRAME_D1 , # 18#
     7,#mt5.TIMEFRAME_W1 , # 19#
     8,#mt5.TIMEFRAME_MN1, # 20#
]

timeMag     = 140
viewMag     =  81
symbol      = 'USDJPY'

#==============================================================================
#------------------------------------------------------------------------------
#
#
# MT5 Sub Function 1
# https://kirinote.com/python-process-getend/
#
#
#------------------------------------------------------------------------------
#==============================================================================
def mt5_close( mt5_EXE ):
    proc    = subprocess.Popen( 'tasklist', shell=True, stdout=subprocess.PIPE )
    flg     = False
    for line in proc.stdout:
        parts   = line.decode( 'shift-jis' ).split()
        if  mt5_EXE in parts:
            pid = int(parts[1])
            subprocess.call(['taskkill', '/F', '/PID', str(pid)])
            flg = True
    return  flg

#==============================================================================
#------------------------------------------------------------------------------
#
#
# MT5 Sub Function 2
# https://qiita.com/mimitaro/items/3506a444f325c6f980b2
#
#
#------------------------------------------------------------------------------
#==============================================================================
def mt5_config( fname ):
    # --------------------------------------------------
    # configparserの宣言とiniファイルの読み込み
    # --------------------------------------------------
    config_ini      = configparser.ConfigParser()
    config_ini.read ( fname, encoding='utf-8' )
    var1            = int( config_ini['DEFAULT']['mt5_ID'] )
    var2            = str( config_ini['DEFAULT']['mt5_SV'] )
    var3            = str( config_ini['DEFAULT']['mt5_PW'] )
    return var1, var2, var3

#==============================================================================
#------------------------------------------------------------------------------
#
#
# MT5 Sub Function 3
#
# tFm: timeframe
# tNm: timeframe_dict[tFm]*timeMag
#
#
#------------------------------------------------------------------------------
#==============================================================================
def update_chart ( parent, interval, tNm, tFm, count, photoimage0 ):
    #--------------------------------------------------------------------------
    # Spyderに表示される svg, browser, png
    pio.renderers.default   = 'svg'
    # 期間を指定    
    rates           = mt5.copy_rates_from_pos( symbol, tFm, 0, 1 )
    menu_top        = parent.menuTOP
    if  rates is None or len(rates)==0 :
        #
        # ERROR: LoginできていないorMT5アプリが閉じられた
        #
        #----------------------------------------------------------------------
        #######################################################################
        msg = (
            f'[STOP 3] Data acquisition failed. ' # MT5 CHART ERROR
            f'{parent.CAN0id}'
        )
        parent.Stext0.text.config( state='normal'   )
        parent.Stext0.insert( END, msg+'\n' )
        parent.Stext0.see   ( END )
        parent.Stext0.text.config( state='disabled' )
        #######################################################################
        #----------------------------------------------------------------------
        if  parent.CAN0id is not None:
            parent.Canvs0.after_cancel( parent.CAN0id )
        parent.mt5_FLG_CHT  = False
        parent.mt5_FLG_EXE  = False
        parent.mt5_FLG_LIN  = False
        parent.CAN0id       = None
        parent.Buttn_TL02.config( image=photoimage0 )
        menu_top.chrt_menu.entryconfig( menu_top.idx_chart, image=menu_top.mt5C_img ) # メニュー画像をfinance   アイコンに変更
    else:
        tSx                 = pd.to_datetime( (rates['time'][0]-tNm), unit='s' )
        tEx                 = pd.to_datetime( (rates['time'][0]    ), unit='s' )
        # UTC形式でデータ抽出期間を指定    
        timezone            = pytz.timezone("Etc/UTC")
        date_from           = datetime( tSx.year, tSx.month, tSx.day, tSx.hour, tSx.minute, tSx.second, 0, tzinfo=timezone ) #2024/6/5 0:00
        date_to             = datetime( tEx.year, tEx.month, tEx.day, tEx.hour, tEx.minute, tEx.second, 0, tzinfo=timezone ) #2024/6/5 0:10    
        # データを抽出する処理
        ticks               = mt5.copy_rates_range( symbol, tFm, date_from, date_to )
        if  ticks is None or len(ticks)==0 :
            #
            # ERROR: LoginできていないorMT5アプリが閉じられた
            #
            #------------------------------------------------------------------
            ###################################################################
            msg = (
                f'[STOP 4] Data acquisition failed. ' # MT5 CHART ERROR
                f'{parent.CAN0id}'
            )
            parent.Stext0.text.config( state='normal'   )
            parent.Stext0.insert( END, msg+'\n' )
            parent.Stext0.see   ( END )
            parent.Stext0.text.config( state='disabled' )
            ###################################################################
            #------------------------------------------------------------------
            if  parent.CAN0id is not None:
                parent.Canvs0.after_cancel( parent.CAN0id )
            parent.mt5_FLG_EXE  = False
            parent.mt5_FLG_LIN  = False
            parent.mt5_FLG_CHT  = False
            parent.CAN0id       = None
            parent.Buttn_TL02.config( image=photoimage0 )
            menu_top.chrt_menu.entryconfig( menu_top.idx_chart, image=menu_top.mt5C_img ) # メニュー画像をfinance   アイコンに変更
        else:
            #
            # 取得したデータをPandasデーターフレーム(df)に変換
            # 日時データを年月日時分秒の表示形式に変換
            #
            df              = pd.DataFrame( ticks )
            df['time']      = pd.to_datetime(df['time'], unit='s')
            df.drop         (columns=['spread', 'real_volume'], inplace=True)
            df.rename       (columns={'tick_volume': 'volume'}, inplace=True)
            df.set_index    ('time', inplace=True)
            #NMP            = df.to_numpy() # NP[hour*minuite][5]
            #CLS            = NMP[:,3]      # Close
            buf             = io.BytesIO()  # bufferを用意
            #------------------------------------------------------------------
            ###################################################################

            
            FIG, ax         = create_fig( df, tFm, viewMag, 0, 8 )
            

            ###################################################################
            #------------------------------------------------------------------            
            buf = io.BytesIO()
            FIG.savefig(buf, format="png", dpi=100, bbox_inches="tight")
            plt.close(FIG)
            buf.seek(0)
            #------------------------------------------------------------------
            #FIG.savefig     ( buf, format='png' )       # bufferに保持
            enc             = np.frombuffer( buf.getvalue(), dtype=np.uint8 ) # bufferからの読み出し
            dst             = cv2.imdecode ( enc, 1 )   # デコード
            dst             = cv2.resize( dst,(800,600),interpolation=cv2.INTER_LANCZOS4 )
            dst             = dst[:,:,::-1]             # BGR->RGB
            #------------------------------------------------------------------
            img             = Image.fromarray( dst )
            parent.img1     = img
            canvas_w        = parent.Canvs0.winfo_width ()
            canvas_h        = parent.Canvs0.winfo_height()
            pil_img         = ImageOps.pad(img, (canvas_w, canvas_h))
            parent.tk_img   = ImageTk.PhotoImage(image=pil_img)
            parent.Canvs0.create_image( canvas_w//2, canvas_h//2, image=parent.tk_img, tag='Photo' )
            #------------------------------------------------------------------
            FIG.clear() 
            plt.close() # https://qiita.com/code0327/items/c27472af808397bcd42b
            del( df  )
            #del( NMP )
            #del( CLS )
            del( FIG )
            del( buf )
            del( enc )
            del( dst )
            del( img )
            del( pil_img )
            #------------------------------------------------------------------
            # Canvas更新
            parent.Canvs0.update()
            #------------------------------------------------------------------
            # 既存の予約があればまずキャンセル??
            #------------------------------------------------------------------
            if  parent.CAN0id is not None:
                parent.Canvs0.after_cancel( parent.CAN0id )
                tFm     = timeframe_numA [parent.mt5_NUM_BTC]   # mt5_NUM_BTC:0~20
                tNm     = (timeframe_dict[tFm])*timeMag         # hour*minuite*sec
            #------------------------------------------------------------------
            # 新しく予約してそのIDを必ず保持
            #------------------------------------------------------------------
            if  parent.mt5_BTL02_PUSH == True: # BTL02が押された状態だったら
                parent.CAN0id   = parent.Canvs0.after ( interval, lambda:update_chart( parent, interval, tNm, tFm, count, photoimage0 ) )
            #------------------------------------------------------------------
            ###################################################################
            msg     = (
                f'[UPDATE] '
                f'{parent.CAN0id} '
                f'{count:06d} '
                f'{tNm} '
                f'{tFm} '
                f'{parent.mt5_FLG_CHT} '
                f'{parent.mt5_FLG_BTC} '
                f'{parent.mt5_NUM_BTC}'
            )
            parent.Stext0.text.config( state='normal'   )
            parent.Stext0.insert( END, msg+'\n' )
            parent.Stext0.see   ( END )
            parent.Stext0.text.config( state='disabled' )
            ###################################################################
            #------------------------------------------------------------------
            count = count + 1
            
#==============================================================================
#------------------------------------------------------------------------------
#
#
# MT5_main Function
# MT5 GREEN CHART button pressed
#
#
#------------------------------------------------------------------------------
#==============================================================================
class MT5_data( ttk.Frame ):
    def __init__( self, parent ):
        super().__init__ ( parent )
        self.parent     = parent            # 親を保持しておく
        
    def make_chart( self ):                 # MT5 Chart ボタンが押された
        parent          = self.parent       # 短い別名にすると読みやすい
        menu_top        = parent.menuTOP
        #----------------------------------------------------------------------
        if  parent.mt5_FLG_CHT == False:    # 再突入防止
            parent.mt5_FLG_CHT  = True      # 再突入防止
            #------------------------------------------------------------------
            if( parent.mt5_FLG_EXE==True and parent.mt5_FLG_LIN==True ):
                #--------------------------------------------------------------
                count   = 0
                tFm     = timeframe_numA[ parent.mt5_NUM_BTC ] # mt5_NUM_BTC:0~20
                tNm     = (timeframe_dict[tFm])*timeMag # hour*minuite*sec
                interV  = (timeframe_dict[tFm])*1000//4 # sec*1000[ms]
                if  parent.CAN0id is not None:
                    parent.mt5_BTL02_PUSH   = False
                    parent.Canvs0.after_cancel( parent.CAN0id )
                    #----------------------------------------------------------
                    ###########################################################
                    msg     = (
                        f'[STOP 0] ' # MT5 CHART PAUSED
                        f'{parent.CAN0id} '
                        f'{parent.mt5_FLG_CHT} '
                        f'{parent.mt5_FLG_BTC} '
                        f'{parent.mt5_NUM_BTC}'
                    )
                    parent.Stext0.text.config( state='normal'   )
                    parent.Stext0.insert( END, msg+'\n' )
                    parent.Stext0.see   ( END )
                    parent.Stext0.text.config( state='disabled' )
                    ###########################################################
                    #----------------------------------------------------------
                    parent.CAN0id           = None
                    parent.Buttn_TL02.config( image=parent.bti0 ) # Green
                    menu_top.chrt_menu.entryconfig( menu_top.idx_chart, image=menu_top.mt5C_img ) # メニュー画像をfinance   アイコンに変更
                else:
                    parent.mt5_BTL02_PUSH   = True
                    parent.Buttn_TL02.config( image=parent.bti1 ) # Orange
                    menu_top.chrt_menu.entryconfig( menu_top.idx_chart, image=menu_top.mt5D_img ) # メニュー画像をpause/stopアイコンに変更
                    #----------------------------------------------------------
                    ###########################################################
                    msg     = (
                        f'UPDATE CHART '
                        f'{parent.CAN0id} '
                        f'{parent.mt5_FLG_CHT} '
                        f'{parent.mt5_FLG_BTC} '
                        f'{parent.mt5_NUM_BTC}'
                    )
                    parent.Stext0.text.config( state='normal'   )
                    parent.Stext0.insert( END, msg+'\n' )
                    parent.Stext0.see   ( END )
                    parent.Stext0.text.config( state='disabled' )
                    ###########################################################
                    #----------------------------------------------------------
                    update_chart ( parent, interV, tNm, tFm, count, parent.bti0 ) # Green
                #--------------------------------------------------------------
            else:
                #--------------------------------------------------------------
                ###############################################################
                msg     = (
                    'Please launch MT5 application and login.'
                )
                parent.Stext0.text.config( state='normal'   )
                parent.Stext0.insert( END, msg+'\n' )
                parent.Stext0.see   ( END )
                parent.Stext0.text.config( state='disabled' )
                ###############################################################
                #--------------------------------------------------------------
                parent.Buttn_TL02.config( image=parent.bti0 ) # Green
                menu_top.chrt_menu.entryconfig( menu_top.idx_chart, image=menu_top.mt5C_img ) # メニュー画像をfinance   アイコンに変更
            #------------------------------------------------------------------
            parent.mt5_FLG_CHT  = False
        #----------------------------------------------------------------------

#==============================================================================
#------------------------------------------------------------------------------
#
#
# MT5_main Function
# MT5 BLUE button pressed
#
#
#------------------------------------------------------------------------------
#==============================================================================
class MT5_main( ttk.Frame ):
    def __init__( self, parent ):
        super().__init__ ( parent )
        self.parent     = parent                # 親を保持しておく
    #--------------------------------------------------------------------------
    # @staticmethod
    # MT5_main のインスタンスを作らず、クラスから直接呼ぶ
    # インスタンスを作って self を使いたい場合は外してシグネチャと呼び出し方を変える
    # def mt5_timef( self, menu_top, parent, tt ):
    # 第一引数に self 追加
    # mt5 = MT5_main(parent)
    # mt5.mt5_timef(menu_top=self.menu_top, parent=parent, tt=0)
    #--------------------------------------------------------------------------
    #@staticmethod
    def mt5_timef( self, tt ):                  # MT5 青ボタンが押された tt:0~20
        parent          = self.parent           # 短い別名にすると読みやすい
        menu_top        = parent.menuTOP
        if( tt!=parent.mt5_NUM_BTC ): # tt:0~20
            #------------------------------------------------------------------
            if  parent.mt5_FLG_BTC == False:    # 再突入防止
                parent.mt5_FLG_BTC  = True      # 再突入防止
                #--------------------------------------------------------------
                # 一旦 OFF色 点灯
                #--------------------------------------------------------------
                vv                  = parent.mt5_NUM_BTC # 0~20
                # mt5_NUM_BTC 更新
                parent.mt5_NUM_BTC  = tt
                uu                  = timeframe_numB[vv] # -1,0,4,8,10,11,14,18,19,20
                if  uu>=0: parent.Buttn_TC[uu].config( image=parent.bti2 )  # Blue
                #--------------------------------------------------------------
                if( parent.mt5_FLG_EXE == True and parent.mt5_FLG_LIN == True ):
                    count   = 0
                    tFm     = timeframe_numA [parent.mt5_NUM_BTC]   # mt5_NUM_BTC:0~20
                    tNm     = (timeframe_dict[tFm])*timeMag         # hour*minuite*sec
                    interV  = (timeframe_dict[tFm])*1000//4         # sec*1000[ms]
                    if  parent.CAN0id is not None:
                        parent.Canvs0.after_cancel( parent.CAN0id )
                        #------------------------------------------------------
                        #######################################################
                        msg     = (
                            f'[STOP 1] ' # TIMEFRAME CHANGED
                            f'{parent.CAN0id} '
                            f'{parent.mt5_FLG_CHT} '
                            f'{parent.mt5_FLG_BTC} '
                            f'{parent.mt5_NUM_BTC}'
                        )
                        parent.Stext0.text.config( state='normal'   )
                        parent.Stext0.insert( END, msg+'\n' )
                        parent.Stext0.see   ( END )
                        parent.Stext0.text.config( state='disabled' )
                        #######################################################
                        #------------------------------------------------------
                        parent.CAN0id   = None
                        update_chart ( parent, interV, tNm, tFm, count, parent.bti0 ) # Green
                    else:
                        #------------------------------------------------------
                        #######################################################
                        msg     = (
                            f'TIMEFRAME changed -- '
                            f'{parent.mt5_NUM_BTC}'
                        )
                        parent.Stext0.text.config( state='normal'   )
                        parent.Stext0.insert( END, msg+'\n' )
                        parent.Stext0.see   ( END )
                        parent.Stext0.text.config( state='disabled' )
                        #######################################################
                        #------------------------------------------------------
                #--------------------------------------------------------------
                # 改めて ON色 点灯
                #--------------------------------------------------------------
                uu                  = timeframe_numB[tt] # 0,4,8,10,11,14,18,19,20
                if  uu>=0: parent.Buttn_TC[uu].config( image=parent.bti1 )  # Orange
                # ここで MenuTOP の timf を変更
                menu_top.timf.set( tt )
                #--------------------------------------------------------------
                parent.mt5_FLG_BTC  = False
            #------------------------------------------------------------------

    def mt5_login( self ):
        parent              = self.parent           # 短い別名にすると読みやすい
        parent.mt5_ID, parent.mt5_SV, parent.mt5_PW = mt5_config( parent.mt5_INI ) # Read .ini file
        mt5ret              = mt5.initialize( login=parent.mt5_ID, server=parent.mt5_SV, password=parent.mt5_PW )
        parent.mt5_FLG_EXE  = True
        if  mt5ret == True:
            # https://stackoverflow.com/questions/78880486/how-to-change-the-state-of-a-ttkbootstrap-scrolledtext-widget-after-creation
            #------------------------------------------------------------------
            ###################################################################
            parent.Stext0.text.config( state='normal'   )
            if  parent.mt5_FLG_LIN==True:
                parent.Stext0.insert( END, 'Aren\'t you already logged in? :-)\n' )
            msg     = (
                'mt5_login__, mt5_FLG_EXE=mt5_FLG_LIN=True'
            )
            parent.Stext0.insert( END, msg+'\n' )
            parent.Stext0.see   ( END )
            parent.Stext0.text.config( state='disabled' )
            ###################################################################
            #------------------------------------------------------------------
            parent.mt5_FLG_LIN  = True
        else:
            #------------------------------------------------------------------
            ###################################################################
            msg     = str( mt5.last_error() )
            parent.Stext0.text.config( state='normal'   )
            parent.Stext0.insert( END, msg+'\n' )
            msg     = (
                'mt5_login__, mt5_FLG_EXE=True,mt5_FLG_LIN=False'
            )
            parent.Stext0.insert( END, msg+'\n' )
            parent.Stext0.text.config( state='disabled' )
            ###################################################################
            #------------------------------------------------------------------
            parent.mt5_FLG_LIN  = False
        
    def mt5_sdown( self ):
        parent              = self.parent           # 短い別名にすると読みやすい
        menu_top            = parent.menuTOP
        if  parent.mt5_FLG_EXE == True:
            #------------------------------------------------------------------
            ###################################################################
            # 接続状態、サーバ名、取引口座に関するデータを表示する
            msg     = str( mt5.terminal_info() )
            parent.Stext0.text.config( state='normal'   )
            parent.Stext0.insert( END, msg+'\n' )
            parent.Stext0.see   ( END )
            parent.Stext0.text.config( state='disabled' )
            ###################################################################
            #------------------------------------------------------------------
            ###################################################################
            # MetaTrader 5バージョンについてのデータを表示する
            msg     = str( mt5.version() )
            parent.Stext0.text.config( state='normal'   )
            parent.Stext0.insert( END, msg+'\n' )
            parent.Stext0.see   ( END )
            parent.Stext0.text.config( state='disabled' )
            ###################################################################
            #------------------------------------------------------------------
            # MetaTrader 5ターミナルへの接続をシャットダウンする
            mt5.shutdown()
            ret = mt5_close( parent.mt5_EXE )
            #------------------------------------------------------------------
            ###################################################################
            parent.Stext0.text.config( state='normal'   )
            if  ret==False:
                parent.Stext0.insert( END, 'No application is running(0).\n' )
            msg     = (
                'mt5_sdown__, mt5_FLG_EXE=mt5_FLG_LIN=False'
            )
            parent.Stext0.insert( END, msg+'\n' )
            parent.Stext0.see   ( END )
            parent.Stext0.text.config( state='disabled' )
            ###################################################################
            #------------------------------------------------------------------
            ###################################################################
            msg     = (
                f'[STOP 2] MT5 application terminated. '  # MT5 APPLICATION TERMINATED
                f'{parent.CAN0id}'
            )
            parent.Stext0.text.config( state='normal'   )
            parent.Stext0.insert( END, msg+'\n' )
            parent.Stext0.see   ( END )
            parent.Stext0.text.config( state='disabled' )
            ###################################################################
            #------------------------------------------------------------------
            if  parent.CAN0id is not None:
                parent.Canvs0.after_cancel( parent.CAN0id )
            parent.mt5_FLG_EXE  = False
            parent.mt5_FLG_LIN  = False
            parent.mt5_FLG_CHT  = False
            parent.CAN0id       = None
            parent.Buttn_TL02.config( image=parent.bti0 )
            menu_top.chrt_menu.entryconfig( menu_top.idx_chart, image=menu_top.mt5C_img ) # メニュー画像をfinance   アイコンに変更
        else:
            #------------------------------------------------------------------
            ###################################################################
            msg     = (
                'No application is running(1).'
            )
            parent.Stext0.text.config( state='normal'   )
            parent.Stext0.insert( END, msg+'\n' )
            parent.Stext0.see   ( END )
            parent.Stext0.text.config( state='disabled' )
            ###################################################################
            #------------------------------------------------------------------

#------------------------------------------------------------------------------

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
