**将零星的星火沉淀为银河，是文字赋予思考的温柔仪式———Deepseek**



#### 二月

##### 2.25

[189.轮转数组](https://leetcode.cn/problems/rotate-array/)(非每日一题)

> - 考虑特殊情况，k大于arr.length时，需要忽略完整圈数
> - 对于 python 切片，很容易就实现 `nums[:] = nums[num - k:] + nums[:num - k] `，这一解法演变出最后面的结题方式。

首先一般数组移位的题目，一般都是涉及到双指针的问题，而轮转又往往涉及到取余实现循环遍历。

最简单的还是所谓的空间换时间大法，直接创建一个新的数组:时间复杂度$O(n)$,空间复杂度$O(n)$

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        num = len(nums)
        arr = [0] * num
        for i in range(num):
            arr[(i+k) % num] = nums[i]

        for i in range(num):
            nums[i] = arr[i]   
```

是否能继续改进？简单模拟一下实现过程，其实很容易发现这个过程其实不存在重复问题，即某一个位置只会有一个正确元素。我们直接参照快排挖坑的方式，<font color=red>拆东墙补西墙</font>。当然在实际测试过程中忽略了一次循环无法遍历完的情况，后续已经完善:时间复杂度$O(n)$,空间复杂度$O(1)$

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        num = len(nums)
        i = 0 # 作为0号坑(存放待填坑的土)
        j = (i+k) % num # 挖个坑(第一个待填的位置)
        if j == i:
            return
        count = 0 # 填坑数
        while count < num: # 一共要填坑num次
            nums[i], nums[j] = nums[j], nums[i] # 填坑(并把土收集起来放到0号坑)
            count += 1 
            j = (j+k) % num # 挖坑(下一个待填的位置)
            if j == i: # 一个循环结束
                nums[i], nums[j] = nums[j], nums[i]
                count += 1
                i += 1
                j = (i+k) % num
```

后面查看题解的时候，也得到一种很好的解法：其实所谓数组轮状本质上就是将后 $k$ 个元素移动到最前面。我们记整个数组序列为$ S $，后面 $k$ 个元素组成序列为 $B$ ，剩余部分就是 $A$，即 $S = A + B$。这里我们记$ \overline{S} $为对$S $序列逆转操作。显然我们需要得到的结果是 $B + A$,其实也就是先得到 $\overline{S} = \overline{B} + \overline{A}$,然后分别执行$ B $、$ A $的逆转即可得到$ B + A $,还是很妙的解法。

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k = k % n  # 去掉完整圈数
        self.reverse(nums, 0, n - 1)
        self.reverse(nums, 0, k - 1)
        self.reverse(nums, k, n - 1)

    def reverse(self, nums: List[int], start: int, end: int) -> None:
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1
```







##### 2.26

[1472.设计浏览器历史记录](https://leetcode.cn/problems/design-browser-history)

> - Python 中没有专门的栈数据结构，但可以用 list 来实现栈，list 提供 append() 和 pop() 方法，可以方便地用来模拟栈的操作。
> - Python 的 list 是动态数组，可以根据需要自动调整大小。
> - 顺便回顾一下 python 语法，Python中的切片访问默认为左闭右开。

其实在看到设计浏览器历史时，就应该想到数据结构中的栈，但是在使用 传统数组和 list 之间犯难。若是采用其他语言刷题，或许需要根据题目设置 5000 长度数组(为啥是5000，题目说每种方法调用次数最多5000)。但是Python 的 list 是动态数组，可以根据需要自动调整大小，就可以无需考虑这个问题。

但是很多时候想法很好的，但是实际操作起来还是会发生很多问题。由于 python 的切片操作可以很方便的对数组和列表进行截取操作，切片在本题中实现连续弹出是很方便的。但是方便都是有代价的，由于切片操作不改变原来数组，那么不难猜测其底层应该会存在复制操作，这就必然会损耗时间。而对于栈，其实我们并没有必要直接删除，直接采用逻辑删除，入栈覆盖的方式，就省去了底层复制的时间。

其实到这里还没有引入关键问题，那就是在本题中，我想将 list 和 逻辑删除 结合。但是list 不能像数组那样直接通过索引插入元素。如果你尝试在一个特定索引位置插入元素，而该位置超出了当前列表的长度，会引发 IndexError。在本题的 visit 方法中，我们若是逻辑删除，就需要判断是采用覆盖的方式，还是采用 append 的方式，这其实是无法判断的(当然前提是你不增加其他标志，如 list 已使用的最大长度，但是这会打乱代码逻辑)。

> 补充:可以在每次 visit 时，使用 append 方法对 list 进行拓容，然后通过索引插入元素。

遇到的坑大致就是这些，下面给出逻辑删除和切片截取的代码实现:

采用原始数组实现，通过栈顶指针 index 实现逻辑删除，size 记录总数据

```python
class BrowserHistory:

    def __init__(self, homepage: str):
        # 初始化栈
        self.stack = [0 for _ in range(5000)] 
        self.stack[0] = homepage
        # index: 栈顶指针, size: 记录的总数
        self.index, self.size = 0, 1

    def visit(self, url: str) -> None:
        # 删除前进记录(逻辑上的删除)
        self.index += 1
        self.size  = self.index + 1
        # 添加新的历史记录(覆盖)
        self.stack[self.index] = url

    def back(self, steps: int) -> str:
        # 在第 index+1 条记录，最多只能回退 index -1 步(除去当前和最初)
        self.index = max(0, self.index - steps)
        return self.stack[self.index]
            
    def forward(self, steps: int) -> str:
        # 在第 index+1 条记录，最多只能前进 size-index 步(除去当前和最后)
        self.index = min(self.size-1, self.index + steps)
        return self.stack[self.index]
```

采用 list 和 切片实现,代码简洁许多，但是实际上切片中可能存在复制行为，会损耗一定时间。

```python
class BrowserHistory:

    def __init__(self, homepage: str):
        self.stack = [homepage]
        self.index = 0

    def visit(self, url: str) -> None:
        self.index += 1
        # 直接截取
        self.stack[self.index:] = [url] 

    def back(self, steps: int) -> str:
        # 最多只能推到 0
        self.index = max(0, self.index - steps)
        return self.stack[self.index]
            
    def forward(self, steps: int) -> str:
        # 最多只能推到 len(stack) - 1
        self.index = min(len(self.stack) - 1, self.index + steps)
        return self.stack[self.index]
```







##### 2.27

[2296.设计一个文本编辑器](https://leetcode.cn/problems/design-a-text-editor)

> - list 中`extend()` 将一个可迭代对象中的所有元素添加到列表的末尾。
> - 在切片操作中，索引越界是允许的。
> - str( list )并不是将 list 元素拼接成字符串，而是将整个结构作为字符串，就很抽象。

设计文本编辑器，涉及大量的中间删除操作，数组是不合适的，显然会想到链表。但是这里还是存在一些顾虑，链表由于需要存储指针，数据存储密度不高，尤其是编辑器这种按字符存储，所以不打算将链表作为第一选择。

但是数组处理中间插入、删除操作十分麻烦，需要频繁的移动。于是我们想到复制，对于插入一串字符，直接复制比移动来的简单快捷。显然 list 就很合适。但是其实对于编辑器而言，每次插入、删除时复制一遍，效率也是很低的。结果就是<font color=red>emmm……测试超时了!!!</font>

```python
class TextEditor:

    def __init__(self):
        self.text = []
        # cursor光标是虚拟的，并不会占用字符位
        self.cursor = 0 # 光标位置(其实也就是光标右侧的字符数)

    def addText(self, text: str) -> None:
        # self.text.extend(text)
        self.text = self.text[:self.cursor] + list(text) + self.text[self.cursor:]
        self.cursor += len(text)

    def deleteText(self, k: int) -> int:
        k = min(self.cursor, k)
        self.text = self.text[:self.cursor - k] + self.text[self.cursor:]
        self.cursor -= k
        return k

    def cursorLeft(self, k: int) -> str:
        k = min(self.cursor, k)
        self.cursor -= k
        return ''.join(self.text[self.cursor-min(10, self.cursor):self.cursor])

    def cursorRight(self, k: int) -> str:
        k = min(len(self.text) - self.cursor, k)
        self.cursor += k
        return ''.join(self.text[self.cursor-min(10, self.cursor):self.cursor])
```

显然，还是回归到链表设计，由于插入、删除都是在光标左侧进行操作，~~其实单向链表，左指针似乎就行~~，左右移动操作无法通过单链表操作，还是需要双链表。在删除操作时，显然一个个遍历删除比较耗时，于是还是采用整段删除比较好，下面给出完整代码:

```python
class Node:
    def __init__(self, val=''):
        self.val = val
        self.pre = None
        self.next = None

    def l_insert(self, node):
        # 尽量最后修改self.pre不然会导致前面的节点丢失
        node.next = self
        node.pre = self.pre
        if self.pre:
            self.pre.next = node
        self.pre = node
    
    def continuous_delete(self, goal):
        # 向左删除
        if goal.pre:
            goal.pre.next = self
            self.pre = goal.pre
        else:
            self.pre = None
    
    def get_l_text(self,len=10):
        res = []
        cursor = self
        while len > 0 and cursor.pre:
            cursor = cursor.pre
            res.append(cursor.val)
            len -= 1
        return ''.join(res[::-1]) # 逆序输出!!!


class TextEditor:
    def __init__(self):
       self.text = Node()
       self.cursor = self.text

    def addText(self, text: str) -> None:
        for c in text:
            node = Node(c)
            self.cursor.l_insert(node)
            # self.cursor = node(不需要移动光标)

    def deleteText(self, k: int) -> int:
        #删除区间:[goal, self.cursor)
        res = 0
        goal = self.cursor
        while k > 0 and goal.pre:
            goal = goal.pre
            k -= 1
            res += 1
        if res != 0:
            self.cursor.continuous_delete(goal)
        return res


    def cursorLeft(self, k: int) -> str:
        for _ in range(k):
            if self.cursor.pre:
                self.cursor = self.cursor.pre
            else:
                break
        return self.cursor.get_l_text()
    
    def cursorRight(self, k: int) -> str:
        for _ in range(k):
            # cursor是虚拟节点,不占用空间
            if self.cursor.next:
                self.cursor = self.cursor.next
            else:
                break
        return self.cursor.get_l_text()
```

实际上在整段删除时，最初考虑的是都是开区间，也就是 goal 不会被删除，但是处理上略麻烦，不同如下:

```python
class Node:
    # ...
    def continuous_delete(self, goal):
        # 向左删除
        if goal:
            goal.next = self
            self.pre = goal
        else:
            self.pre = None

class TextEditor:
    # ...
    def deleteText(self, k: int) -> int:  
        if k == 0 or not self.cursor.pre:
            return 0
        else:
            # 删除区间为开区间 (goal, self.cursor)
            goal = self.cursor.pre
        res = 0
        while k > 0 and goal:
            goal = goal.pre
            k -= 1
            res += 1
        if res:
        	self.cursor.continuous_delete(goal) 
        return res
```

> `get_l_text`一定不要忘记反转！！！
>
> 虽然熟悉链表的原理，但是实际使用的时候还是有一堆的细节没有考虑完全，例如一些边界问题。

查看官方题解提供一个双栈解法(以光标划分)，想不到啊！！！代码简便，逻辑清晰，这应该就是最优解了吧。

```python
class TextEditor:
    def __init__(self):
        self.left = []
        self.right = []

    def addText(self, text: str) -> None:
        self.left.extend(text)

    def deleteText(self, k: int) -> int:
        count = min(k, len(self.left))
        del self.left[-count:] # 使用负数索引删除光标左侧的字符
        return count

    def cursorLeft(self, k: int) -> str:
        for _ in range(min(k, len(self.left))):
            self.right.append(self.left.pop()) #左栈弹出，右栈压入
        return ''.join(self.left[-10:])

    def cursorRight(self, k: int) -> str:
        for _ in range(min(k, len(self.right))):
            self.left.append(self.right.pop()) #右栈弹出，左栈压入
        return ''.join(self.left[-10:])
```

<br><img src="./assets/image-20250227104603029.png" alt="image-20250227104603029" style="zoom:67%;" />







##### 2.28

[2353. 设计食物评分系统](https://leetcode.cn/problems/design-a-food-rating-system)，话说咋最近一直是设计题啊

> - 对于有序链表的排序，其实就是一个个比较，我们只需要实现一个比较的代码，后续直接递归调用即可。
> - 对于有序链表的维护，删除就不说了，插入也简单，唯独更新时需要删除节点重新插入。<font color=red>但是注意重新插入的结点一定要将前后指针置空，不然插入到端点位置会导致循环。</font>
> - 在 2.26 思考的 list 逻辑删除时导致插入需要使用 append 为 list 拓容的想法，也是在最后手动实现堆中得到了运用。

这题关键就两个 修改分数 和 按照分数排序 ，最关键的算法还是排序。对于该系统而言，在内部动态的维护一个排序序列比每次获取时排序要好得多，动态维护的方式只需要在添加、修改、删除的时候动态更新，而获取时可以直接使用。

但是，还是要试一下每次 highestRated 时排序获取，<font color=red>结果也是不出意外的超时了…</font>

```python
from typing import List

class FoodRatings:

    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.foods = foods
        self.cuisines = cuisines
        self.ratings = ratings

    def changeRating(self, food: str, newRating: int) -> None:
        # 找到 food 的索引
        food_index = self.foods.index(food)
        # 修改 food 的评分
        self.ratings[food_index] = newRating

    def highestRated(self, cuisine: str) -> str:
        # 找到所有 cuisine 的索引
        cuisine_index = [i for i, c in enumerate(self.cuisines) if c == cuisine]
        # 找到评分最高的 food
        max_rating = -1
        max_food = ""
        for i in cuisine_index:
            if self.ratings[i] > max_rating:
                max_rating = self.ratings[i]
                max_food = self.foods[i]
            elif self.ratings[i] == max_rating:
                if self.foods[i] < max_food:
                    max_food = self.foods[i]
        return max_food
```

对于动态维护的方式，由于是按照烹饪方式进行排序，不妨建立一个 map ，key 为烹饪方式，value 时一个动态维护的分数排序链表(频繁地插入删除操作)。但是这样的话，在修改评分的时候就麻烦了，我需要遍历所有的结点，于是在此基础上我又建立一个 map 按照食物名称存储其烹饪方式(为啥不直接将烹饪方式存储在结点中？可是我就是要找到结点啊！！！)，这样我们在更新有序链表时更新分数。<font color=red>结果也是出意外的超时了…</font>

```python
from typing import List

class Food:
    def __init__(self, name: str, rating: int):
        self.name = name
        # self.cuisine = cuisine
        self.rating = rating
        self.next = None
    
    def insert(self, food) -> None:
        if self.next is None: 
            self.next = food
        elif self.next.rating < food.rating: 
            food.next = self.next
            self.next = food
        elif self.next.rating == food.rating:
            if self.next.name > food.name:
                food.next = self.next
                self.next = food
            else:
                self.next.insert(food) # 递归插入
        else:
            self.next.insert(food)


class FoodRatings:

    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.map = {}
        self.cui = {} #方便修改评分
        # 为方便插入，有序链表含头结点
        for i in range(len(foods)):
            food = Food(foods[i],ratings[i])
            self.cui[foods[i]] = cuisines[i]
            # 如果cuisine不存在，则创建一个新的链表
            if cuisines[i] not in self.map:
                self.map[cuisines[i]] = Food("", -1)
            # 拿到头结点，插入数据
            self.map[cuisines[i]].insert(food)

    def changeRating(self, food: str, newRating: int) -> None:
        # 获取烹饪方式
        cuisine = self.cui[food]
        # 维护有序链表(删除+插入)
        cursor = self.map[cuisine]
        while cursor.next is not None:
            if cursor.next.name == food:
                break
            cursor = cursor.next
        # 删除节点
        temp = cursor.next
        cursor.next = cursor.next.next
        # 修改评分并重新插入 
        temp.next = None # 若是尾节点,会导致循环！！！
        temp.rating = newRating 
        self.map[cuisine].insert(temp)

    def highestRated(self, cuisine: str) -> str:
        # 由于一定存在(题目)，直接返回
        return self.map[cuisine].next.name
```

我还测试了两遍，全是超时，不干了，退了。<br><img src="./assets/image-20250228093717454.png" alt="image-20250228093717454" style="zoom:67%;" /><br><img src="./assets/image-20250228112451678.png" alt="image-20250228112451678" style="zoom:67%;" />

应该还是初始化有序链表和后续维护有序链表效率太低了，需要遍历。也就是排序算法的问题，对于数组我们可以使用二分法插入，但是数组的插入是一种代价较高的操作，那么链表是否能二分？一般来说不能，但是树可以，但是排序树emmm…就很麻烦。

查看官方的题解，使用有序集合 SortedList ，查了一下底层并不是我猜想的树形结构，而是数组。这时候就不得不提到我一开始就弃用数组的原因，修改时需要移动大量元素。但是在 `SortedList` 中，数据被分成多个段，每个段的大小是 O(√n)。插入新元素时，只需要在某个段内部移动元素，移动的次数最多是 O(√n)。

```python
from collections import defaultdict
from typing import List

from sortedcontainers import SortedList

class FoodRatings:

    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.map = defaultdict(SortedList) 
        self.food_map = {}
        for i in range(len(foods)):
            food = foods[i]
            cuisine = cuisines[i]
            rating = ratings[i]
            self.food_map[food] = (cuisine, rating)
			# 使用负数，从而rating按照从大到小排序
            self.map[cuisine].add((-rating, food))

    def changeRating(self, food: str, newRating: int) -> None:
        cuisine, oldRating = self.food_map[food]
        # 删除旧的
        self.map[cuisine].remove((-oldRating, food))
        # 添加新的
        self.map[cuisine].add((-newRating, food))
        # 更新
        self.food_map[food] = (cuisine, newRating)

    def highestRated(self, cuisine: str) -> str:
        return self.map[cuisine][0][1]
```

> 感觉没有昨天的题解惊艳，还是忘不了昨天的双栈！！！不过 SortedList 通过分块的方式减少插入、删除时元素的移动，还是很巧妙的，既保留数组二分查找的优点，又减缓数组插入的缺点。
>
> 此外，`TreeSet` 是 Java 标准库中的一个有序集合类，基于红黑树实现。它始终保持元素的有序性，并且支持高效的插入、删除和查找操作。

还有一个官方题解，使用堆，说实话自从学了数据结构，这还是第一次遇到堆。堆不支持快速的随机删除与修改操作，因此为了维护堆顶数据的有效性，可以采用懒删除的方法，将维护操作推迟到查询时才进行。<font color=red>也就是在更新的时候插入一个新的食物(同名但是分数不同)，然后再获取最高分数的时候，判断是不是旧的，若是，则删除堆顶元素，重新获取，也是很妙啊</font>！！！堆的实现还是比较简单的，尝试手动实现一下，代码如下:

```python
from typing import List

class Heap:

    def __init__(self,arr:List[int]):
        self.arr = arr
        self.size = len(arr)
        self.buildMinHeap() # 构建最小堆
    
    def buildMinHeap(self):
        # 大元素不断下沉，最后得到递增序列
        for i in range(self.size//2,-1,-1):
            self.minHeapify(i)

    def minHeapify(self,i): 
        temp = self.arr[i]  # 保存当前节点的值
        k = 2*i+1
        while k < self.size:
            # 选取左右孩子中较小的一个(相等时选左孩子)
            if k+1 < self.size and self.arr[k] > self.arr[k+1]:
                k += 1
            if self.arr[k] < temp:
                self.arr[i] = self.arr[k]
                i = k # 继续调整子树
                k = 2*i + 1
            else: # 当前节点值小于左右孩子的最小值，不需要调整
                break
        self.arr[i] = temp

    def siftUp(self,i):
        while i > 0:
            parent = (i-1)//2
            if self.arr[parent] > self.arr[i]: # 父节点大于子节点，交换
                self.arr[parent],self.arr[i] = self.arr[i],self.arr[parent]
                i = parent # 继续上浮调整
            else:
                break
    
    def add(self,value):
        # 这里不能append(pop是逻辑删除，不是真正删除)但是也不能使用索引赋值，因为可能会越界
        # 但是有一个方式一定不会越界，先append拓容，再赋值
        self.arr.append(value)
        self.arr[self.size] = value
    
        self.size += 1
        self.siftUp(self.size-1)  # 新加入的元素上浮
    
    def pop(self):
        if self.size == 0:
            return None
        self.arr[0] = self.arr[self.size-1]
        self.size -= 1
        self.minHeapify(0)

    def top(self):
        if self.size == 0:
            return None
        return self.arr[0]
        

class FoodRatings:

    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        self.foods_map = {}
        self.cuisines_map = {}
        for i in range(len(foods)):
            food = foods[i]
            cuisine = cuisines[i]
            rating = ratings[i]
            self.foods_map[food] = (cuisine,rating)
            if cuisine not in self.cuisines_map:
                self.cuisines_map[cuisine] = []
            self.cuisines_map[cuisine].append((-rating,food))
        for cuisine in self.cuisines_map:
            self.cuisines_map[cuisine] = Heap(self.cuisines_map[cuisine])

    def changeRating(self, food: str, newRating: int) -> None:
        cuisine,rating = self.foods_map[food]
        self.foods_map[food] = (cuisine,newRating)
        self.cuisines_map[cuisine].add((-newRating,food))

        
    def highestRated(self, cuisine: str) -> str:
        heap = self.cuisines_map[cuisine]
        while heap.size > 0:
            rating,food = heap.top()
            if  self.foods_map[food][1] == -rating:
                return food
            heap.pop()
        return ""
```

> 还是遇到一点小问题，之前学习数据结构的时候，构建堆时，0 号位置是不放置树节点的，那么根结点 i 的子结点是 2i 和 2i+1。但是现在 0 号位置存储元素，根结点 a 的子结点就是 2a+1 和 2a+2。

<br><img src="./assets/image-20250228115423907.png" alt="image-20250228115423907" style="zoom:67%;" />





#### 三月

##### 3.1

[131. 分割回文串](https://leetcode.cn/problems/palindrome-partitioning)

> 默认参数在函数定义时就被创建，并在所有函数调用之间共享。对于递归函数中的可变类型参数，若是使用默认参数，可能会导致一些问题。但是其实在本题中无关大雅，只会在第一次调用时使用默认参数。

如何判断一个字符串是回文串？倒序遍历的结果与正序一致或者从两端向中间遍历，每次遍历字符一致。

```python
def adjust(self, head: int, tail: int) -> bool:
    while head < tail:
        if self.s[head] != self.s[tail]:
            return False
        head += 1
        tail -= 1
    return True

def adjust(self, head: int, tail: int) -> bool:
    s = self.s[head:tail+1]
    return s == s[::-1]
```

此外，对于返回全部方案，是否存在这样一种情况，在 A 方案中，我们判断 xxx 是回文串，那么到 B 方案中，我们如何避免再次判断？

那么具体如何解决这个问题，其实稍微尝试一下，大致可以知道对于每一个结果集的下一个结果，是存在多种可能的，类似一种树形结构，对此我还是通过 dfs + 回溯完成:

```python
from typing import List

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        self.s = s
        p = 0 # 遍历指针
        self.res_list = []
        self.dfs(s, p, [])
        return self.res_list


    def dfs(self, s: str, p:int, res: List[str])->None:
        if p == len(s):
            # 可变对象，传参传的是引用
            self.res_list.append(res[:])
            return
        # [p, i] 是回文串?
        for i in range(p, len(s)):
            if self.adjust(p, i):
                res.append(s[p:i+1])
                self.dfs(s, i+1, res)
                res.pop() # 回溯
    
    def adjust(self, head: int, tail: int) -> bool:
        while head < tail:
            if self.s[head] != self.s[tail]:
                return False
            head += 1
            tail -= 1
        return True
```

回到刚开始的问题，是否能避免每次重复判断某个子串是否为回文子串？牺牲空间换时间，设置一个二维数组:

```python
from typing import List

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        self.s = s
        p = 0 # 遍历指针
        self.res_list = [] # 结果集
        # 判断记录
        self.judge = [[0 for _ in range(len(s))] for _ in range(len(s))] 
        self.dfs(s, p, [])
        return self.res_list


    def dfs(self, s: str, p:int, res: List[str])->None:
        if p == len(s):
            # 可变对象，传参传的是引用
            self.res_list.append(res[:])
            return
        # [p, i] 是回文串?
        for i in range(p, len(s)):
            if self.adjust(p, i):
                res.append(s[p:i+1])
                self.dfs(s, i+1, res)
                res.pop() # 回溯
    
    def adjust(self, head: int, tail: int) -> bool:
        # 从判断记录中找结果
        if self.judge[head][tail] == 1:
            return True
        elif self.judge[head][tail] == -1:
            return False
        # 没有判断过
        while head < tail:
            if self.s[head] != self.s[tail]:
                self.judge[head][tail] = -1 # 记录
                return False
            head += 1
            tail -= 1
        self.judge[head][tail] = 1 # 记录
        return True
```

满心欢喜的提交，但是从力扣执行结果而言，提升并不明显，甚至还慢了!!!<br><img src="./assets/image-20250301093420637.png" alt="image-20250301093420637" style="zoom:80%;" />
<br><img src="./assets/image-20250301093337438.png" alt="image-20250301093337438" style="zoom:67%;" />

那么暴力遍历是否能解决这个问题呢，哪怕代价极高？俺不知道也不想知道。但是在查看官方题解的时候，发现官方对于回文串的判断使用动态规划，例如对于一个串 abcba 我们想知道它是不是回文串，我们只要知道两件事就可以判断：去掉两端的子串 bcb 是不是回文串，以及两端是否相等(a=a?)。

但是我有一个问题，这也是我每次遇到动态规划都会想半天的东西，那就是我的子问题一定会在此之前得到答案吗？也就是说 bcb 是否为回文串这个答案一定会在我判断 abcba 之前知道吗？我又如何确保？这是每次使用动态规划都会遇到的难点！！！(自底向上、自顶向下)

动态规划这种方法，想明白就简单方便，想不明白，emm…越看越觉得它在忽悠我。







##### 3.2

[132. 分割回文串 II](https://leetcode.cn/problems/palindrome-partitioning-ii)

看到最小次数，emmm…我直接贪心，每次保证取得最长回文子串。贪心问题一般需要考虑三个问题: 想贪、咋贪、凭啥贪。但是这题emmm…不敢贪，好吧，自娱自乐一下。贪心问题最重要的是找到局部最优解，并且局部最优要直接导向全局最优。但是这题，若是我们每次取最长回文子串，其实会导致一个问题:会影响后面的回文串结构，导致原本可以组成回文的串被迫拆为多个<br><img src="./assets/image-20250302090616575.png" alt="image-20250302090616575" style="zoom:75%;" />

那么，老老实实来吧，昨天的回文串我们已经找到所有的分割方式，那所有的都找了，最小分割不也就有了，无非就是时间代价有点大。当然还是解决一下昨天的遗留问题，动态规划，在昨天的问题中得到 `f[i][j] = (s[i] == s[j]) and f[i + 1][j - 1]`,显然通过表达式知道 i 需要从大到小算，而 j 需要从小到大算，那么前提已经研究清楚，结果也是超时了:

```python
class Solution:
    def minCut(self, s: str) -> int:
        self.s = s
        self.n = len(s)
        self.dp = [[True] * self.n for _ in range(self.n)]
        # 动态规划预处理
        for i in range(self.n - 1, -1, -1):
            for j in range(i + 1, self.n):
                # 忽略 i=j 的情况
                if j - i == 1:
                    self.dp[i][j] = s[i] == s[j]
                else:
                    self.dp[i][j] = self.dp[i + 1][j - 1] and (s[i] == s[j])
        # 初始化最小回文串分割次数
        self.min_cut = self.n - 1 
        self.dfs(0, 0)
        return self.min_cut
    
    def dfs(self, start, cut):
        if start == self.n:
            # 越界，此时cut记录的是分割段数，需要减1才是分割次数
            self.min_cut = min(self.min_cut, cut - 1)
            return   
        if cut >= self.min_cut: # 剪枝(不是最小分割次数，没必要继续)
            return  
        for i in range(start, self.n):
            if self.dp[start][i]:
                self.dfs(i + 1, cut + 1) 
```

贪心贪不了，dfs 又超时……哪怕知道是使用动态规划也是毫无头绪。

根据官方的方法，我们依次求出 [0:n] 状态下的最优解(最短分割),然后对于 [0:m] (m > n) 状态，我们尝试在之前的最优解的基础上( 以 n 为跳板 )继续寻求最优，最后取最小值记作当前状态的最优解。一句话说，整体的解(没说最优)是如何组成的？是由末尾回文子串+前面部分分割方案组成，而这种组成不唯一，我们取最优的那一个，即前面部分分割最优，进而根据末尾回文子串的选取不同得到一个个子问题。

```python
class Solution:
    def minCut(self, s: str) -> int:
        self.s = s
        self.n = len(s)
        self.dp = [[True] * self.n for _ in range(self.n)]
        # 动态规划预处理
        for i in range(self.n - 1, -1, -1):
            for j in range(i + 1, self.n):
                # 忽略 i=j 的情况
                if j - i == 1:
                    self.dp[i][j] = s[i] == s[j]
                else:
                    self.dp[i][j] = self.dp[i + 1][j - 1] and (s[i] == s[j])
        # 记录[0, i]的最小分割次数
        self.min_cut = [0] * self.n

        for i in range(1, self.n):
            # 回文串，无需分割
            if self.dp[0][i]:
                self.min_cut[i] = 0
            else:
                # 取最坏情况
                self.min_cut[i] = self.min_cut[i - 1] + 1
                for j in range(1, i):
                    if self.dp[j][i]: # 取末尾回文子串
                        # 根据末尾回文子串的选取,计算各个情况下的最小分割次数，取最小值
                        self.min_cut[i] = min(self.min_cut[i], self.min_cut[j - 1] + 1)
        return self.min_cut[-1]
```

这个动态规划的方式与昨天(上面的解法)不同的是，父问题的解依赖一群子问题的解，无法判断当前状态是从哪一个子状态转化而来，这种状态转移对我来说还是有点难想。贪心和动态规划也算是力扣上的”黑白无常“了，拼尽全力无法与之匹敌！刷题嘛，慢慢来吧！！！<br><img src="./assets/image-20250302100655153.gif" alt="image-20250302100655153" style="zoom:75%;" />





##### 3.3

[1278. 分割回文串 III](https://leetcode.cn/problems/palindrome-partitioning-iii)

参照前两天的题，其实也猜到了今天依旧是动态规划，首先肯定分析问题，尝试将其数学化，定义状态并确定状态方程。下面我们忽略边界的开闭，简单整理一下思路:对于一个字符串S,我们将其分为 k 个回文串修改最小次数记为 $f(n,k)$,那么其实接下来的思路就和昨天的回文串II类似，我们向前推一个子串$(n-k,n]$那么得到一个子问题$f(n-k,k-1)$，那么记$(n-k,n]$转换为回文串的最小代价为$m$,那么显然$f(n,k)=min(f(n-k,k-1)+m)$。描述的有些粗糙，但是大致是这个意思,写出以下代码，<font color=red>但是很遗憾超时了</font>。

```python
class Solution:
    def palindromePartition(self, s: str, k: int) -> int:
        self.dp = [[True]*len(s) for _ in range(len(s))]
        self.len = len(s)
        for i in range(len(s)-1,-1,-1):
            for j in range(i+1,len(s)):
                self.dp[i][j] = self.dp[i+1][j-1] and s[i] == s[j]
        return self.minReplace(s,len(s)-1,k)

    def minReplace(self, s: str, end: int, k: int) -> int:
        mim_rep = self.len # 用于记录最小替换次数
        if k == 0 and end == -1: #此时恰好分为k个回文串
            return 0
        elif k == 0 or end == -1: # 此时不可能分为k个回文串,设为len让其无法被选中
            return self.len
        for i in range(end,-1,-1):
            if self.dp[i][end]:
                mim_rep = min(mim_rep, self.minReplace(s,i-1,k-1))
            else:
                mim_rep= min(mim_rep, self.minReplace(s,i-1,k-1) + self.replace(s,i,end))
        return mim_rep


    def replace(self, s: str, start: int, end: int) -> int:
        count = 0
        while start < end:
            if s[start] != s[end]:
                count += 1
            start += 1
            end -= 1
        return count
```

动态规划结题，有时会涉及重复调用问题，此时就要考虑记忆搜索，避免多次计算相同子问题。这里最关键的无非是$n、k$,我们将其作为键去存储计算结果，每次先去记录中找，找不到再计算，并把结果保存到记录中。当然其实在前几次的官方题解中，可以学到一招叫做 `@cache`,给出如下代码:

```python
from functools import cache

class Solution:
    def palindromePartition(self, s: str, k: int) -> int:
        self.dp = [[True]*len(s) for _ in range(len(s))]
        self.len = len(s)
        for i in range(len(s)-1,-1,-1):
            for j in range(i+1,len(s)):
                self.dp[i][j] = self.dp[i+1][j-1] and s[i] == s[j]
        return self.minReplace(s,len(s)-1,k)

    @cache
    def minReplace(self, s: str, end: int, k: int) -> int:
        mim_rep = self.len # 用于记录最小替换次数
        if k == 0 and end == -1: #此时恰好分为k个回文串
            return 0
        elif k == 0 or end == -1: # 此时不可能分为k个回文串,设为len让其无法被选中
            return self.len
        for i in range(end,-1,-1):
            if self.dp[i][end]:
                mim_rep = min(mim_rep, self.minReplace(s,i-1,k-1))
            else:
                mim_rep= min(mim_rep, self.minReplace(s,i-1,k-1) + self.replace(s,i,end))
        return mim_rep


    def replace(self, s: str, start: int, end: int) -> int:
        count = 0
        while start < end:
            if s[start] != s[end]:
                count += 1
            start += 1
            end -= 1
        return count
```

其实还是有点好奇，满足(n,k)挺难的吧，真的会那么多次命中记录？我尝试在本地运行代码:第一个使用缓存基本秒出答案，第二个没用缓存等半天手动终止了<br><img src="./assets/image-20250303100655223.png" alt="image-20250303100655223" style="zoom:75%;" />

其实回过头来仔细想想，当$n、k$比较大时，由于我们每次取末尾子串的情况足够复杂，多次取不同长度子串，最后导致不同取法所得结果(依赖的子问题)的$n、k$一致的概率(命中缓存记录)还是很大的。

当然还是老样子，看一下官方的题解，官方使用的是循环实现，这本身问题不大(只是递归对我而言熟悉一些)，但是在官方的第二种结题方式中使用预处理，提前计算了各个子串变为回文串的最小代价。为什么要这样做？回看我的代码，其实它仍有不完善的地方，$self.replace(s,i,end))$显然也是可以缓存的，也存在重复计算的情况，此外也不难看出这又是一个动态规划问题，而且和判断回文串其实差别不大，于是重新优化代码:

```python
from functools import cache

class Solution:
    def palindromePartition(self, s: str, k: int) -> int:
        self.len = len(s)
        self.dp = [[0]*len(s) for _ in range(len(s))]
        # 预处理
        for i in range(self.len-1,-1,-1):
            for j in range(i+1,self.len):
                if s[i] == s[j]:
                    self.dp[i][j] = self.dp[i+1][j-1]
                else:
                    self.dp[i][j] = self.dp[i+1][j-1] + 1
                # self.dp[i][j] = self.dp[i+1][j-1] + (1 if s[i] != s[j] else 0)
        return self.minReplace(s,len(s)-1,k)

    @cache
    def minReplace(self, s: str, end: int, k: int) -> int:
        mim_rep = self.len # 用于记录最小替换次数
        if k == 0 and end == -1: #此时恰好分为k个回文串
            return 0
        elif k == 0 or end == -1: # 此时不可能分为k个回文串,设为len让其无法被选中
            return self.len
        for i in range(end,-1,-1):
            mim_rep = min(mim_rep,self.minReplace(s,i-1,k-1)+self.dp[i][end])
        return mim_rep
```





##### 3.4

[1745. 分割回文串 IV](https://leetcode.cn/problems/palindrome-partitioning-iv)

判断一个字符串能否分割为三个非空回文子串，三个子串，两个分割点，两层循环即可:

```python
class Solution:
    def checkPartitioning(self, s: str) -> bool:
        self.s = s
        self.n = len(s)
        # 不符合参赛要求
        if self.n < 3:
            return False
        # 动态规划预处理
        self.dp = [[True] * self.n for _ in range(self.n)]
        for i in range(self.n - 1, -1, -1):
            for j in range(i + 1, self.n):
                # 当j-1 > i+1(j=i+1)时，默认值为True
                self.dp[i][j] = self.dp[i + 1][j - 1] and s[i] == s[j]
        
        # 分三段找两个分割点[0,i-1], [i,j-1], [j,n-1]
        # i的取值范围[1, n-2]（保证三段都有字符）
        for i in range(1, self.n - 1): 
            # j的取值范围[i+1, n-1](保证第二、三段有字符)
            for j in range(i + 1, self.n): 
                if self.dp[0][i - 1] and self.dp[i][j - 1] and self.dp[j][self.n - 1]:
                    return True
        return False
```

标个困难题吓唬我是吧！！！<br><img src="./assets/image-20250304085348080.png" alt="我思故我在，生日快乐，梦鱼！" style="zoom:67%;" />







##### 3.5

[1328. 破坏回文串](https://leetcode.cn/problems/break-a-palindrome)

首先题目提到一个无法做到的情况，对于任意一个长度大于 1 的字符串，都是可以存在返回值的(其实写到后面才知道没有懂题目的意图，啥情况下无论修改字符都是回文串？奇数中间)。其次那么我们是否需要每次重新判断是否回文串？不需要，~~对于长度大于 1 回文串我们改动任意字符都会使其不再满足回文~~，对于回文串我们改动任意字符(不包含奇数长度的最中间字符)都会使其不再满足回文。要修改后的字典最小，那就尽量从左向右，尽量将字母改小->非a改a，是a的改不了，下一位。当然由于回文串的特性，我们只需要改一半就行(对称)。<font color=red>当所给回文串是奇数长度，修改中间字符后仍是回文串，不满足题意！！！！！！</font>

```python
class Solution:
    def breakPalindrome(self, palindrome: str) -> str:
        if len(palindrome) == 1:
            return ""
        # 从左到右遍历，找到第一个不是a的字符，将其改为a
        for i in range(len(palindrome) // 2):
            if palindrome[i] != 'a':
                return palindrome[:i] + 'a' + palindrome[i + 1:]
        # 如果全是a，将最后一个字符改为b
        return palindrome[:-1] + 'b'
```

看了下官方题解，说这就叫贪心，我都没往贪心那儿想。emmm……难道说贪心是人的本能？不要啊大锅，俺想做个好人！！！<br><img src="./assets/image-20250305085721817.gif" alt="image-20250305085721817" style="zoom:66%;" />







##### 3.6

[2588. 统计美丽子数组数目](https://leetcode.cn/problems/count-the-number-of-beautiful-subarrays)

今天的题，怎么说呢，看懂了就会发现，这不是消消乐嘛！所谓选两个数减去${2^k}$,其实就是$k+1$位上两个 1 抵消了，通过异或操作很容易满足的。所谓美丽子数组，其实子数组内所有元素各个二进制位上的 1 两两一抵消，最后结果为 0 (所有元素异或即可)。<br><img src="./assets/image-20250306102003829.png" alt="image-20250306102003829" style="zoom:66%;" />

 就是于是给出以下代码，但是不幸的是，<font color=red>内存超出限制</font>！！！

```python
class Solution:
    def beautifulSubarrays(self, nums: List[int]) -> int:
        res = 0
        dp = [[0]*len(nums) for _ in range(len(nums))]
        for i in range(len(nums)):
            for j in range(i, len(nums)):
                if j ==i:
                    dp[i][j] = nums[j]
                else:
                    dp[i][j] = dp[i][j-1] ^ nums[j]
                res += 1 if dp[i][j] ==0 else 0
        return res
```

没事内存大了应该是 dp 数组的原因，稍微想一想，异或一个数两次等于没异或，而且异或运算具有交换性，于是只需要一个数组记录上一轮。后续只需要再异或一遍某个元素，消除影响即可。但第一轮需要手动处理一遍，嗯……代码感觉很不优雅！！！并且，<font color=red>这代码它超时了！！！</font>

```python
class Solution:
    def beautifulSubarrays(self, nums: List[int]) -> int:
        res = 0
        # dp[j] 表示上一轮次到j的异或值
        dp = [0] * len(nums)
        
        dp[0] = nums[0]
        res += 1 if dp[0] == 0 else 0

        for i in range(1,len(nums)): # 第一轮处理
            dp[i] = dp[i-1] ^ nums[i]
            res += 1 if dp[i] == 0 else 0

        for i in range(1,len(nums)):
            for j in range(i, len(nums)):
               # 取消上一轮的首位异或值
               dp[j] = dp[j] ^ nums[i-1]
               res += 1 if dp[j] == 0 else 0
        return res
```

能想到撤销前面一个的影响，为啥就想不到撤销前面一群呢？！我真傻,真的，我单想到可以…没想到…

```python
from collections import defaultdict
from typing import List

class Solution:
    def beautifulSubarrays(self, nums: List[int]) -> int:
        res = 0
        prefix_count = defaultdict(int)
        # 初始认为异或结果为0的个数为1,这样后续异或结果为0的时候，可以直接加上这个个数
        prefix_count[0] = 1 
        curr_xor = 0
        for num in nums:
            curr_xor ^=num
            #curr_xor异或一些数结果仍为curr_xor，说明这些数异或结果为0(即得到一个美丽子数组)
            res += prefix_count[curr_xor]
            prefix_count[curr_xor] += 1
        return res
```

吐了，昨晚睡觉之前没忍住看了一眼今天的每日一题，稍微一看，我去这不稳了嘛。emmm……结果确实稳了，躺的稳稳地！！！也算是集齐了力扣常见提交结果了！！！<br><img src="./assets/image-20250306101306954.png" alt="image-20250306101306954" style="zoom:67%;" /><br><img src="./assets/image-20250306101057946.png" alt="image-20250306101057946" style="zoom:75%;" />









##### 3.7

[2597. 美丽子集的数目](https://leetcode.cn/problems/the-number-of-beautiful-subsets)

本来想的是，使用一个字典存储各个数字出现的频率，然后使用排列组合的方式计算，但是实际编写代码的时候发现不太好处理：我似乎需要判断i-k,i+k存在与否，并依次计算组合方式，关键是如何保证不重复计算(当然实际上后面看到官方解法得到启发，排序，然后每次只处理前面的，后面的不管，但是这样计算排列组合也是很麻烦的，依旧存在重复，a 和 b 的组合方式，会影响到 b 和 c 的选取组合)？花了很长时间，最后废弃了！！！<br><img src="./assets/image-20250307105629511.png" alt="image-20250307105629511" style="zoom:80%;" />

但是经过排列组合的分析，我有一个新的想法。对于选择问题而言，无非就是选和不选两个选择，使用 dfs + 回溯还是很好解决的，唯一需要注意的是数字可以是重复的，处理逻辑上可能就需要发生一些变化,最终成品代码如下:

```python
from collections import defaultdict
from typing import List

class Solution:
    def beautifulSubsets(self, nums: List[int], k: int) -> int:
        self.res = 0
        self.nums = nums
        self.k = k
        self.len = len(nums)
        visited = defaultdict(bool) # 默认为False
        self.dfs(0, visited)
        # 去掉空集
        return self.res - 1

    def dfs(self, start: int, visited: defaultdict) -> None:
        if start == self.len:
            self.res += 1
            return
            
        # 不选择当前数字
        self.dfs(start + 1, visited)
        
        # 判断是否可以选择当前数字
        curr = self.nums[start]
        if not visited[curr - self.k] and not visited[curr + self.k]:
            # 判断以前是否选择过相同的数字
            if not visited[curr]: 
                # 选择当前数字
                visited[curr] = True
                self.dfs(start + 1, visited)
                # 回溯，撤销选择()
                visited[curr] = False
            else:
                # 选择当前数字
                self.dfs(start + 1, visited)
```

> 在回溯的时候，脑子没反应过来，就一直觉得后面没有执行代码，回不回溯没啥影响。但是 python 参数传递的是引用，虽然影响不了后面，但是回影响前面(在此次选择之前的选择)，:expressionless:。

依照习俗，感受一下来自算法之神——力扣官方的威压，第一个解法回溯没问题，第二个解法…oh…tomato，啊不是，动态规划。**考虑将每个数根据模 k 的结果进行分组，如果模 k 不同余，那么它们一定不相差 k**。其实大致解释一下官解思路，就是对元素计数之后，按照 k 取模进行分组，这样就可以将相差 k 的若干倍的元素分到一组，此时相差 k 的元素必然在同一组，此时我们再对分组进行排序，那么相差 k 的元素必然在分组中相邻，此时我们只需要对相邻元素进行分析。而最后结果就是所有分组取法的乘积。

```python
from collections import defaultdict
from typing import List

class Solution:
    def beautifulSubsets(self, nums: List[int], k: int) -> int:
        group = defaultdict(dict)
        for num in nums:
            # 将元素计数，按照num % k分组
            # 每个分组中元素之间的差值为k的倍数
            group[num % k][num] = group[num % k].get(num, 0) + 1

        ans = 1

        for g in group.values():
            sorted_g = sorted(g.keys()) # 组内按照元素大小排序
            l = len(sorted_g)
            # i表示元素在sorted_g的位置，j表示是否选取，f[i][j]当前方案数
            f = [[0]*2 for _ in range(l)]
            f[0][0] = 1
            f[0][1] = (1 << g[sorted_g[0]]) - 1
            for i in range(1,l):
                # 当前元素不选取，前面一个元素随意选取
                f[i][0] = f[i-1][0] + f[i-1][1]
                # 首先我们需要知道，当前元素存在 g[sorted_g[i]] 个
                # 至少选一个就是2 ** g[sorted_g[i]] - 1种选择
                if sorted_g[i] - sorted_g[i-1] == k:
                    # 此时，前一个元素不能选
                    f[i][1] = f[i-1][0] * ((1 << g[sorted_g[i]]) - 1)
                else:
                    # 前面一个元素随意选取
                    f[i][1] = (f[i-1][0] + f[i-1][1])* ((1 << g[sorted_g[i]]) - 1)
            ans *= f[l-1][0] + f[l-1][1] # 选取和不选取的方案数相加
        return ans - 1 # 不选取空集
```

> 在Python中，位移运算符 `<<` 的优先级低于减法运算符 `-`。







##### 3.8

[2234. 花园的最大总美丽值](https://leetcode.cn/problems/maximum-total-beauty-of-the-gardens)

~~摆烂一天，待补！！！~~首先找最接近种满的花园把它种满，找花数最少的花园以提高最小值，这肯定是没问题的。但是最初的时候我尝试贪心，我比较把花园种满和提高最小值这两种方式的性价比，我选取最高的那种方式，最后直至无法种植。但是这种方式存在很明显的误区，就是我可能导致后一种方式无法执行，例如原本我可以两次提高最小值，但是由于前一次选择把花园种满的性价比高于提高一次最小值，于是选择种满花园，但是结果导致后面可种植花数不够，但是可能实际两次提高最小值要优于一次种满花园。其实本质上就是性价的代价比难以判断，对于种满花园而言，其代价并不止当前种满改花园所需花数，还包括后面因为该选择浪费的花数，提升最小值的方式同理。

实际上，上面的思路困住我许久…

当然最后还是参照官解思路，其实很简单，种满花园的时候找花数最多的，我们遍历种满若干花园的方式，然后尽可能提高最小值，最后取最大的结果。对于可以填满所有花园的情况，感觉可以直接返回,没必要继续判断:

```python
from typing import List

class Solution:
    def maximumBeauty(self, flowers: List[int], newFlowers: int, target: int, full: int, partial: int) -> int:
        n = len(flowers)
        # 降序排列各个花园的美丽值，超过target的部分全部变为target
        flowers = sorted([min(x, target) for x in flowers], reverse=True)
        total = sum(flowers)
        ans = 0

        # 如果newFlowers足够填满所有花园，那么就初始化为full * n
        # 其实这里是对下面的循环进行了补充,下面循环其实并没有考虑到newFlowers填满所有n个花园的情况(i<n)
        if target * n - total <= newFlowers:
            # ans = full * n
            return max(full * n,full * (n - 1) + partial * (target - 1)) if target * n-total != 0 else full * n
        
        pre = ptr = 0
        for i in range(n):
            if i != 0:
                pre += flowers[i - 1]
            if flowers[i] == target:
                continue
            # 将前面i个花园([0,i-1])中种满花朵，剩余的花朵数为rest
            rest = newFlowers - (target * i - pre)
            if rest < 0:
                break
            # 不妨记ptr为j
            # 找到最小的j(其实就是找最大的flowers[j]，从而使最小值尽可能大)，使得flowers[j] * (n - j) - total <= rest
            while not (ptr >= i and flowers[ptr] * (n - ptr) - total <= rest):
                total -= flowers[ptr]
                ptr += 1
            
            rest -= flowers[ptr] * (n - ptr) - total
            #  尝试将剩余的rest分配给flowers[ptr]，flowers[ptr + 1]...flowers[i]
            #  同时要避免超过target
            ans = max(ans, full * i + partial * (min(flowers[ptr] + rest // (n - ptr), target - 1)))
    
        return ans
```

其实我感觉，我似乎对遍历这种方式存在“偏见”，对于遍历这种方式，我无法通过一种很确切的方式取解释它，它对于我而言似乎只有最后的执行结果是确定的(不知道该如何描述这种感觉)。因此对于一个问题，我总是尝试去贪心、去动态规划、去使用数学方法等等，而对应遍历、模拟这种最好理解的方式最容易忽视。







##### 3.9

[2070. 每一个查询的最大美丽值](https://leetcode.cn/problems/most-beautiful-item-for-each-query)

比昨天的题要简单些，无非就是排序，就前面最大美丽值，然后查找。写完这道题，关于二分查找这部分的理解加深了很多，发现之前学数据结构的时候，自己写的一些代码实现存在很多的问题(主要还是死循环问题)。给出如下代码:

```python
from typing import List

class Solution:
    def maximumBeauty(self, items: List[List[int]], queries: List[int]) -> List[int]:
        # 从小到大排序
        items = sorted(items, key=lambda x: x[0])

        # 计算前缀
        n = len(items)
        max_beauty = 0
        max_list = [0] * n
        for i in range(n):
            max_beauty = max(max_beauty, items[i][1])
            max_list[i] = max_beauty
        

        # 二分查找，返回最后一个小于等于target的位置
        def binary_search(left, right, target):
            while left < right:
                mid = left + (right - left) // 2
                if items[mid][0] <= target: 
                    left = mid + 1
                else:
                    right = mid
            return left  if items[left][0] <= target else left - 1

        # 二分查找获取结果
        ans = []
        left = 0
        right = n - 1
        pre_ans = -1
        for i in range(len(queries)):
            if pre_ans == -1: # 无法使用前一次的结果
                idx = binary_search(left, right, queries[i])
            else:
                # 感觉等于的可能性不大，就不单独处理了
                if queries[i] <= queries[i-1]:
                    idx = binary_search(left, pre_ans, queries[i])
                else:
                    idx = binary_search(pre_ans, right, queries[i])
                
            # 保存前一次的位置和结果
            if idx >= 0:
                pre_ans = idx
                ans.append(max_list[idx])
            else:
                pre_ans = -1
                ans.append(0)

        return ans
```

实际上还是有点不服气，我在二分查找的时候想到，是否可以根据前一次的结果缩短下一次查找的区间，我也确实这样做了，测试结果也是过来，但是实际时间消耗比不优化的时候明显增大了，开摆！！！<br><img src="./assets/image-20250309143205619.png" alt="image-20250309143205619" style="zoom:80%;" />







##### 3.10

[2269. 找到一个数字的 K 美丽值](https://leetcode.cn/problems/find-the-k-beauty-of-a-number)

简简单单一道滑动窗口题,然后就是简单的获取一个整数的高位和低位的问题，结果如下:

```python
class Solution:
    def divisorSubstrings(self, num: int, k: int) -> int:
        n = len(str(num))
        num_bak = num
        if n < k:
            return 0
        ans = 0
        s = 0 # 记录当前的数字
        low = 0
        for high in range(n):
            s = s * 10 + num // (10 ** (n - high - 1)) # 设置s的低位
            if high >= k - 1:
                s %= 10 ** k # 删除s高位
                if  s!= 0 and num_bak % s == 0:
                    ans += 1
                low += 1
            num %= 10 ** (n - high - 1) # 删除num高位
            
        
        return ans
    
```

看了一下官方的题解，大差不差，枚举然后截取转整形。
