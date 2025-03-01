##### 细节性问题

1. 在 Python 中，<font color=red>在递归函数中使用可变对象（如列表、字典）作为默认参数需要格外注意</font>。这是因为默认参数的值在函数定义时仅初始化一次，而不是每次调用函数时重新创建。递归调用中如果不显式传递参数，所有递归层会共享同一个默认参数对象，导致数据污染。

   ```python
   def insert(ele,lst=[]):
       lst.append(ele)
       return lst
   
   print(insert(1))    # [1]
   print(insert(2))    # [1, 2]
   ```

2. pyhton 的参数传递机制有些复杂，对于可变对象，传递的是引用，此时修改参数会影响原变量。而对于不可变参数，其实就是一个新变量(复制)。而在 java 则参数是原变量的复制体。

3. 不要在 for 循环中修改被遍历的可变对象，其实根据上一条，可以很容易理解

   ```python
   # 一直遍历，无法停止
   list = [1, 2, 3, 4, 5]
   for i in list:
       print(i)
       list.append(i)
   ```







##### SortedList

1. SortedList 是 Python 中 sortedcontainers 模块提供的一个数据结构，它是一个有序的列表，支持高效的插入、删除和查找操作。它的设计目标是提供类似于 Python 内置 list 的接口，同时保持元素的有序性。

2. SortedList 的底层实现基于以下几个关键点：

   - 分段有序数组：SortedList 将数据分成多个小的有序数组（称为段），每个段的大小适中，便于快速查找和插入。
   - 二分查找：在插入或查找元素时，使用二分查找算法快速定位元素应该插入的位置。
   - 动态调整：当某个段变得过大时，SortedList 会自动将其拆分成更小的段，以保持操作的效率。

4. 在普通的动态数组中，插入一个元素时，可能需要移动大量的元素。在 SortedList 中，数据被分成多个段，每个段的大小是 O(√n)。插入新元素时，只需要在某个段内部移动元素，移动的次数最多是 O(√n)。

5. SortedList 默认按照元素的自然顺序进行排序。对于数字类型，按升序排列；对于字符串类型，按字典序排列。如果需要自定义排序规则，可以通过 `key` 参数指定一个处理函数，按照函数返回结果排序。

   ```bash
   # 按绝对值排序
   sl = SortedList([-3, 1, -4, 2], key=abs)
   print(sl)  # 输出: SortedList([1, 2, -3, -4])
   ```

6. 使用方法:

   1. `add`插入
   2. `discard`删除
   3. `irange`范围查询
   4. `update`合并





##### defaultdict

1. defaultdict 是 Python 标准库 collections 模块中的一个类，它是 dict 的一个子类。它的特点是：

   1. 当访问一个不存在的键时，defaultdict 会自动调用指定的工厂函数，生成一个默认值，并将该键值对添加到字典中。
   2. 这样可以避免在访问不存在的键时抛出 KeyError 异常。

2. 具体使用:

   ```python
   map = defaultdict(SortedList)
   map[apple].add(20)
   ```

   



##### 优先队列

1. 优先队列(Priority Queue)和堆(Heap)不是同一个东西，但堆是实现优先队列的高效数据结构。优先队列是一种抽象数据类型，支持插入元素和按优先级取出元素，而堆是实现优先队列的一种方式。优先队列可以用堆、有序数组或其他结构实现，但堆是最常用的，因为它效率高。

2. Python 通过 `heapq` 模块提供堆操作，但需注意:默认是最小堆，且底层用列表、模拟堆结构，通过索引关系维护父子节点。

3. 常用方法:

   1. `heapify(x)`:创建堆，将列表 x 原地转换为堆，会修改 x 。<font color=red>x 还是普通 list 类型，不具备堆的各种方法。</font>
   2. `heappush(heap, item)`:插入元素 item 并维护堆结构。
   3. `heappop(heap)`:弹出堆顶元素。
   4. 查看堆顶元素:直接访问 `heap[0]`。
   5. `heapq.merge(*iterables)`:合并堆，合并多个有序迭代器，返回合并后的迭代器。
   6. `heapreplace(heap, item)`:替换堆顶元素,先弹出堆顶，再插入新元素(比 `heappop + heappush` 高效)。
   7. `heappushpop(heap, item)`:插入并弹出,先插入元素，再弹出堆顶(与 `heapreplace` 顺序相反)。

4. <font color=red>Python 的 `heapq` 仅支持最小堆，但可通过取负数模拟最大堆。</font>

5. 具体演示一下:

   ```python
   import heapq
   
   lst = [5, 4, 3, 2, 1]
   heapq.heapify(lst) 
   print(lst) # [1, 2, 3, 5, 4]
   heapq.heappush(lst, 0)
   print(lst) # [0, 2, 1, 5, 4, 3]
   print(heapq.heappop(lst)) # 0
   
   print(type(lst)) # <class 'list'>
   ```

   

