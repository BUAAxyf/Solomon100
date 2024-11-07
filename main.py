import time

from model.VRPTW import VRPTW
from folderScanner.scan_folder import scan_folder
# from test import test
from tqdm import tqdm


def solution_summary(vrptw_dict):
    """
    保存所有实例的最优解的总距离
    """
    # 文件头
    with open(f"result\\summary.txt", "w") as f:
        f.write("Instance\tMin Distance\tSeed\tMin Vehicle Num\tSeed\n")

    with open(f"result\\evaluation_all.txt", "w") as f:
        f.write("All Evaluation:\n")

    total_distance = 0
    total_vehicle_num = 0

    for file_name in tqdm(vrptw_dict, desc="Summary"):
        distances = []
        vehicle_num = []
        for i in range(5):
            evaluation_dict = vrptw_dict[file_name][i].evaluation_dict

            # 写入文件
            with open(f"result\\evaluation_all.txt", "a") as f:
                f.write(f"{file_name}-Seed-{i}: \n")
                for key in evaluation_dict:
                    f.write(f"{key}: {evaluation_dict[key]}\n")

            distances.append(evaluation_dict["Total Distance"])
            vehicle_num.append(evaluation_dict["Used Vehicle Number"])

        # 找最小的距离和车辆数量
        min_distance = min(distances)
        min_vehicle_num = min(vehicle_num)
        min_index = distances.index(min_distance)
        min_vehicle_index = vehicle_num.index(min_vehicle_num)

        total_distance += min_distance
        total_vehicle_num += min_vehicle_num

        # 写入文件
        with open(f"result\\summary.txt", "a") as f:
            f.write(f"{file_name}\t{min_distance}\t{min_index}\t{min_vehicle_num}\t{min_vehicle_index}\n")

    with open(f"result\\summary.txt", "a") as f:
        f.write("\n")
        f.write(f"Average\t{total_distance / len(vrptw_dict)}\t-\t{total_vehicle_num / len(vrptw_dict)}\t-\n")


def main():
    file_folder = "D:\\Project\\DeliveryCourse\\Solomon100\\data\\solomon_100"
    file_list = scan_folder(file_folder)
    # result_folder = "result\\"
    vrptw_dict = {}

    for file_name in tqdm(file_list, desc="Solving"):
    # for file_name in file_list:
        result_folder = "result\\" + file_name.replace(".txt", "") + "\\"
        vrptw_dict[file_name] = []
        time_list = []

        # 尝试不同的种子顾客使用Solomon Insertion Algorithm生成初始解
        for i in range(5):
            # 计时
            start_time = time.time()

            vrptw = VRPTW()

            # 载入Solomon100数据
            vrptw.read_data(file_folder + "\\" + file_name, data_type="solomon")
            # vrptw._read_solomon_data(file_name)
            # print(vrptw)

            # 所罗门插入算法生成初始解
            vrptw.init_solution("SolomonInsertion", seed = i)

            # 计时结束
            end_time = time.time()
            # print(f"{file_name} - Seed {i} - Time: {end_time - start_time:.2f}s")
            time_list.append(end_time - start_time)

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

            vrptw_dict[file_name].append(vrptw)

            # 回收内存
            # del vrptw

        # 输出平均运行时间
        # print(f"{file_name} - Average Time: {sum(time_list) / len(time_list):.2f}s")

    # 总结
    solution_summary(vrptw_dict)

if __name__ == '__main__':
    # test()
    main()
