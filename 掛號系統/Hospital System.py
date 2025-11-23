from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv
import firebase_admin 
from firebase_admin import credentials, firestore 

load_dotenv()

# 初始化 Firebase Admin
try:
    cred = credentials.Certificate("serviceAccountKey.json") 
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK 初始化成功！")
except Exception as e:
    print(f"Firebase Admin SDK 初始化失敗：{e}")

db = firestore.client() #取得 Firestore 資料庫的管理員權限

app = Flask(__name__)

# 設定 Gemini API 金鑰
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# 初始化 Gemini 模型（用最通用的版本）
model = genai.GenerativeModel('gemini-2.0-flash')

# 首頁：掛號主畫面
@app.route("/")
def index():
    return render_template("index.html")

# 獨立的 AI 導診頁面
@app.route("/askai")
def askai():
    return render_template("askai.html")

@app.route("/query")
def query_page():
    return render_template("query.html")

# Gemini 導診功能 API
@app.route("/ask", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        symptoms = data.get("symptoms")
        language = data.get("language", "zh-Hant")

        prompt = f"""
    你是一位醫院導診 AI 助手。

    病人會用任意語言（例如中文、英文、日文）描述他們的症狀，請你依照以下方式回應：
    1. 判斷最適合的掛號科別，盡量只推薦一個科別，除非症狀很模糊（例如：耳鼻喉科、內科、皮膚科）。
    2. 為每個推薦的科別提供簡短的說明。
    3. 若資訊不足，請友善地提醒病人可以補充哪些資訊。
    4. 務必使用 '{language}' 這個語言來覆用戶！如果是 'zh'，請使用繁體中文。
    5. 不要進行醫學診斷，只提供導診建議。
    6. 回應控制在 150 字以內，風格友善，符號簡潔。
    

    病人的症狀如下：
    「{symptoms}」

    """
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"An error occurred: {e}") # 在後台印出錯誤日誌
        return jsonify({"reply": "抱歉，AI 服務目前暫時無法使用，請稍後再試。"}), 500
    

@app.route("/api/query", methods=["POST"])
def query_registration():
    data = request.get_json()
    query_id_number = data.get("id_number")

    
    if not query_id_number:
        return jsonify({"error": "請提供身分證字號"}), 400

    try:
        registrations_ref = db.collection('registrations')
        query = registrations_ref.where('id_number', '==', query_id_number)
        docs = query.stream()

        results = []
        for doc in docs:
            results.append(doc.to_dict())

        if not results:
            return jsonify({"error_key": "NOT_FOUND"}), 404
        
        return jsonify(results)

    except Exception as e:
        print(f"查詢時發生錯誤: {e}")
        return jsonify({"error_key": "SERVER_ERROR"}), 500


if __name__ == "__main__":
    app.run(debug=True)
