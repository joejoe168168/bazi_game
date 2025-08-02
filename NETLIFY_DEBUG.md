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

## 根本原因

**Python 函数在 Netlify 上部署困难**：
1. **复杂依赖**: `lunar-python`, `bidict` 等依赖在 Netlify 环境中可能不稳定
2. **导入路径问题**: Python 模块间的相对导入在无服务器环境中复杂
3. **冷启动性能**: Python 函数启动较慢

## 最终解决方案

**切换到 JavaScript 函数** - 更稳定，部署更可靠：

## 修复方案

### ✅ 最终方案: JavaScript 函数

创建了 JavaScript 版本的函数，具有以下优势：
- **无依赖问题**: JavaScript 函数不需要复杂的 Python 依赖
- **快速部署**: Netlify 对 Node.js 函数支持更好
- **稳定性高**: 避免了 Python 环境配置问题

### 新函数文件:

1. **new_game.js** - 生成随机八字和基础关系检测
2. **check_relationship.js** - 验证用户选择的关系
3. **test.js** - 简单测试函数
4. **hello.py** - Python 测试函数（调试用）

### CORS 处理

所有函数都包含完整的 CORS 支持：
```javascript
if (event.httpMethod === 'OPTIONS') {
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Methods': 'POST, OPTIONS'
    },
    body: ''
  };
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

## 当前文件结构

```
netlify/functions/
├── new_game.js                  # ✅ JavaScript 新游戏函数 (主要)
├── check_relationship.js       # ✅ JavaScript 关系检查函数 (主要)
├── test.js                     # ✅ JavaScript 测试函数
├── hello.py                    # Python 测试函数
├── new_game_standalone.py      # Python 独立函数 (备用)
├── check_relationship_standalone.py # Python 独立函数 (备用)
└── ...其他 Python 文件
```

## 下一步

1. **部署 JavaScript 版本** - 应该可以立即工作
2. **测试基础功能** - 新游戏生成和关系检查
3. **如果成功** - 可以逐步增强关系检测逻辑
4. **如果失败** - 检查 Netlify 部署日志找出问题

## 优势

✅ **JavaScript 函数优势**:
- 无需复杂 Python 依赖
- Netlify 原生支持更好
- 部署速度更快
- 调试更容易
- 冷启动时间更短