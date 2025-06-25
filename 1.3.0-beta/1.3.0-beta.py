# OOP重构

import tkinter as tk
from tkinter import messagebox
from idCode import region_data  # 从idCode.py导入行政区划数据


class IDValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("身份证验证系统")
        self.root.geometry("500x480")
        self.root.minsize(500, 480)
        self.root.resizable(True, True)

        # 颜色配置
        self.bg_color = "#f0f8ff"
        self.frame_color = "#e6f2ff"
        self.button_color = "#4da6ff"
        self.button_hover_color = "#3399ff"
        self.root.config(bg=self.bg_color)

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        """创建所有GUI组件"""
        # 主容器
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 标题
        tk.Label(
            main_container,
            text="身份证信息验证系统",
            font=("微软雅黑", 18, "bold"),
            bg=self.bg_color,
            fg="#0066cc"
        ).pack(pady=(0, 15))

        # 输入区域
        self.create_input_frame(main_container)

        # 结果区域
        self.create_result_frame(main_container)

        # 状态栏
        self.create_status_bar()

    def create_input_frame(self, parent):
        """创建输入区域"""
        input_frame = tk.Frame(parent, bg=self.frame_color, padx=15, pady=15)
        input_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(input_frame, text="身份证号码:", font=("微软雅黑", 12), bg=self.frame_color
                 ).pack(side="left", padx=(0, 10))

        self.entry = tk.Entry(
            input_frame,
            font=("微软雅黑", 12),
            width=22,
            bd=2,
            relief="groove"
        )
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.focus()
        self.entry.bind("<Return>", self.on_validate)

        # 验证按钮
        self.validate_btn = tk.Button(
            input_frame,
            text="验证",
            font=("微软雅黑", 12, "bold"),
            bg=self.button_color,
            fg="white",
            activebackground=self.button_hover_color,
            activeforeground="white",
            relief="flat",
            command=self.on_validate,
            padx=15
        )
        self.validate_btn.pack(side="left", padx=(10, 0))

        # 按钮悬停效果
        self.validate_btn.bind("<Enter>", lambda e: self.validate_btn.config(bg=self.button_hover_color))
        self.validate_btn.bind("<Leave>", lambda e: self.validate_btn.config(bg=self.button_color))

    def create_result_frame(self, parent):
        """创建结果展示区域"""
        result_frame = tk.LabelFrame(
            parent,
            text="身份证信息",
            font=("微软雅黑", 12),
            bg=self.bg_color,
            padx=15,
            pady=15
        )
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 信息项
        info_items = ["性　　别", "出　　生", "省　　级", "地 市 级", "县 区 级", "数据来源"]
        self.value_labels = []

        info_container = tk.Frame(result_frame, bg=self.bg_color)
        info_container.pack(fill="both", expand=True, padx=5, pady=5)

        for item in info_items:
            row_frame = tk.Frame(info_container, bg=self.bg_color)
            row_frame.pack(fill="x", padx=5, pady=2)

            tk.Label(
                row_frame,
                text=item,
                font=("微软雅黑", 12),
                bg=self.bg_color,
                anchor="w",
                width=8
            ).pack(side="left", padx=(0, 5))

            value_label = tk.Label(
                row_frame,
                text="",
                font=("微软雅黑", 12),
                bg=self.bg_color,
                anchor="w",
                wraplength=350,
                justify="left"
            )
            value_label.pack(side="left", fill="x", expand=True)
            self.value_labels.append(value_label)

    def create_status_bar(self):
        """创建状态栏"""
        tk.Label(
            self.root,
            text="中国居民身份证验证系统 | 基于 GB 11643-1999 标准 | MIT License",
            font=("微软雅黑", 10),
            bg="#d9e6f2",
            fg="#333333",
            bd=1,
            relief="sunken",
            anchor="center",
            padx=10,
            pady=8
        ).pack(side="bottom", fill="x")

    @staticmethod
    def validate_id_card(id_number):
        """验证身份证号码的有效性"""
        error_msg = "身份证号码无效，请检查输入！"

        # 处理最后一位的X（转换为大写）
        id_number = id_number.upper()

        # 基本格式检查
        if len(id_number) != 18 or not id_number[:17].isdigit() or id_number[-1] not in "0123456789X":
            return False, error_msg

        # 提取日期部分
        year_str = id_number[6:10]
        month_str = id_number[10:12]
        day_str = id_number[12:14]

        # 日期有效性验证
        try:
            year = int(year_str)
            month = int(month_str)
            day = int(day_str)

            # 年份验证 (1840年是中国近代史开端)
            if year < 1840:
                return False, error_msg

            # 月份验证
            if month < 1 or month > 12:
                return False, error_msg

            # 日期验证
            if month in [1, 3, 5, 7, 8, 10, 12]:
                max_day = 31
            elif month in [4, 6, 9, 11]:
                max_day = 30
            else:  # 2月
                # 闰年判断：能被4整除但不能被100整除，或能被400整除
                max_day = 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28

            if day < 1 or day > max_day:
                return False, error_msg
        except ValueError:
            return False, error_msg

        # 校验码验证
        coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        mapping = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')

        total = sum(int(d) * c for d, c in zip(id_number[:17], coefficients))
        remainder = total % 11

        if mapping[remainder] != id_number[17]:
            return False, error_msg

        # 所有检查通过
        return True, id_number

    @staticmethod
    def extract_info(id_number):
        """从身份证号码中提取基本信息"""
        region_code = id_number[:6]

        # 提取并格式化出生日期
        year = int(id_number[6:10])
        month = int(id_number[10:12])
        day = int(id_number[12:14])

        month_str = str(month) if month >= 10 else f" {month} "
        day_str = str(day) if day >= 10 else f" {day} "
        birth_date = f"{year} 年 {month_str} 月 {day_str} 日"

        # 提取性别
        gender = "男" if int(id_number[16]) % 2 else "女"

        return region_code, birth_date, gender

    @staticmethod
    def find_region_info(region_code):
        """查找行政区划信息"""
        return region_data.get(region_code, ("-", "-", "-", "-"))

    def on_validate(self, event=None):
        """处理验证按钮点击事件"""
        id_number = self.entry.get().strip()

        # 清空结果
        for label in self.value_labels:
            label.config(text="")

        # 验证身份证
        is_valid, result = self.validate_id_card(id_number)

        if not is_valid:
            messagebox.showerror("错误", result)
            return

        # 提取并显示信息
        region_code, birth_date, gender = self.extract_info(result)
        province, city, district, source = self.find_region_info(region_code)

        self.value_labels[0].config(text=gender)
        self.value_labels[1].config(text=birth_date)
        self.value_labels[2].config(text=province)
        self.value_labels[3].config(text=city)
        self.value_labels[4].config(text=district)
        self.value_labels[5].config(text=source)


# 启动应用程序
if __name__ == "__main__":
    root = tk.Tk()
    app = IDValidatorApp(root)
    root.mainloop()
