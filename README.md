### AIPyProject 使用说明

本项目演示：
- 使用百度智能云 OCR（AipOcr）识别图片文字
- 使用本地微型摘要（jieba 词频法）对识别文本进行总结

### 环境准备
- Python 3.8+
- 已开通并获取以下凭据（注意不要泄露）：
  - BAIDU_APP_ID（OCR）
  - BAIDU_API_KEY（OCR/获取 Access Token）
  - BAIDU_SECRET_KEY（OCR/获取 Access Token）

### 安装依赖
```powershell
pip install -r requirements.txt
```

### 配置环境变量（Windows PowerShell 示例）
```powershell
$env:BAIDU_APP_ID="<你的OCR_APP_ID>"
$env:BAIDU_API_KEY="<你的OCR_API_KEY>"
$env:BAIDU_SECRET_KEY="<你的OCR_SECRET_KEY>"

```
注意：设置后需重新打开一个新的终端窗口以生效。

### 目录结构
```
AIPyProject/
  images/
    p479558.png   # 示例图片
  main.py         # 主程序
  requirements.txt
  README.md
```

### 运行
```powershell
python main.py --image ".\images\p479558.png" --max-sentences 3 --log-level INFO
```
程序流程：
1) 从 `images/p479558.png` 读取图片并进行 OCR
2) 打印识别结果
3) 使用本地微型摘要算法生成“结构化摘要”和“简要摘要”
4) 打印摘要结果

### 重要说明与安全建议
- 已将密钥从代码中移除并改为读取环境变量，避免凭据泄露。
- 如果你需要在不同环境运行，建议使用 `.env` 文件配合 `python-dotenv`（未默认启用）。
- 当前版本不再依赖文心工作台对话接口；摘要在本地完成。

### 常见问题排查
- 运行时报 `ImportError`：
  - 未安装依赖，执行 `pip install -r requirements.txt`。
- 找不到图片：
  - 程序使用基于脚本目录的路径。确认 `images/p479558.png` 存在，或自行更换图片路径。

### 可选：使用 .env 管理凭据
在项目根目录创建 `.env`：
```
BAIDU_APP_ID=你的OCR_APP_ID
BAIDU_API_KEY=你的OCR_API_KEY
BAIDU_SECRET_KEY=你的OCR_SECRET_KEY
```
程序会自动加载 `.env`。

### 自定义与扩展
- 更换图片：将你的图片放入 `images/` 并在 `main.py` 中替换文件名。
- 修改提问：调整 `main.py` 中的 `question` 字段内容。
- 更换模型：将 `ai_analyze_text` 中 `payload["model"]` 改为你已开通的模型（如 `ernie-4.0`、`ernie-speed` 等）。

### 免责声明
本项目仅用于学习与演示，请妥善保管账号密钥并遵守相关服务条款与法律法规。

