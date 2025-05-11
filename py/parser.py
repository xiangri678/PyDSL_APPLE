import re
import sys


class Step:
    def __init__(self, name):
        self.name = name
        self.expressions = []  # 用于存储多个 SAY 命令的句子。
        self.listen = []  # 存储听取时长的起始和结束范围。
        self.answers = {}  # 包含可能的后继状态。
        self.default = None  # 如果没有匹配，则转移到默认状态。
        self.awake = None  # 如果无响应，则转移到唤醒状态。


class Script:
    def __init__(self):
        self.steps = []  # 脚本中所有状态的列表。
        self.vars = None  # 脚本使用的所有变量。
        self.actions = {}  # 可用的所有动作。
        self.entry = None  # 脚本的入口状态。

    def add_step(self, step):
        self.steps.append(step)


# 解析文件并返回一个 Script 对象。
def parse_file(file_name):
    script = Script()
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                parse_line(line, script)
    return script


# 解析文件的一行
def parse_line(line, script):
    # 分割行，并保持引号内的字符串不变。
    tokens = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', line)
    # 处理每个分词，如果遇到 '#' 开始的分词则停止。
    for token in tokens:
        if token.startswith('#'):
            index = tokens.index(token)
            tokens = tokens[:index]
            break
    process_tokens(tokens, script)


# 根据首个分词的类型处理剩余的分词。
def process_tokens(tokens, script):
    if tokens[0] == 'Step':
        process_step(script, tokens)
    current_step = script.steps[-1]
    if tokens[0] == 'SAY':
        process_say(current_step, tokens)
    elif tokens[0] == 'LISTEN':
        process_listen(current_step, tokens)
    elif tokens[0] == 'BRANCH':
        process_branch(current_step, script, tokens)
    elif tokens[0] == 'AWAKE':
        current_step.awake = tokens[1]
    elif tokens[0] == 'DEFAULT':
        current_step.default = tokens[1]


# 设置当前步骤的 LISTEN 参数。
def process_listen(current_step, tokens):
    current_step.listen.append(int(tokens[1]))
    current_step.listen.append(int(tokens[2]))


# 向当前步骤添加 SAY 命令的内容。
def process_say(current_step, tokens):
    if len(tokens) == 3:
        current_step.expressions.append(tokens[1].strip('"'))
        current_step.expressions.append(tokens[2])  # 把变量像句子一样存进list，执行的时候检查
    else:
        current_step.expressions.append(tokens[1].strip('"'))


# 创建一个新的 Step 实例并添加到脚本中。
def process_step(script, tokens):
    current_step = Step(tokens[1])
    if len(script.steps) == 0:
        script.entry = current_step
    script.add_step(current_step)


# 为当前步骤添加 BRANCH 条件及其后继状态。
def process_branch(current_step, script, tokens):
    input_token = tokens[1].strip('"')
    current_step.answers[input_token] = tokens[2]
    if input_token not in script.actions:
        script.actions[input_token] = tokens[2].strip('"')


# 解析表达式中的变量和文本。
def process_expression(tokens):
    expression = []
    for token in tokens:
        if token.startswith('#'):
            break
        elif token.startswith('<$') and token.endswith('>'):
            var_name = token[2:-1]
            expression.append(var_name)
            script.vars.append(var_name)
        else:
            expression.append(token.strip('"'))
    return expression


# 从文件中获取脚本并打印到文本文件。
def get_script_from_file(file_name):
    result_script = parse_file(file_name)
    print2txt(file_name, result_script)
    return result_script


# 将脚本信息输出到终端。
def print2terminal(script):
    global index, step
    print("Steps:", script.steps)
    print("Vars:", script.vars)
    print("Actions:", script.actions)
    print("Entry:", script.entry)
    print("Vars:", script.vars)
    # 使用enumerate()函数打印循环的号码
    for index, step in enumerate(script.steps, start=1):  # start=1 表示编号从1开始
        print("Step #{}".format(index))  # 打印当前的步骤号码
        print("Name:", step.name)
        print("Expressions:", step.expressions)
        print("Listen:", step.listen)
        print("Answers:", step.answers)
        print("Awake:", step.awake)
        print("Default:", step.default)


# 将脚本信息输出到文本文件。
def print2txt(file_name, result_script):
    print2file = "result_" + file_name[7:12] + ".txt"
    global file, index, step
    # 打开一个文件用于写入，如果文件不存在则创建它
    with open(print2file, 'w', encoding='utf-8') as file:
        # 使用enumerate()函数打印循环的号码
        for index, step in enumerate(result_script.steps, start=1):  # start=1 表示编号从1开始
            file.write("Step #{}\n".format(index))  # 写入当前的步骤号码
            file.write("Name: {}\n".format(step.name))
            file.write("Expressions: {}\n".format(step.expressions))
            file.write("Listen: {}\n".format(step.listen))
            file.write("Answers: {}\n".format(step.answers))
            file.write("Awake: {}\n".format(step.awake))
            file.write("Default: {}\n\n".format(step.default))


# 检查命令行参数，解析文件，并运行脚本。
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 Parser.py <parameter>")
        sys.exit(1)

    file_name = sys.argv[1]
    script = get_script_from_file(file_name)
