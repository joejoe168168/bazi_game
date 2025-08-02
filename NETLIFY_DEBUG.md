# 🐛 Netlify 函数调试指南

## 问题描述

前端显示错误：
```
生成新的八字中...
启动新游戏失败: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
Failed to load resource: the server responded with a status of 404 ()
```

## 问题分析

这个错误表示：
1. **404 错误**: Netlify 函数没有被找到或部署失败
2. **HTML 响应**: 返回的是 404 页面的 HTML 而不是 JSON
3. **函数路由问题**: `/api/new_game` 路径没有正确映射到函数

## 可能的原因

1. **函数导入错误**: `from bazi_utils import ...` 可能在 Netlify 环境中失败
2. **函数部署失败**: 复杂的依赖关系导致函数无法正常部署
3. **路径映射问题**: `netlify.toml` 中的重定向规则可能有问题

## 修复方案

### 方案1: 独立函数 (当前测试)

创建了独立的函数文件，将所有依赖代码内联：
- `new_game_standalone.py` - 不依赖外部模块
- `check_relationship_standalone.py` - 简化的关系检查

### 方案2: 修复导入问题

为原始函数添加了路径修复：
```python
import sys
import os
sys.path.append(os.path.dirname(__file__))
```

### 方案3: CORS 处理

添加了 OPTIONS 请求处理：
```python
if event.get('httpMethod') == 'OPTIONS':
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': ''
    }
```

## 测试步骤

1. **部署独立函数版本**
   - 推送包含 `*_standalone.py` 文件的版本
   - 前端调用 `/api/new_game_standalone`

2. **检查 Netlify 函数日志**
   - 进入 Netlify Dashboard
   - 查看 Functions 页面
   - 检查部署状态和错误日志

3. **测试简单函数**
   - 访问 `/api/test` 测试基本函数是否工作
   - 确认 404 是函数问题还是路由问题

## 文件结构

```
netlify/functions/
├── test.py                      # 简单测试函数
├── new_game_standalone.py       # 独立新游戏函数 ✅
├── check_relationship_standalone.py # 独立关系检查函数 ✅
├── new_game.py                  # 原始函数 (可能有导入问题)
├── check_relationship.py       # 原始函数 (可能有导入问题)
└── bazi_utils.py               # 工具函数
```

## 下一步

1. 测试独立函数版本是否工作
2. 如果工作，逐步改进功能完整性
3. 如果不工作，检查 Netlify 部署日志
4. 根据结果决定是否需要进一步简化或修复路由