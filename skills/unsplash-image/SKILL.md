---
name: unsplash-image
version: 1.0.0
description: "Use when searching and downloading high-quality free images from Unsplash API (free tier: 50 requests/hour)."
triggers: ['图片，搜索，Unsplash', '免费图片，image', 'photo', 'search', 'wallpaper']
permissions: ['exec', 'web_fetch']
category: visual
author: 太一 AGI
---



# Unsplash Image API

Use this skill when you need high-quality free images from Unsplash.

## Core Truths

- **免费层**: 50 请求/小时
- **高质量**: 专业摄影师作品
- **免版税**: 可商用
- **API Key**: 需要注册 (免费)

## What This Tool Is For

`unsplash-image` provides:

1. **Search Photos** - 搜索图片
2. **Random Photos** - 随机图片
3. **Collections** - 图片合集
4. **Download** - 下载图片

## Authentication

**Get API Key**: https://unsplash.com/join?source=applications

1. 注册 Unsplash 账号
2. 创建应用 (New Application)
3. 获取 Access Key

**太一配置**: 将 API Key 存入 `.env`
```
UNSPLASH_ACCESS_KEY=your_access_key_here
```

## Default Workflow

### 1. Search Photos (搜索图片)

```bash
# 搜索关键词
curl "https://api.unsplash.com/search/photos?query=nature&client_id=YOUR_KEY"

# 指定数量
curl "https://api.unsplash.com/search/photos?query=technology&per_page=10&client_id=YOUR_KEY"

# 指定方向 (landscape, portrait, squarish)
curl "https://api.unsplash.com/search/photos?query=people&orientation=landscape&client_id=YOUR_KEY"
```

**Response**:
```json
{
  "total": 1234,
  "total_pages": 124,
  "results": [
    {
      "id": "abc123",
      "description": "Beautiful nature landscape",
      "urls": {
        "regular": "https://images.unsplash.com/photo-xxx?w=1080",
        "small": "https://images.unsplash.com/photo-xxx?w=400",
        "thumb": "https://images.unsplash.com/photo-xxx?w=200"
      },
      "user": {
        "name": "Photographer Name",
        "username": "photographer"
      }
    }
  ]
}
```

### 2. Random Photos (随机图片)

```bash
# 单张随机
curl "https://api.unsplash.com/photos/random?client_id=YOUR_KEY"

# 多张随机
curl "https://api.unsplash.com/photos/random?count=5&client_id=YOUR_KEY"

# 指定合集
curl "https://api.unsplash.com/photos/random?collections=123456&client_id=YOUR_KEY"
```

### 3. Download Photo (下载图片)

```bash
# 下载链接 (需要用户操作)
curl "https://api.unsplash.com/photos/abc123/download?client_id=YOUR_KEY"
```

**注意**: 下载链接需要用户点击或二次请求

## Integration with Taiyi

### 山木 (内容创作)

**使用场景**:
- 文章配图
- 社交媒体图片
- 壁纸生成

**示例**:
```python
import requests
import os

def search_images(query, count=5):
    access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    url = "https://api.unsplash.com/search/photos"
    params = {
        'query': query,
        'per_page': count,
        'client_id': access_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    for photo in data.get('results', []):
        results.append({
            'url': photo['urls']['regular'],
            'description': photo.get('description', ''),
            'photographer': photo['user']['name']
        })
    return results

# 使用
images = search_images('technology')
for img in images:
    print(f"{img['url']} - {img['photographer']}")
```

### 太一 (系统增强)

**使用场景**:
- 信息卡片配图
- 报告封面
- 头像生成

## Rate Limits

| 层级 | 请求数 | 价格 |
|------|--------|------|
| **免费** | 50/小时 | $0 |
| **Premium** | 5000/小时 | 联系销售 |

**太一策略**:
- 免费层 50 请求/小时 = 每 72 秒 1 次
- 缓存搜索结果 1 小时
- 批量请求分散执行

## Error Handling

### Common Errors

| Error | Code | Solution |
|-------|------|----------|
| Rate Limit | 429 | 等待或缓存 |
| Unauthorized | 401 | 检查 Access Key |
| Not Found | 404 | 检查图片 ID |
| Server Error | 500 | 重试 |

### Fallback APIs

1. **Pexels**: https://www.pexels.com/api/
2. **Pixabay**: https://pixabay.com/api/docs/
3. **Burst**: https://burst.shopify.com/

## Quick Reference

### Popular Keywords

| 关键词 (英文) | 用途 |
|-------------|------|
| nature | 自然风光 |
| technology | 科技 |
| business | 商业 |
| people | 人物 |
| food | 美食 |
| travel | 旅行 |
| architecture | 建筑 |
| animals | 动物 |

### Orientation

| 方向 | 说明 |
|------|------|
| landscape | 横向 |
| portrait | 纵向 |
| squarish | 方形 |

### Image Sizes

| 尺寸 | 宽度 | 用途 |
|------|------|------|
| thumb | 200px | 缩略图 |
| small | 400px | 小图 |
| regular | 1080px | 常规 |
| full | 原始 | 高清 |

## Example Outputs

### Image Search Query

**Input**: "搜索科技图片"

**Output**:
```markdown
## 🖼️ 科技图片 (Top 5)

1. **[图片描述]** by [摄影师]
   ![](https://images.unsplash.com/photo-xxx?w=1080)

2. **[图片描述]** by [摄影师]
   ![](https://images.unsplash.com/photo-yyy?w=1080)

...

共 1234 张 | 来自 Unsplash
```

### Random Image

**Input**: "随机壁纸"

**Output**:
```markdown
## 🎲 随机壁纸

![](https://images.unsplash.com/photo-zzz?w=1920)

**摄影师**: [Name]
**描述**: [Description]

[下载高清原图](https://unsplash.com/photos/zzz/download)
```

## Setup for Taiyi

### 1. Register Unsplash Account

Visit: https://unsplash.com/join?source=applications

### 2. Create Application

1. Login to Unsplash
2. Go to: https://unsplash.com/oauth/applications
3. Click "New Application"
4. Fill in app name and description
5. Accept terms

### 3. Get Access Key

- Copy Access Key from application page
- Add to .env: `UNSPLASH_ACCESS_KEY=your_key`

### 4. Test Connection

```bash
curl "https://api.unsplash.com/photos/random?client_id=$(grep UNSPLASH_ACCESS_KEY .env | cut -d= -f2)"
```

## Notes

- Free tier: 50 requests/hour
- API Key required (free registration)
- Images are royalty-free (can use commercially)
- Cache search results to reduce API calls (1 hour TTL)
- Attribution appreciated but not required

## References

- **API Docs**: https://unsplash.com/documentation
- **Register**: https://unsplash.com/join?source=applications
- **Pricing**: https://unsplash.com/developers

---

*Version: 1.0.0 | Created: 2026-04-04 | Taiyi AGI*
