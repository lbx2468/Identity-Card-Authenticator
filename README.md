# Identity-Card-Authenticator | 身份证验证系统
基于Python GUI的身份证验证系统，支持身份证有效性验证、信息提取和行政区划查询功能。

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 功能特点

- ✅ 身份证有效性验证（符合GB 11643-1999标准）
- 📅 出生日期提取（格式：1970年1月1日）
- ♂️ 性别判断（根据身份证第17位）
- 🗺️ 行政区划信息查询（省级、地市级、县区级、数据来源）
- 🖥️ 简洁美观的GUI界面
- ✨ 按钮悬停高光效果
- 📏 长文本自动换行显示
- ❌ 友好的错误提示

## 界面展示

```
身份证信息验证系统

身份证号码：11010119700101931X    验证

身份证信息
性　　别    男
出　　生    1970 年 1 月 1 日
省　　级    北京市
地 市 级    市辖区
县 区 级    东城区
数据来源    民政部

中国居民身份证验证系统 | 基于 GB 11643-1999 标准
```

## 使用说明

1. **安装依赖**：
   ```bash
   pip install tkinter
   ```

2. **下载项目文件**：
   - `main.py` - 主程序
   - `idCode.py` - 行政区划数据

3. **运行程序**：
   ```bash
   python main.py
   ```

4. **输入身份证号码**：
   - 在输入框中输入18位身份证号码
   - 支持最后一位大小写"X"

5. **点击验证**：
   - 系统将验证身份证有效性
   - 显示提取的身份证信息

## ChangeLog

| 版本 | 主要变更 |
|-------------|-------------|
| v1.0.0-beta | 初始实现身份证验证系统 |
| v1.0.1-beta | 修复信息显示不全问题，优化为三行两列布局 |
| v1.0.2-beta | 支持长地名显示，添加自动换行和滚动条 |
| v1.0.3-beta | 修复信息重复显示问题，分离标签和值显示 |
| v1.0.4-beta | 简化错误提示为"身份证号码格式错误"和"身份证号码无效" |
| v1.0.5-beta | 彻底解决状态栏显示问题，增加窗口最小高度 |
| v1.1.0-beta | 修复了 Excel 文件读取问题，使用Excel存储数据 |
| v1.1.1-beta | 优化代码注释，增加可读性 |
| v1.1.2-beta | 移除Excel依赖，使用idCode.py存储数据，简化查找函数 |
| v1.1.3-beta | 优化出生日期格式为"1970年1月1日"（去除前导零） |
| v1.1.4-beta | 为验证按钮添加鼠标悬停高光效果 |
| v1.2.0-beta | 回车触发验证+日期范围验证 |
| v1.2.1-beta | 简化错误提示，输入错误合并 |
| v1.2.2-beta | 合并验证逻辑，减少重复代码 |
| v1.3.0-beta | OOP重构 |
| v1.3.1-beta | 重构界面布局并简化验证逻辑 |
| v1.4.0-rc   | 新增图标，程序打包为exe |

## 技术栈

- **编程语言**：Python 3.7+
- **GUI框架**：Tkinter
- **数据结构**：字典（存储行政区划数据）
- **验证算法**：GB 11643-1999标准

## 如何贡献

1.  Fork项目仓库
2.  创建新分支 (`git checkout -b feature/your-feature`)
3.  提交更改 (`git commit -am 'Add some feature'`)
4.  推送分支 (`git push origin feature/your-feature`)
5.  创建Pull Request

## 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。
