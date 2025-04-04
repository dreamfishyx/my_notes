#### Cookie

##### 介绍

1. Cookie 是服务器通过 HTTP 响应头(Set-Cookie)发送到客户端(一般是浏览器)的小型文本数据。浏览器会存储这些数据，并在后续的请求中自动携带它们发送回服务器。

2. 核心作用:

   - 维护用户状态,如登录状态、购物车内容。
   - 记录用户偏好,如语言、主题。
   - 跟踪用户行为,如广告推荐。

3. 核心属性:

   | 属性              | 作用                                                         |
   | ----------------- | ------------------------------------------------------------ |
   | **`Expires`**     | 设置 Cookie 过期时间（GMT 格式），过期后浏览器删除。         |
   | **`Max-Age`**     | 设置 Cookie 有效期（秒数），优先级高于 `Expires`。           |
   | **`Domain`**      | 指定 Cookie 生效的域名（默认当前域名）。                     |
   | **`Path`**        | 指定 Cookie 生效的路径（默认当前路径）。                     |
   | **`Secure`**      | 仅通过 HTTPS 协议传输 Cookie，防止中间人窃取。               |
   | **`HttpOnly`**    | 禁止 JavaScript 通过 `document.cookie` 访问，防范 XSS 攻击。 |
   | **`SameSite`**    | 限制跨站请求携带 Cookie，可选值：`Strict`、`Lax`、`None`（默认 Lax）。 |
   | **`Partitioned`** | （实验性）将第三方 Cookie 分区存储，防止跨站追踪。           |

4. Cookie 的安全性:

   1. 主要风险:

      - XSS 攻击: 攻击者窃取未标记 HttpOnly 的 Cookie。

      - CSRF 攻击: 诱导用户携带 Cookie 发起恶意请求。

      - 中间人窃听:未标记 Secure 的 Cookie 通过 HTTP 明文传输。

   2. 防护措施:

      - 始终为敏感 Cookie 设置 Secure 和 HttpOnly。

      - 使用 SameSite=Strict 或 Lax 防范 CSRF。

      - 避免在 Cookie 中存储敏感数据(如密码)，改用加密 Token。

      - 定期更新 Cookie 值(如 Session ID)以降低泄露风险。

5. 





##### 使用









#### Session









#### Token









### **1. Cookie**

- **定义**：存储在客户端（浏览器）的小型文本文件，由服务器通过`Set-Cookie`响应头设置。
- **作用**：保存用户状态（如登录态、偏好设置），每次请求自动携带。
- **特点**：
  - **客户端存储**：数据在浏览器中，可能被篡改或窃取。
  - **安全性**：需配合`HttpOnly`（防XSS）、`Secure`（仅HTTPS）、`SameSite`（防CSRF）等属性提升安全性。
  - **容量限制**：单个域名通常限制为4KB，数量有限。

------

### **2. Session**

- **定义**：服务器端存储的用户会话数据，客户端仅保存**Session ID**（通常通过Cookie传递）。
- **流程**：
  1. 用户登录后，服务器创建Session并存储（如内存、数据库、Redis）。
  2. 返回Session ID给客户端（通过Cookie）。
  3. 后续请求携带Session ID，服务器据此查找会话数据。
- **特点**：
  - **服务端存储**：数据安全，但需额外存储开销。
  - **依赖Cookie**：Session ID通常存于Cookie，也可通过URL传递（不安全）。
  - **扩展性问题**：分布式系统需共享Session存储（如Redis集群）。

------

### **3. Token（如JWT）**

- **定义**：自包含的令牌（如JWT），包含用户信息、签名和过期时间，由服务器生成。
- **流程**：
  1. 用户登录后，服务器生成Token（如JWT）并返回。
  2. 客户端存储Token（如LocalStorage或Cookie），后续请求通过`Authorization: Bearer <token>`发送。
  3. 服务器验证签名和有效性，无需存储Token。
- **特点**：
  - **无状态**：服务器无需存储会话数据，适合分布式系统。
  - **自包含性**：Token包含用户信息，减少数据库查询。
  - **安全性考量**：需防范XSS（避免LocalStorage）、设置短过期时间、使用HTTPS。

------

### **对比总结**

| 特性           | Cookie               | Session                 | Token（如JWT）            |
| -------------- | -------------------- | ----------------------- | ------------------------- |
| **存储位置**   | 客户端               | 服务器端（Session数据） | 客户端（Token内容自包含） |
| **安全性**     | 较低（依赖属性配置） | 较高（数据在服务器）    | 中（需防泄露和签名验证）  |
| **扩展性**     | 无影响               | 需共享存储（如Redis）   | 天然支持分布式            |
| **跨域支持**   | 受限（SameSite策略） | 依赖Session ID传递方式  | 灵活（通过HTTP头）        |
| **服务器开销** | 低                   | 高（存储所有会话数据）  | 低（仅验证签名）          |

------

### **使用场景**

- **Cookie**：保存非敏感信息（如主题偏好），结合Session使用。
- **Session**：需服务器控制会话、对安全性要求较高的场景。
- **Token**：无状态API（如RESTful）、跨域认证（如OAuth 2.0）、微服务架构。

------

### **常见问题**

- **Cookie被盗**：可通过`HttpOnly`和`Secure`缓解。
- **Session劫持**：使用HTTPS、定期更换Session ID。
- **Token失效**：JWT需结合刷新令牌（Refresh Token）机制。

根据需求选择合适方案：传统Web应用常用`Cookie+Session`，现代分布式系统倾向`Token`（如JWT）















##### 前后端认证机制(补充)

在前后端分离架构（Spring Boot + Vue）中实现认证，通常采用 **Token 机制（如 JWT）** 或 **Session-Cookie 机制**，以下是两种常见方案的具体实现流程：

------

### 一、JWT（JSON Web Token）方案（推荐）

#### 1. 后端（Spring Boot）实现

**(1) 添加依赖**

xml

复制

```
<!-- Spring Security -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
<!-- JWT 库 -->
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt</artifactId>
    <version>0.9.1</version>
</dependency>
```



运行 HTML

**(2) 配置 JWT 工具类**

java

复制

```
public class JwtUtils {
    private static final String SECRET_KEY = "your-secret-key";
    private static final long EXPIRATION = 86400000; // 24小时

    // 生成 Token
    public static String generateToken(String username) {
        return Jwts.builder()
                .setSubject(username)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION))
                .signWith(SignatureAlgorithm.HS256, SECRET_KEY)
                .compact();
    }

    // 验证 Token
    public static String validateToken(String token) {
        return Jwts.parser()
                .setSigningKey(SECRET_KEY)
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }
}
```

**(3) 登录接口生成 Token**

java

复制

```
@PostMapping("/login")
public ResponseEntity<?> login(@RequestBody User user) {
    // 1. 验证用户名密码（此处省略具体校验逻辑）
    if (!"admin".equals(user.getUsername()) || !"123456".equals(user.getPassword())) {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
    }

    // 2. 生成 Token
    String token = JwtUtils.generateToken(user.getUsername());
    return ResponseEntity.ok().body(Map.of("token", token));
}
```

**(4) 配置 Spring Security 过滤器链**

java

复制

```
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable()
            .authorizeRequests()
            .antMatchers("/login").permitAll() // 放行登录接口
            .anyRequest().authenticated() // 其他接口需认证
            .and()
            .addFilterBefore(new JwtFilter(), UsernamePasswordAuthenticationFilter.class);
    }
}

// JWT 过滤器
public class JwtFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain) throws ServletException, IOException {
        String token = request.getHeader("Authorization");
        if (token != null && token.startsWith("Bearer ")) {
            try {
                String username = JwtUtils.validateToken(token.substring(7));
                // 将用户信息存入 SecurityContext
                UsernamePasswordAuthenticationToken auth = new UsernamePasswordAuthenticationToken(username, null, new ArrayList<>());
                SecurityContextHolder.getContext().setAuthentication(auth);
            } catch (Exception e) {
                response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid token");
                return;
            }
        }
        chain.doFilter(request, response);
    }
}
```

------

#### 2. 前端（Vue）实现

**(1) 登录后保存 Token**

javascript

复制

```
// Login.vue
axios.post('/api/login', { username: 'admin', password: '123456' })
  .then(response => {
    const token = response.data.token;
    localStorage.setItem('jwt_token', token); // 存储到 localStorage
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`; // 设置请求头
    router.push('/dashboard'); // 跳转到主页
  });
```

**(2) 请求拦截器自动附加 Token**

javascript

复制

```
// main.js
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('jwt_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});
```

**(3) 路由守卫验证登录状态**

javascript

复制

```
// router.js
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('jwt_token');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // 未登录跳转登录页
  } else {
    next();
  }
});
```

------

### 二、Session-Cookie 方案（传统）

#### 1. 后端（Spring Boot）

**(1) 启用 Session**

java

复制

```
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable()
            .authorizeRequests()
            .antMatchers("/login").permitAll()
            .anyRequest().authenticated()
            .and()
            .formLogin()
            .loginProcessingUrl("/login") // 处理登录请求
            .successHandler((req, res, auth) -> res.setStatus(200)) 
            .failureHandler((req, res, e) -> res.sendError(401));
    }
}
```

**(2) 自动管理 Session**
Spring Security 默认通过 `JSESSIONID` Cookie 管理会话，无需额外代码。

------

#### 2. 前端（Vue）

**(1) 登录时启用 withCredentials**

javascript

复制

```
axios.post('/api/login', { username: 'admin', password: '123456' }, {
  withCredentials: true // 允许携带 Cookie
});
```

**(2) 后续请求自动携带 Cookie**

javascript

复制

```
axios.defaults.withCredentials = true; // 全局设置
```

------

### 三、关键差异与选择建议

| 特性     | JWT                    | Session-Cookie               |
| -------- | ---------------------- | ---------------------------- |
| 状态管理 | 无状态（Token 自包含） | 有状态（服务端存储 Session） |
| 扩展性   | 适合分布式系统         | 需要 Session 共享方案        |
| 跨域支持 | 容易（需处理 CORS）    | 需配置 withCredentials       |
| 安全性   | 需防范 XSS/Token 泄露  | 需防范 CSRF                  |

**推荐场景**：

- JWT：移动端/跨域/微服务架构
- Session：传统 Web 应用/快速实现

------

### 四、安全增强措施

1. **HTTPS**：所有认证请求必须通过 HTTPS 传输。
2. **Token 存储**：避免 XSS，建议使用 `HttpOnly` Cookie（但需处理 CSRF）。
3. **短有效期**：Access Token 设置较短有效期（如 15 分钟），搭配 Refresh Token。
4. **黑名单**：JWT 失效需结合黑名单机制。

通过以上方案，您可以灵活选择适合项目的认证方式。
