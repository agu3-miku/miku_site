# 安玖的小站

一个静态摄影作品站。浅蓝主题，首页自动滚动播放每个系列的封面，点击照片进入该系列的完整影集。

- 线上地址：<https://agu3-miku.github.io/miku_site/>
- 仓库：<https://github.com/agu3-miku/miku_site>
- GitHub：<https://github.com/agu3-miku>
- 微信：`D2141161717`

网站程序在 `index.html` 里，CSS 和 JavaScript 全部内嵌；每个系列是仓库根目录下的一个文件夹，文件夹名就是合集名，里面放 JPG / PNG 图片。

页面不再调用 GitHub API，也不把合集清单写死在 HTML 里。合集目录由 `collections.json` 提供，而这个文件由 GitHub Actions 在每次 push 后自动扫描生成。

## 为什么不直接调用 GitHub API

GitHub 匿名 API 每小时只有约 60 次请求额度，而且是按访问者 IP 计算的。网站公开后很容易被限流，表现就是页面打得开、但合集和图片全部空白，控制台出现：

```text
GitHub API responded with 403
API rate limit exceeded
```

所以现在改成同仓库的静态 `collections.json`，没有限流问题。

## 页面如何找到照片

| 环境 | 目录来源 |
| --- | --- |
| GitHub Pages | 读取同仓库的静态 `collections.json`，不请求 GitHub API |
| 本地 `preview.py` | 每次请求 `__local_collections.json` 时现场扫描文件夹 |
| 普通静态服务器 | 读取已经生成好的 `collections.json` |

`collections.json` 长这样，由脚本生成，不需要手写：

```json
{
  "collections": [
    {
      "dir": "10.2大连喵喵港",
      "photos": ["xxx.jpg", "yyy.png", "zzz.jpg"]
    }
  ]
}
```

## 目录结构

```text
.
├── index.html                         # 网站主程序
├── collections.json                   # 自动生成的合集清单
├── build_collections.py               # 扫描文件夹、生成 collections.json
├── preview.py                         # 本地动态预览
├── README.md
├── .nojekyll
├── .github/workflows/
│   └── update-collections.yml         # push 后自动更新清单
├── 10.2大连喵喵港/
│   ├── xxx.jpg
│   ├── yyy.png
│   └── ...
├── 旅顺太阳沟-vivid/
│   └── *.jpg
├── 旅顺太阳沟-夕颜/
│   └── *.jpg
└── 瓷糯/
    └── *.jpg
```

网页只读取根目录下一层文件夹里的图片，不读取子文件夹。

## 第一次上传/修复线上空白

当前线上使用的是会 403 的旧版本。需要把这些文件上传到 `miku_site` 仓库根目录：

1. `index.html`（覆盖旧文件）
2. `collections.json`
3. `build_collections.py`
4. `.github/workflows/update-collections.yml`
5. `preview.py`（线上不需要，但可以一并放）
6. 所有照片文件夹

上传后等 GitHub Pages 部署完成，再强制刷新页面。

如果 GitHub Actions 没有自动运行，可以在仓库 **Actions** 页面手动运行一次 `Update photo collections`，或者本地执行：

```bash
python3 build_collections.py
git add collections.json
git commit -m "update collections"
git push
```

## 增加、删除、重命名系列

GitHub 上直接操作文件夹即可：

- 新增文件夹并放入图片；
- 删除文件夹；
- 重命名文件夹。

push 到 `main` 后，GitHub Actions 会自动重新生成 `collections.json` 并提交。等 Pages 再次部署完，刷新页面就会变化。

如果新增了文件夹但页面没变，按顺序检查：

1. 仓库 **Actions** 里 `Update photo collections` 是否成功；
2. 根目录 `collections.json` 是否更新；
3. GitHub Pages 是否已经重新部署；
4. 浏览器强制刷新（Mac：`Cmd + Shift + R`）。

## 本地预览

```bash
python3 preview.py
```

打开 <http://127.0.0.1:8000>。

`preview.py` 不会修改 HTML，也不会生成清单；它每次被请求时现场扫描文件夹，所以增删文件夹、换文件名后刷新就能看到。

```bash
python3 preview.py --port 8080
```

不要用 `file://` 直接双击打开。

## 封面规则

默认取文件名排序最前的一张，但优先选择 JPG：

- 有 JPG 时，从 JPG 里选封面，避免一张大 PNG 拖慢首屏；
- 只有 PNG 时，从 PNG 里选；
- 想换封面，把想用的照片改成排序更靠前的名字；
- 想改成按哈希值选封面，把 `index.html` 里的 `"coverStrategy": "first"` 改成 `"hash"`。

当前 `10.2大连喵喵港` 的封面是 `0693739...jpg`。

## 图片格式和大小

支持：

- `.jpg`
- `.jpeg`
- `.png`

当前有些相机原图单张超过 10MB，甚至有一张 13MB 的 PNG。网站不会压缩原图，首页会先加载封面，打开影集后再按滚动加载其余照片。

建议发布前导出网页版：

- 长边 1600–2400px
- JPEG 质量 80–85
- 单张 300–800KB

## 联系方式

- GitHub：<https://github.com/agu3-miku>
- 微信：`D2141161717`（页面点击可复制）

修改微信：改 `index.html` 里的：

```json
"contact": {
  "github": "https://github.com/agu3-miku",
  "wechat": "D2141161717"
}
```

## 部署设置

仓库：`agu3-miku/miku_site`

GitHub Pages 设置：

- **Source**：`Deploy from a branch`
- **Branch**：`main` / `/ (root)`

不使用 `CNAME`，也不使用自定义域名；项目站地址是：

`https://agu3-miku.github.io/miku_site/`

## 限制

- **公开仓库**：这是 GitHub Pages 的限制，不是网站代码的问题。
- **目录层级**：只识别根目录下一层文件夹，系列文件夹里不要再嵌套子文件夹。
- **格式**：只识别 `.jpg` / `.jpeg` / `.png`。
- **Actions 权限**：仓库需要允许 Actions 写入内容；如果自动提交失败，按上面的方法本地生成 `collections.json` 再 push。
- **隐私**：照片会公开在 GitHub Pages 上，请勿上传不方便公开的内容。

## 修改颜色

所有视觉变量在 `index.html` 开头：

```css
--paper: #f2f8fb;
--ink: #152c3a;
--blue: #8ac6e1;
--blue-deep: #3e86a9;
```
