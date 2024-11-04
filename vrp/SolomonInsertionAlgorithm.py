import random
from xmlrpc.client import MAXINT

from vrp.Customer import Customer
from vrp.Vehicle import Vehicle

def distance(customer1, customer2):
    """
    计算customer1和customer2的距离
    :param customer1:
    :param customer2:
    :return:
    """
    return ((customer1.x - customer2.x) ** 2 + (customer1.y - customer2.y) ** 2) ** 0.5


def distance_cost(customer, vehicle, position, mu: float = 1.0):
    """
    计算将customer插入到position位置后的距离成本
    :param mu: 原路径距离的系数
    :param customer:
    :param vehicle:
    :param position:
    :return:
    """
    cost = (distance(vehicle.get_route()[position - 1], customer)
                     + distance(customer, vehicle.get_route()[position])
                     - mu * distance(vehicle.get_route()[position - 1], vehicle.get_route()[position]))
    return cost


def find_best_position(customer,
                       vehicle,
                       alpha: float = 0.5,
                       mu: float = 1.0) -> (int, int):
    """
    找到customer在vehicle的路径中的最佳插入位置
    :param mu:
    :param alpha:
    :param customer:
    :param vehicle:
    :return:
    """
    best_position = None
    min_c1 = MAXINT
    for i in range(1, len(vehicle.get_route())):

        # 如果可以插在i位置后
        if vehicle.can_serve_customer_at_position(customer, i):
            # 计算c1
            c11 = distance_cost(customer, vehicle, i, mu = mu)
            c12 = time_cost(customer, vehicle, i)
            c1 = alpha * c11 + (1 - alpha) * c12

        else:
            continue

        # 如果c1比min_c1小, 更新best_position和min_c1
        if c1 < min_c1:
            min_c1 = c1
            best_position = i

        else:
            continue

    return best_position, min_c1


def time_cost(customer, vehicle, position):
    """
    计算将customer插入到position位置后, 后面一位顾客的开始服务时间增量
    :param customer:
    :param vehicle:
    :param position:
    :return:
    """
    # 前一位顾客
    pre_customer = vehicle.get_route()[position-1]
    # 后一位顾客
    post_customer = vehicle.get_route()[position]

    # 计算时间差
    # 如果pre的结束时间早于插入顾客的准备时间, 则插入顾客的结束时间为插入顾客的准备时间+服务时间
    if pre_customer.start_time + pre_customer.service_time <= customer.ready_time:
        customer_end_time = customer.ready_time + customer.service_time

    # 否则, 插入顾客的结束时间为pre顾客的结束时间+插入顾客的服务时间
    else:
        customer_end_time = pre_customer.start_time + pre_customer.service_time + customer.service_time

    # 如果插入顾客的结束时间早于post顾客的开始时间, 则无时间增量
    if customer_end_time <= post_customer.start_time:
        return 0

    # 否则, 时间增量为插入顾客的结束时间-post顾客的开始时间
    else:
        return customer_end_time - post_customer.start_time


def find_seed_customer(customer_list: list[Customer],
                       depot: Customer,
                       seed : int = 0) -> int:
    """
    从customer_list中找到当前车辆的第一个客户
    :param depot:
    :param customer_list:
    :param seed: 寻找初始点的策略: 0-随机, 1-最远距离, 2-最远时间, 3-最远距离+最远时间
    :return: 第一个客户的索引
    """
    # 只有一个顾客
    if len(customer_list) == 1:
        # print(f"Only one customer, select it as initial point")
        return 0

    # 没有
    elif len(customer_list) == 0:
        print(f"No customer to be selected as initial point")
        raise ValueError("No customer to be selected as initial point")

    # 随机策略
    if seed == 0:
        random_index = random.randint(0, len(customer_list)-1)
        print(f"Randomly select customer {customer_list[random_index].id} as initial point")
        return random_index

    # 最远距离策略
    elif seed == 1:

        # 找到距离depot最远的顾客
        max_distance = 0
        max_customer_index = 0

        for i in range(len(customer_list)):
            distance_to_depot = distance(customer_list[i], depot)

            if distance_to_depot > max_distance:
                max_distance = distance_to_depot
                max_customer_index = i

        # print(f"Select customer {customer_list[max_customer_index].id} as initial point, distance to depot: {max_distance}")

        return max_customer_index

    # 最近距离策略
    elif seed == 2:
        # 找到距离depot最近的顾客
        min_distance = 0
        min_customer_index = 0

        for i in range(len(customer_list)):
            distance_to_depot = distance(customer_list[i], depot)

            if distance_to_depot < min_distance:
                min_distance = distance_to_depot
                min_customer_index = i

        # print(f"Select customer {customer_list[max_customer_index].id} as initial point, distance to depot: {min_distance}")

        return min_customer_index

    # 最早截止时间策略
    elif seed == 3:
        # 找到最早截止时间的顾客
        earliest_deadline = MAXINT
        earliest_customer_index = None

        for i in range(len(customer_list)):
            due_date = customer_list[i].due_date

            if due_date < earliest_deadline:
                earliest_deadline = due_date
                earliest_customer_index = i

        # print(f"Select customer {customer_list[earliest_customer_index].id} as initial point, earliest deadline: {earliest_deadline}")
        return earliest_customer_index

    # 最晚截止时间策略
    elif seed == 4:
        # 找到最晚截止时间的顾客
        latest_deadline = 0
        latest_customer_index = None

        for i in range(len(customer_list)):
            due_date = customer_list[i].due_date
            if due_date > latest_deadline:
                latest_deadline = due_date
                latest_customer_index = i

        # print(f"Select customer {customer_list[latest_customer_index].id} as initial point, latest deadline: {latest_deadline}")
        return latest_customer_index

    # 非法种子
    else:
        print("Unsupported seed strategy")
        raise ValueError("Unsupported seed strategy")

def solomon_insertion_algorithm(customer_list: list[Customer],
                                vehicle: Vehicle,
                                seed: int = 0,
                                mu: float = 1.0,
                                alpha: float = 0.5,
                                lmbda: float = 1) -> (Vehicle, list[Customer]):
    """
    Solomon Insertion Algorithm. 在customers列表中, 按照Solomon Insertion Algorithm的顺序, 依次插入到vehicle的路径中
    :param seed:
    :param customer_list:
    :param vehicle:
    :param mu:
    :param alpha:
    :param lmbda:
    :return:
    """
    # 路径为空, 初始化路径
    if vehicle.is_empty():

        # 初始顾客索引
        init_customer_index = find_seed_customer(customer_list, vehicle.get_depot(), seed=seed) # 寻找初始点
        print(f"Initialize vehicle {vehicle.id} with customer {customer_list[init_customer_index].id}")

        # 初始顾客加入vehicle路径
        vehicle.add_customer(customer_list[init_customer_index], 1) # 加入初始顾客

        # 从customer_list中移除初始顾客
        customer_list.remove(customer_list[init_customer_index])

    # 完善此路径
    while True: # 循环一次插入一个顾客

        customer_tobe_inserted = {}

        # 算每个顾客的min_c1和c2
        for customer in customer_list:
            print(f"Evaluating customer {customer.id}...")

            # 如果customer不可以插入
            if not vehicle.can_serve_customer(customer):
                print(f"Cannot insert customer {customer.id} into vehicle {vehicle.id}")
                continue

            # customer可以被服务
            else:
                print(f"Can insert customer {customer.id} into vehicle {vehicle.id}, calculating min_c1 and c2...")

                # 找到最佳插入位置, 计算该位置的c1(即为min_c1)
                best_position, min_c1 = find_best_position(customer, vehicle, alpha=alpha, mu=mu)

                # 计算c2
                c2 = lmbda * distance(vehicle.get_depot(), customer) - min_c1

                # if c2 < 0:
                #     print(f"Inserting customer {customer.id} into vehicle {vehicle.id} is not optimal, c2 is negative")
                #     continue

                # 加入待插入列表
                customer_tobe_inserted[customer] = (best_position, c2)

        # 如果没有可以插入的点
        if not customer_tobe_inserted:
            print(f"No customer can be inserted into vehicle {vehicle.id}")
            break

        # 找到c2最大的顾客
        best_customer = None
        best_position = None
        best_c2 = -MAXINT

        for customer, (position, c2) in customer_tobe_inserted.items():

            # 更新c2
            if c2 > best_c2:
                best_customer = customer
                best_position = position
                best_c2 = c2

        # 如果可以插入的点都不如单独服务
        if not best_customer:
            print(f"Need to distribute the remaining customers to other vehicles")
            print(f"vehicle {vehicle.id} route: ", vehicle.get_route_id_list())
            break

        # 加入顾客
        vehicle.add_customer(best_customer, best_position)
        customer_list.remove(best_customer)
        print(f"Insert customer {best_customer.id} at position {best_position} of vehicle {vehicle.id}")
        print("current route: ", vehicle.get_route_id_list())

    return vehicle, customer_list