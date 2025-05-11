import json
import sys
import time

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QTimer, QEventLoop, QByteArray
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QHBoxLayout

from parser import get_script_from_file

USER_INPUTTED = ''  # 用来存储用户的输入

# SVG 数据，用于按钮图标
svg_data = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none"> <path d="M7 11L12 6L17 11M12 18V7" 
stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </svg>"""


class ChatDialog(QWidget):
    def __init__(self, interpreter):
        super().__init__()
        self.interpreter = interpreter  # 这行代码必须在initUI()调用之前，否则会引用未初始化的interpreter！
        self.initUI()
        print('ChatDialog initialized __init__')

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle(' Apple 支持')
        self.setGeometry(300, 100, 450, 600)

        # 创建垂直布局
        mainLayout = QVBoxLayout()

        # 创建文本编辑区域，用于显示对话历史
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        mainLayout.addWidget(self.textEdit)

        # 创建横向布局用于放置输入框和发送按钮
        bottomLayout = QHBoxLayout()

        # 创建输入框，并设置拉伸因子为1使其填满剩余空间
        self.inputLine = QLineEdit(self)
        bottomLayout.addWidget(self.inputLine, 1)

        # 创建按钮并设置SVG图标
        self.sendButton = QPushButton('发送', self)
        svg_bytes = QByteArray(svg_data.encode('utf-8'))
        svg_renderer = QSvgRenderer(svg_bytes)
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)  # 确保透明背景
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        self.sendButton.setIcon(QIcon(pixmap))

        # 创建发送按钮
        # sendButton = QPushButton('发送', self)
        self.sendButton.clicked.connect(self.send_message)  # 将按钮点击事件连接到 send_message 方法
        self.sendButton.clicked.connect(self.interpreter.on_submit)  # 当按钮被点击时，退出事件循环

        # 添加发送按钮到横向布局，同时添加弹性空间以推送到右下角
        bottomLayout.addWidget(self.sendButton)

        # 将横向布局添加到主垂直布局中
        mainLayout.addLayout(bottomLayout)

        # 设置布局
        self.setLayout(mainLayout)

    # 收到消息时打印在GUI
    def append_text(self, text, speaker="Apple"):
        print('收到：' + text)
        if speaker == "User":
            self.textEdit.append(
                "<b style='font-size:18pt;'>You: </b> <span style='font-size:14pt;'>" + text + "</span>")
        else:
            self.textEdit.append(
                "<b style='font-size:18pt;'>Apple: </b> <span style='font-size:14pt;'>" + text + "</span>")

    # 发送用户输入到Interpreter并清空输入框，通过信号接收回复
    def send_message(self):
        user_input = self.inputLine.text()
        self.interpreter.receive_user_input(user_input)  # 指明用interpreter实例的receive_user_input方法接受user_input
        self.append_text(user_input, speaker="User")
        self.inputLine.clear()


class Interpreter(QObject):
    # 定义一个用于发送响应的信号
    response_signal = pyqtSignal(str)

    # 初始化Interpreter类的实例变量。
    def __init__(self, script):
        super().__init__()
        self.loop = None
        self.script = script
        self.current_step = script.entry
        self.timer = QTimer()  # 创建一个计时器
        self.timer.setSingleShot(True)  # 设置为一次性触发
        self.timer.timeout.connect(self.on_timeout)  # 超时连接到槽函数

    def run(self):
        while self.current_step:
            print("Current step:", self.current_step.name)
            self.execute_step(self.current_step)

    def execute_step(self, step):
        # 执行说话动作
        self.speak(step.expressions)
        intent = self.listen(step)
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
        output = ""
        for sentence in expression:
            if sentence.endswith('：'):
                output += sentence
            elif sentence.startswith("<$") and sentence.endswith(">"):
                # 剥离变量sentence开头的"<$"和结尾的">"
                expect_var = sentence[2:-1]
                # 使用变量名（键）检索数据。如果键不存在，返回默认值
                var_value = self.script.vars.get(expect_var, 'NULL')
                output += str(var_value)
                output += '<br>'
            else:
                output += sentence
        self.response_signal.emit(output)  # 发射整个输出而不是逐句s

    # 执行说话动作并获得用户意图
    def listen(self, step):
        intent = ''
        if step.listen:
            self.loop = QEventLoop()  # 创建局部事件循环：一个QEventLoop对象
            self.timer.start(20000)  # 局部事件循环，等待用户输入，20秒后超时退出
            print('开始等待20秒')
            self.loop.exec_()  # 启动本地事件循环，直到 loop.exit() 被调用
            intent = USER_INPUTTED
        elif step.default:
            intent = 'default'
        else:
            QTimer.singleShot(3500, self.closeApplication)
        return intent

    # 在点击按钮时退出事件循环
    def on_submit(self):
        self.loop.exit()

    # 在超时时退出事件循环
    def on_timeout(self):
        global USER_INPUTTED
        USER_INPUTTED = ''
        self.loop.exit()  # 添加这行来退出事件循环

    # 根据用户意图获取下一个步骤的ID。
    def get_next_step_id(self, step, intent):
        if intent == '':
            return step.awake
        elif intent in step.answers:
            return step.answers[intent]
        else:
            return step.default

    def find_step_by_id(self, step_id):
        for step in self.script.steps:
            if step.name == step_id:
                return step
        return None

    # 检查某个用户是否存在
    def check_user_exists(self, username):
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
        if username in user_data:
            return True, user_data[username]
        else:
            return False, None

    # 返回初始的客服消息
    def initial_message(self):
        return "正在为你创建对话"

    def receive_user_input(self, user_input):
        # 接受用户输入
        global USER_INPUTTED
        USER_INPUTTED = user_input
        self.timer.stop()  # 停止计时器，因为已经收到输入

    def closeApplication(self):
        QApplication.quit()  # 退出应用程序


# 检查命令行参数并启动应用程序
if __name__ == '__main__':
    # 检查是否有足够的参数传递给脚本
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <parameter>")
        sys.exit(1)  # 退出程序并返回错误代码

    # 第一个参数是脚本名，第二个参数是第一个用户提供的参数
    file_name = sys.argv[1]
    script = get_script_from_file(file_name)
    app = QApplication(sys.argv)
    print("QApplication created")  # 确认应用程序已创建

    interpreter = Interpreter(script)  # 创建后端，Interpreter对象
    chatDialog = ChatDialog(interpreter)  # 创建前端， ChatDialog 对象
    print("ChatDialog created")  # 确认聊天对话框对象已创建

    interpreter.response_signal.connect(chatDialog.append_text)  # 连接信号和槽
    chatDialog.show()
    print("chatDialog.show() called")  # 确认 show 方法被调用

    chatDialog.append_text(interpreter.initial_message(), speaker="SYS")
    interpreter.run()

    exit_code = app.exec_()
    sys.exit(exit_code)
