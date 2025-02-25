#### 2025

##### 2.25

[轮转数组](https://leetcode.cn/problems/rotate-array/)

> - 考虑特殊情况，K大于arr.length时，需要忽略完整圈数
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







