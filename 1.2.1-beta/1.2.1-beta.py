# 简化错误提示，输入错误合并

import tkinter as tk
from tkinter import messagebox
from idCode import region_data  # 从idCode.py导入行政区划数据
import datetime

"""
身份证验证函数
功能：验证身份证号码的有效性
参数：id_number - 身份证号码字符串
返回值：元组 (是否有效, 结果信息)
"""


def validate_id_card(id_number):
    # 1. 处理最后一位的X（转换为大写）
    id_number = id_number.upper()

    # 2. 基本格式检查（长度、前17位数字、最后一位合法字符）
    if len(id_number) != 18 or not id_number[:17].isdigit() or id_number[-1] not in "0123456789X":
        return False, "身份证号码无效，请检查输入！"

    # 3. 日期有效性验证
    year_str = id_number[6:10]
    month_str = id_number[10:12]
    day_str = id_number[12:14]

    # 3.1 验证年份范围
    try:
        year = int(year_str)
        if year < 1840:  # 1840年是中国近代史开端
            return False, "身份证号码无效，请检查输入！"
    except ValueError:
        return False, "身份证号码无效，请检查输入！"

    # 3.2 验证月份范围
    try:
        month = int(month_str)
        if month < 1 or month > 12:
            return False, "身份证号码无效，请检查输入！"
    except ValueError:
        return False, "身份证号码无效，请检查输入！"

    # 3.3 验证日期范围
    try:
        day = int(day_str)
        # 检查日期是否有效
        if month in [1, 3, 5, 7, 8, 10, 12]:
            max_day = 31
        elif month in [4, 6, 9, 11]:
            max_day = 30
        else:  # 2月
            # 闰年判断：能被4整除但不能被100整除，或能被400整除
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                max_day = 29
            else:
                max_day = 28

        if day < 1 or day > max_day:
            return False, "身份证号码无效，请检查输入！"
    except ValueError:
        return False, "身份证号码无效，请检查输入！"

    # 4. 校验码计算
    # 4.1 定义系数数组（国家标准GB 11643-1999规定的系数）
    coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 4.2 定义余数到校验码的映射关系
    mapping = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')

    # 4.3 计算加权和
    total = 0
    for i in range(17):
        total += int(id_number[i]) * coefficients[i]

    # 4.4 计算余数
    remainder = total % 11

    # 4.5 验证校验码
    if mapping[remainder] != id_number[17]:
        return False, "身份证号码无效，请检查输入！"

    # 5. 所有检查通过，返回有效的身份证号
    return True, id_number


"""
信息提取函数
功能：从身份证号码中提取基本信息
参数：id_number - 有效的身份证号码字符串
返回值：元组 (行政区划代码, 出生日期, 性别)
"""


def extract_info(id_number):
    # 1. 提取行政区划代码（前6位）
    region_code = id_number[:6]

    # 2. 提取并格式化出生日期（第7-14位）
    year = id_number[6:10]
    month = int(id_number[10:12])
    day = int(id_number[12:14])

    # 格式化日期显示
    month_str = str(month) if month >= 10 else f" {month} "
    day_str = str(day) if day >= 10 else f" {day} "
    birth_date = f"{year} 年 {month_str} 月 {day_str} 日"

    # 3. 提取并判断性别（第17位）
    gender_code = int(id_number[16])
    gender = "男" if gender_code % 2 == 1 else "女"

    return region_code, birth_date, gender


"""
行政区划信息查找函数
功能：在数据字典中查找行政区划信息
参数：region_code - 6位行政区划代码
返回值：元组 (省级, 地市级, 县区级, 数据来源)
"""


def find_region_info(region_code):
    return region_data.get(region_code, ("-", "-", "-", "-"))


"""
验证按钮点击事件处理函数
功能：处理用户点击验证按钮的操作
"""


def on_validate(event=None):
    # 1. 获取用户输入的身份证号码
    id_number = entry.get().strip()

    # 2. 清空结果显示
    for label in value_labels:
        label.config(text="")

    # 3. 验证身份证
    is_valid, result = validate_id_card(id_number)

    # 4. 如果无效，显示错误信息
    if not is_valid:
        messagebox.showerror("错误", result)
        return

    # 5. 提取基本信息
    region_code, birth_date, gender = extract_info(result)

    # 6. 查找行政区划信息
    province, city, district, source = find_region_info(region_code)

    # 7. 更新显示结果
    value_labels[0].config(text=gender)  # 性别
    value_labels[1].config(text=birth_date)  # 出生日期
    value_labels[2].config(text=province)  # 省级
    value_labels[3].config(text=city)  # 地市级
    value_labels[4].config(text=district)  # 县区级
    value_labels[5].config(text=source)  # 数据来源


# ============== 图形用户界面构建 ============== #

# 创建主窗口
root = tk.Tk()
root.title("身份证验证系统")
root.geometry("500x480")
root.minsize(500, 480)
root.resizable(True, True)

# 设置主题颜色
bg_color = "#f0f8ff"
frame_color = "#e6f2ff"
button_color = "#4da6ff"
button_hover_color = "#3399ff"
root.config(bg=bg_color)

# 创建主容器
main_container = tk.Frame(root, bg=bg_color)
main_container.pack(fill="both", expand=True, padx=10, pady=10)

# 标题标签
title_label = tk.Label(
    main_container,
    text="身份证信息验证系统",
    font=("微软雅黑", 18, "bold"),
    bg=bg_color,
    fg="#0066cc"
)
title_label.pack(pady=(0, 15))

# 输入区域框架
input_frame = tk.Frame(main_container, bg=frame_color, padx=15, pady=15)
input_frame.pack(fill="x", padx=5, pady=5)

# 输入提示标签
tk.Label(
    input_frame,
    text="身份证号码:",
    font=("微软雅黑", 12),
    bg=frame_color
).pack(side="left", padx=(0, 10))

# 输入框
entry = tk.Entry(
    input_frame,
    font=("微软雅黑", 12),
    width=22,
    bd=2,
    relief="groove"
)
entry.pack(side="left", padx=(0, 10))
entry.focus()

# 绑定回车键事件
entry.bind("<Return>", on_validate)

# 验证按钮
validate_btn = tk.Button(
    input_frame,
    text="验证",
    font=("微软雅黑", 12, "bold"),
    bg=button_color,
    fg="white",
    activebackground="#3399ff",
    activeforeground="white",
    relief="flat",
    command=on_validate,
    padx=15
)
validate_btn.pack(side="left", padx=(10, 0))


# 按钮悬停效果
def on_enter(e):
    validate_btn.config(bg=button_hover_color)


def on_leave(e):
    validate_btn.config(bg=button_color)


validate_btn.bind("<Enter>", on_enter)
validate_btn.bind("<Leave>", on_leave)

# 结果展示区域
result_frame = tk.LabelFrame(
    main_container,
    text="身份证信息",
    font=("微软雅黑", 12),
    bg=bg_color,
    padx=15,
    pady=15
)
result_frame.pack(fill="both", expand=True, padx=5, pady=5)

# 信息项定义
info_items = [
    "性　　别",
    "出　　生",
    "省　　级",
    "地 市 级",
    "县 区 级",
    "数据来源"
]

# 值标签列表
value_labels = []

# 信息容器
info_container = tk.Frame(result_frame, bg=bg_color)
info_container.pack(fill="both", expand=True, padx=5, pady=5)

# 创建信息行
for i, item in enumerate(info_items):
    row_frame = tk.Frame(info_container, bg=bg_color)
    row_frame.pack(fill="x", padx=5, pady=2)

    # 信息标签
    tk.Label(
        row_frame,
        text=item,
        font=("微软雅黑", 12),
        bg=bg_color,
        anchor="w",
        width=8
    ).pack(side="left", padx=(0, 5))

    # 值标签
    value_label = tk.Label(
        row_frame,
        text="",
        font=("微软雅黑", 12),
        bg=bg_color,
        anchor="w",
        wraplength=350,
        justify="left"
    )
    value_label.pack(side="left", fill="x", expand=True)
    value_labels.append(value_label)

# 底部状态栏
status_bar = tk.Label(
    root,
    text="中国居民身份证验证系统 | 基于 GB 11643-1999 标准 | MIT License",
    font=("微软雅黑", 10),
    bg="#d9e6f2",
    fg="#333333",
    bd=1,
    relief="sunken",
    anchor="center",
    padx=10,
    pady=8
)
status_bar.pack(side="bottom", fill="x", pady=(0, 0))

# 启动主事件循环
root.mainloop()
