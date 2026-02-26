# 🚀 Gemini RAG 知識庫助手 (Tunghai University Edition)

這是一個基於 **Google Gemini 2.5 Flash** 與 **ChromaDB** 構建的檢索增強生成 (RAG) 系統。它可以將本地的 Markdown 檔案轉換為向量知識庫，讓 AI 能根據你提供的特定資料進行精確回答。

---

## DEMO VIDEO

https://youtu.be/yxM8mT3m0HE

## 🛠️ 技術棧 (Tech Stack)

* **語言**: Python 3.12+
* **套件管理**: [uv](https://github.com/astral.sh/uv) (超快速的 Python 專案管理工具)
* **向量資料庫**: ChromaDB (本地持久化存儲)
* **LLM**: Google Gemini 2.5 Flash
* **Embedding 模型**: `all-MiniLM-L6-v2` (Sentence-Transformers)

---

## 📁 專案結構

```text
my_rag_pro/
├── main.py            # 程式進入點，處理使用者互動
├── rag_engine.py      # RAG 核心邏輯 (Embedding, Retrieval, Generation)
├── dog.md             # 知識庫原始檔案 (Markdown 格式)
├── .env               # 存放敏感的 API Key (Git 已忽略)
├── pyproject.toml     # 專案依賴與 uv 設定
└── chroma_db/         # 自動生成的向量資料庫資料夾
```

## ⚙️ 安裝與設定

### 1. 取得 Gemini API Key
前往 Google AI Studio 申請一個免費的 API Key。

### 2. 環境配置

在專案根目錄建立 .env 檔案，並填入你的 Key：

### 3. 安裝依賴
使用 uv 快速建立環境並安裝所有套件：

```PowerShell
uv sync
```

## 🚀 執行方式


啟動主程式進入對話循環：

```PowerShell
uv run main.py
```


* 自動索引: 首次執行時，系統會掃描 dog.md 並建立向量索引。
* 持久化存儲: 資料會存在 chroma_db/，下次啟動無需重新解析。

## 📝 如何更新知識庫？

1. 直接編輯或替換 dog.md 中的文字內容。

2. 刪除專案路徑下的 chroma_db/ 資料夾。

3. 重新執行 uv run main.py，AI 就會學習到新的知識。

## 📄 授權條款

本專案採用 MIT License 授權。

---