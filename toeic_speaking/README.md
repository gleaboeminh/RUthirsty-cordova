# TOEIC Speaking Practice — 构建与运行指南

## 环境要求

- Python 3.8+（Windows 64位推荐）
- Windows 7/10/11

## 安装依赖

```bash
pip install PyQt5 pyttsx3
```

> 如果 PyQt5 安装困难，可改用 PySide6：
> ```bash
> pip install PySide6 pyttsx3
> ```

## 运行程序

```bash
cd toeic_speaking
python main.py
```

## 打包为 Windows EXE（pyinstaller）

```bash
pip install pyinstaller
cd toeic_speaking
pyinstaller --onefile --windowed --name "TOEIC_Speaking_Practice" main.py
```

打包后，将以下内容复制到 `dist/` 目录（与 EXE 同级）：
- `images/` 文件夹（存放题目图片）
- `audio/` 文件夹（存放预录音频，可选）
- `toeic_speaking_config.json`（首次运行会自动创建）

## 目录结构

```
toeic_speaking/
├── main.py                      # 主程序
├── requirements.txt
├── toeic_speaking_config.json   # 自动生成的题目配置文件
├── toeic_speaking_config.json.bak  # 保存时自动备份
├── images/                      # 图片文件夹（PART 2 使用）
│   ├── pic1.jpg
│   └── pic2.jpg
└── audio/                       # 音频文件夹（预留，可选）
```

## 功能说明

### 各 PART 时间安排

| PART | 题目 | 准备时间 | 答题时间 |
|------|------|----------|----------|
| PART 1 | 朗读文本 Q1–Q2 | 45秒 | 45秒 |
| PART 2 | 看图说话 Q3–Q4 | 45秒 | 30秒 |
| PART 3 | 回答问题 Q5–Q6 | 3秒 | 15秒 |
| PART 3 | 回答问题 Q7 | 3秒 | 30秒 |
| PART 4 | 阅读材料 Q8–Q10 | 45秒阅读 | 15/15/30秒 |
| PART 5 | 表达观点 Q11 | 45秒 | 60秒 |

### 编辑模式

点击顶部工具栏 **Edit Mode** 开关：
- 开启后所有文本框变为可编辑状态（橙色边框提示）
- 修改仅保存在内存，需点击 **Save** 才写入 JSON 文件
- 关闭时自动提示是否保存

### TTS 语音

- 需要安装 `pyttsx3`，Windows 上使用 SAPI5 引擎
- 自动使用系统英语语音（可在 Windows 语音设置中添加更多）
- 若未安装 pyttsx3，软件仍可正常运行，仅无语音提示

### 配置文件

`toeic_speaking_config.json` 存储所有题目数据，支持手动编辑或通过软件编辑模式修改。
每次保存时自动创建 `.bak` 备份文件。
