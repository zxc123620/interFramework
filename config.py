import os

# 项目根路径ROOT_PATH
__current_path = os.getcwd()
ROOT_PATH = __current_path[:__current_path.find("interFramework") + len("interFramework")]

# excel文件
EXCEL_FILE_PATH = ROOT_PATH + "/excel/" + "api_cases.xlsx"
TEST_SHEET_NAME = "Sheet1"

if __name__ == '__main__':
    print(ROOT_PATH)
