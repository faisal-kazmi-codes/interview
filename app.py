from fastapi import FastAPI, Depends, WebSocket
from auth import register_user, login_user, get_db
from schemas import UserRegister, UserLogin
from sqlalchemy.orm import Session
from fastapi.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    new_user = register_user(user, db)
    return {"message": "User created successfully", "user_id": new_user.id}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = login_user(user, db)
    return {"access_token": token, "token_type": "bearer"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    response = []
    try:
        while True:
            message = await websocket.receive()
            if message["type"] == "websocket.disconnect":
                print("Client initiated disconnect")
                break

            if message["type"] == "websocket.receive":
                if "text" in message:
                    raw_text = message["text"]
                    try:
                        data = json.loads(raw_text)
                        text_value = data.get("text", "")
                        response.append(text_value)
                        await websocket.send_text(f"Message received: {text_value}")
                    except json.JSONDecodeError:
                        await websocket.send_text("Invalid JSON format.")
                else:
                    await websocket.send_text("Binary messages are not supported.")

    except WebSocketDisconnect:
        print("Client disconnected")

    print("All received text messages:")
    print(response)