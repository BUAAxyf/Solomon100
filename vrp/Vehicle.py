from vrp.Customer import Customer



class Vehicle:
    def __init__(self, vehicle_id: int, capacity: int, depot: Customer):
        """
        初始化车辆
        :param vehicle_id: 车辆的ID
        :param capacity: 车辆的容量
        :param depot: 起点
        """
        self.id = vehicle_id # 车辆的ID
        self.capacity = capacity # 车辆的容量
        self.route = [depot, depot] # 路径
        self.load = 0 # 当前载荷
        self.depot = depot # 起点
        # self.print_route_id_list()

    def __str__(self) -> str:
        return (f"Vehicle {self.id}:"
                f"\n\tcapacity {self.capacity}"
                f"\n\troute {self.route}"
                f"\n\tload {self.load}")

    # def check_route_time(self) -> bool:
    #     """
    #     !已弃用!
    #     判断路径的时间是否合法
    #     :return:
    #     """
    #     current_time = 0
    #     for customer in self.route:
    #
    #         # 没有到达开始时间, 等待开始
    #         if current_time > customer.ready_time:
    #             current_time = customer.ready_time
    #
    #         # 否则, 直接开始
    #         else:
    #             current_time += customer.service_time
    #
    #         # 服务结束后
    #         # 超过结束时间
    #         if current_time > customer.due_date:
    #             return False
    #
    #         # 否则, 继续服务
    #         else:
    #             current_time += customer.service_time
    #
    #     return True

    def print_route_id_list(self):
        print(self.get_route_id_list())

    def get_route_id_list(self):
        return [customer.id for customer in self.route]

    def get_route_start_time_list(self):
        return [customer.start_time for customer in self.route]

    def check_load(self) -> bool:
        """
        判断载荷是否超出容量
        :return:
        """
        if self.load > self.capacity:
            return False
        else:
            return True

    def can_serve_customer_at_position(self, customer: Customer, position: int) -> bool:
        """
        判断客户customer是否可以插入到原路径的第position个顾客之前
        :param customer:
        :param position:
        :return:
        """
        correct = True

        # 尝试插入
        if not self.add_customer(customer, position):
            correct = False

        self.remove_position(position)

        return correct

    def can_serve_customer(self, customer: Customer) -> bool:
        """
        判断客户customer是否有至少一个位置可以插入到route路径中
        :param customer:
        :return:
        """
        # print(f"current length of route is {len(self.route)}")

        for position in range(1, len(self.route)):
            # print(f"trying position {position}")

            if self.can_serve_customer_at_position(customer, position):
                # print(f"vehicle {self.id} can serve customer {customer.id} at position {position}")
                return True

        # print(f"vehicle {self.id} Cannot serve customer {customer.id} due to NO AVAILABLE POSITION")
        return False

    def is_empty(self) -> bool:
        """
        判断车辆是否为空
        :return:
        """
        # 仅包含起点和起点
        if len(self.route) == 2 and self.route[0] == self.route[1] and self.route[0] == self.depot:
            # print(f"vehicle {self.id} is empty")
            return True

        else:
            return False

    def get_route(self) -> list[Customer]:
        """
        获取路径
        :return:
        """
        return self.route

    def get_depot(self):
        """
        获取车辆的起点
        :return:
        """
        return self.depot

    def get_route_location(self) -> (list[int], list[int]):
        """
        获取路径的坐标列表
        :return:
        """
        x_list = []
        y_list = []

        # 起点
        for customer in self.route:
            x_list.append(customer.x)
            y_list.append(customer.y)

        return x_list, y_list

    def add_customer(self, customer: Customer, position: int) -> bool:
        """
        原路径在position位置之前插入客户customer, 并更新路径时间. 返回是否违背约束, !即使违反约束也会更新路径!
        :param position:
        :param customer:
        :return:是否违背约束
        """
        correct = True

        # 合法位置
        if position <= 0 or position > len(self.route) - 1:
            print(f"Cannot insert customer {customer.id} at position {position} of vehicle {self.id} due to INVALID POSITION NUMBER")
            raise ValueError(f"Cannot insert customer {customer.id} at position {position} of vehicle {self.id} due to INVALID POSITION NUMBER")

        # 插入客户
        # self.print_route_id_list()
        # print(self.get_route_start_time_list())
        # print(f"inserting customer {customer.id} at position {position} for vehicle {self.id}")
        self.route.insert(position, customer)
        # print(self.get_route_start_time_list())
        # self.print_route_id_list()
        # print(f"Inserted customer {customer.id} at position {position} for vehicle {self.id}")

        # 更新载荷
        self.load += customer.demand

        # 更新路径上的顾客的服务开始时间, 并判断是否违反时间约束
        if not self.update_route_time():
            # print(f"Inserting customer {customer.id} at position {position} for vehicle {self.id} violates TIME CONSTRAINT")
            correct = False

        # 判断容量约束
        if not self.check_load():
            # print(f"Inserting customer {customer.id} at position {position} for vehicle {self.id} violates CAPACITY CONSTRAINT")
            correct = False

        return correct

    def remove_position(self, position: int) -> bool:
        """
        删除position位置的顾客, 并更新路径时间. 返回是否违背约束, !即使违反约束也会更新路径!
        :param position:
        :return:是否违背约束
        """
        correct = True

        # 非法位置
        if position < 0 or position >= len(self.route):
            print(f"Cannot remove customer at position {position} for vehicle {self.id} due to INVALID POSITION NUMBER")
            raise ValueError(f"Cannot remove customer at position {position} of vehicle {self.id} due to INVALID POSITION NUMBER")

        # 删除客户
        customer = self.route.pop(position)

        # 更新载荷
        self.load -= customer.demand

        # 更新路径上的顾客的服务开始时间, 并判断是否违反时间约束
        if not self.update_route_time():
            # print(f"Removing customer {customer.id} at position {position} for vehicle {self.id} violates TIME CONSTRAINT")
            correct = False

        # 判断容量约束
        if self.load < 0:
            # print(f"Removing customer {customer.id} at position {position} for vehicle {self.id} violates CAPACITY CONSTRAINT")
            correct = False

        return correct

    def update_route_time(self) -> bool:
        """
        更新路径上的顾客的服务开始时间. 如果违反时间约束, 依然更新时间, 但返回False
        :return: 是否违反时间约束
        """
        current_time = 0
        correct_time = True

        for customer in self.route[:-1]:

            # 没有到达开始时间, 等待开始
            if current_time < customer.ready_time:
                customer.set_start_time(customer.ready_time)
                current_time = customer.ready_time

            # 否则, 直接开始
            else:
                customer.set_start_time(current_time)

            # 服务
            current_time += customer.service_time

            # 超过结束时间
            if current_time > customer.due_date:
                # print(f"Cannot update route time for vehicle {self.id} due to TIME CONSTRAINT")
                correct_time = False

        # 超过终点depot的结束时间
        if current_time > self.depot.due_date:
            correct_time = False

        return correct_time



