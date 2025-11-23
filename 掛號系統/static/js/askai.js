const translations = {
  zh: {
    title: " AI 導診系統",
    description: "請輸入您的症狀，AI 會協助建議適合的掛號科別：",
    ask: "送出給 AI",
    result: "AI 建議：",
    back: "⬅ 回掛號主畫面",
    placeholder: "例如：喉嚨痛、頭暈..."
  },
  en: {
    title: " AI Triage Assistant",
    description: "Please enter your symptoms. The AI will suggest a suitable department:",
    ask: "Ask AI",
    result: "AI Suggestion:",
    back: "⬅ Back to Home",
    placeholder: "e.g. ,sore throat, dizziness..."
  },
  ja: {
    title: " AI 診療補助",
    description: "症状を入力してください。AI が適切な診療科を提案します：",
    ask: "AIに送信",
    result: "AIの提案：",
    back: "⬅ 予約フォームへ戻る",
    placeholder: "例：喉の痛み、めまい..."
  },
  ko: {
    title: " AI 진료 보조 시스템",
    description: "증상을 입력하세요. AI가 적절한 진료과를 추천합니다:",
    ask: "AI에게 보내기",
    result: "AI의 추천:",
    back: "⬅ 예약 화면으로 돌아가기",
    placeholder: "예: 인후통, 어지러움..."
  },
  vi: {
    title: " Hệ thống tư vấn khám bệnh AI",
    description: "Vui lòng nhập triệu chứng của bạn. AI sẽ gợi ý chuyên khoa phù hợp:",
    ask: "Gửi cho AI",
    result: "Gợi ý từ AI:",
    back: "⬅ Quay lại đăng ký",
    placeholder: "ví dụ: đau họng, chóng mặt..."
  },
  th: {
    title: " ผู้ช่วยแนะนำแผนกด้วย AI",
    description: "กรุณากรอกอาการของคุณ ระบบ AI จะเสนอแผนกที่เหมาะสม:",
    ask: "ส่งข้อมูลให้ AI",
    result: "คำแนะนำจาก AI:",
    back: "⬅ กลับหน้าลงทะเบียน",
    placeholder: "เช่น เจ็บคอ เวียนศีรษะ..."
  }
};

function switchLanguage() {
  const lang = document.getElementById("language").value;
  const t = translations[lang];

  document.getElementById("title").innerText = t.title;
  document.getElementById("description").innerText = t.description;
  document.getElementById("ask-btn").innerHTML = `<i class="bi bi-send-fill me-2"></i>${t.ask}`; // 保留圖示
  document.getElementById("result-label").innerText = t.result;
  document.getElementById("back-btn").innerHTML = `<i class="bi bi-arrow-left-circle me-1"></i> ${t.back}`; // 保留圖示
  document.getElementById("symptoms").placeholder = t.placeholder;
}


async function askAI() {
  const symptomsInput = document.getElementById("symptoms");
  const symptoms = symptomsInput.value;
  const lang = document.getElementById("language").value;
  const responseArea = document.getElementById("response-area");
  const responseContent = document.getElementById("response-content");
  const loading = document.getElementById("loading");

  // 防呆
  if (!symptoms.trim()) {
    const errorMsg = {
      zh: "請輸入症狀！",
      en: "Please enter symptoms!",
      ja: "症状を入力してください！",
      ko: "증상을 입력하세요!",
      vi: "Vui lòng nhập triệu chứng!",
      th: "กรุณากรอกอาการ!"
    };
    alert(errorMsg[lang] || "請輸入症狀！");
    return;
  }

  
  responseArea.style.display = "none";
  loading.style.display = "block";
  responseContent.innerHTML = ""; 

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symptoms: symptoms, language: lang })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

   
    loading.style.display = "none";
    responseArea.style.display = "block"; 
    
   
    if (typeof marked !== 'undefined') {
        responseContent.innerHTML = marked.parse(data.reply);
    } else {
        responseContent.innerText = data.reply;
    }

  } catch (error) {
    console.error("Error:", error);
    loading.style.display = "none";
    alert("系統發生錯誤，請檢查後端連線或稍後再試。");
  }
}

// 語音辨識功能
function startSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("❌ 抱歉，您的瀏覽器不支援語音辨識功能。請嘗試使用 Chrome 或 Edge 瀏覽器。");
    return;
  }

  const recognition = new SpeechRecognition();
  const symptomsTextarea = document.getElementById("symptoms");
  const voiceBtn = document.getElementById("voice-btn");

  const langMap = { "zh": "zh-TW", "en": "en-US", "ja": "ja-JP", "ko": "ko-KR", "vi": "vi-VN", "th": "th-TH" };
  recognition.lang = langMap[document.getElementById("language").value] || "zh-TW";
  
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    symptomsTextarea.placeholder = "請開始說話，我正在聆聽...";
    voiceBtn.classList.add("listening"); 
    voiceBtn.innerHTML = '<i class="bi bi-stop-circle-fill"></i>';
    voiceBtn.disabled = true;
  };

  recognition.onresult = (event) => {
    const speechResult = event.results[0][0].transcript;
    symptomsTextarea.value += speechResult + " "; 
  };
  
  recognition.onspeechend = () => {
    recognition.stop();
  };

  recognition.onend = () => {
    symptomsTextarea.placeholder = translations[document.getElementById("language").value].placeholder;
    voiceBtn.classList.remove("listening");
    voiceBtn.innerHTML = '<i class="bi bi-mic-fill"></i>';
    voiceBtn.disabled = false;
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error", event.error);
    voiceBtn.classList.remove("listening");
    voiceBtn.innerHTML = '<i class="bi bi-mic-fill"></i>';
    voiceBtn.disabled = false;
  };

  recognition.start();
}


window.addEventListener("DOMContentLoaded", () => {
  
  switchLanguage();

  
  const voiceBtn = document.getElementById("voice-btn");
  if (voiceBtn) {
    voiceBtn.addEventListener("click", startSpeechRecognition);
  }
});