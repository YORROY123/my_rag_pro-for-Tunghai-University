import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
import google.generativeai as genai

# 1. 讀取 .env 中的 Gemini API Key
load_dotenv()

class MyRAG:
    def __init__(self):
        print("🚀 正在啟動 RAG 系統...")
        # 載入 Embedding 模型
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 初始化向量資料庫
        self.db_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.db_client.get_or_create_collection(name="knowledge_base")
        
        # 2. 設定 Gemini (修正重點：確保 API KEY 有讀到)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ 找不到 API Key，請檢查 .env 檔案！")
            
        genai.configure(api_key=api_key)
        
        # 【關鍵修正】：移除 models/ 前綴，直接用名稱
        # 修改前：self.model = genai.GenerativeModel('gemini-1.5-flash')
        # 修正後：對應你截圖中的 Gemini 2.5 Flash
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ 系統準備就緒！")

    def add_document(self, file_path):
        """讀取檔案並存入資料庫"""
        if not os.path.exists(file_path):
            print(f"❌ 找不到檔案：{file_path}")
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 優化分段：用 \n\n (段落) 分段通常比單行更好
        chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 5]
        
        if not chunks:
            print("⚠️ 檔案內容太少，沒有可存入的片段。")
            return

        # 轉換成向量
        embeddings = self.embed_model.encode(chunks).tolist()
        ids = [f"id_{i}_{os.path.basename(file_path)}" for i in range(len(chunks))]
        
        self.collection.add(documents=chunks, embeddings=embeddings, ids=ids)
        print(f"✅ 已成功存入 {len(chunks)} 條知識片段！")

    def ask(self, question):
        """核心 RAG 流程"""
        # A. 檢索 (Retrieval)
        query_vec = self.embed_model.encode([question]).tolist()
        results = self.collection.query(query_embeddings=query_vec, n_results=3)
        
        if not results['documents'][0]:
            return "資料庫裡空空的，請先 add_document 餵我吃資料。"

        context = "\n---\n".join(results['documents'][0])
        
        # B. 提示詞工程 (Prompt Engineering)
        prompt = f"""你是一個專業的 AI 助手。請『僅根據』下方提供的【參考資料】來回答問題。
若資料中沒有答案，請回答『資料庫中目前沒有相關資訊』。

【參考資料】：
{context}

【使用者提問】：
{question}
"""
        # C. 生成 (Generation)
        try:
            # 💡 寫得更好：使用最精簡的名稱，並加上錯誤處理
            # 有些環境需要 'gemini-1.5-flash'，有些需要 'models/gemini-1.5-flash'
            # 我們嘗試直接用模型物件來生成
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # 如果失敗，嘗試切換模型名稱格式
            try:
                print("🔄 正在嘗試備用模型路徑...")
                temp_model = genai.GenerativeModel('models/gemini-1.5-flash')
                response = temp_model.generate_content(prompt)
                return response.text
            except:
                return f"❌ 呼叫 Gemini 時發生錯誤：{str(e)}"