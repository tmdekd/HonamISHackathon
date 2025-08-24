from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Base, User   # ✅ init.py 통해 한 번에 불러오기


from pydantic import BaseModel
from app.chatbot_test_elderly_func import generate_empathic_response
from app.summary import summarize_dialog
from app.diag_gpt import diag_dialog
#CROS코드
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()

from typing import Dict, List
chat_history: List[Dict[str, str]] = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 허용할 프론트엔드 주소
    allow_credentials=True,
    allow_methods=["*"],       # 모든 메서드 허용 (GET, POST 등)
    allow_headers=["*"],       # 모든 헤더 허용
)

@app.get("/api/")
def read_root():
    return {"message": "Hello FastAPI + MySQL"}       

from fastapi import Form

class ChatRequest(BaseModel):
    message: str
    
# @app.post("/api/chatbot/")
# def chat_with_model(req: ChatRequest):
#     reply = generate_empathic_response(req.message)
#     return {"reply": reply}
@app.post("/api/chatbot/")
def chat_with_model(req: ChatRequest):
    user_message = req.message

    # 유저 메시지 저장
    chat_history.append({"role": "user", "content": user_message})

    # 모델 응답 생성
    reply = generate_empathic_response(user_message)

    # 봇 메시지 저장
    chat_history.append({"role": "bot", "content": reply})

    # 필요시 전체 히스토리 반환 가능
    return {"reply": reply, "history": chat_history}

@app.get("/api/list")
def read_root():
    return print(chat_history)      

@app.post("/api/summary")
def summarize_chat():
    if not chat_history:
        return {"summary": "대화 내용이 없습니다."}

    # 대화를 문자열로 합치기
    conversation_text = ""
    for msg in chat_history:
        prefix = "내담자: " if msg["role"] == "user" else "상담사: "
        conversation_text += f"{prefix}{msg['content']}\n"

    # 요약 생성
    summary = summarize_dialog(conversation_text)

    return {"summary": summary}

@app.post("/api/addict")
def check_addiction():
    if not chat_history:
        return {"score": None, "message": "대화 내용이 없습니다."}

    # 전체 대화를 문자열로 합치기
    conversation_text = ""
    for msg in chat_history:
        prefix = "내담자: " if msg["role"] == "user" else "상담사: "
        conversation_text += f"{prefix}{msg['content']}\n"

    # AI 모델로 중독/우울/불안 판별
    result_json = diag_dialog(conversation_text)
    
    # JSON 문자열 → Python dict 변환
    try:
        result_dict = json.loads(result_json)
    except json.JSONDecodeError:
        result_dict = {"우울": 0, "중독": 0, "불안": 0}

    # 우울, 중독, 불안 값만 추출
    depression = result_dict.get("우울", 0)
    addiction  = result_dict.get("중독", 0)
    anxiety    = result_dict.get("불안", 0)

    # 점수 계산
    score = depression + addiction + anxiety  # 0~3

    return {"score": score}
if __name__ == "__main__":
    # 외부에서 접근 가능하도록 host를 0.0.0.0으로 설정
    uvicorn.run(
        "main:app",
        host="0.0.0.0",        # ⭐ 중요: 외부 접근 허용
        port=8000,
        reload=True,           # 개발 중 자동 재시작
        log_level="info"
    )