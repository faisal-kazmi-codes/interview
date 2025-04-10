from fastapi import FastAPI, Depends, WebSocket
from auth import register_user, login_user, get_db
from schemas import UserRegister, UserLogin
from sqlalchemy.orm import Session
from fastapi.websockets import WebSocketDisconnect

app = FastAPI()

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
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")