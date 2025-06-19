# 新增图标，程序打包为exe

import tkinter as tk
from tkinter import messagebox
from idCode import region_data  # 从idCode.py导入行政区划数据
import datetime
import sys
import os


class IDAuthenticator:
    def __init__(self, root):
        self.root = root
        self.root.title("身份证验证系统")
        self.root.geometry("500x480")
        self.root.minsize(500, 480)
        self.root.config(bg="ghostwhite")

        # 设置窗口图标
        self.set_icon()

        # 创建界面
        self.widgets()

    def set_icon(self):
        """设置窗口图标"""
        try:
            # 判断是否打包环境
            if getattr(sys, 'frozen', False):
                # 打包后，图标在sys._MEIPASS指向的临时目录
                base_path = sys._MEIPASS
            else:
                # 未打包，当前脚本所在目录
                base_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_path, "icon.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"图标加载失败: {str(e)}")

    def widgets(self):
        """创建界面组件"""
        # 主标题
        tk.Label(self.root, text="身份证信息验证系统",
                 font=("微软雅黑", 18, "bold"),
                 bg="ghostwhite", fg="dodgerblue"
                 ).pack(pady=(10, 15))

        # 输入区域
        self.input()

        # 结果区域
        self.output()

        # 状态栏
        self.bar()

    def input(self):
        """创建输入区域 - 修正拉伸问题"""
        input_frame = tk.Frame(self.root, bg="aliceblue", padx=15, pady=15)
        input_frame.pack(fill="x", padx=10, pady=5)

        # 使用pack布局实现弹性输入框
        label = tk.Label(input_frame, text="身份证号码:",
                         font=("微软雅黑", 12), bg="aliceblue")
        label.pack(side="left", padx=(0, 10))

        # 创建一个Frame作为输入框和按钮的容器
        entry_container = tk.Frame(input_frame, bg="aliceblue")
        entry_container.pack(side="left", fill="x", expand=True)

        self.entry = tk.Entry(entry_container, font=("微软雅黑", 12), bd=2, relief="groove")
        self.entry.pack(side="left", fill="x", expand=True)  # 关键：设置fill和expand
        self.entry.focus()
        self.entry.bind("<Return>", self.validate)

        # 验证按钮 - 放在entry_container中
        validate_btn = tk.Button(entry_container, text="验证", font=("微软雅黑", 12),
                                 bg="dodgerblue", fg="white", relief="flat",
                                 command=self.validate, padx=15)
        validate_btn.pack(side="right", padx=(10, 0))  # 固定在右侧

        # 按钮悬停效果
        validate_btn.bind("<Enter>", lambda e: validate_btn.config(bg="royalblue"))
        validate_btn.bind("<Leave>", lambda e: validate_btn.config(bg="dodgerblue"))

    def output(self):
        """创建结果展示区域"""
        result_frame = tk.LabelFrame(self.root, text="身份证信息",
                                     font=("微软雅黑", 12), bg="ghostwhite",
                                     padx=15, pady=15)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 信息项和对应的标签
        self.info_labels = {}
        items = [
            ("性　　别", "gender"),
            ("出　　生", "birth"),
            ("省　　级", "province"),
            ("地 市 级", "city"),
            ("县 区 级", "district"),
            ("数据来源", "source")
        ]

        for text, key in items:
            frame = tk.Frame(result_frame, bg="ghostwhite")
            frame.pack(fill="x", padx=5, pady=2)

            tk.Label(frame, text=f"{text}：", font=("微软雅黑", 12),
                     bg="ghostwhite", width=8, anchor="w"
                     ).pack(side="left")

            label = tk.Label(frame, text="", font=("微软雅黑", 12),
                             bg="ghostwhite", anchor="w")
            label.pack(side="left", fill="x", expand=True)
            self.info_labels[key] = label

    def bar(self):
        """创建状态栏"""
        status = tk.Label(self.root,
                          text="中国居民身份证验证系统 | 基于 GB 11643-1999 标准",
                          font=("微软雅黑", 10), bg="lightblue", fg="gray20",
                          bd=1, padx=10, pady=8)
        status.pack(side="bottom", fill="x")

    def validate(self, event=None):
        """验证身份证并显示结果"""
        id_num = self.entry.get().strip().upper()

        # 清空之前的结果
        for label in self.info_labels.values():
            label.config(text="")

        # 只要有任何错误都弹出同一种错误提示
        if not self.check_all(id_num):
            messagebox.showerror("错误", "身份证格式或内容有误")
            return

        # 提取并显示信息
        self.display_info(id_num)

    def check_all(self, id_num):
        """合并所有校验"""
        # 格式和校验码
        if not (len(id_num) == 18 and id_num[:17].isdigit() and
                id_num[-1] in "0123456789X"):
            return False
        if not self.check_verify_code(id_num):
            return False
        if not self.check_birth(id_num):
            return False
        return True

    def check_verify_code(self, id_num):
        """验证校验码"""
        factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        mapping = "10X98765432"
        try:
            total = sum(int(d) * f for d, f in zip(id_num[:17], factors))
            return mapping[total % 11] == id_num[-1]
        except Exception:
            return False

    def check_birth(self, id_num):
        """检查出生日期的有效性"""
        birth_str = id_num[6:14]
        try:
            year = int(birth_str[:4])
            month = int(birth_str[4:6])
            day = int(birth_str[6:8])
            month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            today = datetime.date.today()
            birth_date = datetime.date(year, month, day)
            if year < 1840 or month < 1 or month > 12 or day < 1 or day > month_days[month - 1] or birth_date > today:
                return False
            # 闰年
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                month_days[1] = 29
            return True
        except Exception:
            return False

    def display_info(self, id_num):
        """显示身份证信息"""
        gender = "男" if int(id_num[16]) % 2 else "女"
        self.info_labels["gender"].config(text=gender)

        birth = f"{int(id_num[6:10])} 年 {int(id_num[10:12])} 月 {int(id_num[12:14])} 日"
        self.info_labels["birth"].config(text=birth)

        region_code = id_num[:6]
        province, city, district, source = region_data.get(
            region_code, ("-", "-", "-", "-"))

        self.info_labels["province"].config(text=province)
        self.info_labels["city"].config(text=city)
        self.info_labels["district"].config(text=district)
        self.info_labels["source"].config(text=source)


if __name__ == "__main__":
    root = tk.Tk()
    app = IDAuthenticator(root)
    root.mainloop()
