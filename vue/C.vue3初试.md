##### 创建项目

```bash
## 1.创建命令
npm create vue@latest

## 2.具体配置
## 配置项目名称
√ Project name: vue3_test
## 是否添加TypeScript支持
√ Add TypeScript?  Yes
## 是否添加JSX支持
√ Add JSX Support?  No
## 是否添加路由环境
√ Add Vue Router for Single Page Application development?  No
## 是否添加pinia环境
√ Add Pinia for state management?  No
## 是否添加单元测试
√ Add Vitest for Unit Testing?  No
## 是否添加端到端测试方案
√ Add an End-to-End Testing Solution? » No
## 是否添加ESLint语法检查
√ Add ESLint for code quality?  Yes
## 是否添加Prettiert代码格式化
√ Add Prettier for code formatting?  No
```

> 1.   `index.html`放在了`public`的外面
> 2.   vite以`index.html`作为入口，不再使用`main.ts`作为入口,vite 解析`<script type="module" src="/src/main.js"></script>`指向的 js 。
> 3.   对于vite构建工具来说，配置文件是`vite.config.ts`，相当于webpack当中的`vue.config.js`。如果需要配置代理的话，需要在`vite.config.ts`中配置。至于如何配置，参考[vite官网](https://cn.vitejs.dev/config/server-options.html)。

```bash
# 安装依赖
npm i 
```

