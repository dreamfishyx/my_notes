待补充(neovim、redis、nginx)

#### lua入门

1. `lua`是一门编程语言，在线运行`lua`的网站:[click](https://wiki.luatos.com/_static/luatos-emulator/lua.html)。

2. 注释：

   ```lua
   -- 单行注释
   
   --[[
   多行注释
   --]]
   ```

3. 创建变量：`lua`中创建变量与`python`类似，但是默认是全局变量(其他文件中也可以使用)。如果要创建局部变量，需要使用`local`关键字

   ```lua
   -- 全局变量
   a = 1  
   
   -- 局部变量
   local b = 1 
   
   -- 输出
   print(a)
   ```

4. `lua`中没有声明的变量的值为`nil`类似于`none`:

   ```lua
   print(c)
   -- nil
   ```

5. `lua`类似于python支持多赋值语句：

   ```lua
   a,b = 1,3
   ```

6. 其他语言中`int`、`bool`、`double`等在`lua`中都作为数值型`number`:

   ```lua
   a = true
   b = 12.5
   c = 0x11  -- 十六进制
   d = 2e10  -- 科学计数法
   e = 2^5   -- 幂运算
   ```

7. `lua`中字符串使用`""`或者`''`包裹。而长字符串使用`[[]]`包裹，其中可以使用转义字符但是会认作普通字符串(`\n`不再换行)。此外`lua`中字符串拼接使用`..`而不是`+`:

   ```lua
   a = "hello "
   b = "lua"
   c = a..b -- 拼接
   
   d = [[
       aaaa
       /n
   bbb
   ]]
   ```

8. 使用`tonumber`、`tostring`实现数值与字符串之间的转换，但是转换失败会返回`nil`。可以使用`#`获取字符串的长度。

   ```lua
   a = "10"
   b = tonumber(a) -- str->number
   c = tostring(b) -- number->str
   len = #a  -- 获取字符串长度
   
   print(b,len)
   ```

9. `lua`函数：

   ```lua
   f = function(a,b,c)
       return a,b --多返回值
   end
   
   local a,b = f(1,2) --c参数为nil
   
   
   function h(a,b,c)
       return nil -- 返回nil
   end
   
   print(h(1,2,3))
   ```

10. `lua`表(类似于数组)：

    ```lua
    a = {
        1,
        "a",
        {},
        function (a,b)
            return a+b
        end,
    }
    
    table.insert(a,'b') --插入
    table.insert(a,2,'c') --在索引2位置插入(索引从1开始)
    local c = table.remove(a,2) --删除并返回
    len = #a --获取元素个数
    print(a[1]) --(索引从1开始)
    ```

11. `lua`表(类似于集合)：

    ```lua
    a = {
        a = 1,
        b = {},
        c = function(a,b)
            return a
        end,
        [",,."] = 123 
        --不符合命名规范需要使用[]包裹
    }
    
    print(a["a"]) --key使用""
    print(a.b) --符合命名规范获取
    print(a[",,."]) --不符合命名规范获取
    ```

12. `_G`是一个全局表，里面保存有全局变量。此外`table`也是一个全局变量，里面保存有一些方法(如"insert")：

    ```lua
    a = 1
    print(_G["a"])
    
    print(_G["table"]["insert"])
    ```

13. `lua`中只有`nil`和`false`为假，`0`是真。

14. `lua`中可以使用比较运算符,但是表示不等于用`~=`。

    ```lua
    a = 12 ~= 13
    ```

15. `lua`中可以使用`and`、`or`、`not`，但只有`not`返回严格的`true`或`false`：

    ```lua
    a = nil --假
    b = 0  --真
    print(a and b) -- nil
    print(a or b) -- 0
    print(not a) -- true
    
    
    print(b > 10 and "yes" or "no")  --短路语句实现三元运算
    ```

16. 判断语句：

    ```lua
    a = 5
    
    if a > 10 then
        print("a > 10")
    elseif a < 5 then
        print("a < 5")
    else
        print("5<=a<10")
    end
    ```

17. 循环(三种)：

    ```lua
    for i=10,1,-1 do
        if i == 5 then break end
        i = 9 --不允许修改循环变量i,会创建新变量
    end
    
    
    a = 10
    repeat
        print(a)
        a = a + 1 -- 不存在a++,a+=1
    until(a >15)
    
    
    b = 10
    while n >0 do 
        if n == 5 then break end
        n = n - 1
    end
    ```

18. 迭代器：

    ```lua
    a = {
        "1",
        "2"
    }
    for key,value in ipairs(a) do
        print(key,value)
    end
    ```

    





