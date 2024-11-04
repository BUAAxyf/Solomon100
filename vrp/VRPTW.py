import os

from vrp.SolomonInsertionAlgorithm import solomon_insertion_algorithm
from vrp.Customer import Customer
from vrp.Vehicle import Vehicle

import matplotlib.pyplot as plt

class VRPTW:
    def __init__(self) -> None:
        self.file_name = None # 文件名
        self.vehicle_number = None # 车辆数量
        self.vehicle_capacity = None # 车辆容量
        self.depot = None # 起点
        self.customer_list = [] # 客户列表
        self.customer_tobe_served = [] # 待服务的客户列表
        self.vehicle_list = [] # 车辆列表
        self.vehicle_empty = [] # 空车辆列表
        self.solution = None # 解

    def __str__(self) -> str:
        return (f"file_name: {self.file_name}, "
                f"\n\tvehicle_number: {self.vehicle_number}, "
                f"\n\tvehicle_capacity: {self.vehicle_capacity}, "
                f"\n\tcustomer_list: {self.customer_list}")

    def _init_vehicle_list(self) -> None:
        """
        初始化车辆列表
        """
        for i in range(self.vehicle_number):
            vehicle = Vehicle(i, self.vehicle_capacity, self.depot)
            self.vehicle_list.append(vehicle)
            self.vehicle_empty.append(vehicle)


    def _read_solomon_data(self, file_name) -> None:
        """
        读取file_name(Solomon算例), 初始化类
        """
        with open(file_name, 'r') as file:
            # 读取文件内容
            lines = file.readlines()

        # 解析文件头, 初始化车辆信息, 客户信息
        for i in range(0, 7):
            line = lines[i].strip()  # 去掉行首尾的空白字符

            # 文件名
            if i == 0:
                self.file_name = line[0]

            # 车辆信息
            elif line.startswith('VEHICLE'):
                self.vehicle_number = int(lines[i+2].split()[0])
                self.vehicle_capacity = int(lines[i+2].split()[1])

            # 客户信息
            elif line.startswith('CUSTOMER'):
                break

            else:
                continue

        # 解析客户信息,初始化客户列表
        for line in lines[8:]:
            parts = line.strip().split()

            # 空行
            if not parts:
                continue

            # 读取信息
            customer_info = {'id': int(parts[0]),
                             'x': int(parts[1]),
                             'y': int(parts[2]),
                             'demand': int(parts[3]),
                             'ready_time': int(parts[4]),
                             'due_date': int(parts[5]) + int(parts[6]),
                             'service_time': int(parts[6])}
            customer = Customer(customer_info)

            # 如果是起点
            if customer.id == 0:
                # print("Depot:", customer)
                self.depot = customer
                self.depot.set_start_time(0)
                # print(self.depot)

            # 如果非起点
            else:
                self.customer_list.append(customer)
                self.customer_tobe_served.append(customer)

        # 初始化车辆列表
        self._init_vehicle_list()

    def read_data(self, file_name: str,
                  data_type: str = 'solomon') -> bool:
        """
        读取file_name(数据文件), 初始化类
        """
        if data_type =='solomon':
            self._read_solomon_data(file_name)
            return True

        else:
            print("Unsupported data type")
            raise ValueError("Unsupported data type")

    def get_customer_list(self) -> list:
        """
        获取客户列表
        """
        return self.customer_list

    def get_vehicle_list(self) -> list:
        """
        获取车辆列表
        """
        return self.vehicle_list

    def map(self,
            show_map: bool = True,
            save_map: bool = False,
            save_name: str = 'VRPTW_Map.png'):
        """
        根据当前的车辆与路径绘制地图
        :return:
        """

        plt.figure(figsize=(10, 8))

        # 绘制原点
        plt.scatter(self.depot.x, self.depot.y, c='red', label='Depot', s=100)

        # 绘制车辆及其客户
        for vehicle in self.vehicle_list:

            if vehicle.is_empty():
                continue

            route_x, route_y = vehicle.get_route_location()

            plt.plot(route_x, route_y, marker='o', label=f'Vehicle {vehicle.id}')

        plt.title('VRPTW Map')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()

        # 保存地图
        if save_map:
            plt.savefig(save_name)

        # 显示地图
        if show_map:
            plt.show()

    def init_solution(self, solution_type: str,
                      mu: float = 1.0,
                      alpha: float = 0.5,
                      lmbda: float = 1.0,
                      seed: int = 0) -> bool:
        """
        生成初始解
        :return:
        """
        if solution_type =='SolomonInsertion':

            # 迭代Solomon I1插入算法，直到所有顾客都被分配到车辆上或无可分配的车辆
            while self.customer_tobe_served:

                # 有顾客, 没空车
                if not self.vehicle_empty:
                    print("No available vehicle, some customers may not be served")
                    return False

                # 有顾客, 有空车
                else:
                    vehicle_to_serve = self.vehicle_empty.pop(0)
                    print(f"Vehicle {vehicle_to_serve.id} is serving")
                    vehicle_to_serve, self.customer_tobe_served = solomon_insertion_algorithm(self.customer_tobe_served,
                                                                                              vehicle_to_serve,
                                                                                              mu = mu,
                                                                                              alpha = alpha,
                                                                                              lmbda = lmbda,
                                                                                              seed = seed)
                    print(f"Vehicle {vehicle_to_serve.id} finally serves {vehicle_to_serve.get_route_id_list()}")

        else:
            print("Unsupported solution type")
            raise ValueError("Unsupported solution type")

        self.solution = self.get_solution()

        return True

    def get_solution(self) -> dict[str, list[int]]:
        """
        获取解
        :return:
        """
        solution = {}

        for vehicle in self.vehicle_list:
            solution[vehicle.id] = vehicle.get_route_id_list()

        return solution

    def show_solution(self):
        """
        显示解
        :return:
        """
        # 表头
        print("VehicleID", "\t", "Route")
        for vehicle in self.vehicle_list:
            print(f"{vehicle.id}", end="\t")
            print(vehicle.get_route_id_list())

    def save_solution(self,
                      file_name: str = 'VRPTW_Solution.txt',
                      evaluate: bool = False):
        """
        将解的字典按行保存在文件file_name中
        :param file_name:
        :return:
        """
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        if evaluate:
            self.evaluate_solution()

        with open(file_name, 'w') as file:
            file.write("VehicleID\tCustomerID\n")
            for vehicle in self.vehicle_list:
                file.write(f"{vehicle.id}\to-")
                for customer_id in vehicle.get_route_id_list()[1: -1]:
                    file.write(f"{customer_id}-")
                file.write("d\n")

    def evaluate_solution(self):
        """
        评价解的质量
        :return:
        """
        # 总服务时间
        total_service_time = 0
        for vehicle in self.vehicle_list:
            total_service_time += vehicle.get_service_time()


        pass


