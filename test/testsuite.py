import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()  # 创建测试加载器
    suite = unittest.TestSuite()  # 创建测试套件
    suite.addTests(loader.discover(start_dir='.', pattern='test_*.py'))  # 添加测试到测试套件
    runner = unittest.TextTestRunner(verbosity=2)  # 运行测试套件
    runner.run(suite)
