# 安玖的小站

一个单文件的静态摄影作品站。浅蓝主题，首页自动滚动播放每个系列的封面，点击照片进入该系列的完整影集。

- 线上地址：<https://agumiku.me/>
- GitHub：<https://github.com/agu3-miku>
- 微信：`D2141161717`

网站程序只有 `index.html` 一个文件，CSS 和 JavaScript 都内嵌在里面。每个系列是根目录下的一个文件夹，文件夹名就是合集名，里面有任意数量的 JPG 照片。

**这个版本不再把合集名或照片名写进 HTML。** 删除、增加、重命名文件夹后，线上页面和本地预览都会重新读取目录，不需要改代码。

## 它是怎么找到照片的

| 环境 | 目录来源 |
| --- | --- |
| GitHub Pages / 自定义域名 | 页面读取 `https://api.github.com/repos/agu3-miku/agu3-miku.github.io/git/trees/main?recursive=1`，按根目录下一层文件夹分组，收集里面所有 `.jpg` / `.jpeg` |
| 本地 `preview.py` | 每次请求 `__local_collections.json` 时重新扫描文件夹，返回当前真实目录 |
| 普通静态服务器 | 没有本地扫描接口，页面会回退到 GitHub API，读取已推送的仓库目录 |
| GitHub API 暂时不可用 | 使用浏览器里上一次成功读取的目录缓存 |

所以：

- 文件夹叫 `Cosplay`，页面就显示「Cosplay」。
- 文件名可以是 `1.jpg`、`IMG_1344.jpg`、`IMG_1373_(2).jpg`、`随便什么.JPG`，不需要 `01`、`02` 编号。
- 删除文件夹，刷新页面后对应系列消失。
- 增加文件夹，刷新页面后自动出现。
- 修改文件夹名，刷新页面后合集名跟着变。

## 本地预览

```bash
python3 preview.py
```

打开 <http://127.0.0.1:8000>。

`preview.py` 不会改 HTML，也不会生成清单；它只在浏览器请求 `__local_collections.json` 时现场扫描文件夹。所以增删文件夹、换文件名后，直接刷新页面就能看到。

指定端口：

```bash
python3 preview.py --port 8080
```

不要直接双击 `index.html` 用 `file://` 打开。这样没有本地扫描接口，浏览器的跨域限制也可能让线上 API 请求失败。请用 `preview.py` 或任意静态服务器。

## 目录结构

```text
.
├── index.html            # 网站主程序
├── preview.py            # 本地动态预览服务器（线上不需要）
├── README.md
├── CNAME                 # 自定义域名 agumiku.me
├── .nojekyll             # 告诉 GitHub Pages 不要跑 Jekyll
├── 你的系列/             # 文件夹名 = 合集名
│   ├── 1.jpg
│   ├── IMG_1344.jpg
│   └── ...
└── 另一个系列/
    └── *.jpg
```

`README.md`、`preview.py`、`CNAME`、`.nojekyll` 不会被当成系列。网页只读取根目录下一层文件夹里的 JPG。

## 部署到 GitHub Pages

当前配置对应仓库：

```text
https://github.com/agu3-miku/agu3-miku.github.io
分支：main
自定义域名：agumiku.me
```

把这些文件推到该仓库的 `main` 分支：

```bash
git add .
git commit -m "update photo site"
git push
```

然后在仓库 **Settings → Pages** 确认：

- **Source**：`Deploy from a branch`
- **Branch**：`main` / `/ (root)`

等 GitHub Pages 部署完成后访问 <https://agumiku.me/>。页面每次加载都会向 GitHub 读取最新目录，所以之后加照片只需要 push，不需要修改 `index.html`。

### 如果换了仓库或域名

打开 `index.html` 末尾的 `site-config`：

```json
"github": {
  "owner": "agu3-miku",
  "repo": "agu3-miku.github.io",
  "branch": "main"
}
```

改成新的用户名、仓库名和分支即可。使用自定义域名时必须填这一项，因为网页无法从域名猜出仓库。

## 封面规则

默认取 **文件名自然排序最前的一张**：

- `1.jpg` 排在 `10.jpg` 前面；
- 想换封面，调整文件名，或把想用的照片改成排序更靠前的名字；
- 如果更想用哈希值最小的照片，把 `index.html` 里的 `"coverStrategy": "first"` 改成 `"hash"`。

## 联系方式

页面上已经放好：

- GitHub：<https://github.com/agu3-miku>
- 微信：`D2141161717`（点击会复制）

要修改微信，改 `index.html` 的 `site-config`：

```json
"contact": {
  "wechat": "D2141161717"
}
```

## 图片建议

当前网站直接引用原图，不压缩、不生成缩略图。相机原图单张可能超过 10MB，首屏会加载封面，打开影集会加载更多照片。

建议发布前导出网页版：

- 长边 1600–2400px
- JPEG 质量 80–85
- 单张 300–800KB

保留原图在别处，文件夹里放网页版即可。这样手机端会顺畅很多。

## 说明与限制

- **公开仓库**：GitHub 匿名目录 API 只能读取公开仓库；私有仓库需要登录，静态网页不能安全携带 token。
- **目录层级**：只识别根目录下一层文件夹，系列文件夹里不要再嵌套子文件夹。
- **格式**：只识别 `.jpg` / `.jpeg`，其他格式会被忽略。
- **缓存**：浏览器会缓存上次目录，API 请求失败时用它兜底；正常加载仍会请求最新目录。
- **限额**：GitHub 匿名 API 每小时约 60 次请求，个人站点正常使用足够。
- **隐私**：照片会被公开在 GitHub Pages 上，请勿上传不方便公开的内容。

## 修改颜色

所有视觉变量在 `index.html` 开头：

```css
--paper: #f2f8fb;
--ink: #152c3a;
--blue: #8ac6e1;
--blue-deep: #3e86a9;
```

把 `--paper` 和 `--blue-*` 换成喜欢的浅蓝即可。
