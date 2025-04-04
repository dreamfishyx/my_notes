##### 基本数据类型

1. 布尔类型：`boolean`，布尔类型

   ```typescript
   let isDone: boolean = false;
   isDone = true;
   ```

2. 数字类型：`number`

   ```typescript
   let a1: number = 10 // 十进制
   let a2: number = 0b1010  // 二进制 0b
   let a3: number = 0o12 // 八进制 0o
   let a4: number = 0xa // 十六进制 0x
   ```

3. 字符串类型：`string`

   ```typescript
   let name:string = 'tom'
   name = 'jack'
   let age:number = 12
   
   // 字符串拼接
   const info = `My name is ${name}, I am ${age} years old!`
   ```

4. `undefined` 和 `null`：`TypeScript `里，`undefined` 和 `null` 两者各自有自己的类型分别叫做 `undefined` 和 `null`。 它们的本身的类型用处不是很大，但是二者均可以作为其他类型的子类型，即可以将二者赋值给其他类型的变量：

   ```typescript
   let u: undefined = undefined
   let n: null = null
   
   let str:string = null
   let str:string = undefined
   ```

5. 数组：`TypeScript `像 `JavaScript `一样可以操作数组元素。 有两种方式可以定义数组。 第一种，可以在元素类型后面接上`[]`，表示由此类型元素组成的一个数组。也可以使用数组泛型，`Array<元素类型>`。

   ```typescript
   let list1: number[] = [1, 2, 3]
   const list2: number[] = [4, 5, 6]
   let list3: Array<number> = [1, 2, 3]
   ```

6. `tuple`:元组类型允许表示一个已知元素数量和类型的数组，各元素的类型不必相同。 你可以定义一对值分别为 `string` 和 `number` 类型的元组。不妨联想python中元组和类实例的关系，似乎就容易理解元组的用途。

   ```typescript
   let t1: [string, number]
   t1 = ['hello', 10] // OK
   t1 = [10, 'hello'] // Error
   ```

7. `enum` ：枚举类型是对 `JavaScript `标准数据类型的一个补充。 使用枚举类型可以为一组数值赋予友好的名字。枚举数值默认从`0`开始依次递增,你可以根据特定的名称得到对应的枚举数值。当然也可以指定索引从`1`开始或者手动赋值。

   ```typescript
   enum Color {
       Red,
       Green,
       Blue
   }
   let myColor: Color = Color.Green  // 0
   console.log(myColor, Color.Red, Color.Blue)
   ```

   ```typescript
   enum color{
       red=1,
       green,
       blue=5
   }
   alert(`color green: ${color.green}`); // 2
   alert(`color blue: ${color.blue}`); // 5
   ```

   此外，当我们知道一个枚举类型的值时，我们还可以通过值得到其对应的名字：

   ```typescript
   enum Color {Red = 1, Green, Blue}
   let colorName: string = Color[2]
   
   console.log(colorName)  // 'Green'
   ```

   非number类型时，需要为每个枚举元素手动赋值：

   ```typescript
   enum color{
       red='r',
       green='g',
       blue='b'
   }
   alert(`color green: ${color.green}`);  // g
   ```

8. 有时候，我们会想要为那些在编程阶段还不清楚类型的变量指定一个类型。 这些值可能来自于动态的内容，比如来自用户输入或第三方代码库。 这种情况下，我们不希望类型检查器对这些值进行检查而是直接让它们通过编译阶段的检查。 那么我们可以使用 `any` 类型来标记这些变量。但是使用`any`基本上就意味着放弃`ts`的类型特性，与`js`无异,必要时可以实义泛型。

   ```typescript
   let notSure: any = 4
   notSure = 'maybe a string'
   notSure = false // 也可以是个 boolean
   ```

   在对现有代码进行改写的时候，`any` 类型是十分有用的，它允许你在编译时可选择地包含或移除类型检查。并且当你只知道一部分数据的类型时，`any` 类型也是有用的。 比如，你有一个数组，它包含了不同的类型的数据：

   ```typescript
   let list: any[] = [1, true, 'free']
   list[1] = 100
   ```

9. 某种程度上来说，`void` 类型像是与 `any` 类型相反，它表示没有任何类型。 当一个函数没有返回值时，你通常会见到其返回值类型是 `void`：

   ```typescript
   function fn(): void {
       console.log('fn()')
       // return undefined
       // return null
       // return 1 (error)
   }
   ```

   声明一个 `void` 类型的变量没有什么大用，因为你只能为它赋予 `undefined` 和 `null`：

   ```typescript
   let unusable: void = undefined
   ```

10. `object`类型：`object` 表示非原始类型，也就是除 `number`，`string`，`boolean`之外的类型。使用 `object` 类型，就可以更好的表示像 `Object.create` 这样的 `API`。例如：

    ```typescript
    function fn2(obj:object):object {
        console.log('fn2()', obj)
        return {}
        // return undefined
        // return null
    }
    console.log(fn2(new String('abc')))
    // console.log(fn2('abc') // error
    console.log(fn2(String))
    ```

11. 联合数据类型：联合类型（Union Types）表示取值可以为多种类型中的一种。`toString() `方法返回一个表示该对象的字符串。

    ```typescript
    function toString2(x: number | string) : string {
        return x.toString()
    }
    ```

12. 类型断言：通过类型断言这种方式可以告诉编译器，“相信我，我知道自己在干什么”。 类型断言<font color=red>好比其它语言里的类型转换</font>，但是不进行特殊的数据检查和解构。 它没有运行时的影响，只是在编译阶段起作用。类型断言有两种形式。 其一是`<Type> value`语法, 另一个为 `value as Type` 语法。

    ```typescript
    function getLength(x: number | string) {
        if ((<string>x).length) {
            return (x as string).length
        } else {
            return x.toString().length
        }
    }
    console.log(getLength('abcd'), getLength(1234))
    ```

13. 类型推断: TS会在没有明确的指定类型的时候推测出一个类型。 定义变量时赋值了, 推断为对应的类型。 定义变量时没有赋值, 推断为`any`类型。

    ```typescript
    // 定义变量时赋值了, 推断为对应的类型
    let b9 = 123 // number
    // b9 = 'abc' // error
    
    // 定义变量时没有赋值, 推断为any类型
    let b10  // any类型
    b10 = 123
    b10 = 'abc'
    ```





----

##### 接口

1. `TypeScript `的核心原则之一是对值所具有的结构进行类型检查。我们使用接口（Interfaces）来定义对象的类型。<font color=red>接口是对象的状态(属性)和行为(方法)的抽象(描述)</font>。

2. 可选属性：带有可选属性的接口与普通的接口定义差不多，只是在可选属性名字定义的后面加一个 `?` 符号。可选属性的好处之一是可以对可能存在的属性进行预定义，好处之二是可以捕获引用了不存在的属性时的错误。

3. 只读属性：一些对象属性只能在对象刚刚创建的时候修改其值。 你可以在属性名前用 `readonly` 来指定只读属性。一旦赋值后再也不能被改变了。

4. 下面不妨定义一个接口：`id`为只读属性，`sex`为可选属性。

   ```typescript
   interface IPerson {
       readonly id: number
       name: string
       age: number
       sex?: string
   }
   
   const person2: IPerson = {
       id: 2,
       name: 'tom',
       age: 20,
       // sex: '男' // 可以没有
   }
   
   person2.id = 2 // error
   ```

5. 最简单判断该用 `readonly` 还是 `const` 的方法是看要把它做为变量使用还是做为一个属性。 做为变量使用的话用 `const`，若做为属性则使用 `readonly`。

6. 函数类型：为了使用接口表示函数类型，我们需要给<font color=red>接口定义一个调用签名。它就像是一个只有参数列表和返回值类型的函数定义,参数列表里的每个参数都需要名字和类型</font>。当一个函数实现接口类型时，函数的参数类型就可以省略。此处也可以通过箭头函数快速实现接口。

   ```typescript
   // 接口可以描述函数类型(参数的类型与返回的类型)
   interface SearchFunc {
       (source: string, subString: string): boolean
   }
   
   // 实现接口
   const mySearch: SearchFunc = function (source: string, sub: string): boolean {
       return source.search(sub) > -1
   }
   
   // 省略参数类型(lamada表达式/箭头函数)
   const mySearch: SearchFunc =  (source, sub) => source.search(sub) > -1
   ```
   
7. 接口可以视为类的类型，一个类可以实现多个接口。

   ```typescript
   interface Alarm {
       alert(): any;
   }
   
   interface Light {
       lightOn(): void;
       lightOff(): void;
   }
   
   class Car2 implements Alarm, Light {
       alert() {
           console.log('Car alert');
       }
       lightOn() {
           console.log('Car light on');
       }
       lightOff() {
           console.log('Car light off');
       }
   }
   ```

8. 和类一样，接口也可以相互继承。 这让我们能够从一个接口里复制成员到另一个接口里，可以更灵活地将接口分割到可重用的模块里。

   ```typescript
   interface LightableAlarm extends Alarm, Light {}
   ```

   



----

##### 类

1. 类：参考java和python。

   ```typescript
   class Greeter {
       // 声明属性
       message: string
   
       // 构造方法
       constructor (message: string) {
           this.message = message
       }
   
       // 一般方法
       greet (): string {
           return 'Hello ' + this.message
       }
   }
   
   // 创建类的实例
   alert((new Greeter('world')).greet())
   ```

2. 继承、多态：参考java、python。

   ```typescript
   class Animal {
       name: string
   
       constructor (name: string) {
           this.name = name
       }
   
       run (distance: number=0) {
           console.log(`${this.name} run ${distance}m`)
       }
   
   }
   
   class Snake extends Animal {
       constructor (name: string) {
           // 调用父类型构造方法
           super(name)
       }
   
       // 重写父类型的方法
       run (distance: number=5) {
           console.log('sliding...')
           super.run(distance)
       }
   } 
   // 父类型引用指向子类型的实例 ==> 多态
   const tom: Animal = new Snake('ho22')
   tom.run()
   
   ```

3. 属性修饰符：`private、protected、public`。其中`protected` 修饰符与 `private` 修饰符的行为很相似，但有一点不同，`protected`成员在派生类中仍然可以访问。<font color=red>(默认为`plublic`)</font>

   ```typescript
   class A{
       private name: string = '?';
       public age: number;
       protected sex: string = "武装直升机";
   
       constructor(name:string,age:number,sex:string){
           this.name = name;
           this.age = age;
           this.sex = sex;
       }
   }
   
   class B extends A{
       log(){
           console.log(this.sex); //success
           console.log(this.name); //error
       }
   }
   ```

4. 可以使用 `readonly` 关键字将属性设置为只读的。 只读属性必须在声明时或构造函数里被初始化(<font color=red>也就是说，是可以在构造函数中对只读属性进行修改的！！！</font>)。

   ```typescript
   class Person {
       readonly name: string = 'abc'
       constructor(name: string) {
           this.name = name
       }
   }
   ```

5. 参数属性：我们再构造函数中使用`readonly`修饰参数，那么该参数可以称之为参数属性，此时类中相当于存在一个`readonly`修饰的同名属性。同理，`private、protected、public`也是一样的。

   ```typescript
   class Person{
       constructor(public name: string, readonly age: number,private id: number) {}
   }
   const person = new Person('John', 30, 1);
   ```

6. <font color=red>类似于`python`，`js`和`ts`中也是支持默认参数的。</font>

   ```typescript
   let plus = (a: number, b=5) => a + b;
   console.log(plus(3)); 
   ```

7. 存取器： 

   ```typescript
   class Person{
       constructor(private name: string){
           this.name = name;
       }
   
       get Name(){
           return this.name;
       }
   
       set Name(name: string){
           this.name = name;
       }
   }
   
   let person = new Person('John');
   console.log(person.Name);
   person.Name = 'Doe';
   ```

8. 静态属性：不同于`java`，`ts`中的静态属性、静态方法无法通过实例访问，只能通过类本身访问。此外构造函数不能使用`static`修饰。

   ```typescript
   // 每个类中都存在一个name属性记录类名
   class Person{  
       static _name: string = 'No name';
   
       static log(){
           console.log('This is a Person class');
       }
   }
   console.log(Person.name);
   console.log(Person._name);
   Person.log();
   ```

9. 抽象类做为其它派生类的基类使用。 它们不能被实例化。不同于接口，抽象类可以包含成员的实现细节。 `abstract` 关键字是用于定义抽象类和在抽象类内部定义抽象方法。抽象类可以存在抽象方法和实例方法。实际上抽象类中也可以存在抽象属性，但是没有啥用！！！

   ```typescript
   abstract class Animal {
       //抽象方法
       abstract eat(thing: string): void;
       //实例方法
       move(distance: number = 0) {
           console.log(`Animal moved ${distance}m.`);
       }
   }
   
   class Dog extends Animal {
       eat(thing: string): void {
           console.log(`Dog eat ${thing}`);
       }
   }
   ```





----

##### 函数

1. 函数的使用方式基本同`js`，但是可以为函数设置参数和返回值类型。

   ```typescript
   // 命名函数
   function add(x: number, y: number): number {
       return x + y
   }
   
   // 匿名函数
   let myAdd = function(x: number, y: number): number { 
       return x + y
   }
   ```

2. 实际上函数的完整形式为：其中`(x: number, y: number) => number`可以认为是这个函数的类型。

   ```typescript
   let myAdd2: (x: number, y: number) => number = 
       function(x: number, y: number): number {
           return x + y
       }
   ```

3. 可选参数和默认参数:

   ```typescript
   let f = (firstName?: string,lastName:string='fish') => {
       if (firstName) {
           return firstName;
       } else {
           return lastName;
       }
   }
   console.log(f('dream')); 
   console.log(f()); 
   ```

4. 剩余参数：同时操作多个参数，或者你并不知道会有多少参数传递进来。 在 `JavaScript `里，你可以使用 `arguments` 来访问所有传入的参数。在 `TypeScript `里，你可以把所有参数收集到一个变量里：剩余参数会被当做个数不限的可选参数。 可以一个都没有，同样也可以有任意个。 编译器创建参数数组，名字是你在省略号（ `...`）后面给定的名字，你可以在函数体内使用这个数组。

   ```typescript
   function info(x: string, ...args: string[]) {
       console.log(x, args)
   }
   info('abc', 'c', 'b', 'a')
   ```

5. <font color=red>可以在箭头函数中使用:默认参数、剩余参数、可选参数！！！</font>感觉和python的参数类型差不多。

   ```typescript
   let f = (a: string, b: string = 'b', ...args: string[]) => {
       console.log(a);
       console.log(b);
       console.log(args);
   }
   
   ```

6. 函数重载：函数名相同, 而形参不同的多个函数

   ```typescript
   /* 
   我们有一个add函数，它可以接收2个string类型的参数进行拼接，也可以接收2个number类型的参数进行相加 
   */
   
   // 重载函数声明
   function add (x: string, y: string): string
   function add (x: number, y: number): number
   
   // 定义函数实现
   function add(x: string | number, y: string | number): string | number {
       if (typeof x === 'string' && typeof y === 'string') {
           return x + y
       } else if (typeof x === 'number' && typeof y === 'number') {
           return x + y
       }
   }
   
   console.log(add(1, 2))
   console.log(add('a', 'b'))
   // console.log(add(1, 'a')) // error
   ```





---

##### 泛型

1.  泛型指在定义函数、接口或类的时候，不预先指定具体的类型，而在使用的时候再指定具体类型的一种特性。

2. 其中`<T>`可以认为是定义泛型，后就可以将`T`作为一种类型使用。

   ```typescript
   function createArray<T> (value: T, count: number) {
       const arr: Array<T> = []
       for (let index = 0; index < count; index++) {
           arr.push(value)
       }
       return arr
   }
   
   let a = createArray<number>(1, 3)
   let b = createArray('x', 3) // 类型推断
   ```

3. 一个函数可以定义多个泛型参数。

   ```typescript
   function swap <K, V> (a: K, b: V): [K, V] {
       return [a, b]
   }
   const result = swap<string, number>('abc', 123)
   ```

4. 泛型接口：例如下面定义一个泛型接口，存储某个类型的数据。

   ```typescript
   interface IbaseCRUD<T> {
       data: T[]
       add: (t: T) => void
       getById: (id: number) => T
   }
   
   class User {
       id?: number;
       name: string;
       age: number;
   
       constructor(name: string, age: number) {
           this.name = name
           this.age = age
       }
   }
   
   class UserCRUD implements IbaseCRUD<User> {
       data: User[] = []
   
       add(user: User): void {
           //...展开运算符：将一个元组或者对象转为用逗号分隔的参数序列，类似于python中的*args和**kwargs
           user = { ...user, id: Date.now() }
           this.data.push(user)
           console.log('保存user', user.id)
       }
   
       getById(id: number): User {
           // tsconfig.json中的static设置为false，不然报错
           return this.data.find(item => item.id === id)
       }
   }
   
   const userCRUD = new UserCRUD()
   userCRUD.add(new User('tom', 12))
   userCRUD.add(new User('tom2', 13))
   ```

5. 泛型类：在定义类时, 为类中的属性或方法定义泛型类型 在创建类的实例时, 再指定特定的泛型类型。

   ```typescript
   class GenericNumber<T> {
       zeroValue: T
       add: (x: T, y: T) => T
   }
   
   let myGenericNumber = new GenericNumber<number>()
   myGenericNumber.zeroValue = 0
   myGenericNumber.add = function(x, y) {
       return x + y 
   }
   
   let myGenericString = new GenericNumber<string>()
   myGenericString.zeroValue = 'abc'
   myGenericString.add = function(x, y) { 
       return x + y
   }
   ```

6. 实际上，`js`、`python`这类弱语言有许多有趣的使用方式,而`ts`由于是`js`的超集，自然也可以：

   ```js
   class person{
       add(){
           console.log('add function');
       }
   }
   let p = new person();
   p.add = function(){
       console.log('a new add function');
   }
   ```

7. 泛型约束：类似于`java`,`ts`中也存在泛型约束：可以使用类或者接口(仍使用`extends`而非`implements`)对泛型进行约束。

   ```typescript
   // 泛型T必需为SomeClass或其子类
   function myFunction<T extends SomeClass>(arg: T): void {
       // 函数体
   }
   ```

   ```typescript
   interface Lengthwise {
       length: number;
   }
   
   // 指定泛型约束
   function fn2 <T extends Lengthwise>(x: T): void {
       console.log(x.length)
   }
   ```





----

##### 声明文件

1. 当使用第三方库时，我们需要引用它的声明文件，才能获得对应的代码补全、接口提示等功能。假如我们想使用第三方库 `jQuery`，一种常见的方式是在 `html `中通过 `<script>` 标签引入 `jQuery`，然后就可以使用全局变量 `$` 或 `jQuery` 了。但是在 `ts `中，编译器并不知道 `$ `或 `jQuery `是什么东西。
2. 当然我们可以使用`declare var jQuery: (selector: string) => any`手动声明。我们可以 把声明语句放到一个单独的文件（`jQuery.d.ts`）中, ts会自动解析到项目中所有声明文件。文件后缀为`.d.ts`即可。
3. 实际上我们可以通过` npm install @types/jquery --save-dev`安装`jquery`的声明文件。
4. 有的第三库在下载时就会自动下载对应的声明文件库(比如: `webpack`),有的可能需要单独下载(比如`jQuery`、`react`)
5. [查询](https://www.npmjs.com/package/package)



---

##### 内置类型

1. `JavaScript `中有很多内置对象，它们可以直接在 `TypeScript `中当做定义好了的类型。内置对象是指根据标准在全局作用域（`Global`）上存在的对象。这里的标准是指 `ECMAScript `和其他环境（比如 DOM）的标准。

2. `ECMAScript `的内置对象:`Boolean、Number、String、Date、RegExp、Error`。

   ```typescript
   let b: Boolean = new Boolean(1)
   let n: Number = new Number(true)
   let s: String = new String('abc')
   let d: Date = new Date()
   let r: RegExp = /^1/
   let e: Error = new Error('error message')
   b = true
   // let bb: boolean = new Boolean(2)  // error
   ```

3. `BOM `和 `DOM `的内置对象:`Window、Document、HTMLElement、DocumentFragment、Event、NodeList`

   ```typescript
   const div: HTMLElement = document.getElementById('test')
   const divs: NodeList = document.querySelectorAll('div')
   document.addEventListener('click', (event: MouseEvent) => {
     console.dir(event.target)
   })
   const fragment: DocumentFragment = document.createDocumentFragment()
   ```

   





##### 导入和导出

```ts
// 导出类型 (types.ts)
interface Product {
    id: string
    price: number
}
a = 5
export { Product,a }

// 导入类型 (app.ts)
import type { type Product } from './types'

// 同时导入值和类型
import { type Product, a } from './types'
```

