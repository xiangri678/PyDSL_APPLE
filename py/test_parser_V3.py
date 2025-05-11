import unittest

from parser import get_script_from_file


class TestParser(unittest.TestCase):
    def compare_files(self, script_file, result_file):
        # 读取预期结果文件的内容
        with open(result_file, 'r') as f:
            expected_result = f.read()
        # 调用 get_script_from_file 函数获取实际结果
        get_script_from_file(script_file)
        # 读取运行结果文件的内容
        print2file = "result_" + script_file[7:12] + ".txt"
        with open(print2file, 'r') as f:
            actual_result = f.read()
        # 比较预期结果和实际结果
        self.assertEqual(expected_result, actual_result, f"File {script_file} does not match {result_file}")

    def test_files(self):
        # 定义文件对列表
        files_to_compare = [
            ("script_pre_sale.txt", "parse_pre_sale.txt"),
            ("script_after_sale.txt", "parse_after_sale.txt"),
            ("script_support.txt", "parse_support.txt"),
            ("script_wechat.txt", "parse_wechat.txt"),
        ]
        # 遍历文件对列表，比较每一对文件
        for script_file, result_file in files_to_compare:
            with self.subTest(script_file=script_file, result_file=result_file):
                self.compare_files(script_file, result_file)


if __name__ == '__main__':
    unittest.main()
