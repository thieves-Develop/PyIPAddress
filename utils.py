import tkinter as tk
import time

def start_animation(is_calculating, loading_label):
    """顯示計算中的動畫"""
    def animate():
        while is_calculating:
            for symbol in "|/-\\":
                loading_label.config(text=f"計算中... {symbol}")
                time.sleep(0.1)
        loading_label.config(text="")
    # 啟動動畫
    return animate

def show_mask(root):
    """創建遮罩窗口"""
    mask = tk.Toplevel(root)
    mask.geometry("600x600")
    mask.configure(bg="gray")
    mask.attributes("-alpha", 0.3)  # 輕微透明
    mask.grab_set()  # 禁止操作其他窗口
    return mask

