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
model = genai.GenerativeModel('gemini-2.5-flash')

# ===  完整韓文測試集 (50題 / 50 Cases) ===
test_cases = [
    # --- Internal Medicine (내과) ---
    {"symptom": "배가 너무 아프고 설사가 멈추지 않아요.", "expected": "내과"}, # 肚子痛腹瀉
    {"symptom": "가슴이 답답하고 숨쉬기가 힘들어요.", "expected": "내과"}, # 胸悶呼吸困難
    {"symptom": "어지럽고 토할 것 같고, 열도 있는 것 같아요.", "expected": "내과"}, # 頭暈想吐發燒
    {"symptom": "최근 소변을 자주 보고, 볼 때마다 따끔거려요.", "expected": "내과"}, # 頻尿灼熱
    {"symptom": "위산이 역류해서 가슴이 타는 듯한 느낌이 들어요.", "expected": "내과"}, # 胃食道逆流
    {"symptom": "혈압이 높고 뒷목이 뻣뻣한 느낌이에요.", "expected": "내과"}, # 高血壓脖子緊
    {"symptom": "계속 목이 마르고 물을 많이 마시는데도 살이 빠져요.", "expected": "내과"}, # 糖尿病徵兆
    {"symptom": "심장이 너무 빨리 뛰고(두근거림) 불편해요.", "expected": "내과"}, # 心悸
    {"symptom": "얼굴이 창백하고 일어서면 어지러워요(빈혈).", "expected": "내과"}, # 貧血
    {"symptom": "며칠째 잠을 못 자서(불면증) 너무 피곤해요.", "expected": "내과"}, # 失眠

    # --- Surgery (외과) ---
    {"symptom": "과일을 깎다가 손을 깊게 베여서 피가 많이 나요.", "expected": "외과"}, # 切到手
    {"symptom": "넘어져서 무릎을 부딪혔는데, 퉁퉁 부어서 걸을 수가 없어요.", "expected": "외과"}, # 跌倒撞膝蓋
    {"symptom": "뜨거운 물에 데어서 피부가 빨개지고 물집이 잡혔어요.", "expected": "외과"}, # 燙傷
    {"symptom": "자전거 사고로 찰과상을 입었는데 상처에 모래가 들어갔어요.", "expected": "외과"}, # 車禍擦傷
    {"symptom": "치질인 것 같은데, 앉을 때마다 아파요.", "expected": "외과"}, # 痔瘡
    {"symptom": "어깨가 빠진 것 같아요(탈구), 팔을 들 수가 없어요.", "expected": "외과"}, # 脫臼
    {"symptom": "오른쪽 아랫배가 심하게 아파요, 맹장염 같아요.", "expected": "외과"}, # 盲腸炎
    {"symptom": "길거리 개한테 다리를 물려서 피가 나요.", "expected": "외과"}, # 被狗咬
    {"symptom": "등에 혹(피지낭종)이 생겼는데 점점 커지고 있어요.", "expected": "외과"}, # 粉瘤
    {"symptom": "발톱이 살을 파고들어서(내성발톱) 곪고 아파요.", "expected": "외과"}, # 凍甲

    # --- ENT (이비인후과) ---
    {"symptom": "목이 너무 아파서 침을 삼키면 칼로 베는 것 같아요.", "expected": "이비인후과"}, # 喉嚨痛
    {"symptom": "비염 때문에 재채기와 콧물이 멈추지 않아요.", "expected": "이비인후과"}, # 過敏流鼻水
    {"symptom": "귀 안에서 벌레가 날아다니는 듯한 소리가 들려요.", "expected": "이비인후과"}, # 耳鳴/蟲
    {"symptom": "목소리가 쉬어서 말이 잘 안 나와요.", "expected": "이비인후과"}, # 沙啞
    {"symptom": "편도선이 부어서 아파요.", "expected": "이비인후과"}, # 扁桃腺
    {"symptom": "코피가 나는데 멈추지 않아요.", "expected": "이비인후과"}, # 流鼻血
    {"symptom": "세상이 빙글빙글 도는 것 같고(현기증) 토할 것 같아요.", "expected": "이비인후과"}, # 眩暈
    {"symptom": "귀가 막힌 느낌이고 소리가 잘 안 들려요.", "expected": "이비인후과"}, # 耳朵塞住
    {"symptom": "생선 가시를 삼켰는데 목에 걸린 것 같아요.", "expected": "이비인후과"}, # 魚刺
    {"symptom": "입안이 헐어서(구내염) 너무 아파서 밥을 못 먹겠어요.", "expected": "이비인후과"}, # 口內炎

    # --- Dermatology (피부과) ---
    {"symptom": "얼굴에 여드름이 많이 나서 치료받고 싶어요.", "expected": "피부과"}, # 青春痘
    {"symptom": "등에 붉은 발진이 생기고 너무 가려워요.", "expected": "피부과"}, # 紅疹
    {"symptom": "발바닥에 티눈이 생겨서 걸을 때 아파요.", "expected": "피부과"}, # 雞眼
    {"symptom": "비듬이 심하고 두피가 가려워요.", "expected": "피부과"}, # 頭皮屑
    {"symptom": "손톱이 회색으로 변하고 두꺼워졌어요(무좀).", "expected": "피부과"}, # 灰指甲
    {"symptom": "온몸에 두드러기가 나서 미치도록 가려워요.", "expected": "피부과"}, # 蕁麻疹
    {"symptom": "요즘 머리카락이 많이 빠져서 원형탈모 같아요.", "expected": "피부과"}, # 掉髮
    {"symptom": "발바닥에 딱딱한 사마귀가 생겼어요.", "expected": "피부과"}, # 病毒疣
    {"symptom": "바닷가에서 심하게 타서(일광화상) 등 껍질이 벗겨지고 따가워요.", "expected": "피부과"}, # 曬傷
    {"symptom": "몸에 있는 점이 최근에 커지고 모양이 이상해졌어요.", "expected": "피부과"}, # 黑痣變化

    # --- Ophthalmology (안과) ---
    {"symptom": "눈이 빨갛고 눈곱이 많이 껴요.", "expected": "안과"}, # 紅眼/分泌物
    {"symptom": "시야가 흐릿하고 검은 그림자가 보여요.", "expected": "안과"}, # 視力模糊
    {"symptom": "눈이 건조하고(안구건조증) 뻑뻑해요.", "expected": "안과"}, # 乾眼
    {"symptom": "다래끼가 나서 눈꺼풀이 부었어요.", "expected": "안과"}, # 針眼
    {"symptom": "근시가 심해진 것 같아서 멀리 있는 게 잘 안 보여요.", "expected": "안과"}, # 近視
    {"symptom": "콘택트렌즈가 안 빠져서 눈이 아파요.", "expected": "안과"}, # 隱形眼鏡
    {"symptom": "눈앞에 날파리가 날아다니는 것 같아요(비문증).", "expected": "안과"}, # 飛蚊症
    {"symptom": "눈 안쪽이 아프고 머리도 아파요(눈의 피로).", "expected": "안과"}, # 眼壓高/疲勞
    {"symptom": "흰자위가 터져서 빨갛게 충혈됐어요.", "expected": "안과"}, # 眼球出血
    {"symptom": "직선이 휘어져 보여요.", "expected": "안과"} # 視力變形
]

correct_count = 0
results = []

print(f"🚀 한국어 테스트를 시작합니다. 총 {len(test_cases)} 건...\n")
print("⏳ API 호출 제한을 피하기 위해 5초 간격으로 실행합니다 (약 4분 소요)...")

# 您的前端 index.js 使用的韓文選項
valid_departments = "내과, 외과, 이비인후과, 피부과, 안과"

for i, case in enumerate(test_cases):
    # 使用包含「思維引導 (Step-by-step)」的 Prompt
    prompt = f"""
    You are a professional Hospital Triage AI.
    
    Patient Symptom (Korean): "{case['symptom']}"
    
    Task:
    1. First, analyze the root cause and severity of the symptom (e.g., trauma, infection, or chronic issue).
    2. Then, select the ONE most suitable department from this list: [{valid_departments}].
    
    Output Requirements:
    - Output ONLY the department name from the list in Korean.
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
                
            print(f"[{i+1}/{len(test_cases)}] {status} | 증상: {case['symptom'][:15]}... -> 예상: {case['expected']} | AI: {ai_reply}")
            
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
print(f"🏆 테스트 종료! (Test Finished)")
print(f"Total Cases: {len(test_cases)}")
print(f"Success: {correct_count}")
print(f"Failed: {len(test_cases) - correct_count}")
print(f"Accuracy: {accuracy:.2f}%")
print(f"{'='*30}")

# 存檔
try:
    df = pd.DataFrame(results)
    filename = "ai_test_result_ko_50.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"📄 Report saved to: {filename}")
except Exception as e:
    print(f"Save failed: {e}")