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





##### 常用

1. `enumerate()`函数用于在循环中同时获取元素的索引和值，使代码更简洁高效。

   1. 语法:`enumerate(iterable, start=0)`

      - `iterable`：可迭代对象（如列表、字符串等）。
      - `start`：索引的起始值（默认为0）。

   2. 返回值：生成一个枚举对象，每次迭代返回一个包含索引和元素值的元组`(index, element)`。

      ```python
      fruits = ['apple', 'banana', 'cherry']
      for index, fruit in enumerate(fruits, start=1):
          print(index, fruit)
      ```

2. `zip()`函数用于将多个可迭代对象的元素按顺序配对，生成一个迭代器，返回元组序列。它常用于并行处理多个序列，是同步迭代的高效工具。

   1. 语法:`zip(*iterables)`，提供多个可迭代对象，如列表、元组、字符串等。

   2. 返回值：生成一个迭代器，每次迭代返回一个元组，包含所有输入可迭代对象中对应位置的元素。

      ```python
      names = ["Alice", "Bob", "Charlie"]
      ages = [25, 30, 28]
      
      for name, age in zip(names, ages):
          print(f"{name} is {age} years old")
      ```

   3. 处理不同长度的可迭代对象:当输入的可迭代对象长度不同时，`zip()`会按最短的长度截断。若是需要保留所有元素，需使用`itertools.zip_longest()`(需导入`itertools`模块),此时迭代器中元祖中会使用 None 补齐。

      ```python
      from itertools import zip_longest
      
      list1 = [1, 2, 3]
      list2 = ['a', 'b']
      
      # 默认截断
      print(list(zip(list1, list2)))  # 输出：[(1, 'a'), (2, 'b')]
      
      # 保留所有元素（缺失值填充为None）
      print(list(zip_longest(list1, list2)))  # 输出：[(1, 'a'), (2, 'b'), (3, None)]
      ```

3.  `pairwise()` 函数用于将可迭代对象的相邻元素两两配对，生成连续的元组序列。它从 Python 3.10 开始被引入标准库的 `itertools` 模块中，是处理滑动窗口或相邻元素关系的实用工具。

   ```python
   temperatures = [22.5, 23.1, 24.3, 21.8]
   diffs = [b - a for a, b in pairwise(temperatures)]
   print(diffs)  # 输出：[0.6, 1.2, -2.5]
   ```

   > 可以和`enumerate()`和`zip()`一同使用！！！

4. 进制转换函数:

   1. `bin()`函数用于将整数转换为二进制字符串，格式为`0b`开头加二进制数值。它是处理二进制数据的基础工具，适用于位运算、编码转换等场景。
   2. `oct()`转换为八进制字符串,前缀`0o`。
   3. `hex()`转换为十六进制字符串,前缀`0x`。
   4. `format()`灵活控制进制输出格式,如`format(15, '04b')`生成`1111`。

5. 







##### SortedList

1. SortedList 是 Python 中 sortedcontainers 模块提供的一个数据结构，它是一个有序的列表，支持高效的插入、删除和查找操作。它的设计目标是提供类似于 Python 内置 list 的接口，同时保持元素的有序性。

2. SortedList 的底层实现基于以下几个关键点：

   - 分段有序数组：SortedList 将数据分成多个小的有序数组（称为段），每个段的大小适中，便于快速查找和插入。
   - 二分查找：在插入或查找元素时，使用二分查找算法快速定位元素应该插入的位置。
   - 动态调整：当某个段变得过大时，SortedList 会自动将其拆分成更小的段，以保持操作的效率。

3. 在普通的动态数组中，插入一个元素时，可能需要移动大量的元素。在 SortedList 中，数据被分成多个段，每个段的大小是 O(√n)。插入新元素时，只需要在某个段内部移动元素，移动的次数最多是 O(√n)。

4. SortedList 默认按照元素的自然顺序进行排序。对于数字类型，按升序排列；对于字符串类型，按字典序排列。如果需要自定义排序规则，可以通过 `key` 参数指定一个处理函数，按照函数返回结果排序。

   ```bash
   # 按绝对值排序
   sl = SortedList([-3, 1, -4, 2], key=abs)
   print(sl)  # 输出: SortedList([1, 2, -3, -4])
   ```

5. 使用方法:

   1. `add(value)`插入元素并保持有序性。

   2. `discard(value)`若存在删除元素，无返回值。不存在则抛出 `ValueError`。！！！

   3. `index(value)`返回元素第一次出现的索引，不存在则抛出 `ValueError`。

   4. `count(value)`返回元素出现的次数。

   5. `irange(min, max)`返回一个迭代器，包含 `[min, max]` 范围内的元素。

   6. `clear()`清空列表。

   7. `update(iterable)`批量添加元素,可以视为一种合并操作。

   8. `bisect_left(value)`返回元素应插入的位置索引(最左侧的位置)，以保持列表有序。若元素已存在，返回第一个匹配项的左侧位置。

      ```python
      sl = SortedList([1, 3, 3, 5])
      print(sl.bisect_left(3))  # 输出: 1（第一个3的左侧）
      print(sl.bisect_left(4))  # 输出: 3（插入到5的左侧）
      ```

   9. `bisect_right(value)`返回元素应插入的位置索引(最右侧的位置)。若元素已存在，返回最后一个匹配项的右侧位置。

      ```python
      print(sl.bisect_right(3))  # 输出: 3（最后一个3的右侧）
      ```

6. SortedList 支持索引和切片操作。







##### defaultdict

1. defaultdict 是 Python 标准库 collections 模块中的一个类，它是 dict 的一个子类。它的特点是：

   1. 当访问一个不存在的键时，defaultdict 会自动调用指定的工厂函数，生成一个默认值，并将该键值对添加到字典中。
   2. 这样可以避免在访问不存在的键时抛出 KeyError 异常。

2. 具体使用:

   ```python
   map = defaultdict(SortedList)
   map[apple].add(20)
   ```






##### Counter

1. 在 Python 中，`Counter` 是 `collections` 模块中提供的一个高效计数工具类，专门用于统计可哈希对象的出现次数。它本质上是字典 dict 的子类，key 是元素，value 是元素的计数。

2. 核心方法:

   1. `elements()`返回一个迭代器，按元素出现次数重复生成元素。元素按首次出现的顺序排列,计数为 0 或负数时，元素不会被输出。

      ```python
      from collections import Counter
      
      c = Counter(a=3, b=2, c=1)
      print(list(c.elements()))  # ['a', 'a', 'a', 'b', 'b', 'c']
      ```

   2. `most_common(n)`返回频率最高的前 `n` 个元素及其计数的元组列表,若省略 `n`，则返回所有元素。

      ```python
      from collections import Counter
      
      c = Counter('abracadabra')
      print(c.most_common(2))  # [('a', 5), ('b', 2)]
      ```

   3.  `update(iterable_or_mapping)`合并新的可迭代对象或计数器到当前计数器中,计数叠加。

      ```python
      c = Counter(a=3, b=1)
      c.update({'a': 1, 'b': 2})
      print(c)  # Counter({'a': 4, 'b': 3})
      ```

   4. `subtract(iterable_or_mapping)`从当前计数器中减去另一个可迭代对象或计数器的计数,结果允许负数。

      ```python
      c = Counter(a=4, b=3)
      c.subtract({'a': 2, 'b': 5})
      print(c)  # Counter({'a': 2, 'b': -2})
      ```

   5. `total()`(Python 3.10+)返回所有计数的总和。

      ```python
      c = Counter(a=3, b=2)
      print(c.total())  # 5
      ```

   6. `clear()`: 清空所有计数。

   7. 继承自字典的方法:略。

3. 计算:

   1. 加法 `+`: 合并两个计数器，仅保留正计数。
   2. 减法 `-`: 从第一个计数器减去第二个计数器，仅保留正计数。







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

6. 也可以使用下面的 `queue.PriorityQueue` ，二者比较如下:

   | 特性     | `queue.PriorityQueue`            | `heapq`            |
   | -------- | -------------------------------- | ------------------ |
   | 线程安全 | ✅ 是                             | ❌ 否               |
   | 用途     | 多线程优先级队列                 | 单线程优先级堆操作 |
   | 阻塞支持 | ✅ 支持 `block` 和 `timeout`      | ❌ 无               |
   | 任务跟踪 | ✅ 提供 `task_done()` 和 `join()` | ❌ 无               |
   | 性能     | 较高（基于堆，但含锁开销）       | 更高（无锁开销）   |







##### 队列

1. 在 Python 中，队列是一种先进先出(FIFO)的数据结构，它类似于现实生活中的排队场景，如在银行或超市排队等待服务。队列的实现允许元素按照它们被添加的顺序进行处理，这在多线程编程中尤其有用，可以安全地在多个线程之间传递消息。Python 提供了多种队列实现，包括普通队列、LIFO队列（后进先出，类似于栈）、优先级队列和双端队列。这些队列都支持线程安全的操作，使得它们适用于多线程环境中的任务调度和通信。

2. 普通队列(`queue.Queue`):是标准库 `queue` 模块中提供的线程安全队列实现，专为多线程编程设计，支持先进先出（FIFO）的数据存取。它封装了线程同步机制，确保多线程环境下的数据安全交换。

   1. 创建队列:

      ```python
      import queue
      
      # 创建一个最多容纳5个元素的队列
      q_0 = queue.Queue(maxsize=5)
      # 创建一个无限制大小的队列
      q_2 = queue.Queue()
      ```

   2. `put(item, block=True, timeout=None)`将元素 `item` 添加到队列。

      - `block`：队列满时是否阻塞等待（默认为 `True`）。
      - `timeout`：阻塞的最长时间（秒），超时后抛出 `queue.Full` 异常。

   3. `put_nowait(item)`,非阻塞版，等价于 `put(block=False)`，队列满时直接抛出异常。

   4. `get(block=True, timeout=None)`移除并返回队列中的一个元素。

      - `block`：队列空时是否阻塞等待（默认为 `True`）。
      - `timeout`：阻塞的最长时间（秒），超时后抛出 `queue.Empty` 异常。

   5. `get_nowait()`,非阻塞版，等价于 `get(block=False)`，队列空时直接抛出异常。

   6. `task_done()`标记队列中的一个任务已完成，必须与 `get()` 成对使用，用于通知队列任务处理完毕。

      ```python
      while not q.empty():
          item = q.get()
          process(item)
          q.task_done()  # 通知队列任务完成
      ```

   7. `join()`阻塞主线程，直到队列中所有任务被处理完成,即所有 `task_done()` 被调用。用于等待队列清空，避免提前退出主线程。

   8. `qsize()`返回队列当前元素数量,结果在多线程中可能不精确。

   9. `empty()`判断队列是否为空,结果在多线程中可能不精确。

   10. `full()`判断队列是否已满,结果在多线程中可能不精确。

   > 当调用 `put()` 或 `get()` 时，队列的容量或数据状态可能导致线程需要等待，具体场景包括：
   >
   > - 队列已满（`put` 时）：生产者需要等待消费者取出数据腾出空间。
   > - 队列为空（`get` 时）：消费者需要等待生产者放入数据。
   >
   > 此时，阻塞操作会让线程暂停（挂起），直到满足条件（如队列有空位或新数据到来），从而避免以下问题：
   >
   > - 资源浪费：非阻塞场景下，线程可能通过循环反复尝试操作（忙等待），消耗 CPU 资源。
   > - 数据丢失：若队列满时直接丢弃数据（非阻塞抛异常），可能导致重要任务未被处理。

3. 双端队列(`collections.deque`):是一个高效的双端队列，支持从两端快速插入和删除元素。与 `queue.Queue` 不同，它更轻量且专注于通用数据结构操作，而不是多线程通信。

   1. 创建队列:`deque(a, maxlen=6)`,需要导包`from collections import deque`。

      - `iterable`:可选,初始化的可迭代对象如列表、元组，默认创建空队列。
      - `maxlen`:可选,设置队列的最大长度。当队列满时，旧元素从另一端被自动丢弃。

      ```python
      from collections import deque
      a = [1, 2, 3, 4, 5]
      q = deque(a, maxlen=3)
      ```

   2. `append(x)`在队列右端(队尾)添加元素。

   3. `appendleft(x)`在队列左端(队头)添加元素。

   4. `extend(iterable)`在队尾批量添加多个元素。

   5. `extendleft(iterable)`在队头批量添加多个元素，注意插入顺序相反。

   6. `pop()`移除并返回右端(队尾)的元素,队列为空时抛出 `IndexError`。

   7. `popleft()`移除并返回队头的元素,队列为空时抛出 `IndexError`。

   8. `rotate(n=1)`将队列向右循环移动 `n` 步,`n` 为负时向左移动。可以理解为“元素轮转”。

      ```python
      from collections import deque
      
      d = deque(["A", "B", "C", "D", "E"])
      d.rotate(1)
      print(d)  # 输出: deque(['E', 'A', 'B', 'C', 'D'])
      ```

   9. `clear()`清空队列。

   10. `copy()`Python 3.5+,创建队列的浅拷贝。

   11. `count(x)`统计元素 `x` 出现的次数。

   12. `maxlen`返回队列的最大长度，若未设置则为 `None`。

4. 优先级队列(`queue.PriorityQueue`):是一个基于优先级的线程安全队列，继承自 `queue.Queue`。它按照元素的优先级顺序(默认从小到大)取出元素，适用于需要动态调整任务处理顺序的多线程场景。

   1. 创建方法:需要导包`from queue import PriorityQueue`。`maxsize`设置队列的最大容量，默认值为0。`maxsize ≤ 0`队列大小无限制；`maxsize > 0`时，队列满时，`put()` 会阻塞生产者线程，直到有空间可用。

      ```python
      from queue import PriorityQueue
      
      pq = PriorityQueue(maxsize=10)
      ```

   2. 其他方法参考`queue.Queue`。

5. LIFO队列(`queue.LifoQueue`):略

> 对于线程安全的方式，会有一些额外的开销，一般情况下不适合选用！！！







##### python缓存

1. 在Python中，`@lru_cache`和`@cache`是用于缓存函数调用结果的装饰器，可显著优化递归等重复计算的性能。

2. `@lru_cache(maxsize=None)`通过LRU(最近最少使用)算法缓存函数结果,`maxsize=None`表示缓存无大小限制，所有结果均保留。避免重复计算。例如斐波那契递归中，`fib(n)`的结果会被缓存，后续相同参数的调用直接返回缓存值。

3. `@cache`( python 3.9+)等价于`@lru_cache(maxsize=None)`，是无限制缓存的语法糖。

4. 使用示例:

   ```python
   from functools import lru_cache, cache
   
   # 使用 lru_cache
   @lru_cache(maxsize=None)
   def fib_lru(n):
       if n <= 1:
           return n
       return fib_lru(n-1) + fib_lru(n-2)
   
   # 使用 cache
   @cache
   def fib_cache(n):
       if n <= 1:
           return n
       return fib_cache(n-1) + fib_cache(n-2)
   ```

5. 二者均用于缓存函数结果，优化性能。但`@lru_cache`需指定`maxsize`，灵活性更高。`@cache`是`@lru_cache(maxsize=None)`的简化版，仅适用于Python 3.9及以上版本。

> 若是参数中含有可变类型，以下装饰器如何判断参数是否一致呢？在没有完全理解了解慎用！！！
>
> - 在 Python 中，`@cache` 或 `@lru_cache` 装饰器通过将函数参数转换为可哈希的键来判断调用是否相同。
> - 装饰器会将所有位置参数`*args`和关键字参数`**kwargs`组合成一个哈希键，作为缓存字典的键。
> - 可变对象(如列表、字典)本身不可哈希，直接作为参数会报错，此时需要转换为不可变类型，其中细节部分都需要去尝试！！！

| 问                   | 答                                   |
| -------------------- | ------------------------------------ |
| 可变对象存储方式     | 存储为地址引用，内容可变但地址不变。 |
| 列表转元组地址变化   | 地址会变，生成新对象。               |
| 元组哈希依据         | 基于内容，而非地址。                 |
| 可变对象不可哈希原因 | 内容可变会导致哈希不一致。           |







##### 判断质数

```python
def isPrime(n):
    if n <= 2: # 1和2都是素数
        return False
    for i in range(2, n): # 判断是否可以被2~n-1整除
        if n % i == 0:
            return False
    return True
```

```python
from math import sqrt

def isPrime(n):
    if n <= 2: 
        return False
    for i in range(2, int(sqrt(n)) + 1 ):  # int(num**0.5) + 1
        if n % i == 0:
            return False
    return True
```
线性筛选:???





##### 公因数、公倍数

```python
# 最大公约数
def gcd(a, b):
    if a < b: # 保证a大于b
        a, b = b, a
    while b != 0: # 辗转相除法
        a, b = b, a % b
    return a
```

```python
def gcd(a, b):
    if a < b: # 保证a大于b
        a, b = b, a
    while b != 0: # 辗转相除法
        a, b = b, a % b
    return a

# 最小公倍数
def lcm(a, b):
    return a * b // gcd(a, b)
```









##### 贪心

1. 首先，贪心算法是在每一步选择当前看起来最优的解，希望这样能得到全局最优。但问题在于，并不是所有问题都适用，因为局部最优的累积不一定是全局最优。比如背包问题，如果是分数背包的话，贪心是有效的，但如果是0-1背包，贪心可能就不行，因为可能选了某个高价值但重量大的物品，导致后面装不下更多有价值的轻物品。
2. 何时使用贪心算法?

   1. **最优子结构**：问题的最优解包含子问题的最优解。
   2. **贪心选择性质**：每一步的局部最优选择能导向全局最优解，无需回溯。
   3. **无后效性**：当前决策不影响后续子问题的结构。

3. 如何验证贪心正确性？

   1. 数学证明：
      1. <font color=red>替换法：假设存在一个最优解，证明用贪心选择替换后仍最优。(反证法)</font>
      2. 归纳法：证明贪心选择在每一步均保持最优解的可能性。

   2. 反例测试：构造可能使贪心失效的案例（如非规范硬币找零、0-1背包问题）。

4. 正确运用贪心的技巧

   1. 问题分析：
      - 识别是否为经典贪心问题（任务调度、最小生成树、霍夫曼编码等）。
      - 检查是否满足最优子结构和贪心选择性质。
   2. 策略设计：
      - 按特定属性排序（如结束时间、权重密度等）。
      - 选择当前最优指标（最短路径、最大收益等）。
   3. 验证与调试：
      - 严格数学证明或反例验证。
      - 对比动态规划解法，判断是否贪心足够。

5. 经典应用场景

   - 分数背包：按价值密度排序，贪心有效。

   - 活动选择：按结束时间排序选最多活动。

   - Dijkstra算法：无负权边时，贪心选择最短路径。

   - Prim/Kruskal算法：构造最小生成树的贪心策略。







##### 动态规划

1. 何时使用动态规划？动态规划的核心在于 **状态设计** 与 **递推关系**,动态规划适用于满足以下两个关键条件的问题：

   1. **最优子结构**: 问题的最优解包含其子问题的最优解。例如，最短路径问题中，A→B→C的最短路径必然包含A→B的最短路径。

   1. **重叠子问题**: 子问题在求解过程中被重复计算多次。例如，斐波那契数列中，计算 `fib(5)` 需要多次计算 `fib(3)` 和 `fib(2)`。

2. 正确运用DP的技巧:

   1. 状态定义: 将问题转化为可递推的数学形式。

      - 背包问题: `dp[i][w]` 表示前 i 个物品在容量 w 下的最大价值。
      - 编辑距离: `dp[i][j]` 表示字符串 `A[0..i]` 和 `B[0..j]` 的最小编辑次数。

   2. 状态转移方程: 明确父问题与子问题的递推关系。

      - 斐波那契数列: `dp[i] = dp[i-1] + dp[i-2]`。

      - 最长公共子序列:

        ```python
        if A[i] == B[j]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        ```

   3. 初始化与边界条件: 明确最小子问题的解。

      - 网格路径: `dp[0][0] = grid[0][0]`(起点)。
      - 硬币找零: `dp[0] = 0`(总金额为0时不需要硬币)。

   4. 填表顺序: 确保子问题在父问题之前解决。

      - **自底向上(迭代)**: 按状态维度从小到大遍历（如二维表按行或列填充）。
      - **自顶向下(记忆化搜索)**: 通过递归+缓存(如Python的`lru_cache`)实现按需计算。

   5. 空间优化

      - **滚动数组**：压缩状态空间，例如将二维DP优化为一维数组(如背包问题的空间优化)。
      - **状态合并**：去除冗余维度(如斐波那契数列只需保留前两项)。

3. 如何保证子问题在父问题前被解决？

   - 自底向上方法:显式按顺序计算子问题

     - 在编辑距离问题中，按行或列填充二维表，确保 `dp[i][j]` 计算时，`dp[i-1][j]`、`dp[i][j-1]` 和 `dp[i-1][j-1]` 已计算。
     - 在背包问题中，外层循环遍历物品，内层循环遍历容量，保证每个容量状态按顺序更新。

   - 自顶向下方法:通过递归调用自动分解问题，配合缓存记录已解决的子问题。

     ```python
     from functools import lru_cache
     
     @lru_cache(maxsize=None)
     def fib(n):
         if n <= 1:
             return n
         return fib(n-1) + fib(n-2)
     ```

4. 验证与调试技巧:

   1. 手动模拟小例子: 例如，对于 `dp[i][j] = dp[i-1][j] + dp[i][j-1]`（网格路径数），手动计算 `2x2` 网格验证结果是否为2。
   2. 打印DP表: 输出中间状态，观察是否符合预期。例如，检查硬币找零问题中 `dp` 数组的逐步填充过程。
   3. 对比暴力解: 对于小规模输入，对比DP解与暴力递归的结果是否一致。
   4. 数学归纳法: 假设子问题的解正确，证明父问题的解正确。例如，证明LCS的递推关系成立。

5. 典型应用场景:

   - **背包问题**: 0-1背包、完全背包、多重背包。

   - **序列问题**: 最长公共子序列 LCS、最长递增子序列 LIS。

   - **路径规划**: 网格最小路径和、编辑距离。

   - **资源分配**: 任务调度、矩阵链乘法。

6. 经典示例：硬币找零问题:给定硬币面额 `coins = [1, 2, 5]` 和总金额 `amount = 11`，求最少需要多少枚硬币。

   1. 状态定义: `dp[i]` 表示凑出金额 `i` 所需的最少硬币数。
   2. 状态转移: `dp[i] = min(dp[i - coin] + 1 for coin in coins if i >= coin)`。
   3. 初始化: `dp[0] = 0`，其余初始化为正无穷。
   4. 填表顺序: 从 `i=1` 到 `i=amount` 依次计算。
   5. 结果: `dp[11] = 3`(5+5+1)。

7. 经验之谈:

   1. 不一定是从一个固定转态转移到下一个转态，也就是一个问题肯能依赖一圈问题的解。
   2. <font color=red>不一定是单个转态集合之间的转变，可能是不同转态集合之前来回切换。</font>
   3. 有是可以对记忆数组进行优化，注意转态的构建顺序。
