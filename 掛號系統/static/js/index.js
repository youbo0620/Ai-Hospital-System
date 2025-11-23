import { db } from './firebase-config.js';
import { collection, addDoc, serverTimestamp, query, where, getDocs } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";


// Translations 
const translations = {
  zh: { title: " 醫院掛號表單", name: "姓名：", id: "身分證字號：", department: "掛號科別：", time: "看診時間：", submit: "送出掛號", ask: "👉 問 AI 看該掛哪一科",dontKnow: "不知道要掛哪一科嗎？",query: "查詢掛號紀錄" ,aiSectionTitle:"AI 智慧導診"},
  en: { title: " Hospital Registration", name: "Name:", id: "National ID:", department: "Department:", time: "Appointment Date:", submit: "Submit", ask: "👉 Ask AI to recommend a department",dontKnow: "Not sure which department?",query: "Query Registration",aiSectionTitle:"AI Diagnosis Assistant" },
  ja: { title: " 病院予約フォーム", name: "氏名：", id: "身分証番号：", department: "診療科：", time: "診察日：", submit: "予約する", ask: "👉 AIに診療科を聞く",dontKnow: "どの科を選べばいいかわかりませんか？",query: "予約照会",aiSectionTitle:"AI 診療補助" },
  ko: { title: " 병원 예약 양식", name: "이름:", id: "주민등록번호:", department: "진료과:", time: "진료 날짜:", submit: "예약하기", ask: "👉 AI에게 물어보기",dontKnow: "어떤 진료과를 선택해야 할지 모르시겠습니까?",query: "예약 조회" ,aiSectionTitle:"AI 진료 보조 시스템"},
  vi: { title: " Mẫu đăng ký khám bệnh", name: "Họ tên:", id: "CMND/CCCD:", department: "Chuyên khoa:", time: "Ngày khám:", submit: "Đăng ký", ask: "👉 Hỏi AI nên khám khoa nào", dontKnow: "Không biết nên chọn khoa nào?",query: "Tra cứu đăng ký" ,aiSectionTitle:"Hệ thống tư vấn khám bệnh AI"},
  th: { title: " แบบฟอร์มลงทะเบียนโรงพยาบาล", name: "ชื่อ:", id: "รหัสประชาชน:", department: "แผนกที่ต้องการพบแพทย์:", time: "วันที่นัดพบแพทย์:", submit: "ลงทะเบียน", ask: "👉 ถาม AI ว่าควรพบแผนกใด", dontKnow: "ไม่แน่ใจว่าควรพบแผนกใด?",query: "ค้นหาการลงทะเบียน" ,aiSectionTitle:"ผู้ช่วยแนะนำแผนกด้วย AI"},
  success: {
    zh: "✅ 掛號成功！您的掛號編號為：",
    en: "✅ Registration successful! Your ID is: ",
    ja: "✅ 予約が完了しました！あなたの番号は：",
    ko: "✅ 예약이 완료되었습니다! 등록 번호: ",
    vi: "✅ Đăng ký thành công! Mã số của bạn là: ",
    th: "✅ ลงทะเบียนสำเร็จ! หมายเลขของคุณคือ: "
  }
};

// Departments 
const departments = {
  zh: [ { value: "", label: "請選擇" }, { value: "內科", label: "內科" }, { value: "外科", label: "外科" }, { value: "耳鼻喉科", label: "耳鼻喉科" }, { value: "皮膚科", label: "皮膚科" }, { value: "眼科", label: "眼科" } ],
  en: [ { value: "", label: "Please select" }, { value: "Internal Medicine", label: "Internal Medicine" }, { value: "Surgery", label: "Surgery" }, { value: "ENT", label: "ENT" }, { value: "Dermatology", label: "Dermatology" }, { value: "Ophthalmology", label: "Ophthalmology" } ],
  ja: [ { value: "", label: "選択してください" }, { value: "内科", label: "内科" }, { value: "外科", label: "外科" }, { value: "耳鼻科", label: "耳鼻科" }, { value: "皮膚科", label: "皮膚科" }, { value: "眼科", label: "眼科" } ],
  ko: [ { value: "", label: "선택하세요" }, { value: "내과", label: "내과" }, { value: "외과", label: "외과" }, { value: "이비인후과", label: "이비인후과" }, { value: "피부과", label: "피부과" }, { value: "안과", label: "안과" } ],
  vi: [ { value: "", label: "Vui lòng chọn" }, { value: "Nội khoa", label: "Nội khoa" }, { value: "Ngoại khoa", label: "Ngoại khoa" }, { value: "Tai Mũi Họng", label: "Tai Mũi Họng" }, { value: "Da liễu", label: "Da liễu" }, { value: "Mắt", label: "Mắt" } ],
  th: [ { value: "", label: "กรุณาเลือก" }, { value: "อายุรกรรม", label: "อายุรกรรม" }, { value: "ศัลยกรรม", label: "ศัลยกรรม" }, { value: "หู คอ จมูก", label: "หู คอ จมูก" }, { value: "ผิวหนัง", label: "ผิวหนัง" }, { value: "จักษุ", label: "จักษุ" } ]
};

let fp=null;

// Helpers 
function validateForm({ name, idNumber, department, date }) {
  if (!name.trim()) return "請輸入姓名 / Name is required";
  if (!idNumber.trim()) return "請輸入身分證字號 / ID number is required";
  if (!department.trim()) return "請選擇科別 / Department is required";
  if (!date.trim()) return "請選擇日期 / Date is required";
  return null;
}

// 產生掛號編號 REGyyyyMMddNN (01–99)
async function generateRegistrationID(date) {
  const dateStr = date.replaceAll("/", "");
  const q = query(collection(db, "registrations"), where("date", "==", date));
  const snapshot = await getDocs(q);
  const count = snapshot.size;
  if (count >= 99) throw new Error("今日掛號已滿 99 筆！");
  const serial = String(count + 1).padStart(2, "0");
  return `REG${dateStr}${serial}`;
}

// Submit 
async function submitForm(event) {
  event.preventDefault();

  const lang = document.getElementById("language").value;
  const name = document.getElementById("name").value || "";
  const idNumber = document.getElementById("id").value || "";
  const department = document.getElementById("department").value || "";
  const date = document.getElementById("time").value || "";

  const err = validateForm({ name, idNumber, department, date });
  if (err) return alert(err);

  try {
    const regID = await generateRegistrationID(date);
    await addDoc(collection(db, "registrations"), {
      name,
      id_number: idNumber,
      department,
      date,
      registration_id: regID,
      timestamp: serverTimestamp()
    });

    const msg = translations.success[lang] + regID;
    const box = document.getElementById("success-message");
    box.innerText = msg;
    box.style.display = "block";

    document.getElementById("register-form").reset(); 
    
    setTimeout(() => {
      box.style.display = "none";
    }, 5000);
    

  } catch (e) {
    console.error("Firestore write error:", e);
    if (e.code === "permission-denied") {
      alert("❌ 無法寫入 Firestore（權限不足）。請到 Firebase Console 調整 Firestore 規則。");
    } else {
      alert("❌ 發生錯誤：" + (e.message || e));
    }
  }
}

// Language & Datepicker
function switchLanguage() {
  const lang = document.getElementById("language").value;
  const t = translations[lang];

  document.getElementById("title").innerText = t.title;
  document.getElementById("label-name").innerText = t.name;
  document.getElementById("label-id").innerText = t.id;
  document.getElementById("label-dept").innerText = t.department;
  document.getElementById("label-time").innerText = t.time;
  document.getElementById("submit-btn").innerText = t.submit;
  document.getElementById("query-btn").innerText = t.query;
  document.getElementById("ask-label").innerText = t.dontKnow;
  document.getElementById("ask-btn").innerText = t.ask;
  document.getElementById("ai-section-title").innerText = t.aiSectionTitle;

  const deptSelect = document.getElementById("department");
  deptSelect.innerHTML = "";
  departments[lang].forEach(option => {
    const opt = document.createElement("option");
    opt.value = option.value;
    opt.text = option.label;
    deptSelect.appendChild(opt);
  });

  
  const localeMap = {
    en: "en",
    zh: flatpickr.l10ns.zh_tw,
    ja: flatpickr.l10ns.ja,
    ko: flatpickr.l10ns.ko,
    vi: flatpickr.l10ns.vn,
    th: flatpickr.l10ns.th
  };
  if (fp) fp.set("locale", localeMap[lang] ?? "en");
}

window.switchLanguage = switchLanguage;

window.addEventListener('DOMContentLoaded', () => {
  fp = flatpickr("#time", {
    dateFormat: "Y/m/d",
    locale: flatpickr.l10ns.zh_tw
  });
  document.getElementById("register-form").addEventListener("submit", submitForm);
  switchLanguage();
});






