import tkinter as tk
from tkinter import messagebox
from idCode import region_data  # 从idCode.py导入行政区划数据


class IDValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("身份证验证系统")
        self.root.geometry("500x480")
        self.root.minsize(500, 480)
        self.root.config(bg="#f0f8ff")  # 背景色

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        """创建界面组件"""
        # 主标题
        tk.Label(self.root, text="身份证信息验证系统",
                 font=("微软雅黑", 18, "bold"),
                 bg="#f0f8ff", fg="#0066cc"
                 ).pack(pady=(10, 15))

        # 输入区域
        self.create_input_section()

        # 结果区域
        self.create_result_section()

        # 状态栏
        self.create_status_bar()

    def create_input_section(self):
        """创建输入区域"""
        input_frame = tk.Frame(self.root, bg="#e6f2ff", padx=15, pady=15)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="身份证号码:",
                 font=("微软雅黑", 12), bg="#e6f2ff"
                 ).pack(side="left", padx=(0, 10))

        self.entry = tk.Entry(input_frame, font=("微软雅黑", 12), width=22, bd=2)
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.focus()
        self.entry.bind("<Return>", self.validate)

        # 验证按钮
        validate_btn = tk.Button(input_frame, text="验证", font=("微软雅黑", 12),
                                 bg="#4da6ff", fg="white",
                                 command=self.validate)
        validate_btn.pack(side="left", padx=(10, 0))

        # 按钮悬停效果
        validate_btn.bind("<Enter>", lambda e: validate_btn.config(bg="#3399ff"))
        validate_btn.bind("<Leave>", lambda e: validate_btn.config(bg="#4da6ff"))

    def create_result_section(self):
        """创建结果展示区域"""
        result_frame = tk.LabelFrame(self.root, text="身份证信息",
                                     font=("微软雅黑", 12), bg="#f0f8ff",
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
            frame = tk.Frame(result_frame, bg="#f0f8ff")
            frame.pack(fill="x", padx=5, pady=2)

            tk.Label(frame, text=f"{text}：", font=("微软雅黑", 12),
                     bg="#f0f8ff", width=8, anchor="w"
                     ).pack(side="left")

            label = tk.Label(frame, text="", font=("微软雅黑", 12),
                             bg="#f0f8ff", anchor="w", width=25)
            label.pack(side="left", fill="x", expand=True)
            self.info_labels[key] = label

    def create_status_bar(self):
        """创建状态栏"""
        status = tk.Label(self.root,
                          text="中国居民身份证验证系统 | 基于 GB 11643-1999 标准",
                          font=("微软雅黑", 10), bg="#d9e6f2", fg="#333333",
                          bd=1, relief="sunken", padx=10, pady=8)
        status.pack(side="bottom", fill="x")

    def validate(self, event=None):
        """验证身份证并显示结果"""
        id_num = self.entry.get().strip().upper()

        # 清空之前的结果
        for label in self.info_labels.values():
            label.config(text="")

        # 基本格式检查+验证校验码
        if not (len(id_num) == 18 and id_num[:17].isdigit() and
                id_num[-1] in "0123456789X") or not self.check_verify_code(id_num):
            messagebox.showerror("错误", "身份证格式错误")
            return

        # 提取并显示信息
        self.display_info(id_num)

    def check_verify_code(self, id_num):
        """验证校验码"""
        factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        mapping = "10X98765432"

        total = sum(int(d) * f for d, f in zip(id_num[:17], factors))
        return mapping[total % 11] == id_num[-1]

    def display_info(self, id_num):
        """显示身份证信息"""
        # 性别信息 (第17位奇数为男，偶数为女)
        gender = "男" if int(id_num[16]) % 2 else "女"
        self.info_labels["gender"].config(text=gender)

        # 出生日期
        birth = f"{id_num[6:10]}年{id_num[10:12]}月{id_num[12:14]}日"
        self.info_labels["birth"].config(text=birth)

        # 行政区划信息
        region_code = id_num[:6]
        province, city, district, source = region_data.get(
            region_code, ("-", "-", "-", "-"))

        self.info_labels["province"].config(text=province)
        self.info_labels["city"].config(text=city)
        self.info_labels["district"].config(text=district)
        self.info_labels["source"].config(text=source)


if __name__ == "__main__":
    root = tk.Tk()
    app = IDValidatorApp(root)
    root.mainloop()
