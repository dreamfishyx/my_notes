**将零星的星火沉淀为银河，是文字赋予思考的温柔仪式————Deepseek**



#### 二月

##### 2.25

[189.轮转数组](https://leetcode.cn/problems/rotate-array/)

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

还有一个官方题解，使用堆，说实话自从学了数据结构，这还是第一次遇到堆。堆不支持快速的随机删除与修改操作，因此为了维护堆顶数据的有效性，可以采用懒删除的方法，将维护操作推迟到查询时才进行。<font color=red>也就是在更新的时候插入一个新的食物(同名但是分数不同)，然后再获取最高分数的时候，判断是不是旧的，若是，则删除堆顶元素，重新获取，也是很妙啊</font>！！！

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
        # 不要在for循环的条件中使用变量，因为变量会在循环中改变！！！
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





