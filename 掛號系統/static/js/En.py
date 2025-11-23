import google.generativeai as genai
import os
import time
import pandas as pd
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

# 設定你的 API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 檢查是否成功讀取 Key
if not GOOGLE_API_KEY:
    raise ValueError("❌ 找不到 GOOGLE_API_KEY，請檢查 .env 檔案設定！")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# === 🏥 完整英文測試集 (50題 / 50 Cases) ===
test_cases = [
    # --- Internal Medicine (內科) ---
    {"symptom": "I have a terrible stomach ache and diarrhea.", "expected": "Internal Medicine"},
    {"symptom": "My chest feels tight and I'm having trouble breathing.", "expected": "Internal Medicine"},
    {"symptom": "I feel dizzy, nauseous, and I think I have a fever.", "expected": "Internal Medicine"},
    {"symptom": "Frequent urination with a burning sensation.", "expected": "Internal Medicine"},
    {"symptom": "I have acid reflux and a burning feeling in my chest (heartburn).", "expected": "Internal Medicine"},
    {"symptom": "My blood pressure is very high and my neck feels stiff.", "expected": "Internal Medicine"},
    {"symptom": "I'm constantly thirsty, drinking lots of water but losing weight.", "expected": "Internal Medicine"}, # Diabetes signs
    {"symptom": "My heart is beating very fast (palpitations) and I feel uncomfortable.", "expected": "Internal Medicine"},
    {"symptom": "I look pale and feel dizzy whenever I stand up (anemia).", "expected": "Internal Medicine"},
    {"symptom": "I haven't been able to sleep for days (insomnia) and feel exhausted.", "expected": "Internal Medicine"},

    # --- Surgery (外科) ---
    {"symptom": "I cut my hand deeply while slicing fruit and it's bleeding heavily.", "expected": "Surgery"},
    {"symptom": "I fell on my knee, it's swollen and I can't walk.", "expected": "Surgery"},
    {"symptom": "I got burned by hot water, my skin is red and blistering.", "expected": "Surgery"},
    {"symptom": "I was in a bike accident and have road rash with debris in the wound.", "expected": "Surgery"},
    {"symptom": "I have hemorrhoids and it hurts when I sit down.", "expected": "Surgery"},
    {"symptom": "I think I dislocated my shoulder, I can't raise my arm.", "expected": "Surgery"},
    {"symptom": "Severe pain in my lower right abdomen, looking like appendicitis.", "expected": "Surgery"},
    {"symptom": "I was bitten by a stray dog on my leg and it's bleeding.", "expected": "Surgery"},
    {"symptom": "I have a growing lump (cyst) on my back.", "expected": "Surgery"},
    {"symptom": "I have an ingrown toenail that is infected and painful.", "expected": "Surgery"},

    # --- ENT (耳鼻喉科) ---
    {"symptom": "I have a severe sore throat, it feels like razor blades when I swallow.", "expected": "ENT"},
    {"symptom": "My nose is running constantly and I keep sneezing (allergies).", "expected": "ENT"},
    {"symptom": "I feel like there's a bug buzzing inside my ear.", "expected": "ENT"},
    {"symptom": "I lost my voice and sound very hoarse.", "expected": "ENT"},
    {"symptom": "My tonsils are swollen and painful.", "expected": "ENT"},
    {"symptom": "I have a nosebleed that won't stop.", "expected": "ENT"},
    {"symptom": "Everything is spinning (vertigo) and I feel like vomiting.", "expected": "ENT"},
    {"symptom": "My ear feels blocked and I can't hear clearly.", "expected": "ENT"},
    {"symptom": "I accidentally swallowed a fish bone and it's stuck in my throat.", "expected": "ENT"},
    {"symptom": "I have painful mouth ulcers (canker sores) and can't eat.", "expected": "ENT"},

    # --- Dermatology (皮膚科) ---
    {"symptom": "I have a lot of acne on my face and want treatment.", "expected": "Dermatology"},
    {"symptom": "I have a red, itchy rash all over my back.", "expected": "Dermatology"},
    {"symptom": "I have a corn on the bottom of my foot that hurts when I walk.", "expected": "Dermatology"},
    {"symptom": "I have severe dandruff and an itchy scalp.", "expected": "Dermatology"},
    {"symptom": "My fingernails are turning grey and thick (fungal infection).", "expected": "Dermatology"},
    {"symptom": "I broke out in hives all over my body and it's extremely itchy.", "expected": "Dermatology"},
    {"symptom": "I'm losing a lot of hair recently, there's a bald spot.", "expected": "Dermatology"},
    {"symptom": "I have a hard wart on the sole of my foot.", "expected": "Dermatology"},
    {"symptom": "I got a bad sunburn at the beach, my back is peeling and painful.", "expected": "Dermatology"},
    {"symptom": "A mole on my body is changing shape and growing bigger.", "expected": "Dermatology"},

    # --- Ophthalmology (眼科) ---
    {"symptom": "My eyes are very red and have a lot of discharge.", "expected": "Ophthalmology"},
    {"symptom": "My vision is blurry and I see dark shadows.", "expected": "Ophthalmology"},
    {"symptom": "My eyes feel dry, gritty, and irritated.", "expected": "Ophthalmology"},
    {"symptom": "I have a stye on my eyelid and it's swollen.", "expected": "Ophthalmology"},
    {"symptom": "I feel like my nearsightedness has gotten worse, I can't see clearly.", "expected": "Ophthalmology"},
    {"symptom": "My contact lens is stuck and my eye hurts.", "expected": "Ophthalmology"},
    {"symptom": "I see floating spots (floaters) moving in my vision.", "expected": "Ophthalmology"},
    {"symptom": "My eyes feel very pressured and sore, with a headache.", "expected": "Ophthalmology"},
    {"symptom": "The white part of my eye is bleeding (red patch).", "expected": "Ophthalmology"},
    {"symptom": "Straight lines look wavy and distorted to me.", "expected": "Ophthalmology"}
]

correct_count = 0
results = []

print(f"🚀 Starting English Test with {len(test_cases)} cases...\n")
print("⏳ Waiting 5 seconds between requests to avoid Rate Limits (approx. 4 mins)...")

# 你的前端 index.js 使用的英文選項
valid_departments = "Internal Medicine, Surgery, ENT, Dermatology, Ophthalmology"

for i, case in enumerate(test_cases):
    # Prompt 改為全英文指令，確保 AI 進入英文模式
    prompt = f"""
    You are a professional Hospital Triage AI.
    
    Patient Symptom: "{case['symptom']}"
    
    Task:
    1. First, analyze the root cause and severity of the symptom (e.g., trauma, infection, or chronic issue).
    2. Then, select the ONE most suitable department from this list: [{valid_departments}].
    
    Output Requirements:
    - Output ONLY the department name from the list.
    - Do NOT output your analysis or any other text.
    """
    
    # 重試機制 (與中文版相同)
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
                
            print(f"[{i+1}/{len(test_cases)}] {status} | Symptom: {case['symptom'][:20]}... -> Exp: {case['expected']} | AI: {ai_reply}")
            
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
print(f"🏆 Test Finished!")
print(f"Total Cases: {len(test_cases)}")
print(f"Success: {correct_count}")
print(f"Failed: {len(test_cases) - correct_count}")
print(f"Accuracy: {accuracy:.2f}%")
print(f"{'='*30}")

# 存檔
try:
    df = pd.DataFrame(results)
    filename = "ai_test_result_en_50.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"📄 Report saved to: {filename}")
except Exception as e:
    print(f"Save failed: {e}")