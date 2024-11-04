from vrp.VRPTW import VRPTW
from folderScanner.scan_folder import scan_folder
from test import test
from tqdm import tqdm

def main():
    file_folder = "D:\\Mirror\\PostgraduateCourse\\01配送系统建模与分析\\Homework\\3\\solomon_100"
    file_list = scan_folder(file_folder)
    # result_folder = "result\\"
    vrptw_list = []

    for file_name in tqdm(file_list, desc="Solving"):
        result_folder = "result\\" + file_name.replace(".txt", "") + "\\"

        vrptw = VRPTW() # 创建VRPTW类

        # 载入Solomon100数据
        vrptw.read_data(file_name, data_type = "solomon")
        # vrptw._read_solomon_data(file_name)
        # print(vrptw) # test

        # 使用Solomon Insertion Algorithm生成初始解
        vrptw.init_solution("SolomonInsertion")
        vrptw.save_solution(result_folder + file_name.replace(".txt", "_solution.txt"))

        # 绘制地图并保存
        vrptw.map(show_map = True, save_map = True, save_name = result_folder + file_name.replace(".txt", ".png"))
        # vrptw.save_map(result_folder + file_name.replace(".txt", ".png"))

        # 运行遗传算法优化
        # vrptw.optimize("GeneticAlgorithm"， max_iter = 1000)
        vrptw.save_solution(result_folder + file_name.replace(".txt", "_solution.txt"))

        vrptw_list.append(vrptw)


if __name__ == '__main__':
    # main()
    test()
