import google.generativeai as genai
import os
import time
import pandas as pd
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

# 設定你的 API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 檢查是否成功讀取 Key，避免程式崩潰
if not GOOGLE_API_KEY:
    raise ValueError("❌ 找不到 GOOGLE_API_KEY，請檢查 .env 檔案設定！")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# === 🏥 完整中文測試集 (50題) ===
# 每個科別擴充至 10 題
test_cases = [
    # --- 內科 (Internal Medicine) [10題] ---
    {"symptom": "肚子痛，而且一直拉肚子", "expected": "內科"},
    {"symptom": "胸口悶悶的，感覺呼吸不太順", "expected": "內科"},
    {"symptom": "頭暈想吐，量體溫好像有點發燒", "expected": "內科"},
    {"symptom": "最近一直頻尿，尿尿會有灼熱感", "expected": "內科"},
    {"symptom": "胃酸逆流，火燒心的感覺", "expected": "內科"},
    {"symptom": "血壓很高，覺得脖子緊緊的", "expected": "內科"},
    {"symptom": "最近一直覺得口渴，喝很多水還是渴，體重減輕", "expected": "內科"}, # 糖尿病徵兆
    {"symptom": "心臟突然跳很快，感覺心悸，很不舒服", "expected": "內科"},
    {"symptom": "臉色蒼白，站起來容易頭暈，感覺是貧血", "expected": "內科"},
    {"symptom": "晚上都睡不著，失眠好幾天了，精神很差", "expected": "內科"}, # 或身心科，一般導診先歸內科

    # --- 外科 (Surgery) [10題] ---
    {"symptom": "切水果不小心切到手，傷口很深流血", "expected": "外科"},
    {"symptom": "跌倒撞到膝蓋，現在腫起來不能走路", "expected": "外科"},
    {"symptom": "被熱水燙傷，皮膚起水泡紅腫", "expected": "外科"},
    {"symptom": "車禍擦傷，傷口有沙子要處理", "expected": "外科"},
    {"symptom": "好像長了痔瘡，坐著會痛", "expected": "外科"},
    {"symptom": "肩膀脫臼了，手舉不起來", "expected": "外科"},
    {"symptom": "右下腹突然劇痛，痛到站不起來，想吐", "expected": "外科"}, # 盲腸炎徵兆
    {"symptom": "被野狗咬到小腿，傷口流血", "expected": "外科"},
    {"symptom": "背部長了一個粉瘤（凸起物），越來越大顆", "expected": "外科"},
    {"symptom": "腳趾甲凍甲（甲溝炎），走路刺痛流膿", "expected": "外科"},

    # --- 耳鼻喉科 (ENT) [10題] ---
    {"symptom": "喉嚨超級痛，吞口水像被刀割", "expected": "耳鼻喉科"},
    {"symptom": "鼻子過敏一直打噴嚏流鼻水", "expected": "耳鼻喉科"},
    {"symptom": "耳朵裡面好像有蟲跑進去，嗡嗡叫", "expected": "耳鼻喉科"},
    {"symptom": "聲音沙啞，講不出話來", "expected": "耳鼻喉科"},
    {"symptom": "扁桃腺發炎腫起來了", "expected": "耳鼻喉科"},
    {"symptom": "流鼻血流不停", "expected": "耳鼻喉科"},
    {"symptom": "突然天旋地轉，躺著也暈，想吐", "expected": "耳鼻喉科"}, # 眩暈症
    {"symptom": "耳朵聽不太清楚，好像塞住了一樣", "expected": "耳鼻喉科"},
    {"symptom": "吃飯不小心吞到魚刺，卡在喉嚨", "expected": "耳鼻喉科"},
    {"symptom": "嘴巴裡面破好幾個洞（口內炎），痛到不能吃東西", "expected": "耳鼻喉科"},

    # --- 皮膚科 (Dermatology) [10題] ---
    {"symptom": "臉上長了很多青春痘，想治療", "expected": "皮膚科"},
    {"symptom": "背上長了一圈紅紅的疹子，很癢", "expected": "皮膚科"},
    {"symptom": "腳底長了雞眼，走路會痛", "expected": "皮膚科"},
    {"symptom": "頭皮屑很多，而且頭皮會癢", "expected": "皮膚科"},
    {"symptom": "手指甲灰灰的，好像是灰指甲", "expected": "皮膚科"},
    {"symptom": "全身起蕁麻疹，癢到受不了", "expected": "皮膚科"},
    {"symptom": "最近掉髮很嚴重，頭頂禿了一塊", "expected": "皮膚科"},
    {"symptom": "腳底長了病毒疣，摸起來硬硬的", "expected": "皮膚科"},
    {"symptom": "去海邊曬傷，背部紅腫脫皮，很痛", "expected": "皮膚科"},
    {"symptom": "身上的黑痣最近變大，形狀怪怪的", "expected": "皮膚科"},

    # --- 眼科 (Ophthalmology) [10題] ---
    {"symptom": "眼睛紅紅的，分泌物很多", "expected": "眼科"},
    {"symptom": "看東西模糊，覺得眼前有黑影", "expected": "眼科"},
    {"symptom": "眼睛乾澀，覺得刺刺的", "expected": "眼科"},
    {"symptom": "長針眼了，眼皮腫起來", "expected": "眼科"},
    {"symptom": "覺得近視好像加深了，看不清楚", "expected": "眼科"},
    {"symptom": "隱形眼鏡拿不下來，眼睛很痛", "expected": "眼科"},
    {"symptom": "眼前有蚊子在飛的感覺（飛蚊症）", "expected": "眼科"},
    {"symptom": "眼睛很酸，眼壓好像很高，頭有點痛", "expected": "眼科"},
    {"symptom": "眼白部分出血，紅紅一大塊", "expected": "眼科"},
    {"symptom": "看直線會彎曲，視力變形", "expected": "眼科"}
]

correct_count = 0
results = []


print(f"🚀 開始測試中文語料，共 {len(test_cases)} 題...\n")
print("⏳ 為了符合 API 速率限制 (15 RPM)，每題將間隔 5 秒，請耐心等待約 4 分鐘...")

valid_departments = "內科、外科、耳鼻喉科、皮膚科、眼科"

for i, case in enumerate(test_cases):
    # 模仿後端 Prompt (保持一致性)
    prompt = f"""
    You are a professional Hospital Triage AI.
    
    Patient Symptom (Chinese-zh): "{case['symptom']}"
    
    Task:
    1. First, analyze the root cause and severity of the symptom (e.g., trauma, infection, or chronic issue).
    2. Then, select the ONE most suitable department from this list: [{valid_departments}].
    
    Output Requirements:
    - Output ONLY the department name from the list in Chinese-zh.
    - Do NOT output your analysis or any other text.
    """
    
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 記錄開始時間
            start_time = time.time()
            
            response = model.generate_content(prompt)
            ai_reply = response.text.strip()
            
            # 判斷邏輯
            is_correct = case['expected'] in ai_reply
            
            status = "✅" if is_correct else "❌"
            if is_correct:
                correct_count += 1
                
            # 顯示進度
            print(f"[{i+1}/{len(test_cases)}] {status} | 症狀: {case['symptom'][:10]}... -> 預期: {case['expected']} | AI: {ai_reply}")
            
            # 記錄詳細結果
            results.append({
                "編號": i+1,
                "症狀": case['symptom'],
                "預期科別": case['expected'],
                "AI 回答": ai_reply,
                "結果": "通過" if is_correct else "失敗"
            })
            
            # 成功了就跳出重試迴圈
            break 
            
        except Exception as e:
            if "429" in str(e): # 如果是速率限制錯誤
                print(f"⚠️ 速度太快了 (Case {i+1})，正在冷靜 30 秒後重試... (嘗試 {attempt+1}/{max_retries})")
                time.sleep(30) # 遇到錯誤時，休息久一點
            else:
                print(f"⚠️ Error at case {i+1}: {e}")
                break # 其他錯誤就不重試了


    time.sleep(5) 



# 計算與顯示結果
accuracy = (correct_count / len(test_cases)) * 100
print(f"\n{'='*30}")
print(f"🏆 測試結束！")
print(f"總題數: {len(test_cases)}")
print(f"成功: {correct_count}")
print(f"失敗: {len(test_cases) - correct_count}")
print(f"準確率: {accuracy:.2f}%")
print(f"{'='*30}")

# 匯出 Excel (如果有裝 openpyxl)
try:
    df = pd.DataFrame(results)
    filename = "ai_test_result_zh_50.csv" # 存成 csv 比較通用
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"📄 詳細報告已儲存為: {filename}")
except Exception as e:
    print(f"存檔失敗 (可能是沒裝 pandas): {e}")