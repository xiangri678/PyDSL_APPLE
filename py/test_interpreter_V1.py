import sys
import unittest

from interpreter import Interpreter
from parser import get_script_from_file


class InterpreterTest(unittest.TestCase):
    def run_interpreter_with_input(self, input_file, script_file):
        # 准备脚本对象
        script = get_script_from_file(script_file)
        # 将 stdout 重定向，以捕获解释器的打印输出
        self.original_stdout = sys.stdout
        self.output_file = 'test_output.txt'
        sys.stdout = open(self.output_file, 'w')
        # 重定向 stdin 从输入文件中读取
        with open(input_file, 'r') as input_data:
            original_stdin = sys.stdin
            sys.stdin = input_data
            interpreter = Interpreter(script)
            try:
                interpreter.run()
            except SystemExit as e:
                # 捕获 SystemExit 异常
                self.assertEqual(e.code, 666)  # 检查退出码是否为预期值
            # 重置 stdin
            sys.stdin = original_stdin

        # 关闭重定向的 stdout 文件并重置 stdout
        sys.stdout.flush()  # Flush 标准输出缓冲区 stdout buffer
        sys.stdout.close()  # 手动关闭文件，全部全部数据已经写回
        sys.stdout = self.original_stdout  # 重置stdout为初始状态

    def compare_output(self, expected_file):
        # 读取预期的输出
        with open(expected_file, 'r') as file:
            expected_output = file.read()
        # 读取测试的实际输出
        with open(self.output_file, 'r') as file:
            actual_output = file.read()
        self.maxDiff = None
        # 比较预期输出和实际输出
        self.assertEqual(expected_output, actual_output)

    def test_interpreter(self):
        # 定义输入和预期输出文件
        names_index = ['pre_sale.txt', 'after_sale.txt', 'support.txt', 'wechat.txt']
        # 遍历文件列表，比较每一对文件
        for i in names_index:
            script_file = 'script_' + i
            input_file = 'input_' + i
            expected_file = 'expect_' + i
            with self.subTest(input_file=input_file, expected_file=expected_file):
                # 使用提供的输入运行解释器
                self.run_interpreter_with_input(input_file, script_file)
                # 将输出与预期输出进行比较
                self.compare_output(expected_file)


if __name__ == '__main__':
    unittest.main()
