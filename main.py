from model.VRPTW import VRPTW
from folderScanner.scan_folder import scan_folder
# from test import test
from tqdm import tqdm

def main():
    file_folder = "D:\\Project\\DeliveryCourse\\Solomon100\\data\\solomon_100"
    file_list = scan_folder(file_folder)
    # result_folder = "result\\"
    vrptw_dict = {}

    for file_name in tqdm(file_list, desc="Solving"):
        result_folder = "result\\" + file_name.replace(".txt", "") + "\\"

        # 尝试不同的种子顾客使用Solomon Insertion Algorithm生成初始解
        for i in range(5):
            vrptw_dict[file_name] = []

            vrptw = VRPTW()

            # 载入Solomon100数据
            vrptw.read_data(file_folder + "\\" + file_name, data_type="solomon")
            # vrptw._read_solomon_data(file_name)
            # print(vrptw)

            # 所罗门插入算法生成初始解
            vrptw.init_solution("SolomonInsertion", seed = i)

            # 保存解
            vrptw.save_solution(result_folder + file_name.replace(".txt", f"_solution_{i}.txt"))

            # 绘制地图并保存
            vrptw.map(show_map = False,
                      save_map = True,
                      save_name = result_folder + file_name.replace(".txt", f"_{i}.png"))

            # 运行VNS算法优化
            # vrptw.optimize("VNS"， max_iter = 1000)

            # 保存最优解
            # vrptw.save_solution(result_folder + file_name.replace(".txt", f"_optimal_solution_{i}.txt"))

            # 输出最优解
            # print(f"{file_name} - Seed {i} - Optimal Solution:")
            # vrptw.print_solution()

            # vrptw_dict[file_name].append(vrptw)

            # 回收内存
            del vrptw


if __name__ == '__main__':
    # test()
    main()
