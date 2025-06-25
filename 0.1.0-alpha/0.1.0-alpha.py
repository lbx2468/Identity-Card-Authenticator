import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re


class IDCardValidator:
    def __init__(self, root):
        self.root = root
        self.root.title("身份证验证程序")

        # 行政区划代码字典
        self.area_codes = self.load_area_codes()

        # 系数列表
        self.coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]

        # 校验码对应表
        self.check_digit_map = {
            0: '1', 1: '0', 2: 'X', 3: '9', 4: '8',
            5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'
        }

        # 创建界面
        self.create_widgets()

    def load_area_codes(self):
        # 这里应该从Excel文件加载行政区划代码
        # 为了演示，我们使用一个简化的字典
        # 实际应用中，应从附件中的Excel文件加载完整数据
        return {
            "110000": {"province": "北京市", "city": "北京市", "district": "-"},
            "120000": {"province": "天津市", "city": "天津市", "district": "-"},
            "130000": {"province": "河北省", "city": "-", "district": "-"},
            "130100": {"province": "河北省", "city": "石家庄市", "district": "-"},
            "130102": {"province": "河北省", "city": "石家庄市", "district": "长安区"},
            # 添加更多行政区划代码...
            # 实际应用中，应该从Excel文件完整加载所有代码
        }

    def create_widgets(self):
        # 输入框和标签
        tk.Label(self.root, text="请输入身份证号码:").grid(row=0, column=0, padx=10, pady=10)
        self.id_entry = tk.Entry(self.root, width=30)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)

        # 验证按钮
        tk.Button(self.root, text="验证", command=self.validate_id).grid(row=0, column=2, padx=10, pady=10)

        # 结果显示区域
        tk.Label(self.root, text="验证结果:").grid(row=1, column=0, padx=10, pady=10)
        self.result_text = tk.Text(self.root, width=50, height=10)
        self.result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def validate_id(self):
        id_number = self.id_entry.get().strip()

        # 清空结果区域
        self.result_text.delete(1.0, tk.END)

        # 检查长度
        if len(id_number) != 18:
            messagebox.showerror("错误", "身份证号码长度必须为18位!")
            return

        # 检查格式
        if not re.match(r'^\d{17}[0-9Xx]$', id_number):
            messagebox.showerror("错误", "身份证号码格式不正确!")
            return

        # 校验码计算
        if not self.check_check_digit(id_number):
            messagebox.showerror("错误", "身份证校验码不正确!")
            return

        # 提取信息
        self.extract_information(id_number)

    def check_check_digit(self, id_number):
        # 计算前17位的加权和
        total = 0
        for i in range(17):
            digit = int(id_number[i])
            weight = self.coefficients[i]
            total += digit * weight

        # 计算余数
        remainder = total % 11

        # 获取校验码
        expected_check_digit = self.check_digit_map.get(remainder, '')

        # 检查校验码是否匹配
        actual_check_digit = id_number[17].upper()
        return expected_check_digit == actual_check_digit

    def extract_information(self, id_number):
        # 提取省份、城市、区县信息
        area_code = id_number[:6]
        area_info = self.area_codes.get(area_code, {"province": "未知", "city": "未知", "district": "未知"})

        # 提取出生日期
        birth_date_str = id_number[6:14]
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y%m%d")
            birth_date_str = birth_date.strftime("%Y年%m月%d日")
        except ValueError:
            birth_date_str = "无效的出生日期"

        # 提取性别
        gender_digit = int(id_number[16])
        gender = "女" if gender_digit % 2 == 0 else "男"

        # 显示结果
        result = f"身份证号码: {id_number}\n"
        result += f"省份: {area_info['province']}\n"
        result += f"城市: {area_info['city']}\n"
        result += f"区县: {area_info['district']}\n"
        result += f"出生日期: {birth_date_str}\n"
        result += f"性别: {gender}\n"
        result += "身份证有效!"

        self.result_text.insert(tk.END, result)


if __name__ == "__main__":
    root = tk.Tk()
    app = IDCardValidator(root)
    root.mainloop()
