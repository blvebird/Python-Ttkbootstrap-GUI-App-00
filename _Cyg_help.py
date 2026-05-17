# ! python
# -*- coding: utf-8 -*-
#==============================================================================
#------------------------------------------------------------------------------
#
# Spyder Editor
# Name          : _Cyg_help.py
# Purpose       : **
# Comment Lang  : JP
# Author        : Blve Bird
# Created Date  : 01/03/2026
# Version       : 0.0.0.1
#
#------------------------------------------------------------------------------
#==============================================================================

#------------------------------------------------------------------------------
import ttkbootstrap             as ttk
from   ttkbootstrap.constants   import *
import _Cyg_conf
#------------------------------------------------------------------------------
class AboutDialog(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__( title="About", transient=parent, resizable=(False, False) ) # 親ウィンドウにぶら下げる
        # モーダル化
        self.grab_set()
        # 本体フレーム
        frm         = ttk.Frame( self, padding=15 )
        frm.pack( fill=BOTH, expand=YES )
        # アプリ情報
        lbl_title   = ttk.Label( frm, text="CYGNUS", font=("Helvetica", 12, "bold") )
        lbl_title.pack  ( anchor=W )
        lbl_ver     = ttk.Label( frm, text="Version "+_Cyg_conf.Tool_ver )
        lbl_ver.pack    ( anchor=W, pady=(2, 0) )
        lbl_copy    = ttk.Label( frm, text="© 2026 Blve Bird" )
        lbl_copy.pack   ( anchor=W, pady=(2,10) )
        
        lbl_desc    = ttk.Label( frm, text="FX Trading Tool for XMTrading MT5", wraplength=350, justify=LEFT )
        
        lbl_desc.pack   (anchor=W)
        # OK ボタン
        btn_ok      = ttk.Button( frm, text="OK", width=5, bootstyle=PRIMARY, command=self._on_ok ) # width: 文字数ベースの幅指定
        btn_ok.pack     ( anchor=E, pady=(12,0) )
        # 中央に出す
        self.update_idletasks()
        self._place_center(parent)
        # Enter キーで閉じる
        btn_ok.focus_set()
        self.bind("<Return>", lambda e: self._on_ok())
        # ×ボタンも OK と同じ
        self.protocol("WM_DELETE_WINDOW", self._on_ok)
        # 閉じられるまでブロック
        self.wait_window(self)

    def _place_center(self, parent):
        # 親ウィンドウ中央に配置
        px          = parent.winfo_rootx ()
        py          = parent.winfo_rooty ()
        pw          = parent.winfo_width ()
        ph          = parent.winfo_height()
        sw          = self.winfo_width ()
        sh          = self.winfo_height()
        x           = px + (pw - sw) // 2
        y           = py + (ph - sh) // 2
        self.geometry(f"+{x}+{y}")

    def _on_ok(self):
        self.grab_release()
        self.destroy()

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
