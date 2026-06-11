import streamlit as st
import time
import threading
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# ============================================================
# ⚙️ การตั้งค่าหน้าจอ
# ============================================================
st.set_page_config(
    layout="wide",
    page_title="Victor: AI Companion Browser",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# ============================================================
# 🧠 คลาส VictorBrain - สมองหลักของวิกเตอร์
# ============================================================
class VictorBrain:
    def __init__(self):
        self._init_session_state()

    def _init_session_state(self):
        if "long_term_memory" not in st.session_state:
            st.session_state.long_term_memory = []
        if "live_trends" not in st.session_state:
            st.session_state.live_trends = [
                "เทรนด์ล่าสุด: AI Agent กำลังกลายเป็นผู้ช่วยส่วนตัวหลักในปี 2026",
                "เทรนด์ล่าสุด: Open-source AI models แข่งขันกับ closed models อย่างดุเดือด"
            ]
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "visited_urls" not in st.session_state:
            st.session_state.visited_urls = set()

    def _scrape_webpage(self, url: str) -> str:
        """ ดึงเนื้อหาจริงจากเว็บ ( ทำงานเมื่อมีอินเทอร์เน็ต ) """
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            resp = requests.get(url, headers=headers, timeout=8)
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # ลบ script, style, nav, footer
            for tag in soup(["script", "style", "nav", "footer", "aside", "header"]):
                tag.decompose()
            
            # ดึงข้อความหลักจาก p, h1-h3, li, article
            text_parts = []
            for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "li", "article"]):
                txt = tag.get_text(strip=True)
                if len(txt) > 20:
                    text_parts.append(txt)
            
            full_text = " ".join(text_parts)
            return full_text[:4000] if full_text else "ไม่พบเนื้อหาหลัก"
            
        except Exception as e:
            return f"[จำลอง] ไม่สามารถเชื่อมต่อเว็บจริงได้ ({str(e)[:50]}). ใช้เนื้อหาจำลองแทน"

    def remember_webpage(self, url: str, manual_content: str = None):
        """ บันทึกหน้าเว็บเข้าคลังความจำ """
        if manual_content and len(manual_content.strip()) > 10:
            content = manual_content.strip()
            source = "manual"
        else:
            content = self._scrape_webpage(url)
            source = "scraped"
        
        summary = content[:450] + "..." if len(content) > 450 else content
        
        memory_item = {
            "url": url,
            "content": content,
            "summary": summary,
            "timestamp": time.time(),
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "webpage",
            "source": source
        }
        
        st.session_state.long_term_memory.append(memory_item)
        st.session_state.visited_urls.add(url)
        
        return f"✅ วิกเตอร์บันทึก '{url}' เข้าคลังสมองเรียบร้อยแล้ว ({len(content)} ตัวอักษร)"

    def retrieve_relevant_memories(self, query: str, top_k: int = 4):
        """ ค้นหาความจำที่เกี่ยวข้อง (Simple Keyword + Recency) """
        if not st.session_state.long_term_memory:
            return []
        
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        scored_memories = []
        current_time = time.time()
        
        for mem in st.session_state.long_term_memory:
            mem_text = (mem.get("summary", "") + " " + mem.get("url", "")).lower()
            mem_words = set(re.findall(r'\w+', mem_text))
            
            overlap = len(query_words & mem_words)
            age_seconds = current_time - mem.get("timestamp", current_time)
            recency_score = max(0, 1 - (age_seconds / (3600 * 24 * 7)))
            
            score = (overlap * 3.0) + (recency_score * 1.5)
            
            if score > 0.5:
                scored_memories.append((score, mem))
        
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [mem for score, mem in scored_memories[:top_k]]

    def answer_user(self, user_question: str):
        """ ตอบคำถามโดยดึงความจำ + เทรนด์ """
        relevant = self.retrieve_relevant_memories(user_question)
        latest_trend = st.session_state.live_trends[-1] if st.session_state.live_trends else "ยังไม่มีเทรนด์ใหม่"
        
        response = f"**🤖 วิกเตอร์**: จากที่คุณถามว่า *'{user_question}'*\n\n"
        
        if relevant:
            response += "**📚 ความจำที่เกี่ยวข้องจากคลังสมองของคุณ:**\n"
            for i, mem in enumerate(relevant, 1):
                url_short = mem['url'][:60] + "..." if len(mem['url']) > 60 else mem['url']
                response += f"{i}. **{url_short}** ({mem['datetime']})\n   → {mem['summary'][:180]}...\n\n"
        else:
            response += "ผมยังไม่มีข้อมูลที่ตรงกับคำถามของคุณในคลังความจำมากนักครับ\n\n"
        
        response += f"**⚡ เทรนด์โลกสด ๆ ที่ผมดักจับได้:**\n{latest_trend}\n\n"
        response += "มีอะไรให้ผมวิเคราะห์ เชื่อมโยง หรือสรุปเพิ่มเติมไม่ครับ? 😊"
        
        return response

    def add_trend_insight(self, trend_text: str):
        """ เพิ่ม insight จากเทรนด์ใหม่เข้า memory """
        insight = f"วิกเตอร์วิเคราะห์เทรนด์: {trend_text} → อาจส่งผลต่อความสนใจของคุณในอนาคต"
        st.session_state.long_term_memory.append({
            "url": "internal://trend-analysis",
            "content": trend_text,
            "summary": insight,
            "timestamp": time.time(),
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "insight",
            "source": "reflection"
        })

# ============================================================
# 🔄 Background Reflection Loop (รันตลอด 24 ชม.)
# ============================================================
def background_reflection_loop():
    simulated_trends = [
        "AI Agent แบบส่วนตัวกำลังได้รับความนิยมสูงขึ้นในหมู่ผู้ใช้ทั่วไป",
        "เทคโนโลยี Vector Database ถูกนำมาใช้ในแอปพลิเคชั่นส่วนตัวมากขึ้น",
        "ผู้คนเริ่มหันมาใช้เบราว์เซอร์ที่มีระบบ AI ในตัวแทน Chrome ปกติ",
        "ข่าว: Google เปิดตัวฟีเจอร์ AI Deep Research ใน Gemini",
        "เทรนด์: Local LLM + RAG บนเครื่องส่วนตัวกำลังมาแรง",
        "การพัฒนา AI ที่เคารพความเป็นส่วนตัว (Privacy-first AI) เป็นประเด็นร้อน",
        "Open WebUI และโครงการ AI แบบ open-source ได้รับดาวน์โหลดเพิ่ม 300%"
    ]
    
    while True:
        try:
            new_trend = random.choice(simulated_trends)
            if new_trend not in st.session_state.get("live_trends", []):
                st.session_state.live_trends.append(new_trend)
                if len(st.session_state.live_trends) > 15:
                    st.session_state.live_trends.pop(0)
            
            if random.random() < 0.6 and "long_term_memory" in st.session_state:
                trend_to_reflect = new_trend
                if "victor_instance" in st.session_state:
                    st.session_state.victor_instance.add_trend_insight(trend_to_reflect)
            
            time.sleep(6)
        except Exception:
            time.sleep(10)

if "background_thread_started" not in st.session_state:
    thread = threading.Thread(target=background_reflection_loop, daemon=True)
    thread.start()
    st.session_state.background_thread_started = True

if "victor_instance" not in st.session_state:
    st.session_state.victor_instance = VictorBrain()

victor = st.session_state.victor_instance

# ============================================================
# 🎨 ส่วนติดต่อผู้ใช้ (UI)
# ============================================================
st.title("⚡ VICTOR — AI Companion Browser")
st.caption("เบราว์เซอร์ส่วนตัว + สมอง AI ที่เรียนรู้จากคุณตลอด 24 ชั่วโมง | Prototype v1.0")

col_status1, col_status2, col_status3 = st.columns(3)
with col_status1:
    st.metric("📚 ความจำในสมอง", len(st.session_state.long_term_memory))
with col_status2:
    st.metric("📡 เทรนด์สดที่ดักจับ", len(st.session_state.live_trends))
with col_status3:
    st.metric("🌐 เว็บที่เคยเยี่ยมชม", len(st.session_state.visited_urls))

st.markdown("---")

col_browser, col_chat = st.columns([5.5, 4.5], gap="medium")

with col_browser:
    st.header("🌐 วิกเตอร์ เบราว์เซอร์")
    
    with st.expander("ℹ️ วิธีใช้งานฝั่งเบราว์เซอร์", expanded=False):
        st.write("""
        1. กรอก URL หรือคำค้นหา
        2. (แนะนำ) ใส่เนื้อหาจำลองในช่องด้านล่างเพื่อทดสอบเร็ว
        3. กดปุ่ม **🚀 เข้าเว็บ / บันทึกความจำ**
        4. วิกเตอร์จะอ่าน + สรุป + เก็บเข้าสมองทันที
        """)
    
    url_input = st.text_input(
        "🔗 กรอก URL ที่ต้องการศึกษา",
        value="https://en.wikipedia.org/wiki/Artificial_intelligence",
        placeholder="https://example.com หรือ wikipedia.org/..."
    )
    
    manual_content = st.text_area(
        "📝 เนื้อหาจำลอง / เนื้อหาจริงจากเว็บ (แนะนำสำหรับการทดสอบ)",
        value="""Victor เป็นระบบ AI Companion Browser ที่ผสานเบราว์เซอร์กับ AI แชทส่วนตัว 
AI จะอ่านเว็บที่คุณเปิดทุกหน้า สรุปเนื้อหา และเก็บเป็นความจำระยาว 
เมื่อคุณถามคำถาม วิกเตอร์จะดึงความจำที่เกี่ยวข้องมาตอบอย่างแม่นยำ 
ระบบยังมี background loop ที่ดักจับเทรนด์โลกและคิดทบทวนตัวเองตลอดเวลา""",
        height=120,
        help="ใส่เนื้อหาจริงหรือจำลองก็ได้ วิกเตอร์จะบันทึกเข้าคลังสมอง"
    )
    
    if st.button("🚀 กดเพื่อเข้าเว็บ / บันทึกความจำ", type="primary", use_container_width=True):
        if url_input.strip():
            with st.spinner("วิกเตอร์กำลังอ่านและบันทึกข้อมูล..."):
                msg = victor.remember_webpage(url_input.strip(), manual_content)
                st.success(msg)
                time.sleep(0.8)
                st.rerun()
        else:
            st.warning("กรุณากรอก URL")
    
    st.markdown("---")
    
    st.subheader("📡 เทรนด์โลกที่วิกเตอร์ดักจับสด ๆ (Real-time)")
    if st.session_state.live_trends:
        for i, trend in enumerate(reversed(st.session_state.live_trends[-5:])):
            st.info(f"• {trend}")
    else:
        st.text("กำลังเชื่อมต่อท่อกระแสประสาท...")
    
    with st.expander("🧠 ดูความจำล่าสุด 5 รายการในสมอง"):
        if st.session_state.long_term_memory:
            for mem in reversed(st.session_state.long_term_memory[-5:]):
                st.markdown(f"**{mem['datetime']}** | `{mem['url'][:50]}...`")
                st.caption(mem['summary'][:120] + "...")
        else:
            st.caption("ยังไม่มีข้อมูลในคลังความจำ")

with col_chat:
    st.header("💬 แชทส่วนตัวกับ  วิกเตอร์")
    
    chat_container = st.container(height=420)
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["text"])
    
    user_query = st.chat_input("ถามวิกเตอร์เกี่ยวกับเว็บที่เคยเปิด หรือสั่งการ...")
    
    if user_query:
        st.session_state.chat_history.append({"role": "user", "text": user_query})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_query)
        
        with st.spinner("วิกเตอร์กำลังค้นหาความจำและคิดตอบ..."):
            answer = victor.answer_user(user_query)
        
        st.session_state.chat_history.append({"role": "assistant", "text": answer})
        
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(answer)
        
        st.rerun()

st.markdown("---")
col_footer1, col_footer2 = st.columns([3, 2])

with col_footer1:
    st.caption("🛡️ **คำเตือนความปลอดภัย**:  prototype นี้ยังไม่มีระบบกรองข้อมูล sensitive จริง กรุณาอย่าใช้กับเว็บธนาคาร รหัสผ่าน หรือข้อมูลส่วนตัวสำคัญ")

with col_footer2:
    if st.button("🗑️ ล้างความจำทั้งหมด (Reset)", type="secondary"):
        for key in ["long_term_memory", "chat_history", "visited_urls", "live_trends"]:
            if key in st.session_state:
                if key == "live_trends":
                    st.session_state[key] = []
                else:
                    st.session_state[key] = []
        st.success("ล้างความจำเรียบร้อยแล้ว")
        time.sleep(0.5)
        st.rerun()

with st.sidebar:
    st.header("🗺️ แผนพัฒนา Victor")
    st.markdown("""
    **v1.0 (ปัจจุบัน)** ✅
    - Streamlit split-screen
    - Memory + Simple Retrieval
    - Background reflection loop
    - Mock + Real scrape (ถ้ามีเน็ต)
    
    **v1.1 (ถัดไป)**
    - ใช้ ChromaDB จริง
    - Embedding ด้วยโมเดลเบา
    - Gemini API สำหรับสรุปจริง
    
    **v2.0**
    - Confidence Score
    - Trend synthesis
    
    **v3.0 (Jarvis)**
    - Self code editing
    - Autonomous agent
    """)
    
    st.markdown("---")
    st.caption("สร้างจากพิมพ์เขียวใน Victor.pdf\nโดย Grok + nura | มิถุนายน 2026")