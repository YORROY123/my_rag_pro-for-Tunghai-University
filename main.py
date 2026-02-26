from rag_engine import MyRAG
import os

def main():
    # 1. 初始化引擎
    bot = MyRAG()

    # 2. 自動化管理資料庫 (寫得更好：檢查有無資料，避免重複存入)
    # 檢查資料庫目前的片段數量
    count = bot.collection.count()
    
    if count == 0:
        print("首次執行，正在將 dog.md 寫入資料庫...")
        if os.path.exists("dog.md"):
            bot.add_document("dog.md")
        else:
            print("❌ 錯誤：找不到 dog.md 檔案，請先建立它！")
            return
    else:
        print(f"✅ 資料庫已就緒 (目前有 {count} 條知識片段)")

    # 3. 進入提問循環
    print("\n--- RAG 助手啟動成功 (輸入 quit 離開) ---")
    
    while True:
        q = input("\n請輸入你的問題: ")
        
        # 簡單處理離開邏輯
        if q.lower() in ["quit", "exit", "離開", "q"]:
            print("再見！")
            break
        
        if not q.strip():
            continue

        # 執行 RAG 檢索與回答
        print("🔍 正在檢索並生成答案...")
        answer = bot.ask(q)
        
        print(f"\n💡 AI 回答：\n{answer}")

if __name__ == "__main__":
    main()