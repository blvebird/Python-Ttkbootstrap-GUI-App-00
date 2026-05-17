# ! python
# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
#
# Spyder Editor
# Name          : _Cyg_main.py
# Purpose       : **
# Comment Lang  : JP
# Author        : Blve Bird
# Created Date  : 01/03/2026
# Version       : 0.0.0.1
#
#------------------------------------------------------------------------------
#==============================================================================
# Reference Sites
# [Common]
# https://www.youtube.com/watch?v=3VW8zbTHakI
# https://github.com/clear-code-projects/tkinter-complete/blob/main/3%20style/3_5_2_ttkbootstrap_conversion.py
# https://www.xanthium.in/short-concise-tutorial-python-gui-design-using-tkinter-ttkbootstrap-beginners
# https://imagingsolution.net/program/python/tkinter/canvas_draw_image/

#------------------------------------------------------------------------------
from   tkinter                 import filedialog
import tkinter                 as     tk
import ttkbootstrap            as     ttk
from   ttkbootstrap            import Style
from   ttkbootstrap.dialogs    import Messagebox
from   ttkbootstrap.widgets.scrolled import ScrolledText
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
#------------------------------------------------------------------------------
import math
import sys
import time
import subprocess
import asyncio
import MetaTrader5             as mt5
#------------------------------------------------------------------------------
import _Cyg_conf
from   _Mt5_main               import MT5_main, MT5_data
from   _Cyg_sub0               import MainMC0, MainMC1, Image_loader, resize_window_big, resize_window_def, resize_window_full, show_message1, load_inverted_icon
from   _Cyg_help               import AboutDialog
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Global Variables
#------------------------------------------------------------------------------

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Window Application
#
#
#------------------------------------------------------------------------------
#==============================================================================
class Application( ttk.Window ):
    def __init__( self, title, size ):
        #----------------------------------------------------------------------
        # Main Setup
        super().__init__( themename=_Cyg_conf.Main_them )
        self.title( title )
        self.geometry( f'{size[0]}x{size[1]}+{size[2]}+{size[3]}' )
        self.minsize ( size[0], size[1] )
        #self.focus_force()
        self.focus()
        #----------------------------------------------------------------------
        self.padx       = _Cyg_conf.Grid_padx
        self.pady       = _Cyg_conf.Grid_pady
        self.BtpadA     = _Cyg_conf.Butt_padA
        #----------------------------------------------------------------------
        # Global Variables
        self.LBL2id     = None # 時計用
        self.CAN0id     = None # Canvas用
        #----------------------------------------------------------------------
        A               = _Cyg_conf.Size_A
        B               = _Cyg_conf.Size_B
        self.iF1_relx   = 0
        self.iF1_rely   = 0
        self.iF1_rwid   = A
        self.iF1_rhei   = B
        #----------------------------------------------------------------------
        self.iF2_relx   = A
        self.iF2_rely   = 0
        self.iF2_rwid   = 1-A
        self.iF2_rhei   = B
        #----------------------------------------------------------------------
        self.iF3_relx   = 0
        self.iF3_rely   = B
        self.iF3_rwid   = 1
        self.iF3_rhei   = 1-B
        #----------------------------------------------------------------------
        # Black Image
        npimg           = np.full((150,200),16)
        self.img1       = Image.fromarray( npimg )
        self.img2       = Image.fromarray( npimg )
        self.img3       = Image.fromarray( npimg )
        del( npimg )
        #----------------------------------------------------------------------
        # Button Images
        photo           = ttk.PhotoImage(file = './_images/_button00.png') # Green
        self.bti0       = photo.subsample(3,3)
        photo           = ttk.PhotoImage(file = './_images/_button01.png') # Orange
        self.bti1       = photo.subsample(3,3)
        photo           = ttk.PhotoImage(file = './_images/_button02.png') # Blue
        self.bti2       = photo.subsample(3,3)
        #----------------------------------------------------------------------
        # MT5 Configuration
        self.mt5_EXE        = _Cyg_conf.mt5_EXE         # 'terminal64.exe'
        self.mt5_FLG_EXE    = _Cyg_conf.mt5_FLG_EXE     # False
        self.mt5_FLG_LIN    = _Cyg_conf.mt5_FLG_LIN     # False
        self.mt5_FLG_CHT    = _Cyg_conf.mt5_FLG_CHT     # False
        self.mt5_FLG_BTC    = _Cyg_conf.mt5_FLG_BTC     # False
        self.mt5_NUM_BTC    = _Cyg_conf.mt5_NUM_BTC     # Default: 0
        self.mt5_BTL02_PUSH = _Cyg_conf.mt5_BTL02_PUSH  # BTL02 pushed or not
        self.mt5_INI        = _Cyg_conf.mt5_INI         # '_Mt5_info.ini'
        #----------------------------------------------------------------------
        self.mt5_data       = MT5_data(self)            # ここでインスタンスを作っておく
        self.mt5_main       = MT5_main(self)            # ここでインスタンスを作っておく
        #----------------------------------------------------------------------
        # Button Style Setting
        app_style       = ttk.Style()
        app_style.configure( 'TButton', font=("Helvetica",6), anchor='center', compound='top', justify='center' )
        #----------------------------------------------------------------------
        # Some SEttings
        self.styTOP     = _Cyg_conf.styTOP
        self.styBTN     = _Cyg_conf.styBTN
        self.styBT0     = _Cyg_conf.styBT0
        self.styBT1     = _Cyg_conf.styBT1
        self.styML0     = _Cyg_conf.styML0
        self.styML1     = _Cyg_conf.styML1
        self.styMR0     = _Cyg_conf.styMR0
        self.styMR1     = _Cyg_conf.styMR1
        self.styMC0     = _Cyg_conf.styMC0
        self.styMC1     = _Cyg_conf.styMC1
        #----------------------------------------------------------------------
        # Some Widgets
        self.menuTOP    = MenuTOP( self )           # Top    Menu
        self.config     ( menu=self.menuTOP )       # ここで初めて「ウィンドウ上部のメニューバー」として認識される
        self.mainTOP    = MainTOP( self )           # Top    Left
        self.mainBTM    = MainBTM( self )           # Bottom Left
        self.mainML0    = MainML0( self )           # Middle Left
        self.mainMR0    = MainMR0( self )           # Middle Right
        self.mainMC0    = MainMC0( self )           # Middle Center 1
        self.mainMC1    = MainMC1( self )           # Middle Center 2
        #----------------------------------------------------------------------
        # Termination
        self.protocol( "WM_DELETE_WINDOW", self.on_closing )
        
    def on_closing  ( self ):
        #print( "TERMINATED1", self.LBL2id )
        #onemore = Messagebox.yesno( "Check Termination: Yes or No", "TTKBootstrap" )
        #onemore = messagebox.askyesno( 'Check Termination', '本当に終了しますか？' )
        #if onemore=="Yes":
            # 完了ダイアログを出す
            # messagebox.showinfo('', '完了！！')
            # rootを破棄（これでmainloopを抜けるはず）
            #print( id )
            #time.sleep(2.0)
            #task = self.Label3.after_cancel
        if( self.LBL2id is not None ):
            self.Label3.after_cancel( self.LBL2id )
            self.LBL2id = None # RESET
        if( self.CAN0id is not None ):
            self.Canvs0.after_cancel( self.CAN0id )
            self.CAN0id = None
        try:
            if  self.mt5_FLG_EXE == True:
                self.mt5_main.mt5_sdown ()
        finally:
            self.destroy()

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Main Menu
# https://stackoverflow.com/questions/79594723/pyhton-ttkbootstrap-menu-style-not-applied
#
# ::File
# ::View
# ::Charts
# ::Window
# ::Help
#
#------------------------------------------------------------------------------
#==============================================================================
class MenuTOP( tk.Menu ):
    def __init__( self, parent ):
        #----------------------------------------------------------------------
        #
        # Create menu with theme colors
        #
        #----------------------------------------------------------------------
        menu_style  = {
            "background":       parent.style.colors.bg,
            "foreground":       parent.style.colors.fg,
            "activebackground": parent.style.colors.selectbg,
            "activeforeground": parent.style.colors.selectfg
        }
        #----------------------------------------------------------------------
        #
        # 画像はインスタンス変数で保持する
        #
        #----------------------------------------------------------------------
        self.open_img   = load_inverted_icon( './_images/_open.png', (24, 24), 1 )
        self.exit_img   = load_inverted_icon( './_images/_exit.png', (24, 24), 1 )
        self.warn_img   = load_inverted_icon( './_images/_warn.png', (24, 24), 1 )
        self.grph_img   = load_inverted_icon( './_images/_grph.png', (24, 24), 1 )
        self.siz0_img   = load_inverted_icon( './_images/_siz0.png', (24, 24), 1 )
        self.siz1_img   = load_inverted_icon( './_images/_siz1.png', (24, 24), 1 )
        self.siz2_img   = load_inverted_icon( './_images/_siz2.png', (24, 24), 1 )
        self.info_img   = load_inverted_icon( './_images/_info.png', (24, 24), 1 )
        self.mt5A_img   = load_inverted_icon( './_images/_mt5A.png', (24, 24), 1 )
        self.mt5B_img   = load_inverted_icon( './_images/_mt5B.png', (24, 24), 1 )
        self.mt5C_img   = load_inverted_icon( './_images/_mt5C.png', (24, 24), 1 ) # CHART
        self.mt5D_img   = load_inverted_icon( './_images/_mt5D.png', (24, 24), 1 ) # PAUSE
        self.mt5E_img   = load_inverted_icon( './_images/_mt5E.png', (24, 24), 1 ) # CLOCK
        #----------------------------------------------------------------------
        #
        # 自分自身をメニューバーとして初期化
        #
        #----------------------------------------------------------------------
        super().__init__( parent, **menu_style )
        
        #======================================================================
        #----------------------------------------------------------------------
        #
        # File Menu File Menu File Menu File Menu File Menu File Menu File Menu
        #
        #----------------------------------------------------------------------
        #======================================================================
        self.file_menu  = tk.Menu   ( self, tearoff= False, **menu_style )
        self.add_cascade            ( label="File" ,           menu=self.file_menu, underline=0 )
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        self.file_menu.add_command  ( label="Open" ,           command=lambda:Image_loader(parent), accelerator="Ctrl+O", image=self.open_img, compound='left' )
        # Bind the CTRL+O shortcut to the `Image_loader()` function.
        # https://syschill.com/engineering/post-217/
        # https://pythonassets.com/posts/menubar-in-tk-tkinter/
        parent.bind_all             ( "<Control-o>", lambda _: Image_loader(parent) )
        #----------------------------------------------------------------------
        self.file_menu.add_separator()
        #----------------------------------------------------------------------
        self.file_menu.add_command  ( label='Exit' ,           command=parent.on_closing, image=self.exit_img, compound='left' )
        #----------------------------------------------------------------------
        
        #======================================================================
        #----------------------------------------------------------------------
        #
        # View Menu View Menu View Menu View Menu View Menu View Menu View Menu
        #
        #----------------------------------------------------------------------
        #======================================================================
        self.view_menu  = tk.Menu   ( self, tearoff= False, **menu_style )
        self.add_cascade            ( label="View"           , menu=self.view_menu, underline=0 )
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        self.view_menu.add_command  ( label='Color Themes...', command=lambda:show_message1( parent ), image=self.warn_img, compound='left' )
        #----------------------------------------------------------------------
        self.view_menu.add_separator()
        #----------------------------------------------------------------------
        self.view_menu.add_command  ( label='Status Bar...'  , command=lambda:show_message1( parent ), image=self.warn_img, compound='left' )
        #----------------------------------------------------------------------
        
        #======================================================================
        #----------------------------------------------------------------------
        #
        # Chrt Menu Chrt Menu Chrt Menu Chrt Menu Chrt Menu Chrt Menu Chrt Menu
        #
        #----------------------------------------------------------------------
        #======================================================================
        self.chrt_menu  = tk.Menu   ( self, tearoff= False, **menu_style )
        self.add_cascade            ( label="Charts"    ,      menu=self.chrt_menu, underline=0 )
        #----------------------------------------------------------------------

        #----------------------------------------------------------------------
        self.chrt_menu.add_command  ( label='MT5 Open ',       command=parent.mt5_main.mt5_login , image=self.mt5A_img, compound='left' ) # MT5 Open   ボタンが押された
        self.chrt_menu.add_command  ( label='MT5 Close',       command=parent.mt5_main.mt5_sdown , image=self.mt5B_img, compound='left' ) # MT5 Cloase ボタンが押された
        self.chrt_menu.add_command  ( label='MT5 Chart',       command=parent.mt5_data.make_chart, image=self.mt5C_img, compound='left' ) # MT5 Chart  ボタンが押された
        self.idx_chart  = 2 # 必要ならインデックスを記録しておく
        #----------------------------------------------------------------------
        self.chrt_menu.add_separator()
        #----------------------------------------------------------------------
        self.timf_menu  = tk.Menu   ( self, tearoff= False, **menu_style )
        #----------------------------------------------------------------------
        self.chrt_menu.add_cascade  ( label='Timeframes',      menu=self.timf_menu, underline=0  , image=self.mt5E_img, compound='left' )
        self.timf   = tk.IntVar     ( parent ) # ここが重要: インスタンス変数にする
        self.timf.set( 0 ) # Default timeframe ("M01".)
        self.timf_menu.add_radiobutton( label='M01', variable=self.timf, value= 0, command=lambda:parent.mt5_main.mt5_timef( tt= 0 ) )
        self.timf_menu.add_radiobutton( label='M02', variable=self.timf, value= 1, command=lambda:parent.mt5_main.mt5_timef( tt= 1 ) )
        self.timf_menu.add_radiobutton( label='M03', variable=self.timf, value= 2, command=lambda:parent.mt5_main.mt5_timef( tt= 2 ) )
        self.timf_menu.add_radiobutton( label='M04', variable=self.timf, value= 3, command=lambda:parent.mt5_main.mt5_timef( tt= 3 ) )
        self.timf_menu.add_radiobutton( label='M05', variable=self.timf, value= 4, command=lambda:parent.mt5_main.mt5_timef( tt= 4 ) )
        self.timf_menu.add_radiobutton( label='M06', variable=self.timf, value= 5, command=lambda:parent.mt5_main.mt5_timef( tt= 5 ) )
        self.timf_menu.add_radiobutton( label='M10', variable=self.timf, value= 6, command=lambda:parent.mt5_main.mt5_timef( tt= 6 ) )
        self.timf_menu.add_radiobutton( label='M12', variable=self.timf, value= 7, command=lambda:parent.mt5_main.mt5_timef( tt= 7 ) )
        self.timf_menu.add_radiobutton( label='M15', variable=self.timf, value= 8, command=lambda:parent.mt5_main.mt5_timef( tt= 8 ) )
        self.timf_menu.add_radiobutton( label='M20', variable=self.timf, value= 9, command=lambda:parent.mt5_main.mt5_timef( tt= 9 ) )
        self.timf_menu.add_radiobutton( label='M30', variable=self.timf, value=10, command=lambda:parent.mt5_main.mt5_timef( tt=10 ) )
        self.timf_menu.add_radiobutton( label='H01', variable=self.timf, value=11, command=lambda:parent.mt5_main.mt5_timef( tt=11 ) )
        self.timf_menu.add_radiobutton( label='H02', variable=self.timf, value=12, command=lambda:parent.mt5_main.mt5_timef( tt=12 ) )
        self.timf_menu.add_radiobutton( label='H03', variable=self.timf, value=13, command=lambda:parent.mt5_main.mt5_timef( tt=13 ) )
        self.timf_menu.add_radiobutton( label='H04', variable=self.timf, value=14, command=lambda:parent.mt5_main.mt5_timef( tt=14 ) )
        self.timf_menu.add_radiobutton( label='H06', variable=self.timf, value=15, command=lambda:parent.mt5_main.mt5_timef( tt=15 ) )
        self.timf_menu.add_radiobutton( label='H08', variable=self.timf, value=16, command=lambda:parent.mt5_main.mt5_timef( tt=16 ) )
        self.timf_menu.add_radiobutton( label='H12', variable=self.timf, value=17, command=lambda:parent.mt5_main.mt5_timef( tt=17 ) )
        self.timf_menu.add_radiobutton( label='D01', variable=self.timf, value=18, command=lambda:parent.mt5_main.mt5_timef( tt=18 ) )
        self.timf_menu.add_radiobutton( label='W01', variable=self.timf, value=19, command=lambda:parent.mt5_main.mt5_timef( tt=19 ) )
        self.timf_menu.add_radiobutton( label='MN1', variable=self.timf, value=20, command=lambda:parent.mt5_main.mt5_timef( tt=20 ) )
        #----------------------------------------------------------------------
        
        #======================================================================
        #----------------------------------------------------------------------
        #
        # Wind Menu Wind Menu Wind Menu Wind Menu Wind Menu Wind Menu Wind Menu
        #
        #----------------------------------------------------------------------
        #======================================================================
        self.wind_menu  = tk.Menu   ( self, tearoff= False, **menu_style )
        self.add_cascade            ( label="Window"        ,  menu=self.wind_menu, underline=0 )
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        self.wind_menu.add_command  ( label='Default Screen',  command=lambda:resize_window_def (parent), image=self.siz0_img, compound='left' )
        self.wind_menu.add_command  ( label='Large Screen  ',  command=lambda:resize_window_big (parent), image=self.siz1_img, compound='left' )
        self.wind_menu.add_command  ( label='Full Screen   ',  command=lambda:resize_window_full(parent), image=self.siz2_img, compound='left' )
        #----------------------------------------------------------------------
        
        #======================================================================
        #----------------------------------------------------------------------
        #
        # Help menu Help menu Help menu Help menu Help menu Help menu Help menu
        #
        #----------------------------------------------------------------------
        #======================================================================
        self.help_menu  = tk.Menu   ( self, tearoff= False, **menu_style )
        self.add_cascade            ( label="Help"    ,        menu=self.help_menu, underline=0 )
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        self.help_menu.add_command  ( label='About', command=lambda:AboutDialog( parent ), image=self.info_img, compound='left' )
        #----------------------------------------------------------------------

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Main Frame (TOP)
#
#
#------------------------------------------------------------------------------
#==============================================================================
class MainTOP( ttk.Frame ):
    def __init__( self, parent ):
        super().__init__( parent, style=parent.styTOP )
        self.parent     = parent                # 親を保持しておく
        self.pack( side='top', fill="both", expand=False, padx=parent.padx, pady=parent.pady )
        self.create_widgets( )
        # メニューバーを作成して親ウィンドウに設定
        #self.menu_top   = MenuTOP( parent )    # Application 側の self.menuTOP を正とする
        #parent.config( menu=self.menu_top )    # Application 側の self.menuTOP を正とする
        
    def create_widgets( self ):
        parent          = self.parent           # 短い別名にすると読みやすい
        photoimage0     = parent.bti0 #photo.subsample(3,3)
        photoimage1     = parent.bti1 #photo.subsample(3,3)
        photoimage2     = parent.bti2 #photo.subsample(3,3)
        #----------------------------------------------------------------------
        # Set Window Size
        #----------------------------------------------------------------------
        '''
        def resize_window_big():
            parent.state   ( 'normal' )
            parent.geometry( f'{_Cyg_conf.Lwin_size[0]}x{_Cyg_conf.Lwin_size[1]}+{parent.winfo_x()}+{parent.winfo_y()}' )
        def resize_window_def():
            parent.state   ( 'normal' )
            parent.geometry( f'{_Cyg_conf.Swin_size[0]}x{_Cyg_conf.Swin_size[1]}+{parent.winfo_x()}+{parent.winfo_y()}' )
        #'''
        #----------------------------------------------------------------------
        # Create Buttons (Left side)
        #----------------------------------------------------------------------
        parent.Buttn_TL00   = ttk.Button( self, bootstyle=parent.styBTN, image=photoimage0, text='MT5\nOpen' , compound='top' )
        parent.Buttn_TL01   = ttk.Button( self, bootstyle=parent.styBTN, image=photoimage0, text='MT5\nClose', compound='top' )
        parent.Buttn_TL02   = ttk.Button( self, bootstyle=parent.styBTN, image=photoimage0, text='MT5\nChart', compound='top' )
        parent.Buttn_TL00.pack( side='left',  padx=parent.padx, pady=parent.pady )
        parent.Buttn_TL01.pack( side='left',  padx=parent.padx, pady=parent.pady )
        parent.Buttn_TL02.pack( side='left',  padx=parent.padx, pady=parent.pady )
        
        parent.Buttn_TL00.config( command=parent.mt5_main.mt5_login  ) # MT5 Open   ボタンが押された
        parent.Buttn_TL01.config( command=parent.mt5_main.mt5_sdown  ) # MT5 Cloase ボタンが押された
        parent.Buttn_TL02.config( command=parent.mt5_data.make_chart ) # MT5 Chart  ボタンが押された
        #----------------------------------------------------------------------
        # Create Buttons (Center) datetime setting
        #----------------------------------------------------------------------
        parent.Buttn_TC     = [] # 配列にできるか？
        parent.Buttn_TC.append( ttk.Button( self, bootstyle=parent.styBTN, image=photoimage1, text='MT5\nM1' , compound='top', command=lambda:parent.mt5_main.mt5_timef( tt= 0 ) ) )
        parent.Buttn_TC.append( ttk.Button( self, bootstyle=parent.styBTN, image=photoimage2, text='MT5\nM5' , compound='top', command=lambda:parent.mt5_main.mt5_timef( tt= 4 ) ) )
        parent.Buttn_TC.append( ttk.Button( self, bootstyle=parent.styBTN, image=photoimage2, text='MT5\nM15', compound='top', command=lambda:parent.mt5_main.mt5_timef( tt= 8 ) ) )
        parent.Buttn_TC.append( ttk.Button( self, bootstyle=parent.styBTN, image=photoimage2, text='MT5\nM30', compound='top', command=lambda:parent.mt5_main.mt5_timef( tt=10 ) ) )
        parent.Buttn_TC.append( ttk.Button( self, bootstyle=parent.styBTN, image=photoimage2, text='MT5\nH1' , compound='top', command=lambda:parent.mt5_main.mt5_timef( tt=11 ) ) )
        parent.Buttn_TC.append( ttk.Button( self, bootstyle=parent.styBTN, image=photoimage2, text='MT5\nH4' , compound='top', command=lambda:parent.mt5_main.mt5_timef( tt=14 ) ) )
        parent.Buttn_TC.append( ttk.Button( self, bootstyle=parent.styBTN, image=photoimage2, text='MT5\nD1' , compound='top', command=lambda:parent.mt5_main.mt5_timef( tt=18 ) ) )
        parent.Buttn_TC.append( ttk.Button( self, bootstyle=parent.styBTN, image=photoimage2, text='MT5\nW1' , compound='top', command=lambda:parent.mt5_main.mt5_timef( tt=19 ) ) )
        parent.Buttn_TC.append( ttk.Button( self, bootstyle=parent.styBTN, image=photoimage2, text='MT5\nMN' , compound='top', command=lambda:parent.mt5_main.mt5_timef( tt=20 ) ) )
        parent.Buttn_TC[0].pack( side='left',  padx=parent.BtpadA, pady=parent.pady )
        parent.Buttn_TC[1].pack( side='left',  padx=parent.padx,   pady=parent.pady )
        parent.Buttn_TC[2].pack( side='left',  padx=parent.padx,   pady=parent.pady )
        parent.Buttn_TC[3].pack( side='left',  padx=parent.padx,   pady=parent.pady )
        parent.Buttn_TC[4].pack( side='left',  padx=parent.padx,   pady=parent.pady )
        parent.Buttn_TC[5].pack( side='left',  padx=parent.padx,   pady=parent.pady )
        parent.Buttn_TC[6].pack( side='left',  padx=parent.padx,   pady=parent.pady )
        parent.Buttn_TC[7].pack( side='left',  padx=parent.padx,   pady=parent.pady )
        parent.Buttn_TC[8].pack( side='left',  padx=parent.padx,   pady=parent.pady )

        #----------------------------------------------------------------------
        # Create Buttons (Right side)
        #----------------------------------------------------------------------
        parent.Buttn_TR00   = ttk.Button( self, bootstyle=parent.styBTN, image=photoimage0, text='WIN\nBig'  , compound='top' )
        parent.Buttn_TR01   = ttk.Button( self, bootstyle=parent.styBTN, image=photoimage0, text='WIN\nDef'  , compound='top' )
        parent.Buttn_TR02   = ttk.Button( self, bootstyle=parent.styBTN, image=photoimage0, text='IMG\nOpen' , compound='top' )
        parent.Buttn_TR00.pack ( side='right', padx=parent.padx, pady=parent.pady )
        parent.Buttn_TR01.pack ( side='right', padx=parent.padx, pady=parent.pady )
        parent.Buttn_TR02.pack ( side='right', padx=parent.padx, pady=parent.pady )
        
        parent.Buttn_TR00.config( command=lambda:resize_window_big(parent) )
        parent.Buttn_TR01.config( command=lambda:resize_window_def(parent) )
        parent.Buttn_TR02.config( command=lambda:Image_loader(parent) )
        
#==============================================================================
#------------------------------------------------------------------------------
#
#
# Main Frame (MIDDLE L&R 2 Frames)
#
#
#------------------------------------------------------------------------------
#==============================================================================
class MainML0( ttk.Frame ):
    def __init__( self, parent ):
        super().__init__( parent, style=parent.styML0 )
        self.pack( side='left', fill="y", expand=False, padx=parent.padx, pady=parent.pady )
        self.create_widgets( parent )

    def create_widgets( self, parent ):
        # Create Label
        parent.Label_ML00   = ttk.Label( self, text='-----------------------------------', bootstyle=parent.styML1, font=("Segoe UI", 10,'') )
        parent.Label_ML00.pack( side='top',  padx=parent.padx, pady=parent.pady )

class MainMR0( ttk.Frame ):
    def __init__( self, parent ):
        super().__init__( parent, style=parent.styMR0 )
        self.pack( side='right', fill="both", expand=False, padx=parent.padx, pady=parent.pady )
        self.create_widgets( parent )

    def create_widgets( self, parent ):
        # Create Label
        parent.Label_MR00   = ttk.Label( self, text='---------------------------'        , bootstyle=parent.styMR1, font=("Segoe UI", 10,'') )
        parent.Label_MR00.pack( side='top',  padx=parent.padx, pady=parent.pady )
        
#==============================================================================
#------------------------------------------------------------------------------
#
#
# Main Frame (BOTTOM)
#
#
#------------------------------------------------------------------------------
#==============================================================================
class MainBTM( ttk.Frame ):
    def __init__( self, parent ):
        super().__init__( parent, style=parent.styBT0 )
        self.pack( side='bottom', fill="both", expand=False, padx=parent.padx, pady=parent.pady )
        self.create_widgets( parent )

    def create_widgets( self, parent ):
        # Create Label
        parent.Label_BL00   = ttk.Label( self, text='BOTTOM LEFT Frame (LEFT)' , bootstyle=parent.styBT1, font=("Segoe UI", 10,'') )
        parent.Label_BL00.pack( side='left',  padx=parent.padx, pady=parent.pady )
        parent.Label_BL01   = ttk.Label( self, text='BOTTOM LEFT Frame (RIGHT)', bootstyle=parent.styBT1, font=("Segoe UI", 10,'') )
        parent.Label_BL01.pack( side='right', padx=parent.padx, pady=parent.pady )
        
#==============================================================================
#------------------------------------------------------------------------------
#
#
# MAIN Finction
#
#
#------------------------------------------------------------------------------
#==============================================================================
def main():
    # https://stackoverflow.com/questions/77759772/ttkbootstrap-bgerror-failed-to-handle-background-error
    ttk.Style.instance = None
    app = Application( _Cyg_conf.Main_titl, _Cyg_conf.Main_size )
    app.mainloop()

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Call MAIN Finction
#
#
#------------------------------------------------------------------------------
#==============================================================================
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
    #
    #

# End of File -----------------------------------------------------------------
