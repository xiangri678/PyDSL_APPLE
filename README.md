# Apple_RSL: Domain-Specific Language for Customer Service Chatbot

![Apple_RSL](https://img.shields.io/badge/Apple__RSL-Customer%20Service%20DSL-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-red)

A domain-specific language (DSL) for defining and implementing automated customer service chatbots. This project provides a language interpreter that processes scripts written in Apple_RSL and executes them to create interactive customer service experiences.

## Features

- Custom DSL designed specifically for customer service interactions
- Script parser that transforms text scripts into executable structures
- Interactive interpreter with both CLI and GUI interfaces
- User data management and authentication
- 6 service categories: Product Information, Order Processing, Account Management, Technical Support, Company Policies, and Promotions
- Comprehensive testing framework

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/Apple_RSL.git
cd Apple_RSL
```

2. Install dependencies

```bash
pip install PyQt5
```

## Usage

### Running the GUI version

```bash
python interpreter_GUI.py script_after_sale.txt
```

### Running the CLI version

```bash
python interpreter.py script_pre_sale.txt
```

### Available Scripts

- `script_pre_sale.txt` - Pre-sales service including product info, promotions, and company policies
- `script_after_sale.txt` - After-sales service including order processing, tech support, and company policies
- `script_support.txt` - Customer support services including account management and order processing
- `script_wechat.txt` - WeChat interface including product info, promotions, and order processing

## Project Structure

```
Apple_RSL/
├── py/                  # Python source files
│   ├── parser.py        # Script parser implementation
│   ├── interpreter.py   # CLI interpreter
│   └── interpreter_GUI.py  # GUI interpreter implementation
├── script/              # Apple_RSL scripts
│   ├── script_pre_sale.txt
│   ├── script_after_sale.txt
│   ├── script_support.txt
│   └── script_wechat.txt
├── test/                # Testing files and modules
│   ├── test_parser_V3.py
│   ├── test_interpreter_V1.py
│   └── testsuite.py
├── user_data.json       # Sample user data for testing
└── README.md
```

## Apple_RSL Language Specification

Apple_RSL is defined using BNF notation:

```
<Script> ::= <Step>+
<Step> ::= "Step" <Identifier> <NewLine> <Command>+
<Command> ::= <Say> | <Listen> | <Branch> | <Awake> | <Default> | <Exit>

<Say> ::= "SAY" <QuotedString> <NewLine>
<Listen> ::= "LISTEN" <Number> <Number> <NewLine>
<Branch> ::= "BRANCH" <QuotedString> <Identifier> <NewLine>
<Awake> ::= "AWAKE"  <Identifier> <NewLine>
<Default> ::= "DEFAULT" <Identifier> <NewLine>
<Exit> ::= "EXIT" <NewLine>
```

## Testing

Run the test suite to verify all components:

```bash
python testsuite.py
```

Individual tests can also be run:

```bash
# Test the parser
python test_parser_V3.py

# Test the interpreter
python test_interpreter_V1.py
```

## License

[MIT License](LICENSE)

# Apple_RSL: 基于领域特定语言的客服机器人设计与实现

![Apple_RSL](https://img.shields.io/badge/Apple__RSL-客服DSL-blue)
![Python](https://img.shields.io/badge/Python-3.x-green)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-red)

这是一个领域特定语言(DSL)项目，用于定义和实现自动化客服机器人。该项目提供了一个语言解释器，可以处理使用Apple_RSL编写的脚本并执行它们来创建交互式客服体验。

## 功能特点

- 专为客服交互设计的自定义DSL
- 将文本脚本转换为可执行结构的脚本解析器
- 支持CLI和GUI界面的交互式解释器
- 用户数据管理和身份验证
- 6种服务类别：产品信息、订单处理、账户管理、技术支持、公司政策和促销活动
- 全面的测试框架


## 安装方法

1. 克隆仓库

```bash
git clone https://github.com/yourusername/Apple_RSL.git
cd Apple_RSL
```

2. 安装依赖

```bash
pip install PyQt5
```

## 使用方法

### 运行GUI版本

```bash
python interpreter_GUI.py script_after_sale.txt
```

### 运行CLI版本

```bash
python interpreter.py script_pre_sale.txt
```

### 可用脚本

- `script_pre_sale.txt` - 售前服务，包括产品信息、促销活动和公司政策
- `script_after_sale.txt` - 售后服务，包括订单处理、技术支持和公司政策
- `script_support.txt` - 客户支持服务，包括账户管理和订单处理
- `script_wechat.txt` - 微信接口，包括产品信息、促销活动和订单处理

## 项目结构

```
Apple_RSL/
├── py/                  # Python源文件
│   ├── parser.py        # 脚本解析器实现
│   ├── interpreter.py   # CLI解释器
│   └── interpreter_GUI.py  # GUI解释器实现
├── script/              # Apple_RSL脚本
│   ├── script_pre_sale.txt
│   ├── script_after_sale.txt
│   ├── script_support.txt
│   └── script_wechat.txt
├── test/                # 测试文件和模块
│   ├── test_parser_V3.py
│   ├── test_interpreter_V1.py
│   └── testsuite.py
├── user_data.json       # 用于测试的示例用户数据
└── README.md
```

## Apple_RSL语言规范

Apple_RSL使用BNF表示法定义：

```
<Script> ::= <Step>+
<Step> ::= "Step" <Identifier> <NewLine> <Command>+
<Command> ::= <Say> | <Listen> | <Branch> | <Awake> | <Default> | <Exit>

<Say> ::= "SAY" <QuotedString> <NewLine>
<Listen> ::= "LISTEN" <Number> <Number> <NewLine>
<Branch> ::= "BRANCH" <QuotedString> <Identifier> <NewLine>
<Awake> ::= "AWAKE"  <Identifier> <NewLine>
<Default> ::= "DEFAULT" <Identifier> <NewLine>
<Exit> ::= "EXIT" <NewLine>
```

## 测试

运行测试套件以验证所有组件：

```bash
python testsuite.py
```

也可以单独运行各个测试：

```bash
# 测试解析器
python test_parser_V3.py

# 测试解释器
python test_interpreter_V1.py
```

## 许可证

[MIT许可证](LICENSE)
