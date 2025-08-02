# 八字关系互动游戏 - 部署指南

## 🎯 项目概述

这是一个互动的八字关系游戏，用户可以点击八字字符找出其中的关系（天干相合相冲，地支六合三合等）。

## 🚀 本地开发

### 预备条件
- Python 3.8+ 
- 虚拟环境（推荐）

### 本地启动步骤

1. **克隆项目并进入目录**
```bash
cd bazi2
```

2. **激活虚拟环境并安装依赖**
```bash
source venv/bin/activate
pip install -r requirements.txt flask flask-cors
```

3. **运行本地测试**
```bash
python test_local.py
```

4. **启动本地开发服务器**
```bash
python app.py
```

5. **访问游戏**
打开浏览器访问: `http://localhost:5000`

## ☁️ Netlify 部署

### 文件结构
```
bazi2/
├── index.html              # 前端游戏页面
├── netlify.toml            # Netlify 配置
├── requirements.txt        # Python 依赖
├── runtime.txt             # Python 版本
├── app.py                 # 本地 Flask 服务器
├── netlify/
│   └── functions/         # Netlify 无服务器函数
│       ├── new_game.py    # 新游戏 API
│       ├── check_relationship.py  # 检查关系 API
│       ├── bazi_utils.py  # 工具函数
│       ├── ganzhi.py      # 干支数据
│       ├── datas.py       # 基础数据
│       └── common.py      # 通用函数
└── test_local.py          # 本地测试脚本
```

### Netlify 部署步骤

1. **连接 GitHub 仓库**
   - 登录 Netlify
   - 点击 "New site from Git"
   - 选择你的 GitHub 仓库

2. **构建设置**
   - Build command: (留空)
   - Publish directory: `.` (当前目录)
   - Functions directory: `netlify/functions`

3. **环境变量** (可选)
   - `PYTHON_VERSION`: `3.8`

4. **手动部署**
   也可以直接拖拽项目文件夹到 Netlify 进行部署

### 部署配置文件

#### netlify.toml
```toml
[build]
  publish = "."

[functions]
  directory = "netlify/functions/"
  
[build.environment]
  PYTHON_VERSION = "3.8"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

#### requirements.txt
```
lunar-python==1.4.4
bidict==0.22.1
```

#### runtime.txt
```
3.8
```

## 🔧 故障排除

### 常见问题

1. **Netlify 构建失败 - 依赖安装错误**
   - 检查 `requirements.txt` 中的版本号是否正确
   - 确保 `lunar-python` 使用兼容版本 `1.4.4`
   - 检查 `runtime.txt` 指定正确的 Python 版本

2. **本地导入错误**
   - 确保激活了虚拟环境: `source venv/bin/activate`
   - 安装所有依赖: `pip install -r requirements.txt flask flask-cors`

3. **API 调用失败**
   - 本地测试: 检查 Flask 服务器是否正常启动
   - Netlify: 检查函数日志，确保无服务器函数正常部署

4. **版本兼容性问题**
   - 使用 `python test_local.py` 检查所有模块是否正常导入
   - 确保所有依赖版本兼容

### 调试命令

```bash
# 测试本地兼容性
python test_local.py

# 启动本地服务器
python app.py

# 检查虚拟环境
source venv/bin/activate
pip list
```

## 📋 功能特性

- ✅ 地支相刑默认关闭
- ✅ 持久化设置存储 (localStorage)
- ✅ 支持基础模式 (4柱) 和高级模式 (6柱)
- ✅ 实时关系提示和进度跟踪
- ✅ 完整的关系类型支持
- ✅ 响应式设计，支持移动端

## 🔄 本地与 Netlify 兼容性

该项目设计为同时支持本地开发和 Netlify 部署：

- **本地开发**: 使用 `app.py` Flask 服务器
- **Netlify 部署**: 使用 `netlify/functions/` 无服务器函数
- **共享代码**: `netlify/functions/` 中的工具函数可以被两种环境使用

## 🎮 游戏说明

1. 点击2-3个八字寻找关系
2. 天干关系：相合、相冲
3. 地支关系：六合、相冲、三合、三会、半合、半会、相刑、相害、相破
4. 找到关系可获得分数
5. 找出所有关系完成游戏
6. 可在设置中自定义启用的关系类型