#### 2025



**将零星的星火沉淀为银河，是文字赋予思考的温柔仪式————Deepseek**



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

