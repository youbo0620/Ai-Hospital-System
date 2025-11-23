//  語言翻譯功能 
const translations = {
  zh: {
    pageTitle: "掛號查詢",
    title: " 掛號紀錄查詢",
    description: "請輸入您的身分證字號以查詢掛號紀錄：",
    labelId: "身分證字號：",
    queryBtn: "查詢",
    resultLabel: "查詢結果：",
    backBtn: "⬅ 回掛號主畫面",
    enterId: "請輸入身分證字號。",
    querying: "查詢中...",
    notFound: "查無此身分證字號的掛號紀錄。",
    serverError: "伺服器內部錯誤，請稍後再試。",
    connectionError: "查詢時發生連線錯誤。",
    recordTitle: "掛號科別：",
    recordDate: "看診日期：",
    recordName: "掛號姓名：",
    recordRegId: "掛號編號：",
    emptyHint: "請輸入資料進行查詢" 
  },
  en: {
    pageTitle: "Query Registration",
    title: " Query Registration",
    description: "Please enter your National ID to query records:",
    labelId: "National ID:",
    queryBtn: "Query",
    resultLabel: "Query Results:",
    backBtn: "⬅ Back to Home",
    enterId: "Please enter an ID number.",
    querying: "Querying...",
    notFound: "No registration record found for this ID.",
    serverError: "Server error, please try again later.",
    connectionError: "A connection error occurred during the query.",
    recordTitle: "Department:",
    recordDate: "Appointment Date:",
    recordName: "Name:",
    recordRegId: "Registration ID:",
    emptyHint: "Please enter ID to query" 
  },
  ja: {
    pageTitle: "予約照会",
    title: " 予約履歴照会",
    description: "身分証番号を入力して予約履歴を照会してください：",
    labelId: "身分証番号：",
    queryBtn: "照会",
    resultLabel: "照会結果：",
    backBtn: "⬅ メイン画面に戻る",
    enterId: "身分証番号を入力してください。",
    querying: "照会中...",
    notFound: "この身分証番号の予約記録は見つかりませんでした。",
    serverError: "サーバーエラーが発生しました。後でもう一度お試しください。",
    connectionError: "照会中に接続エラーが発生しました。",
    recordTitle: "診療科：",
    recordDate: "診察日：",
    recordName: "氏名：",
    recordRegId: "予約番号：",
    emptyHint: "データを入力して照会してください"
  },
  ko: {
    pageTitle: "예약 조회",
    title: " 예약 기록 조회",
    description: "주민등록번호를 입력하여 예약 기록을 조회하세요:",
    labelId: "주민등록번호:",
    queryBtn: "조회",
    resultLabel: "조회 결과:",
    backBtn: "⬅ 메인 화면으로 돌아가기",
    enterId: "주민등록번호를 입력하세요.",
    querying: "조회 중...",
    notFound: "이 주민등록번호에 대한 예약 기록이 없습니다.",
    serverError: "서버 오류가 발생했습니다. 나중에 다시 시도해 주세요.",
    connectionError: "조회 중 연결 오류가 발생했습니다.",
    recordTitle: "진료과:",
    recordDate: "진료 날짜:",
    recordName: "이름:",
    recordRegId: "등록 번호:",
    emptyHint: "조회할 데이터를 입력하세요" 
  },
  vi: {
    pageTitle: "Tra cứu đăng ký",
    title: " Tra cứu hồ sơ đăng ký",
    description: "Vui lòng nhập số CMND/CCCD để tra cứu hồ sơ:",
    labelId: "CMND/CCCD:",
    queryBtn: "Tra cứu",
    resultLabel: "Kết quả tra cứu:",
    backBtn: "⬅ Quay lại trang chủ",
    enterId: "Vui lòng nhập số CMND/CCCD.",
    querying: "Đang tra cứu...",
    notFound: "Không tìm thấy hồ sơ đăng ký cho số ID này.",
    serverError: "Lỗi máy chủ, vui lòng thử lại sau.",
    connectionError: "Đã xảy ra lỗi kết nối khi tra cứu.",
    recordTitle: "Chuyên khoa:",
    recordDate: "Ngày khám:",
    recordName: "Họ tên:",
    recordRegId: "Mã số đăng ký:",
    emptyHint: "Vui lòng nhập dữ liệu để tra cứu"
  },
  th: {
    pageTitle: "ค้นหาการลงทะเบียน",
    title: " ค้นหาบันทึกการลงทะเบียน",
    description: "กรุณาป้อนรหัสประชาชนของคุณเพื่อค้นหาบันทึก:",
    labelId: "รหัสประชาชน:",
    queryBtn: "ค้นหา",
    resultLabel: "ผลการค้นหา:",
    backBtn: "⬅ กลับไปที่หน้าหลัก",
    enterId: "กรุณาป้อนรหัสประชาชน",
    querying: "กำลังค้นหา...",
    notFound: "ไม่พบข้อมูลการลงทะเบียนสำหรับรหัสประชาชนนี้",
    serverError: "เซิร์ฟเวอร์มีปัญหา กรุณาลองใหม่อีกครั้ง",
    connectionError: "เกิดข้อผิดพลาดในการเชื่อมต่อระหว่างค้นหา",
    recordTitle: "แผนก:",
    recordDate: "วันที่นัด:",
    recordName: "ชื่อ:",
    recordRegId: "รหัสการลงทะเบียน:",
    emptyHint: "กรุณากรอกข้อมูลเพื่อค้นหา" 
  }
};

function switchLanguage() {
  const lang = document.getElementById("language").value;
  const t = translations[lang];

  document.getElementById("page-title").innerText = t.pageTitle;
  document.getElementById("title").innerText = t.title;
  document.getElementById("description").innerHTML = `<i class="bi bi-info-circle me-2"></i>${t.description}`;
  document.getElementById("label-id").innerText = t.labelId;
  
  const queryBtn = document.getElementById("query-btn");
  if (queryBtn) queryBtn.innerHTML = `<i class="bi bi-search me-2"></i>${t.queryBtn}`;
  
  document.getElementById("result-label").innerText = t.resultLabel;
  
  const backBtn = document.getElementById("back-btn");
  if (backBtn) backBtn.innerHTML = `<i class="bi bi-arrow-left-circle me-1"></i> ${t.backBtn}`;

  
  const emptyHint = document.getElementById("empty-hint");
  if (emptyHint) {
    emptyHint.innerText = t.emptyHint;
  }
}



// 查詢功能
window.switchLanguage = switchLanguage;

window.addEventListener("DOMContentLoaded", () => {
  
  document.getElementById("query-btn").addEventListener("click", performQuery);
  
  
  switchLanguage();
});

async function performQuery() {
  const idNumber = document.getElementById("id_number").value;
  const resultsDiv = document.getElementById("results");
  const lang = document.getElementById("language").value; 
  const t = translations[lang]; 

  if (!idNumber) {
    resultsDiv.innerHTML = `
      <div class="alert alert-danger d-flex align-items-center" role="alert">
        <i class="bi bi-exclamation-circle-fill fs-4 me-2"></i>
        <div>${t.enterId}</div>
      </div>`;
    return;
  }

  resultsDiv.innerHTML = `
    <div class="text-center py-5 text-secondary">
      <div class="spinner-border text-secondary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">${t.querying}</p>
    </div>`;

  try {
    const response = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id_number: idNumber })
    });

    const data = await response.json();

    if (!response.ok) {
      if (data.error_key === "NOT_FOUND") {
        resultsDiv.innerHTML = `
          <div class="alert alert-warning d-flex align-items-center" role="alert">
            <i class="bi bi-exclamation-triangle-fill fs-4 me-2"></i>
            <div>${t.notFound}</div>
          </div>`;
      } else {
        resultsDiv.innerHTML = `
          <div class="alert alert-danger d-flex align-items-center" role="alert">
            <i class="bi bi-x-octagon-fill fs-4 me-2"></i>
            <div>${t.serverError}</div>
          </div>`;
      }
    } else {
      displayResults(data);
    }

  } catch (error) {
    console.error("Fetch error:", error);
    resultsDiv.innerHTML = `
      <div class="alert alert-danger d-flex align-items-center" role="alert">
        <i class="bi bi-wifi-off fs-4 me-2"></i>
        <div>${t.connectionError}</div>
      </div>`;
  }
}

function displayResults(records) {
  const resultsDiv = document.getElementById("results");
  const lang = document.getElementById("language").value; 
  const t = translations[lang]; 

  if (records.length === 0) {
    resultsDiv.innerHTML = `
      <div class="alert alert-warning d-flex align-items-center" role="alert">
        <i class="bi bi-exclamation-triangle-fill fs-4 me-2"></i>
        <div>${t.notFound}</div>
      </div>`;
    return;
  }

  
  let html = '';
  records.forEach(record => {
    html += `
      <div class="result-card">
        <div class="d-flex justify-content-between align-items-start mb-3">
          <div>
            <div class="result-label">${t.recordTitle}</div>
            <span class="badge-dept"><i class="bi bi-hospital me-1"></i>${record.department}</span>
          </div>
          <div class="text-end">
            <div class="result-label">${t.recordDate}</div>
            <div class="result-value text-primary">${record.date}</div>
          </div>
        </div>
        
        <div class="row g-2">
          <div class="col-6">
            <div class="result-label">${t.recordName}</div>
            <div class="result-value">${record.name}</div>
          </div>
          <div class="col-6">
            <div class="result-label">${t.recordRegId}</div>
            <div class="result-value text-secondary font-monospace small">${record.registration_id}</div>
          </div>
        </div>
      </div>
    `;
  });
  
  resultsDiv.innerHTML = html;
}
