##### 创建vue3项目

1. 创建项目的方式基本与之前一致，但是需要选中`Typescript`。

2. 除了使用脚手架的方式创建之外，还可以使用`vite`的方式创建项目：`vite `是一个由原生 `ESM `驱动的 `Web `开发构建工具。在开发环境下基于浏览器原生 ES imports 开发，它做到了本地快速开发启动, 在生产环境下基于 `Rollup `打包。

   ```cmd
   npm init vite-app <project-name>
   cd <project-name>
   npm install
   npm run dev
   ```

3. `vue3+Typescript`中`import App from './App.vue' `报错，在根目录新建`env.d.ts`文件，写入以下内容:

   ```ts
   declare module '*.vue' {
     import type { DefineComponent } from 'vue'
     // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/ban-types
     const component: DefineComponent<{}, {}, any>
     export default component
   }
   ```

4. 报错：`volar`是`vetur`的升级版本，提供了更牛叉的功能并有更好的TS支持。卸载`vetur`，安装`volar`插件。但是`vscode`显示此扩展已弃用，请改用`Vue - Official`扩展。

   ```tex
   Module '"d:/vue_vite/src/components/TheWelcome.vue"' has no default export.Vetur(1192)
   ```

   

##### 组合式API

1. 使用`TypeScript`时，`<script>`标签属性如下：

   ```vue
   <script setup lang="ts"></script>
   
   <script lang="ts">
       setup(){
           return {}
       }
   </script>
   ```



##### 全局属性

1. 在`vue3`中取消了`Vue.prototype`，推荐使用`globalProperties`来绑定，即改用`app.config.globalProperties.$xxx`添加全局属性。

2. 此外`vue3`中没有`this`的，所以我们需要用到`vue3`中的`getCurrentInstance()`方法来获取上下文。

3. 在`Vue3`中，`getCurrentInstance`返回的对象包含了组件实例的内部信息。`ctx`和`proxy`是其中的两个属性，它们的作用和适用场景有所不同。

   1. `ctx`是组件实例的上下文对象，包含了组件的内部状态和方法。只能在开发环境下使用。在生产环境中，`ctx`属性会被移除，因此无法访问。
   2. <font color=red>(推荐)</font>`proxy`是组件实例的代理对象，通过代理对象可以访问组件的所有属性和方法。在开发环境和生产环境下都能使用。

4. 不妨演示一下:

   1. 创建插件`src/plugins/addVariable.ts`：

      ```ts
      export default {
          install(app: any, ...options: any[]) {
              // 注册全局函数
              app.config.globalProperties.$addVariable = (key: string, value: any) => {
                  const name = '$' + key
                  app.config.globalProperties[name] = value
              }
          }
      }
      ```

   2. 使用插件`main.ts`：

      ```ts
      import './assets/main.css'
      
      import { createApp } from 'vue'
      import App from './App.vue'
      // 导入插件
      import addVariable from './plugins/addVariable'
      
      // createApp(App).mount('#app')
      const app = createApp(App)
      
      // 使用插件
      app.use(addVariable)
      
      app.mount('#app')
      ```

   3. 在组件中使用`xxx.vue`：由于使用`TypeScript`，存在类型检查，略显麻烦。

      ```vue
      <template>
      <!--vue3不在需要单入口-->
      <input type="text" ref="inputRef" />
      </template>
      
      <script lang="ts">
          import { getCurrentInstance, type ComponentInternalInstance } from 'vue';
          export default {
              setup() {
                  // 获取组件实例
                  const { appContext } = getCurrentInstance() as ComponentInternalInstance
                  const proxy = appContext.config.globalProperties
                  // 通过插件中的函数注册全局属性
                  proxy.$addVariable("myVariable", "myValue");
                  // 访问全局属性
                  console.log(proxy.$myVariable);
              },
      
          };
      </script>
      
      ```




##### 多页面配置

1. `vite.congif.ts`配置多个页面：<font color=red>`vue3`中将`html`文件作为入口文件，需要在`html`文件中引入`js`文件</font>。

   ```js
   import { defineConfig } from 'vite';
   import vue from '@vitejs/plugin-vue';
   import { resolve } from 'path';
   
   export default defineConfig({
       plugins: [vue()],
       build: {
           rollupOptions: {
               input: {
                   main: resolve(__dirname, 'index.html'),  // 主入口
                   home: resolve(__dirname, 'src/pages/home/index.html'),  // home 页面入口
                   about: resolve(__dirname, 'src/pages/about/index.html')  // about 页面入口
               }
           }
       }
   });
   ```

2. 使用 `Vue CLI` 创建项目，你将不会有 `vite.config.js` 文件，而是会有 `vue.config.js` 文件来进行配置。

   

   

