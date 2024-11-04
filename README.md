# Solomon100

[TOC]

## 关于项目
Solomon100 是一个用于解决带时间窗和容量约束的车辆路径问题（CVRPTW）的Python项目。该项目实现了Solomon插入算法，并提供了按照格式输入Solomon100算例和保存、可视化结果测试等功能。

项目开源：[BUAAxyf/Solomon100: Solve VRPTW using Solomon's 100 customers Problems Instances](https://github.com/BUAAxyf/Solomon100)

## 作者信息

- **[谢奕飞]** - 清华大学深圳国际研究生院 -  [邮箱](yifei_tse@163.com)

查看 [贡献者列表](https://github.com/BUAAxyf/Solomon100/graphs/contributors) 以获取所有为该项目做出贡献的人。

## 运行环境

### 操作系统

- Windows 10 家庭中文版（或更高版本）
- 64 位操作系统

### 硬件设备

- 处理器：AMD Ryzen 7 4800H with Radeon Graphics 
- 内存：16 GB RAM

### 软件依赖

- Python 3.10.8 (tags/v3.10.8:aaaf517, Oct 11 2022, 16:50:30) [MSC v.1933 64 bit (AMD64)] on win32
- 依赖库：项目依赖的第三方库将在 `requirements.txt` 文件中列出，可以通过 `pip install -r requirements.txt` 命令安装

| 软件包          | 当前版本    | 最新版本（2024.11.4） |
| --------------- | ----------- | --------------------- |
| colorama        | 0.4.6       | 0.4.6                 |
| contourpy       | 1.3.0       | 1.3.0                 |
| cycler          | 0.12.1      | 0.12.1                |
| fonttools       | 4.54.1      | 4.54.1                |
| kiwisolver      | 1.4.7       | 1.4.7                 |
| matplotlib      | 3.9.2       | 3.9.2                 |
| numpy           | 2.1.2       | 2.1.3                 |
| packaging       | 24.1        | 24.1                  |
| pillow          | 11.0.0      | 11.0.0                |
| pip             | 24.3.1      | 24.3.1                |
| pyparsing       | 3.2.0       | 3.2.0                 |
| python-dateutil | 2.9.0.post0 | 2.9.0.post0           |
| setuptools      | 69.1.1      | 75.3.0                |
| six             | 1.16.0      | 1.16.0                |
| tqdm            | 4.66.6      | 4.66.6                |
| wheel           | 0.42.0      | 0.44.0                |

## 数据集：以C101.txt为例

数据集来自Solomon's 100 customers Problems Instances [VRP Web](https://www.bernabe.dorronsoro.es/vrp/index.html?/Problem_Instances/CVRPTWInstances.html)

`C101.txt` 是 Solomon 100 数据集中的一个实例，用于CVRPTW的研究和算法测试。该数据集包含车辆、客户和相关参数的信息，是解决VRPTW问题的基础输入。

### 数据集概述

- **车辆信息**：
  - 车辆数量：25
  - 车辆容量：200

- **客户信息**：
  - 客户数量：100（包括起点和终点）
  - 每个客户有以下属性：
    - 客户ID
    - X坐标
    - Y坐标
    - 需求量
    - 准备时间
    - 截止时间
    - 服务时间

### 数据集格式

部分数据展示如下：

```txt
C101

VEHICLE
NUMBER     CAPACITY
  25         200

CUSTOMER
CUST NO.  XCOORD.   YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE   TIME
 
    0      40         50          0          0       1236          0   
    1      45         68         10        912        967         90   
    2      45         70         30        825        870         90   
    3      42         66         10         65        146         90    
...
```

数据集以文本格式存储，包含以下部分：

- **车辆信息**：包括车辆数量和容量。
- **客户信息**：包括每个客户的详细信息，如坐标、需求、时间窗等。

### 使用示例

在项目中，`C101` 数据集被用于：

- 初始化车辆和客户实例。
- 应用Solomon插入算法生成初始解。
- 评估和优化车辆路径。

### 注意事项

- 确保数据集格式正确，以便项目中的算法能够正确读取和处理。
- 数据集中的时间和坐标信息应根据实际应用场景进行调整。

## 项目结构

### 文件目录

```
Solomon100/
│
├── data/
│   └── solomon_100
│
├── folderScanner/
│   ├── __init__.py
│   └── scan_folder.py
│
├── model/
│   ├── __init__.py
│   ├── Customer.py
│   ├── SolomonInsertionAlgorithm.py
│   ├── Vehicle.py
│   └── VRPTW.py
│
├── result/
│   ├── C101
│   └── ...
│
├── result_test/
│   ├── C101
│   └── ...
│
├── venv/
│
├── .gitattributes
├── main.py
├── README.md
├── requirements.txt
└── test.py
```

### 内部结构

其中，详细内部结构如下：

```
@startuml
package "Solomon100 Project" {
  
  package "data" {
    folder "solomon_100" {
      file "C101.txt"
      file "..."
    }
  }
  
  package "folderScanner" {
    class __init__ {
    }
    class scan_folder {
      function scan_folder(file_folder) : list[str]
    }
  }
  
  package "model" {
    class __init__ {
    }
    class Customer {
      attribute id : int
      attribute x : int
      attribute y : int
      attribute demand : int
      attribute ready_time : int
      attribute due_date : int
      attribute service_time : int
      attribute start_time : int
      function __init__(customer_info : dict) : None
      function __str__() : str
      function set_start_time(start_time : int) : None
      function get_distance_to(customer : Customer) : float
    }
    
    class Vehicle {
      attribute id : int
      attribute capacity : int
      attribute route : list[Customer]
      attribute load : int
      attribute depot : Customer
      function __init__(vehicle_id : int, capacity : int, depot : Customer) : None
      function __str__() : str
      function print_route_id_list() : None
      function get_route_id_list() : list[int]
      function get_route_start_time_list() : list[int]
      function get_route_distance() : float
      function check_load() : bool
      function can_serve_customer_at_position(customer : Customer, position : int) : bool
      function can_serve_customer(customer : Customer) : bool
      function is_empty() : bool
      function get_route() : list[Customer]
      function get_depot() : Customer
      function get_route_location() : (list[int], list[int])
      function add_customer(customer : Customer, position : int) : bool
      function remove_position(position : int) : bool
      function update_route_time() : bool
    }
    
    class SolomonInsertionAlgorithm {
      function euclidean_distance(customer1 : Customer, customer2 : Customer) : float
      function distance_cost(customer : Customer, vehicle : Vehicle, position : int, mu : float) : float
      function find_best_position(customer : Customer, vehicle : Vehicle, alpha : float, mu : float) : (int, int)
      function time_cost(customer : Customer, vehicle : Vehicle, position : int) : int
      function find_seed_customer(customer_list : list[Customer], depot : Customer, seed : int) : int
      function solomon_insertion_algorithm(customer_list : list[Customer], vehicle : Vehicle, seed : int, mu : float, alpha : float, lmbda : float) : (Vehicle, list[Customer])
    }
    
    class VRPTW {
      // VRPTW 类的属性和方法
    }
  }
  
  class main {
    function main() : None
    function solution_summary(vrptw_dict) : None
  }
  
  file "README.md"
  
}

@enduml
```

## 主程序：main.py

`main.py` 是本项目的主程序，它负责执行以下任务：

1. 扫描指定文件夹中的所有数据文件。
2. 对每个文件使用Solomon Insertion Algorithm生成五个不同的初始解（通过改变种子顾客）。
3. 保存每个初始解和对应的地图。
4. 评估每个解的质量，并将结果保存到文件中。
5. 生成所有实例的最优解的总距离的总结报告。

### 功能概述

- **数据扫描**：使用 `folderScanner` 模块扫描 `data/solomon_100` 文件夹中的所有 `.txt` 文件。
- **初始解生成**：对每个文件，使用Solomon Insertion Algorithm生成5个不同的初始解。
- **结果保存**：将每个初始解和对应的地图保存到 `result` 文件夹中，文件名包含原始文件名和种子顾客编号。
- **解的评估**：评估每个解的总距离和使用的车辆数量，并将详细评估结果保存到 `evaluation_all.txt` 文件中。
- **总结报告**：生成一个总结报告，包含所有实例的最优解的总距离和相关信息，保存到 `summary.txt` 文件中。

### 如何运行

要运行 `main.py`，请确保你已经设置了Python环境，并且安装了所有必要的依赖项。然后在命令行中执行以下命令：

```bash
python main.py
```

## 测试脚本：test.py

`test.py` 是本项目的测试脚本，它用于验证 `VRPTW` 类的主要功能是否按预期工作。该脚本执行以下任务：

1. 扫描 `data/solomon_100` 文件夹中的所有数据文件。
2. 选择第一个文件进行测试。
3. 使用Solomon Insertion Algorithm生成初始解。
4. 输出和展示初始解。
5. 可视化解（可选）。
6. 评价解的效果。
7. 将解保存为文件。

### 功能概述

- **数据读取**：从 `data/solomon_100` 文件夹中读取第一个数据文件。
- **初始解生成**：使用Solomon Insertion Algorithm生成初始解，种子顾客为1。
- **解的展示**：在控制台中打印初始解。
- **解的可视化**：（目前注释掉）绘制初始解的地图并保存为 `.png` 文件。
- **解的评价**：计算并打印解的效果评价指标。
- **结果保存**：将初始解保存到 `result_test` 文件夹中。

### 如何运行

要运行 `test.py`，请确保你已经设置了Python环境，并且安装了所有必要的依赖项。然后在命令行中执行以下命令：

```bash
python test.py
```

## 文件夹扫描模块：scan_folder.py

`scan_folder.py` 模块提供了一个函数 `scan_folder`，用于扫描指定目录下的所有文件，并返回一个包含所有文件名的列表。这个模块在项目中用于读取数据文件夹中的所有数据文件，以便进行后续处理。

### 功能概述

- **目录读取**：使用 `os.listdir` 函数读取指定文件夹中的所有内容。
- **文件过滤**：通过列表推导式和 `os.path.isfile` 函数过滤出所有文件，排除子目录。
- **错误处理**：捕获并处理可能出现的 `FileNotFoundError` 和其他异常，确保程序的健壮性。

### 使用方法

在项目中，你可以通过以下方式调用 `scan_folder` 函数：

```python
from folderScanner.scan_folder import scan_folder

file_folder = "data/solomon_100"
file_list = scan_folder(file_folder)
```

## 车辆路径问题带时间窗（VRPTW）模块：VRPTW.py

`VRPTW.py` 模块定义了一个 `VRPTW` 类，用于处理车辆路径问题带时间窗（Vehicle Routing Problem with Time Windows, VRPTW）。该类提供了读取数据、生成初始解、评估解质量、保存解等功能。

### 功能概述

- **数据读取**：从Solomon算例或其他数据源读取VRPTW问题的数据。
- **初始解生成**：使用Solomon插入算法生成问题的初始解。
- **解的展示与保存**：在控制台中打印解，并将其保存到文件中。
- **解的可视化**：使用matplotlib绘制解的地图，并可选择保存为图片。
- **解的评价**：计算解的总服务距离和使用的车辆数量等评价指标。

### 主要方法

- `read_data(file_name, data_type)`：读取数据文件并初始化类。
- `init_solution(solution_type, mu, alpha, lmbda, seed)`：生成初始解。
- `print_solution()`：在控制台中打印解。
- `save_solution(file_name, evaluation)`：将解保存到文件中。
- `evaluate_solution(distance, vehicle_number)`：评价解的质量。
- `map(show_map, save_map, save_name)`：绘制解的地图。

### 使用示例

```python
from model.VRPTW import VRPTW

# 创建VRPTW实例
vrptw = VRPTW()

# 读取数据
vrptw.read_data('data/solomon_100/C101.txt')

# 生成初始解
vrptw.init_solution('SolomonInsertion', seed=1)

# 打印解
vrptw.print_solution()

# 保存解
vrptw.save_solution('result/C101_solution.txt')

# 绘制并保存地图
vrptw.map(show_map=False, save_map=True, save_name='result/C101_map.png')
```

## Solomon插入算法模块：SolomonInsertionAlgorithm.py

`SolomonInsertionAlgorithm.py` 模块实现了Solomon插入算法，这是一种用于解决车辆路径问题（VRPTW）的启发式算法。该算法通过迭代地将客户插入到车辆路径中，以生成问题的初始解。

### 功能概述

- **距离计算**：计算客户之间的欧式距离。
- **成本评估**：评估将客户插入到车辆路径中特定位置的距离成本。
- **时间成本**：计算插入客户后，后续客户开始服务时间的增量。
- **最佳位置查找**：为每个客户找到其在车辆路径中的最佳插入位置。
- **种子客户选择**：根据不同的策略选择种子客户，作为车辆路径的起点。
- **初始解生成**：使用Solomon插入算法生成VRPTW问题的初始解。

### 主要函数

- `euclidean_distance(customer1, customer2)`：计算两个客户之间的欧式距离。
- `distance_cost(customer, vehicle, position, mu)`：计算将客户插入到车辆路径特定位置的距离成本。
- `find_best_position(customer, vehicle, alpha, mu)`：找到客户在车辆路径中的最佳插入位置。
- `time_cost(customer, vehicle, position)`：计算插入客户后的时间成本。
- `find_seed_customer(customer_list, depot, seed)`：根据策略选择种子客户。
- `solomon_insertion_algorithm(customer_list, vehicle, seed, mu, alpha, lmbda)`：实现Solomon插入算法，生成初始解。

### 使用示例

```python
from model.Vehicle import Vehicle
from model.Customer import Customer
from SolomonInsertionAlgorithm import solomon_insertion_algorithm

# 假设已经有了客户列表和车辆实例
customer_list = [Customer(...), Customer(...), ...]
vehicle = Vehicle(...)

# 使用Solomon插入算法生成初始解
vehicle, customer_list = solomon_insertion_algorithm(customer_list, vehicle, seed=1)
```

## 客户类模块：Customer.py

`Customer.py` 模块定义了一个 `Customer` 类，用于表示车辆路径问题带时间窗（VRPTW）中的客户。该类封装了客户的基本信息和相关操作。

### 功能概述

- **属性**：客户ID、位置坐标（x, y）、需求量、准备时间、截止时间、服务时间、开始服务时间。
- **方法**：
  - `__str__`：返回客户的字符串表示，便于打印和调试。
  - `set_start_time`：设置客户的开始服务时间。
  - `get_distance_to`：计算并返回当前客户到另一个客户的距离。

### 客户类属性

- `id` (int): 客户的唯一标识符。
- `x` (int): 客户的x坐标。
- `y` (int): 客户的y坐标。
- `demand` (int): 客户的需求量。
- `ready_time` (int): 客户准备接受服务的时间。
- `due_date` (int): 客户要求完成服务的截止时间。
- `service_time` (int): 服务该客户所需的时间。
- `start_time` (int): 客户开始接受服务的时间（可由算法动态设置）。

### 使用示例

```python
from model.Customer import Customer

# 创建客户实例
customer_info = {
    'id': 1,
    'x': 100,
    'y': 200,
    'demand': 10,
    'ready_time': 8,
    'due_date': 18,
    'service_time': 2
}
customer = Customer(customer_info)

# 打印客户信息
print(customer)

# 设置开始服务时间
customer.set_start_time(9)

# 计算到另一个客户的距离
another_customer = Customer({...})  # 另一个客户实例
distance = customer.get_distance_to(another_customer)
print(f"Distance to another customer: {distance}")
```

## 车辆类模块：Vehicle.py

`Vehicle.py` 模块定义了一个 `Vehicle` 类，用于表示车辆路径问题带时间窗（VRPTW）中的车辆。该类封装了车辆的基本信息和相关操作，是解决VRPTW问题的核心组件之一。

### 功能概述

- **属性**：车辆ID、容量、路径（包括起点和一系列客户）、当前载荷、起点。
- **方法**：
  - `__str__`：返回车辆的字符串表示，便于打印和调试。
  - `get_route_id_list`：获取车辆路径中所有客户的ID列表。
  - `get_route_start_time_list`：获取车辆路径中所有客户的开始服务时间列表。
  - `get_route_distance`：计算车辆路径的总距离。
  - `check_load`：检查车辆的当前载荷是否超出容量。
  - `can_serve_customer_at_position`：判断车辆是否可以在特定位置插入客户。
  - `can_serve_customer`：判断车辆是否有至少一个位置可以插入客户。
  - `is_empty`：判断车辆是否为空（仅包含起点）。
  - `get_route`：获取车辆的路径。
  - `get_depot`：获取车辆的起点。
  - `get_route_location`：获取车辆路径的坐标列表。
  - `add_customer`：在车辆路径的特定位置插入客户，并更新路径时间。
  - `remove_position`：从车辆路径中移除特定位置的客户，并更新路径时间。
  - `update_route_time`：更新车辆路径上所有客户的服务开始时间。

### 使用示例

```python
from model.Customer import Customer
from model.Vehicle import Vehicle

# 创建客户实例
customer_info = {
    'id': 1,
    'x': 100,
    'y': 200,
    'demand': 10,
    'ready_time': 8,
    'due_date': 18,
    'service_time': 2
}
customer = Customer(customer_info)

# 创建车辆实例
depot = Customer({'id': 0, 'x': 0, 'y': 0, 'demand': 0, 'ready_time': 0, 'due_date': 24, 'service_time': 0})
vehicle = Vehicle(1, 100, depot)

# 尝试在车辆路径中插入客户
vehicle.add_customer(customer, 1)

# 打印车辆路径信息
print(vehicle)
```