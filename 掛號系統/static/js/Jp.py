import google.generativeai as genai
import os
import time
import pandas as pd
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

# 設定你的 API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ 找不到 GOOGLE_API_KEY，請檢查 .env 檔案設定！")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# ===  完整日文測試集 (50題 / 50 Cases) ===
test_cases = [
    # --- Internal Medicine (内科) ---
    {"symptom": "お腹が痛くて、下痢が止まりません。", "expected": "内科"},
    {"symptom": "胸が苦しくて、息をするのが辛いです。", "expected": "内科"},
    {"symptom": "めまいがして吐き気があり、熱もあるようです。", "expected": "内科"},
    {"symptom": "最近トイレが近く、排尿時に痛みがあります。", "expected": "内科"},
    {"symptom": "胸焼けがして、酸っぱいものがこみ上げてくる感じがします。", "expected": "内科"}, # 胃食道逆流
    {"symptom": "血圧が高くて、首の後ろが張っている感じがします。", "expected": "内科"},
    {"symptom": "喉が渇いて仕方なく、水をたくさん飲んでいるのに体重が減っています。", "expected": "内科"}, # 糖尿病症狀
    {"symptom": "心臓がドキドキして（動悸）、胸がざわざわします。", "expected": "内科"},
    {"symptom": "顔色が悪く、立ち上がるとめまいがします（貧血気味）。", "expected": "内科"},
    {"symptom": "何日も眠れなくて（不眠）、疲れが取れません。", "expected": "内科"},

    # --- Surgery (外科) ---
    {"symptom": "果物を切っていて手を深く切ってしまい、血が止まりません。", "expected": "外科"},
    {"symptom": "転んで膝を打ち、腫れあがって歩けません。", "expected": "外科"},
    {"symptom": "お湯で火傷をしてしまい、皮膚が赤くなって水ぶくれができました。", "expected": "外科"},
    {"symptom": "交通事故で擦り傷を負い、傷口に砂が入っています。", "expected": "外科"},
    {"symptom": "痔のようで、座るとお尻が痛いです。", "expected": "外科"},
    {"symptom": "肩が外れたようで（脱臼）、腕が上がりません。", "expected": "外科"},
    {"symptom": "右下腹部が激しく痛みます、盲腸かもしれません。", "expected": "外科"},
    {"symptom": "野良犬に足を噛まれて、出血しています。", "expected": "外科"},
    {"symptom": "背中にしこり（粉瘤）ができて、だんだん大きくなっています。", "expected": "外科"},
    {"symptom": "足の爪が食い込んで（巻き爪）、化膿して痛いです。", "expected": "外科"},

    # --- ENT (耳鼻科) *您的系統設定為「耳鼻科」---
    {"symptom": "喉が激しく痛くて、飲み込むとカミソリで切られたようです。", "expected": "耳鼻科"},
    {"symptom": "鼻炎で、くしゃみと鼻水が止まりません。", "expected": "耳鼻科"},
    {"symptom": "耳の中で虫が羽ばたいているような音がします。", "expected": "耳鼻科"},
    {"symptom": "声が枯れてしまって、うまく話せません。", "expected": "耳鼻科"},
    {"symptom": "扁桃腺が腫れて痛いです。", "expected": "耳鼻科"},
    {"symptom": "鼻血が出て、なかなか止まりません。", "expected": "耳鼻科"},
    {"symptom": "目が回るようで（めまい）、吐き気がします。", "expected": "耳鼻科"}, # 梅尼爾氏症等眩暈常看耳鼻科
    {"symptom": "耳が詰まった感じで、音がよく聞こえません。", "expected": "耳鼻科"},
    {"symptom": "魚の骨を飲み込んでしまって、喉に刺さっています。", "expected": "耳鼻科"},
    {"symptom": "口内炎がたくさんできて痛くて、食事ができません。", "expected": "耳鼻科"},

    # --- Dermatology (皮膚科) ---
    {"symptom": "顔にニキビがたくさんできて、治療したいです。", "expected": "皮膚科"},
    {"symptom": "背中に赤い発疹ができて、すごく痒いです。", "expected": "皮膚科"},
    {"symptom": "足の裏に魚の目ができて、歩くと痛いです。", "expected": "皮膚科"},
    {"symptom": "フケがひどくて、頭皮が痒いです。", "expected": "皮膚科"},
    {"symptom": "足の爪が白く濁って厚くなっています（爪水虫）。", "expected": "皮膚科"},
    {"symptom": "全身に蕁麻疹が出て、痒くてたまりません。", "expected": "皮膚科"},
    {"symptom": "最近抜け毛がひどくて、円形脱毛症のようです。", "expected": "皮膚科"},
    {"symptom": "足の裏に硬いイボができました。", "expected": "皮膚科"},
    {"symptom": "海で日焼けをして、背中の皮がむけてヒリヒリ痛いです。", "expected": "皮膚科"},
    {"symptom": "体のほくろが最近大きくなって、形が変わってきました。", "expected": "皮膚科"},

    # --- Ophthalmology (眼科) ---
    {"symptom": "目が真っ赤で、目やにが多いです。", "expected": "眼科"},
    {"symptom": "視界がぼやけて、黒い影が見えます。", "expected": "眼科"},
    {"symptom": "目が乾いて（ドライアイ）、ゴロゴロします。", "expected": "眼科"},
    {"symptom": "ものもらいができて、まぶたが腫れています。", "expected": "眼科"},
    {"symptom": "近視が進んだようで、遠くが見えにくいです。", "expected": "眼科"},
    {"symptom": "コンタクトレンズが外れなくて、目が痛いです。", "expected": "眼科"},
    {"symptom": "目の前に蚊が飛んでいるようなものが見えます（飛蚊症）。", "expected": "眼科"},
    {"symptom": "目の奥が痛くて、頭痛もします（眼精疲労）。", "expected": "眼科"},
    {"symptom": "白目の部分が出血して、赤くなっています。", "expected": "眼科"},
    {"symptom": "直線が歪んで見えます。", "expected": "眼科"}
]

correct_count = 0
results = []

print(f"🚀 日本語のテストを開始します。全 {len(test_cases)} 件...\n")
print("⏳ APIレート制限回避のため、5秒間隔で実行します（約4分かかります）...")

# 您的前端 index.js 使用的日文選項
valid_departments = "内科, 外科, 耳鼻科, 皮膚科, 眼科"

for i, case in enumerate(test_cases):
    # 使用包含「思維引導 (Step-by-step)」的 Prompt，以獲得最高準確率
    prompt = f"""
    You are a professional Hospital Triage AI.
    
    Patient Symptom (Japanese): "{case['symptom']}"
    
    Task:
    1. First, analyze the root cause and severity of the symptom (e.g., trauma, infection, or chronic issue).
    2. Then, select the ONE most suitable department from this list: [{valid_departments}].
    
    Output Requirements:
    - Output ONLY the department name from the list in Japanese.
    - Do NOT output your analysis or any other text.
    """
    
    # 重試機制
    max_retries = 3
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            response = model.generate_content(prompt)
            ai_reply = response.text.strip()
            
            # 判斷邏輯
            is_correct = case['expected'] in ai_reply
            
            status = "✅" if is_correct else "❌"
            if is_correct:
                correct_count += 1
                
            print(f"[{i+1}/{len(test_cases)}] {status} | 症状: {case['symptom'][:15]}... -> 予想: {case['expected']} | AI: {ai_reply}")
            
            results.append({
                "ID": i+1,
                "Symptom": case['symptom'],
                "Expected": case['expected'],
                "AI_Reply": ai_reply,
                "Result": "Pass" if is_correct else "Fail"
            })
            
            break 
            
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Rate limit hit (Case {i+1}), cooling down for 30s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(30)
            else:
                print(f"⚠️ Error at case {i+1}: {e}")
                break

    time.sleep(5) 

# 計算結果
accuracy = (correct_count / len(test_cases)) * 100
print(f"\n{'='*30}")
print(f"🏆 テスト終了！ (Test Finished)")
print(f"Total Cases: {len(test_cases)}")
print(f"Success: {correct_count}")
print(f"Failed: {len(test_cases) - correct_count}")
print(f"Accuracy: {accuracy:.2f}%")
print(f"{'='*30}")

# 存檔
try:
    df = pd.DataFrame(results)
    filename = "ai_test_result_ja_50.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"📄 Report saved to: {filename}")
except Exception as e:
    print(f"Save failed: {e}")