# python实现的简单绘图语言解释器

通过编写一个简单的绘图语言解释器加深对编译原理中词法、语法、语义分析的理解

### 实现语句

- 循环绘图（FOR—DRAW）
- 比例设置（SCALE）
- 角度旋转（ROT）
- 坐标平移（ORIGIN）
- 注释（--或//）
- 颜色设置（COLOR）

### 函数绘图源程序举例

```
-- 函数f(t)=t的图形
origin is (100, 300);	-- 设置原点的偏移量
rot is 0;			-- 设置旋转角度(不旋转)
scale is (1, 1);		-- 设置横坐标和纵坐标的比例
color is RED;		-- 设置颜色为红色
for T from 0 to 200 step 1 draw (t, 0);
				-- 横坐标的轨迹（纵坐标为0）
for T from 0 to 150 step 1 draw (0, -t);
				-- 纵坐标的轨迹（横坐标为0）
for T from 0 to 120 step 1 draw (t, -t);
				-- 函数f(t)=t的轨迹 
```

### 文件说明

Lexer.py：词法分析器

Parser.py：语法分析和语义分析（采用的语法制导的语义分析）

utils.py：辅助类、函数

test.txt, test2.txt：测试文本，前者是基本测试，后者加入了颜色设置语句

### 运行结果示例

![img](https://res.cloudinary.com/du3fbbzfy/image/upload/v1545461745/Interpreter/TIM%E6%88%AA%E5%9B%BE20181222145425.png)

