import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
from datetime import datetime


class IDValidator:
    def __init__(self):
        # 创建行政区划代码映射
        self.area_codes = {}
        self.load_area_codes()

        # 创建省级映射
        self.province_map = {
            '11': '北京市', '12': '天津市', '13': '河北省', '14': '山西省', '15': '内蒙古自治区',
            '21': '辽宁省', '22': '吉林省', '23': '黑龙江省', '31': '上海市', '32': '江苏省',
            '33': '浙江省', '34': '安徽省', '35': '福建省', '36': '江西省', '37': '山东省',
            '41': '河南省', '42': '湖北省', '43': '湖南省', '44': '广东省', '45': '广西壮族自治区',
            '46': '海南省', '50': '重庆市', '51': '四川省', '52': '贵州省', '53': '云南省',
            '54': '西藏自治区', '61': '陕西省', '62': '甘肃省', '63': '青海省', '64': '宁夏回族自治区',
            '65': '新疆维吾尔自治区'
        }

    def load_area_codes(self):
        # 这里简化了行政区划代码的加载
        # 实际应用中可以从Excel文件加载完整数据
        self.area_codes = {
            '110101': '北京市东城区', '110102': '北京市西城区', '110105': '北京市朝阳区',
            '110106': '北京市丰台区', '110107': '北京市石景山区', '110108': '北京市海淀区',
            '110109': '北京市门头沟区', '110111': '北京市房山区', '110112': '北京市通州区',
            '110113': '北京市顺义区', '110114': '北京市昌平区', '110115': '北京市大兴区',
            '110116': '北京市怀柔区', '110117': '北京市平谷区', '110118': '北京市密云区',
            '110119': '北京市延庆区', '120101': '天津市和平区', '120102': '天津市河东区',
            '120103': '天津市河西区', '120104': '天津市南开区', '120105': '天津市河北区',
            '120106': '天津市红桥区', '120110': '天津市东丽区', '120111': '天津市西青区',
            '120112': '天津市津南区', '120113': '天津市北辰区', '120114': '天津市武清区',
            '120115': '天津市宝坻区', '120116': '天津市滨海新区', '120117': '天津市宁河区',
            '120118': '天津市静海区', '120119': '天津市蓟州区', '130102': '石家庄市长安区',
            '130104': '石家庄市桥西区', '130105': '石家庄市新华区', '130107': '石家庄市井陉矿区',
            '130108': '石家庄市裕华区', '130109': '石家庄市藁城区', '130110': '石家庄市鹿泉区',
            '130111': '石家庄市栾城区', '130121': '石家庄市井陉县', '130123': '石家庄市正定县',
            '130125': '石家庄市行唐县', '130126': '石家庄市灵寿县', '130127': '石家庄市高邑县',
            '130128': '石家庄市深泽县', '130129': '石家庄市赞皇县', '130130': '石家庄市无极县',
            '130131': '石家庄市平山县', '130132': '石家庄市元氏县', '130133': '石家庄市赵县',
            '130181': '石家庄市辛集市', '130183': '石家庄市晋州市', '130184': '石家庄市新乐市',
            '130202': '唐山市路南区', '130203': '唐山市路北区', '130204': '唐山市古冶区',
            '130205': '唐山市开平区', '130207': '唐山市丰南区', '130208': '唐山市丰润区',
            '130209': '唐山市曹妃甸区', '130224': '唐山市滦南县', '130225': '唐山市乐亭县',
            '130227': '唐山市迁西县', '130229': '唐山市玉田县', '130281': '唐山市遵化市',
            '130283': '唐山市迁安市', '130284': '唐山市滦州市', '130302': '秦皇岛市海港区',
            '130303': '秦皇岛市山海关区', '130304': '秦皇岛市北戴河区', '130306': '秦皇岛市抚宁区',
            '130321': '秦皇岛市青龙满族自治县', '130322': '秦皇岛市昌黎县', '130324': '秦皇岛市卢龙县',
            '130402': '邯郸市邯山区', '130403': '邯郸市丛台区', '130404': '邯郸市复兴区',
            '130406': '邯郸市峰峰矿区', '130407': '邯郸市肥乡区', '130408': '邯郸市永年区',
            '130423': '邯郸市临漳县', '130424': '邯郸市成安县', '130425': '邯郸市大名县',
            '130426': '邯郸市涉县', '130427': '邯郸市磁县', '130430': '邯郸市邱县',
            '130431': '邯郸市鸡泽县', '130432': '邯郸市广平县', '130433': '邯郸市馆陶县',
            '130434': '邯郸市魏县', '130435': '邯郸市曲周县', '130481': '邯郸市武安市',
            '130502': '邢台市襄都区', '130503': '邢台市信都区', '130505': '邢台市任泽区',
            '130506': '邢台市南和区', '130522': '邢台市临城县', '130523': '邢台市内丘县',
            '130524': '邢台市柏乡县', '130525': '邢台市隆尧县', '130528': '邢台市宁晋县',
            '130529': '邢台市巨鹿县', '130530': '邢台市新河县', '130531': '邢台市广宗县',
            '130532': '邢台市平乡县', '130533': '邢台市威县', '130534': '邢台市清河县',
            '130535': '邢台市临西县', '130581': '邢台市南宫市', '130582': '邢台市沙河市',
            '130602': '保定市竞秀区', '130606': '保定市莲池区', '130607': '保定市满城区',
            '130608': '保定市清苑区', '130609': '保定市徐水区', '130623': '保定市涞水县',
            '130624': '保定市阜平县', '130626': '保定市定兴县', '130627': '保定市唐县',
            '130628': '保定市高阳县', '130629': '保定市容城县', '130630': '保定市涞源县',
            '130631': '保定市望都县', '130632': '保定市安新县', '130633': '保定市易县',
            '130634': '保定市曲阳县', '130635': '保定市蠡县', '130636': '保定市顺平县',
            '130637': '保定市博野县', '130638': '保定市雄县', '130681': '保定市涿州市',
            '130682': '保定市定州市', '130683': '保定市安国市', '130684': '保定市高碑店市',
            '130702': '张家口市桥东区', '130703': '张家口市桥西区', '130705': '张家口市宣化区',
            '130706': '张家口市下花园区', '130708': '张家口市万全区', '130709': '张家口市崇礼区',
            '130722': '张家口市张北县', '130723': '张家口市康保县', '130724': '张家口市沽源县',
            '130725': '张家口市尚义县', '130726': '张家口市蔚县', '130727': '张家口市阳原县',
            '130728': '张家口市怀安县', '130730': '张家口市怀来县', '130731': '张家口市涿鹿县',
            '130732': '张家口市赤城县', '130802': '承德市双桥区', '130803': '承德市双滦区',
            '130804': '承德市鹰手营子矿区', '130821': '承德市承德县', '130822': '承德市兴隆县',
            '130824': '承德市滦平县', '130825': '承德市隆化县', '130826': '承德市丰宁满族自治县',
            '130827': '承德市宽城满族自治县', '130828': '承德市围场满族蒙古族自治县',
            '130881': '承德市平泉市', '130902': '沧州市新华区', '130903': '沧州市运河区',
            '130921': '沧州市沧县', '130922': '沧州市青县', '130923': '沧州市东光县',
            '130924': '沧州市海兴县', '130925': '沧州市盐山县', '130926': '沧州市肃宁县',
            '130927': '沧州市南皮县', '130928': '沧州市吴桥县', '130929': '沧州市献县',
            '130930': '沧州市孟村回族自治县', '130981': '沧州市泊头市', '130982': '沧州市任丘市',
            '130983': '沧州市黄骅市', '130984': '沧州市河间市', '131002': '廊坊市安次区',
            '131003': '廊坊市广阳区', '131022': '廊坊市固安县', '131023': '廊坊市永清县',
            '131024': '廊坊市香河县', '131025': '廊坊市大城县', '131026': '廊坊市文安县',
            '131028': '廊坊市大厂回族自治县', '131081': '廊坊市霸州市', '131082': '廊坊市三河市',
            '131102': '衡水市桃城区', '131103': '衡水市冀州区', '131121': '衡水市枣强县',
            '131122': '衡水市武邑县', '131123': '衡水市武强县', '131124': '衡水市饶阳县',
            '131125': '衡水市安平县', '131126': '衡水市故城县', '131127': '衡水市景县',
            '131128': '衡水市阜城县', '131182': '衡水市深州市'
        }

    def validate_id(self, id_number):
        """验证身份证号码的有效性"""
        # 基本格式验证
        if not re.match(r'^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dX]$', id_number):
            return False, "身份证格式不正确"

        # 校验码验证
        factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

        total = 0
        for i in range(17):
            total += int(id_number[i]) * factors[i]

        remainder = total % 11
        if id_number[17].upper() != check_codes[remainder]:
            return False, "校验码错误"

        # 日期验证
        try:
            birth_date = datetime.strptime(id_number[6:14], '%Y%m%d')
            if birth_date > datetime.now():
                return False, "出生日期无效"
        except ValueError:
            return False, "出生日期无效"

        return True, "身份证有效"

    def get_area_info(self, id_number):
        """获取地区信息"""
        area_code = id_number[:6]
        province_code = id_number[:2]

        # 获取省级名称
        province = self.province_map.get(province_code, "未知省份")

        # 获取详细地区信息
        area = self.area_codes.get(area_code, "未知地区")

        return f"{province} {area}"

    def get_birth_date(self, id_number):
        """获取出生日期"""
        birth_str = id_number[6:14]
        try:
            birth_date = datetime.strptime(birth_str, '%Y%m%d')
            return birth_date.strftime('%Y年%m月%d日')
        except ValueError:
            return "未知"

    def get_gender(self, id_number):
        """获取性别"""
        gender_digit = int(id_number[16])
        return "男" if gender_digit % 2 == 1 else "女"

    def get_age(self, id_number):
        """计算年龄"""
        birth_str = id_number[6:14]
        try:
            birth_date = datetime.strptime(birth_str, '%Y%m%d')
            today = datetime.now()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return str(age)
        except:
            return "未知"


class IDValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("中国居民身份证验证系统")
        self.root.geometry("600x450")
        self.root.resizable(True, True)

        # 设置应用图标
        try:
            self.root.iconbitmap("id_icon.ico")
        except:
            pass

        # 创建验证器实例
        self.validator = IDValidator()

        # 创建样式
        self.create_styles()

        # 创建UI
        self.create_widgets()

    def create_styles(self):
        # 创建样式对象
        self.style = ttk.Style()

        # 配置标签样式
        self.style.configure("Header.TLabel",
                             font=("微软雅黑", 14, "bold"),
                             foreground="#2c3e50",
                             padding=10)

        # 配置输入框样式
        self.style.configure("Input.TEntry",
                             font=("微软雅黑", 12),
                             padding=5)

        # 配置按钮样式
        self.style.configure("Action.TButton",
                             font=("微软雅黑", 12, "bold"),
                             foreground="white",
                             background="#3498db",
                             padding=10)

        self.style.map("Action.TButton",
                       background=[("active", "#2980b9")])

        # 配置结果框样式
        self.style.configure("Result.TFrame",
                             background="#ecf0f1",
                             borderwidth=2,
                             relief="groove")

        self.style.configure("Result.TLabel",
                             font=("微软雅黑", 11),
                             background="#ecf0f1",
                             foreground="#2c3e50",
                             padding=(10, 5))

        self.style.configure("Value.TLabel",
                             font=("微软雅黑", 11, "bold"),
                             background="#ecf0f1",
                             foreground="#e74c3c",
                             padding=(10, 5))

    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        header = ttk.Label(main_frame,
                           text="中国居民身份证验证系统",
                           style="Header.TLabel")
        header.pack(pady=(0, 20))

        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(input_frame, text="身份证号码:", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.W)

        self.id_entry = ttk.Entry(input_frame, width=25, font=("微软雅黑", 12))
        self.id_entry.grid(row=0, column=1, padx=10)
        self.id_entry.bind("<Return>", self.validate_id)

        validate_btn = ttk.Button(input_frame,
                                  text="验证",
                                  style="Action.TButton",
                                  command=self.validate_id)
        validate_btn.grid(row=0, column=2)

        # 示例标签
        example_label = ttk.Label(input_frame,
                                  text="示例: 110101199001011234",
                                  font=("微软雅黑", 9),
                                  foreground="#7f8c8d")
        example_label.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=(5, 0))

        # 结果区域
        result_frame = ttk.LabelFrame(main_frame, text="验证结果", style="Result.TFrame")
        result_frame.pack(fill=tk.BOTH, expand=True)

        # 创建结果标签
        labels = ["有效性:", "地区信息:", "出生日期:", "年龄:", "性别:"]
        self.result_vars = {}

        for i, label in enumerate(labels):
            ttk.Label(result_frame, text=label, style="Result.TLabel").grid(
                row=i, column=0, sticky=tk.W, padx=10, pady=5
            )

            value_var = tk.StringVar(value="")
            value_label = ttk.Label(result_frame, textvariable=value_var, style="Value.TLabel")
            value_label.grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)

            self.result_vars[label] = value_var

        # 分隔线
        separator = ttk.Separator(result_frame, orient=tk.HORIZONTAL)
        separator.grid(row=len(labels), column=0, columnspan=2, sticky=tk.EW, pady=10, padx=10)

        # 额外信息
        ttk.Label(result_frame, text="校验码验证:", style="Result.TLabel").grid(
            row=len(labels) + 1, column=0, sticky=tk.W, padx=10, pady=5
        )

        self.check_var = tk.StringVar(value="")
        ttk.Label(result_frame, textvariable=self.check_var, style="Value.TLabel").grid(
            row=len(labels) + 1, column=1, sticky=tk.W, padx=10, pady=5
        )

        # 版权信息
        copyright_label = ttk.Label(
            main_frame,
            text="© 2023 中国居民身份证验证系统 | 基于国家标准 GB 11643-1999",
            font=("微软雅黑", 8),
            foreground="#7f8c8d"
        )
        copyright_label.pack(side=tk.BOTTOM, pady=(10, 0))

    def validate_id(self, event=None):
        """验证身份证号码并显示结果"""
        id_number = self.id_entry.get().strip()

        # 清空结果
        for var in self.result_vars.values():
            var.set("")
        self.check_var.set("")

        if not id_number:
            messagebox.showwarning("输入错误", "请输入身份证号码")
            return

        # 验证身份证
        is_valid, message = self.validator.validate_id(id_number)

        # 显示验证结果
        self.result_vars["有效性:"].set("有效" if is_valid else "无效")

        if is_valid:
            # 显示详细信息
            self.result_vars["地区信息:"].set(self.validator.get_area_info(id_number))
            self.result_vars["出生日期:"].set(self.validator.get_birth_date(id_number))
            self.result_vars["年龄:"].set(self.validator.get_age(id_number))
            self.result_vars["性别:"].set(self.validator.get_gender(id_number))

            # 显示校验码验证详情
            self.check_var.set("校验通过")
        else:
            # 显示错误信息
            messagebox.showerror("身份证无效", message)
            self.check_var.set("验证失败")


if __name__ == "__main__":
    root = tk.Tk()
    app = IDValidatorApp(root)
    root.mainloop()
