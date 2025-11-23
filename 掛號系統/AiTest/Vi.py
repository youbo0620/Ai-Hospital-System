import google.generativeai as genai
import os
import time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ 找不到 GOOGLE_API_KEY，請檢查 .env 檔案設定！")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# === 🇻🇳 完整越南文測試集 (50 Cases) ===
test_cases = [
    # --- Nội khoa (Internal Medicine) ---
    {"symptom": "Đau bụng dữ dội và bị tiêu chảy liên tục.", "expected": "Nội khoa"}, # 腹痛腹瀉
    {"symptom": "Tức ngực, cảm thấy khó thở.", "expected": "Nội khoa"}, # 胸悶
    {"symptom": "Hoa mắt, chóng mặt, buồn nôn và hình như bị sốt.", "expected": "Nội khoa"}, # 頭暈發燒
    {"symptom": "Gần đây đi tiểu nhiều lần, cảm thấy đau rát khi tiểu.", "expected": "Nội khoa"}, # 頻尿灼熱
    {"symptom": "Bị trào ngược axit, cảm giác nóng rát ở ngực (ợ nóng).", "expected": "Nội khoa"}, # 胃食道逆流
    {"symptom": "Huyết áp cao, cảm thấy cứng cổ.", "expected": "Nội khoa"}, # 高血壓
    {"symptom": "Luôn cảm thấy khát nước, uống nhiều nước nhưng vẫn sụt cân.", "expected": "Nội khoa"}, # 糖尿病
    {"symptom": "Tim đập rất nhanh (hồi hộp) và cảm thấy khó chịu.", "expected": "Nội khoa"}, # 心悸
    {"symptom": "Mặt tái nhợt, đứng lên là bị chóng mặt (thiếu máu).", "expected": "Nội khoa"}, # 貧血
    {"symptom": "Mất ngủ nhiều ngày nay, người rất mệt mỏi.", "expected": "Nội khoa"}, # 失眠

    # --- Ngoại khoa (Surgery) ---
    {"symptom": "Cắt hoa quả bị dao cứa sâu vào tay, máu chảy nhiều.", "expected": "Ngoại khoa"}, # 切到手
    {"symptom": "Bị ngã đập đầu gối, giờ sưng to không đi được.", "expected": "Ngoại khoa"}, # 跌倒撞膝蓋
    {"symptom": "Bị bỏng nước sôi, da đỏ và nổi mụn nước.", "expected": "Ngoại khoa"}, # 燙傷
    {"symptom": "Bị tai nạn xe máy, trầy xước da và có cát bụi trong vết thương.", "expected": "Ngoại khoa"}, # 車禍擦傷
    {"symptom": "Hình như bị trĩ, ngồi xuống là đau.", "expected": "Ngoại khoa"}, # 痔瘡
    {"symptom": "Hình như bị trật khớp vai, không nhấc tay lên được.", "expected": "Ngoại khoa"}, # 脫臼
    {"symptom": "Đau dữ dội vùng bụng dưới bên phải, giống như viêm ruột thừa.", "expected": "Ngoại khoa"}, # 盲腸炎
    {"symptom": "Bị chó hoang cắn vào chân, đang chảy máu.", "expected": "Ngoại khoa"}, # 狗咬
    {"symptom": "Có một khối u (u nang) ở lưng, ngày càng to ra.", "expected": "Ngoại khoa"}, # 粉瘤
    {"symptom": "Móng chân mọc ngược đâm vào thịt, sưng mủ và đau.", "expected": "Ngoại khoa"}, # 凍甲

    # --- Tai Mũi Họng (ENT) ---
    {"symptom": "Đau họng kinh khủng, nuốt nước bọt đau như bị dao cứa.", "expected": "Tai Mũi Họng"}, # 喉嚨痛
    {"symptom": "Bị viêm mũi dị ứng, hắt hơi và chảy nước mũi liên tục.", "expected": "Tai Mũi Họng"}, # 過敏
    {"symptom": "Cảm giác như có con gì bay vo ve trong tai.", "expected": "Tai Mũi Họng"}, # 耳鳴/蟲
    {"symptom": "Bị khản tiếng, không nói ra hơi.", "expected": "Tai Mũi Họng"}, # 沙啞
    {"symptom": "Amidan bị sưng và đau.", "expected": "Tai Mũi Họng"}, # 扁桃腺
    {"symptom": "Chảy máu cam không cầm được.", "expected": "Tai Mũi Họng"}, # 流鼻血
    {"symptom": "Cảm thấy trời đất quay cuồng (chóng mặt), buồn nôn.", "expected": "Tai Mũi Họng"}, # 眩暈
    {"symptom": "Tai bị ù, nghe không rõ.", "expected": "Tai Mũi Họng"}, # 耳塞
    {"symptom": "Nuốt phải xương cá, bị mắc kẹt trong họng.", "expected": "Tai Mũi Họng"}, # 魚刺
    {"symptom": "Bị nhiệt miệng (loét miệng) đau không ăn được.", "expected": "Tai Mũi Họng"}, # 口內炎

    # --- Da liễu (Dermatology) ---
    {"symptom": "Mặt nổi nhiều mụn trứng cá, muốn điều trị.", "expected": "Da liễu"}, # 青春痘
    {"symptom": "Lưng nổi mẩn đỏ, rất ngứa.", "expected": "Da liễu"}, # 紅疹
    {"symptom": "Bị chai chân ở lòng bàn chân, đi lại rất đau.", "expected": "Da liễu"}, # 雞眼
    {"symptom": "Nhiều gàu và da đầu rất ngứa.", "expected": "Da liễu"}, # 頭皮屑
    {"symptom": "Móng tay chuyển màu xám và dày lên (nấm móng).", "expected": "Da liễu"}, # 灰指甲
    {"symptom": "Nổi mề đay khắp người, ngứa không chịu nổi.", "expected": "Da liễu"}, # 蕁麻疹
    {"symptom": "Gần đây rụng tóc nhiều, có mảng hói trên đầu.", "expected": "Da liễu"}, # 掉髮
    {"symptom": "Lòng bàn chân mọc mụn cóc cứng.", "expected": "Da liễu"}, # 病毒疣
    {"symptom": "Đi biển bị cháy nắng, da lưng bong tróc và đau rát.", "expected": "Da liễu"}, # 曬傷
    {"symptom": "Nốt ruồi trên cơ thể to lên và thay đổi hình dạng.", "expected": "Da liễu"}, # 黑痣

    # --- Mắt (Ophthalmology) ---
    {"symptom": "Mắt đỏ ngầu và có nhiều ghèn.", "expected": "Mắt"}, # 紅眼
    {"symptom": "Nhìn mờ, thấy có bóng đen trước mắt.", "expected": "Mắt"}, # 視力模糊
    {"symptom": "Mắt bị khô, cảm giác cộm xốn.", "expected": "Mắt"}, # 乾眼
    {"symptom": "Bị lẹo mắt, mí mắt sưng lên.", "expected": "Mắt"}, # 針眼
    {"symptom": "Cảm giác cận thị nặng hơn, nhìn xa không rõ.", "expected": "Mắt"}, # 近視
    {"symptom": "Kính áp tròng bị kẹt, mắt rất đau.", "expected": "Mắt"}, # 隱形眼鏡
    {"symptom": "Thấy có đốm đen bay trước mắt (hiện tượng ruồi bay).", "expected": "Mắt"}, # 飛蚊症
    {"symptom": "Nhức hốc mắt, đau đầu (mỏi mắt).", "expected": "Mắt"}, # 眼壓高
    {"symptom": "Lòng trắng mắt bị xuất huyết đỏ.", "expected": "Mắt"}, # 出血
    {"symptom": "Nhìn đường thẳng thấy bị cong méo.", "expected": "Mắt"} # 視力變形
]

correct_count = 0
results = []

print(f"🚀 Bắt đầu kiểm tra tiếng Việt ({len(test_cases)} cases)...\n")
print("⏳ Đang chạy 5s/câu để tránh giới hạn API (khoảng 4 phút)...")

# 您的前端 index.js 使用的越南文選項
valid_departments = "Nội khoa, Ngoại khoa, Tai Mũi Họng, Da liễu, Mắt"

for i, case in enumerate(test_cases):
    prompt = f"""
    You are a professional Hospital Triage AI.
    
    Patient Symptom (Vietnamese): "{case['symptom']}"
    
    Task:
    1. First, analyze the root cause and severity of the symptom (e.g., trauma, infection, or chronic issue).
    2. Then, select the ONE most suitable department from this list: [{valid_departments}].
    
    Output Requirements:
    - Output ONLY the department name from the list in Vietnamese.
    - Do NOT output your analysis or any other text.
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            response = model.generate_content(prompt)
            ai_reply = response.text.strip()
            
            is_correct = case['expected'] in ai_reply
            status = "✅" if is_correct else "❌"
            if is_correct:
                correct_count += 1
                
            print(f"[{i+1}/{len(test_cases)}] {status} | Triệu chứng: {case['symptom'][:15]}... -> {case['expected']} | AI: {ai_reply}")
            
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
                print(f"⚠️ Rate limit hit (Case {i+1}), cooling down for 30s...")
                time.sleep(30)
            else:
                print(f"⚠️ Error at case {i+1}: {e}")
                break

    time.sleep(5) 

accuracy = (correct_count / len(test_cases)) * 100
print(f"\n{'='*30}")
print(f"🏆 Kết thúc kiểm tra! (Test Finished)")
print(f"Accuracy: {accuracy:.2f}%")
print(f"{'='*30}")

try:
    df = pd.DataFrame(results)
    df.to_csv("ai_test_result_vi_50.csv", index=False, encoding='utf-8-sig')
    print("📄 Saved to ai_test_result_vi_50.csv")
except:
    pass