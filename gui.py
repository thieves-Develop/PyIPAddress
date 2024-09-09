import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from threading import Thread
from ip_calculator import calculate_ip_info, netmask_to_cidr, cidr_to_netmask
from utils import start_animation, show_mask

class IPApp:
    def __init__(self):
        # 創建主窗口
        self.root = tk.Tk()
        self.root.title("IP 計算器")
        self.root.geometry("520x420")

        # 設置 GUI 結構
        self.setup_gui()

        # 動畫相關
        self.is_calculating = False

    def setup_gui(self):
        # 設置界面佈局
        self.label_ip = tk.Label(self.root, text="輸入 IP 網段 / 網絡掩碼：", font=("Arial", 14),  fg="white")
        self.label_ip.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        self.entry_ip = tk.Entry(self.root, font=("Arial", 14), width=30, bg="white", fg="black")
        self.entry_ip.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # 按鈕
        self.btn_calculate = tk.Button(self.root, text="計算", font=("Arial", 14), bg="white", fg="black", command=self.start_calculation)
        self.btn_calculate.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.btn_export = tk.Button(self.root, text="導出結果", font=("Arial", 14), bg="white", fg="black", command=self.export_results)
        self.btn_export.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # 結果顯示區
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=10, font=("Arial", 14), bg="white", fg="black")
        self.text_area.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.label_result = tk.Label(self.root, text="", font=("Arial", 14), fg="white")
        self.label_result.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        self.loading_label = tk.Label(self.root, text="", font=("Arial", 14), fg="red")
        self.loading_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        # 自動轉換功能
        self.entry_ip.bind("<KeyRelease>", self.auto_convert)

    def start_calculation(self):
        # 開啟新執行緒進行計算
        Thread(target=self.calculate).start()

    def calculate(self):
        # 計算並顯示結果
        mask = show_mask(self.root)  # 顯示遮罩
        try:
            self.is_calculating = True
            start_animation(self.is_calculating, self.loading_label)

            ip_input = self.entry_ip.get()
            result = calculate_ip_info(ip_input)  # 從 ip_calculator 模組獲取計算結果

            # 顯示結果
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, result)
        except ValueError as e:
            messagebox.showerror("錯誤", str(e))
        finally:
            if isinstance(mask, tk.Toplevel):
                mask.destroy()
            self.is_calculating = False

    def auto_convert(self, event):
        # 自動轉換網絡掩碼或 CIDR
        input_value = self.entry_ip.get()
        try:
            if '/' in input_value:
                ip, mask = input_value.split('/')
                if '.' in mask:
                    cidr = netmask_to_cidr(mask)
                    self.label_result.config(text=f"網絡掩碼 {mask} 對應的 CIDR 格式為: /{cidr}")
                else:
                    netmask = cidr_to_netmask(mask)
                    self.label_result.config(text=f"CIDR /{mask} 對應的網絡掩碼為: {netmask}")
        except ValueError as e:
            self.label_result.config(text=str(e))

    def export_results(self):
        result_text = self.text_area.get(1.0, tk.END).strip()
        if not result_text:
            messagebox.showwarning("警告", "沒有可導出的內容。")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(result_text)
            messagebox.showinfo("成功", "結果已成功保存。")

    def run(self):
        # 啟動主循環
        self.root.mainloop()

