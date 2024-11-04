from model.VRPTW import VRPTW
from folderScanner.scan_folder import scan_folder


def test():
    """
    测试程序
    """
    file_folder = "data/solomon_100"
    file_list = scan_folder(file_folder)
    file_name = file_list[0]
    result_folder = "result_test\\" + file_name.replace(".txt", "") + "\\"
    # print(file)

    vrptw = VRPTW()
    # print(vrptw)

    # 读取solomon_100数据集
    vrptw.read_data(file_folder + "/" + file_list[0])
    # for customer in vrptw.get_customer_list():
    #     print(customer)
    # for vehicle in vrptw.get_vehicle_list():
    #     print(vehicle)

    # 生成初始解
    vrptw.init_solution("SolomonInsertion", seed = 1)

    # 输出解
    # solution = vrptw.get_solution()
    # print(solution)

    # 展示解
    vrptw.print_solution()

    # 解的可视化
    # vrptw.map(show_map = True,
    #           save_map = True,
    #           save_name = result_folder + file_name.replace(".txt", ".png"))

    # 评价解效果
    print(vrptw.evaluate_solution())

    # 保存为文件
    vrptw.save_solution(result_folder + file_name.replace(".txt", "_solution.txt"))
