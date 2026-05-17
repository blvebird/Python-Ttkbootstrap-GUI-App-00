# ! python
# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
#
# Spyder Editor
# Name          : _Cyg_sub1.py
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
#------------------------------------------------------------------------------

#==============================================================================
#------------------------------------------------------------------------------
#
#
# Image Loader
# # https://thepythoncode.com/article/make-an-image-editor-in-tkinter-python
# # https://terakoya.sejuku.net/question/detail/57833
#
#
#------------------------------------------------------------------------------
#==============================================================================
def Image_loader( parent ):
    filename            = askopenfilename(\
                                          title="Open Image File",\
                                          filetypes=[("Image Files","*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.tif;*.gif"),\
                                                     ("All Files","*.*"),])
    if not filename:
        return
    try:
        img             = Image.open( open(filename,'rb') )
        #print( img.verify() )
        parent.img1     = img
        canvas_w        = parent.Canvs0.winfo_width ()
        canvas_h        = parent.Canvs0.winfo_height()
        pil_img         = ImageOps.pad(img, (canvas_w, canvas_h))
        parent.tk_img0  = ImageTk.PhotoImage(image=pil_img)
        parent.Canvs0.create_image( canvas_w//2, canvas_h//2, image=parent.tk_img0, tag='Photo' )
        #----------------------------------------------------------------------
        #print( filename )
        parent.Stext0.text.config( state='normal'   )
        parent.Stext0.insert( END, filename )
        parent.Stext0.insert( END, '\n' )
        parent.Stext0.see   ( END )
        parent.Stext0.text.config( state='disabled' )
        #----------------------------------------------------------------------
        parent.Label1["text"]   = filename
    except( PIL.UnidentifiedImageError, IOError, SyntaxError ) as err: #except PIL.UnidentifiedImageError:
        #----------------------------------------------------------------------
        #print( f"Skipping corrupt image: {filename}", err )
        parent.Stext0.text.config( state='normal'   )
        parent.Stext0.insert( END, filename )
        parent.Stext0.insert( END, 'Skipping corrupt image: ' )
        parent.Stext0.insert( END, err )
        parent.Stext0.insert( END, '\n' )
        parent.Stext0.see   ( END )
        parent.Stext0.text.config( state='disabled' )
        #----------------------------------------------------------------------

def show_message1( parent ):
    parent.Stext0.text.config( state='normal'   )
    parent.Stext0.insert( END, 'The menu is not ready yet, sorry..\n' )
    parent.Stext0.see   ( END )
    parent.Stext0.text.config( state='disabled' )

def resize_window_big ( parent ):
    parent.state   ( 'normal' )
    parent.geometry( f'{_Cyg_conf.Lwin_size[0]}x{_Cyg_conf.Lwin_size[1]}+{parent.winfo_x()}+{parent.winfo_y()}' )

def resize_window_def ( parent ):
    parent.state   ( 'normal' )
    parent.geometry( f'{_Cyg_conf.Swin_size[0]}x{_Cyg_conf.Swin_size[1]}+{parent.winfo_x()}+{parent.winfo_y()}' )

def resize_window_full( parent ):
    parent.state   ( 'zoomed' )

def load_inverted_icon( path: str, size=(24, 24), flg=0 ) -> ImageTk.PhotoImage:
    """透過PNGの色だけ反転し、指定サイズにリサイズして返す"""
    img = Image.open(path).convert("RGBA")

    # RGBAを分解してRGBだけ反転
    r, g, b, a  = img.split()
    rgb         = Image.merge( "RGB", (r,g,b) )
    if  flg:
        rgb     = ImageOps.invert( rgb )
    img_inv     = Image.merge( "RGBA", (*rgb.split(),a) )

    # リサイズ
    if size is not None:
        img_inv = img_inv.resize( size, Image.LANCZOS )

    return ImageTk.PhotoImage( img_inv )

#==============================================================================
#------------------------------------------------------------------------------
#
#
# MainMC1 Function
# https://www.tutorialspoint.com/how-to-set-the-canvas-size-properly-in-tkinter
# https://www.python-beginners.com/entry/20210515/1621007804
#
#
#------------------------------------------------------------------------------
#==============================================================================
class MainMC0( ttk.Frame ):
    def __init__( self, parent ):
        super().__init__( parent, style=parent.styMC0 )
        self.pack( side='top', fill="both", expand=False, padx=(2,2), pady=(2,2) )
        self.create_widgets ( parent )
        
    def create_widgets( self, parent ):
        self.columnconfigure( _Cyg_conf.ColseqFC, weight=1, uniform='a' )
        self.rowconfigure   ( _Cyg_conf.RowseqFC, weight=1, uniform='a' )
        parent.Label0   = ttk.Label ( self, text='LABEL0', background='' ) # 左寄せ
        parent.Label0.grid  ( row= 0, column= 0, columnspan= 1, rowspan= 1, sticky='nsw', padx=parent.padx, pady=parent.pady ) # 左 nsw
        parent.Label1   = ttk.Label ( self, text='LABEL1', background='' ) # センタリング
        parent.Label1.grid  ( row= 0, column= 1, columnspan= 1, rowspan= 1, sticky='ns' , padx=parent.padx, pady=parent.pady ) # 中央 ns
        parent.Label2   = ttk.Label ( self, text='LABEL2', background='' ) # 右寄せ
        parent.Label2.grid  ( row= 0, column= 2, columnspan= 1, rowspan= 1, sticky='nse', padx=parent.padx, pady=parent.pady ) # 右 nse
        def update_time(): # https://jobcode.jp/python-tkinter/
            # 現在時刻を「時:分:秒」のフォーマットで取得
            current_time    = time.strftime( '%Y/%m/%d %H:%M' )
            # time_labelウィジェットのテキストを現在の時刻に更新
            parent.Label2.config( text=current_time )
            # 10000ミリ秒後に、再び update_time 関数を呼び出す
            # これにより、10秒ごとに時刻が更新され続けるループが作られる
            if  parent.LBL2id:
                parent.LBL2id  = parent.Label2.after( 10000, update_time ) # 10秒後
            #print( 'update_time', parent.LBL2id )
        update_time ()
        
#==============================================================================
#------------------------------------------------------------------------------
#
#
# MainMC2 Function
#
#
#------------------------------------------------------------------------------
#==============================================================================
class MainMC1( ttk.Frame ):
    def __init__( self, parent ):
        super().__init__( parent, style=parent.styMC1 )
        self.pack( side='top', fill="both", expand=True, padx=parent.padx, pady=parent.pady )
        self.create_widgets ( parent )
        
    def create_widgets( self, parent ):
        #----------------------------------------------------------------------
        innerF0         = ttk.Frame( self, style="Light" )
        innerF0.place( relx=parent.iF1_relx, rely=parent.iF1_rely, relwidth=parent.iF1_rwid, relheight=parent.iF1_rhei )
        innerF0.columnconfigure( _Cyg_conf.ColseqFA, weight=1, uniform='a' )
        innerF0.rowconfigure   ( _Cyg_conf.RowseqFA, weight=1, uniform='a' )
        #----------------------------------------------------------------------
        innerF1         = ttk.Frame( self, style="Success" )
        innerF1.place( relx=parent.iF2_relx, rely=parent.iF2_rely, relwidth=parent.iF2_rwid, relheight=parent.iF2_rhei )
        innerF1.columnconfigure( _Cyg_conf.ColseqFB, weight=1, uniform='a' )
        innerF1.rowconfigure   ( _Cyg_conf.RowseqFB, weight=1, uniform='a' )
        #----------------------------------------------------------------------
        innerF2         = ttk.Frame( self, style="Light" )
        innerF2.place( relx=parent.iF3_relx, rely=parent.iF3_rely, relwidth=parent.iF3_rwid, relheight=parent.iF3_rhei )
        innerF2.columnconfigure( _Cyg_conf.ColseqFC, weight=1, uniform='a' )
        innerF2.rowconfigure   ( _Cyg_conf.RowseqFC, weight=1, uniform='a' )
        #----------------------------------------------------------------------
        parent.Canvs0   = ttk.Canvas( innerF0, bg="#03948a" )
        parent.Canvs0.grid  ( row= 0, column= 0, columnspan= 1, rowspan= 1, sticky='nswe', padx=parent.padx, pady=parent.pady )
        parent.Canvs1   = ttk.Canvas( innerF1, bg="#03948a" )
        parent.Canvs1.grid  ( row= 0, column= 0, columnspan= 1, rowspan= 1, sticky='nswe', padx=parent.padx, pady=parent.pady )
        parent.Canvs2   = ttk.Canvas( innerF1, bg="#03948a" )
        parent.Canvs2.grid  ( row= 1, column= 0, columnspan= 1, rowspan= 1, sticky='nswe', padx=parent.padx, pady=parent.pady )
        
        def draw_canvas():
            self.update()   # Canvasのサイズを取得するためFrameを更新しておく
            canvas_w        = parent.Canvs0.winfo_width ()
            canvas_h        = parent.Canvs0.winfo_height()
            img             = parent.img1
            pil_img         = ImageOps.pad(img, (canvas_w, canvas_h))
            self.tk_img0    = ImageTk.PhotoImage(image=pil_img)
            parent.Canvs0.create_image( canvas_w//2, canvas_h//2, image=self.tk_img0, tag='Photo' )
            canvas_w        = parent.Canvs1.winfo_width ()
            canvas_h        = parent.Canvs1.winfo_height()
            img             = parent.img2
            pil_img         = ImageOps.pad(img, (canvas_w, canvas_h))
            self.tk_img1    = ImageTk.PhotoImage(image=pil_img)
            parent.Canvs1.create_image( canvas_w//2, canvas_h//2, image=self.tk_img1, tag='Photo' )
            canvas_w        = parent.Canvs2.winfo_width ()
            canvas_h        = parent.Canvs2.winfo_height()
            img             = parent.img3
            pil_img         = ImageOps.pad(img, (canvas_w, canvas_h))
            self.tk_img2    = ImageTk.PhotoImage(image=pil_img)
            parent.Canvs2.create_image( canvas_w//2, canvas_h//2, image=self.tk_img2, tag='Photo' )
        
        def show_geometry_info( event ):
            draw_canvas ()
            parent.Label0["text"]  = '(',parent.Canvs0.winfo_width(),'x',parent.Canvs0.winfo_height(),')'\
                                     '(',parent.Canvs1.winfo_width(),'x',parent.Canvs1.winfo_height(),')'\
                                     '(',parent.Canvs2.winfo_width(),'x',parent.Canvs2.winfo_height(),')'
        
        self.bind( "<Configure>", show_geometry_info )
        #----------------------------------------------------------------------
        style           = ttk.Style()
        parent.Stext0   = ScrolledText( master=innerF2, highlightcolor=style.colors.success, highlightbackground=style.colors.border, highlightthickness=1, autohide=True, hbar=True, state='disabled', font=("Segoe UI",7) )
        parent.Stext0.grid  ( row= 0, column= 0, columnspan= 1, rowspan= 2, sticky='nswe', padx=parent.padx, pady=parent.pady ) # 左 nsw
        parent.Stext1   = ScrolledText( master=innerF2, highlightcolor=style.colors.success, highlightbackground=style.colors.border, highlightthickness=1, autohide=True, hbar=True, state='disabled' )
        parent.Stext1.grid  ( row= 0, column= 1, columnspan= 1, rowspan= 1, sticky='nswe', padx=parent.padx, pady=parent.pady ) # 中央 ns
        parent.Stext2   = ScrolledText( master=innerF2, highlightcolor=style.colors.success, highlightbackground=style.colors.border, highlightthickness=1, autohide=True, hbar=True, state='disabled' )
        parent.Stext2.grid  ( row= 0, column= 2, columnspan= 1, rowspan= 1, sticky='nswe', padx=parent.padx, pady=parent.pady ) # 右 nse
        #----------------------------------------------------------------------
        
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
