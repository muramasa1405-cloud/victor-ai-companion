# ⚡ VICTOR (วิกเตอร์) - AI Companion Browser v1.0

** พิมพ์เขียวที่กลายเป็นโปรเจกต์จริง **  
เบราว์เซอร์ส่วนตัว + AI ผู้ช่วยอัจฉริยะที่เรียนรู้จากคุณตลอด 24 ชั่วโมง

Victor คือระบบที่รวม **เบราว์เซอร์ + แชท AI** เข้าด้วยกัน โดย AI จะ:
- อ่านและจำเนื้อหาเว็บทุกหน้าที่คุณเปิด
- สรุปใจความสำคัญอัตโนมัติ
- ตอบคำถามโดยดึงความจำส่วนตัวของคุณ
- ดักจับเทรนด์โลกแบบเรียลไทม์
- คิดทบทวนตัวเอง (Reflection) เพื่อสร้าง insight ใหม่

---

## 🚀 วิธีติดตั้งและรัน (5 นาที)

```bash
# 1. ดาวน์โหลดโปรเจกต์
git clone https://github.com/muramasa1405-cloud/victor-ai-companion.git victor
cd victor

# หรือโหลด ZIP แล้วแตก

# 2. ติดตั้ง dependencies
pip install -r requirements.txt

# 3. รันแอป
streamlit run app.py
```

แล้วเปิดเบราว์เซอร์ที่ **http://localhost:8501**

---

## ✨ ฟีเจอร์ในเวอร์ชั่น Prototype 1.0

| ฟีเจอร์ | สถานะ | รายละเอียด |
|--------|--------|-----------|
| Split-screen UI (ซ้าย Browser / ขวา Chat) | ✅ | ใช้ Streamlit columns |
| จำลองการเข้าเว็บ + บันทึกความจำ | ✅ | กดปุ่ม → ระบบ scrape (หรือ manual) → เก็บเข้า memory |
| Real-time Trend Stream | ✅ | Background thread ดักจับเทรนด์ทุก 6 วินาที |
| Autonomous Reflection Loop | ✅ | สร้าง insight ใหม่จากเทรนด์โดยอัตโนมัติ |
| Retrieval Augmented Chat | ✅ | ค้นหาความจำที่เกี่ยวข้องก่อนตอบ |
| Privacy note | ✅ | มีคำเตือน + ตัวกรองเบื้องต้น |
| 3 ระยะการพัฒนา | 📝 | มีแผนใน README |

---

## 🧠 สถาปัตยกรรม (ตรงตามพิมพ์เขียว)

```
[User] 
   ↓
[Streamlit UI] ←→ [VictorBrain]
   ↓              ↓
Browser (ซ้าย)   Memory (list + simple retrieval)
   ↓              ↓
Scraper         Background Reflection Loop
   ↓              ↓
Vector Memory   Live Trends
```

**ในเวอร์ชั่นจริง (Roadmap):**
- ใช้ ChromaDB / Pinecone แทน list
- ใช้ Gemini / OpenAI API สำหรับสรุปและตอบจริง
- ใช้ LangChain สำหรับ orchestration
- Deploy บน Streamlit Cloud หรือ HuggingFace + GitHub backend

---

## 🔒 ความปลอดภัย (สำคัญ!)

ในโค้ดปัจจุบันเป็น **prototype** — ยังไม่มี Security Filter จริง  
** ห้าม** ใช้กับเว็บที่ sensitive (ธนาคาร, รหัสผ่าน) จนกว่าจะมีตัวกรอง

ในอนาคตจะเพิ่ม:
- ตรวจจับ URL sensitive
- ไม่บันทึก input ที่มี pattern รหัสผ่าน / เลขบัตร
- User confirmation ก่อนบันทึก

---

## 🗺️ แผนพัฒนาต่อ (Roadmap)

1. **v1.1** — เพิ่ม ChromaDB จริง + Embedding ด้วย sentence-transformers (เบา)
2. **v1.2** — เชื่อม Gemini API สำหรับสรุปและตอบที่ฉลาดขึ้น
3. **v2.0** — Self-reflection ลึกขึ้น + Confidence Score
4. **v3.0** — Autonomous code editing บน GitHub (ระยะ Jarvis)

---

## 💡 วิธีใช้ตัวอย่าง

1. กรอก URL เช่น `https://en.wikipedia.org/wiki/Artificial_intelligence`
2. กดปุ่ม **🚀 กดเพื่อเข้าเว็บ / บันทึกความจำ**
3. ไปที่ช่องแชทขวา พิมพ์คำถาม เช่น  “วิกเตอร์ สรุปเรื่อง AI ให้หน่อย” หรือ “เทรนด์ล่าสุดคืออะไร?”
4. Victor จะตอบโดยอ้างอิงความจำที่เพิ่งบันทึก + เทรนด์สด

---

**สร้างโดย**: จากพิมพ์เขียวในอถกสาร Victor.pdf  
**สถานะ**: Prototype พร้อมรันได้ทันที | โดย Grok + nura | มิถุนายน 2026