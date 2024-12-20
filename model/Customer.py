class Customer:
    """
    客户类
    """

    def __init__(self, customer_info: dict) -> None:
        self.id = customer_info['id']
        self.x = customer_info['x']
        self.y = customer_info['y']
        self.demand = customer_info['demand']
        self.ready_time = customer_info['ready_time']
        self.due_date = customer_info['due_date']
        self.service_time = customer_info['service_time']
        self.start_time = None


    def __str__(self) -> str:
        return (f"Customer {self.id}: "
                f"\n\tLocation ({self.x}, {self.y})"
                f"\n\tdemand {self.demand}"
                f"\n\tready_time {self.ready_time}"
                f"\n\tdue_date {self.due_date}"
                f"\n\tservice_time {self.service_time}")


    def set_start_time(self, start_time: int) -> None:
        self.start_time = start_time


    def get_start_time(self) -> int:
        return self.start_time


    def get_distance_to(self, customer: 'Customer'):
        """
        计算到customer的距离
        :param customer:
        :return:
        """
        return ((self.x - customer.x) ** 2 + (self.y - customer.y) ** 2) ** 0.5


