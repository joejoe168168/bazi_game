# 🚀 Netlify 部署配置

## ✅ 修复的问题

1. **netlify.toml 语法错误**: 移除了无效的 `python_version` 配置
2. **简化配置**: 使用最小化的有效配置
3. **移除 runtime.txt**: 让 Netlify 自动检测 Python 版本

## 📁 最终文件结构

```
bazi2/
├── index.html              # 前端游戏页面 (必须在根目录)
├── netlify.toml            # Netlify 配置 (已修复)
├── requirements.txt        # Python 依赖
├── app.py                 # 本地开发服务器
├── netlify/
│   └── functions/         # 无服务器函数
│       ├── new_game.py    # 新游戏 API
│       ├── check_relationship.py  # 检查关系 API
│       ├── bazi_utils.py  # 八字工具函数
│       ├── ganzhi.py      # 干支数据
│       ├── datas.py       # 基础数据
│       └── common.py      # 通用函数
└── test_local.py          # 本地测试
```

## 🔧 最终配置文件

### netlify.toml (已修复)
```toml
[build]
  publish = "."

[functions]
  directory = "netlify/functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

### requirements.txt
```
lunar-python==1.4.4
bidict==0.22.1
```

## ⚡ Netlify 部署步骤

1. **推送到 GitHub**: 确保所有文件都在仓库中
2. **连接 Netlify**: 
   - 登录 Netlify Dashboard
   - 点击 "New site from Git"
   - 选择 GitHub 仓库 `bazi_game`
3. **构建设置**:
   - Build command: (留空)
   - Publish directory: `.`
   - Functions directory: `netlify/functions`
4. **部署**: 点击 "Deploy site"

## 🧪 本地测试

```bash
# 测试兼容性
source venv/bin/activate
python test_local.py

# 运行本地服务器
python app.py
# 访问 http://localhost:5000
```

## 📋 配置说明

- **无需 runtime.txt**: Netlify 会自动检测 Python 版本
- **简化 netlify.toml**: 移除了所有无效配置
- **函数目录**: `netlify/functions` (无尾随斜杠)
- **重定向**: `/api/*` → `/.netlify/functions/:splat`

## 🎯 应该可以工作的功能

✅ 静态文件服务 (index.html)
✅ 无服务器函数 (new_game, check_relationship)  
✅ API 路由重定向
✅ Python 依赖安装
✅ 设置持久化存储
✅ 地支相刑默认关闭

## 🔍 如果仍有问题

1. 检查 Netlify 构建日志中的具体错误
2. 确认所有文件都推送到 GitHub
3. 验证函数目录路径正确
4. 检查 Python 语法错误 (本地运行 `python test_local.py`)