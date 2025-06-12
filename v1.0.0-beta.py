# 初始实现身份证验证系统，使用Excel存储数据

import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os


# 身份证验证函数
def validate_id_card(id_number):
    """验证身份证号码的有效性"""
    # 处理最后一位的X
    id_number = id_number.upper()

    # 基本检查
    if len(id_number) != 18:
        return False, "长度错误，身份证应为18位"

    if not id_number[:17].isdigit():
        return False, "前17位必须为数字"

    if id_number[-1] not in "0123456789X":
        return False, "最后一位应为数字或X"

    # 校验码计算
    coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    mapping = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}

    total = 0
    for i in range(17):
        total += int(id_number[i]) * coefficients[i]

    remainder = total % 11
    if mapping[remainder] != id_number[17]:
        return False, f"校验码错误，应为{mapping[remainder]}"

    return True, id_number


# 提取信息函数
def extract_info(id_number):
    """从身份证号码中提取信息"""
    # 行政区划代码（前6位）
    region_code = id_number[:6]

    # 出生日期（7-14位）
    birth_date = f"{id_number[6:10]}-{id_number[10:12]}-{id_number[12:14]}"

    # 性别（第17位）
    gender_code = int(id_number[16])
    gender = "男" if gender_code % 2 == 1 else "女"

    return region_code, birth_date, gender


# 查找行政区划信息
def find_region_info(region_code):
    """在Excel中查找行政区划信息"""
    # 尝试从Excel文件读取数据
    try:
        # 创建模拟的Excel数据（实际使用时请替换为真实文件）
        data = {
            '行政区划代码': ['110000', '110100', '110101', '110102', '110105', '110106', '110107', '110108', '110109',
                             '120000', '120100', '120101'],
            '省级': ['北京市', '北京市', '北京市', '北京市', '北京市', '北京市', '北京市', '北京市', '北京市', '天津市',
                     '天津市', '天津市'],
            '地市级': ['', '市辖区', '市辖区', '市辖区', '市辖区', '市辖区', '市辖区', '市辖区', '市辖区', '', '市辖区',
                       '市辖区'],
            '县区级': ['', '', '东城区', '西城区', '朝阳区', '丰台区', '石景山区', '海淀区', '门头沟区', '', '',
                       '和平区'],
            '数据来源': ['民政部', '国标', '民政部', '民政部', '民政部', '民政部', '民政部', '民政部', '民政部',
                         '民政部', '国标', '民政部']
        }
        df = pd.DataFrame(data)

        # 在实际应用中，使用以下代码读取Excel文件
        # df = pd.read_excel('idCode.xlsx')

        # 查找匹配的行政区划代码
        match = df[df['行政区划代码'] == region_code]

        if not match.empty:
            return (
                match.iloc[0]['省级'],
                match.iloc[0]['地市级'],
                match.iloc[0]['县区级'],
                match.iloc[0]['数据来源']
            )
        return "未知", "未知", "未知", "未知"
    except Exception as e:
        print(f"读取行政区划信息出错: {e}")
        return "未知", "未知", "未知", "未知"


# 验证按钮点击事件
def on_validate():
    """处理验证按钮点击事件"""
    id_number = entry.get().strip()

    # 清空结果显示
    for label in info_labels:
        label.config(text="")

    # 验证身份证
    is_valid, result = validate_id_card(id_number)

    if not is_valid:
        messagebox.showerror("错误", f"身份证无效: {result}")
        return

    # 提取基本信息
    region_code, birth_date, gender = extract_info(result)

    # 查找行政区划信息
    province, city, district, source = find_region_info(region_code)

    # 更新显示结果
    info_labels[0].config(text=f"省级: {province}")
    info_labels[1].config(text=f"地市级: {city}")
    info_labels[2].config(text=f"县区级: {district}")
    info_labels[3].config(text=f"数据来源: {source}")
    info_labels[4].config(text=f"出生日期: {birth_date}")
    info_labels[5].config(text=f"性别: {gender}")


# 创建主窗口
root = tk.Tk()
root.title("身份证验证系统")
root.geometry("500x400")
root.resizable(False, False)

# 设置主题颜色
bg_color = "#f0f8ff"  # 浅蓝色背景
frame_color = "#e6f2ff"  # 浅蓝色框架
button_color = "#4da6ff"  # 蓝色按钮
root.config(bg=bg_color)

# 标题
title_label = tk.Label(
    root,
    text="身份证信息验证系统",
    font=("微软雅黑", 18, "bold"),
    bg=bg_color,
    fg="#0066cc"
)
title_label.pack(pady=15)

# 输入框区域
input_frame = tk.Frame(root, bg=frame_color, padx=15, pady=15)
input_frame.pack(fill="x", padx=20, pady=10)

tk.Label(
    input_frame,
    text="请输入身份证号码:",
    font=("微软雅黑", 12),
    bg=frame_color
).pack(side="left", padx=(0, 10))

entry = tk.Entry(
    input_frame,
    font=("微软雅黑", 12),
    width=20,
    bd=2,
    relief="groove"
)
entry.pack(side="left", padx=(0, 10))
entry.focus()

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
validate_btn.pack(side="left")

# 结果展示区域
result_frame = tk.LabelFrame(
    root,
    text="身份证信息",
    font=("微软雅黑", 12),
    bg=bg_color,
    padx=15,
    pady=15
)
result_frame.pack(fill="both", expand=True, padx=20, pady=10)

# 创建6个标签用于显示结果
info_texts = ["省级:", "地市级:", "县区级:", "数据来源:", "出生日期:", "性别:"]
info_labels = []

for text in info_texts:
    label = tk.Label(
        result_frame,
        text=text,
        font=("微软雅黑", 12),
        bg=bg_color,
        anchor="w",
        width=30
    )
    label.pack(fill="x", padx=10, pady=5)
    info_labels.append(label)

# 底部状态栏
status_bar = tk.Label(
    root,
    text="中国居民身份证验证系统 | 基于GB 11643-1999标准",
    font=("微软雅黑", 9),
    bg="#d9e6f2",
    fg="#666666",
    bd=1,
    relief="sunken",
    anchor="center"
)
status_bar.pack(side="bottom", fill="x")

# 运行主循环
root.mainloop()
