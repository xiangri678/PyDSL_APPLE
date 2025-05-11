import json
import signal
import sys

from parser import get_script_from_file


class Interpreter:
    def __init__(self, script):
        self.script = script
        self.current_step = script.entry

    def run(self):
        while self.current_step:
            self.execute_step(self.current_step)

    def execute_step(self, step):
        # 执行说话动作
        self.speak(step.expressions)

        # 执行听的动作
        if step.listen:
            intent = self.listen(step.listen)
        elif step.default:
            intent = 'default'
        else:
            exit(666)

        if step.name.startswith("validation"):
            valid, self.script.vars = self.check_user_exists(intent)
            if valid:
                intent = 'pass'
            else:
                intent = 'fail'

        # 获取下一个步骤的 ID
        next_step_id = self.get_next_step_id(step, intent)

        # 将当前步骤设置为新的步骤
        self.current_step = self.find_step_by_id(next_step_id)

    def speak(self, expression):
        for sentence in expression:
            if sentence.endswith('：'):
                print(sentence, end='')  # 不添加换行
            elif sentence.startswith("<$") and sentence.endswith(">"):
                # 剥离变量sentence开头的"<$"和结尾的">"
                expect_var = sentence[2:-1]
                # 使用变量名（键）检索数据
                var_value = self.script.vars.get(expect_var, 'NULL')  # 如果键不存在，返回默认值
                print(var_value)
            else:
                print(sentence)

    def listen(self, listen):
        # 在真正的应用中，这会更复杂，
        # 涉及到自然语言处理，以理解用户的意图
        try:
            # 设置信号闹钟
            # print('listen[1] is ', listen[1])
            signal.alarm(listen[1])
            user_input = input()
            signal.alarm(0)  # 输入完成，取消闹钟
            return user_input
        except TimeoutException:
            return ''  # 或者返回一个默认值

    def get_next_step_id(self, step, intent):
        if intent == '':
            return step.awake  # 去往本状态定义的保活状态
        elif intent in step.answers:
            return step.answers[intent]
        else:
            return step.default

    def find_step_by_id(self, step_id):
        for step in self.script.steps:
            if step.name == step_id:
                return step
        return None

    # 检查某个用户是否存在的函数
    def check_user_exists(self, username):
        # 首先读取文件
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)

        if username in user_data:
            return True, user_data[username]
        else:
            return False, None


# 定义一个超时的异常
class TimeoutException(Exception):
    pass


# 超时的处理函数
def signal_handler(signum, frame):
    raise TimeoutException


# 设置信号处理函数
signal.signal(signal.SIGALRM, signal_handler)

if __name__ == '__main__':
    # 检查是否有足够的参数传递给脚本
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <parameter>")
        sys.exit(1)

    # 第一个参数是脚本名，第二个参数是第一个用户提供的参数
    file_name = sys.argv[1]
    script = get_script_from_file(file_name)

    interpreter = Interpreter(script)
    interpreter.run()


