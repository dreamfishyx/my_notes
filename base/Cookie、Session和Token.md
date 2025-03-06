#### Cookie









#### Session









#### Token













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
