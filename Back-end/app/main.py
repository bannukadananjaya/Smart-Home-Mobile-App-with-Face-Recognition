from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, logs, faceRecognition, doorHandle
from .database import init_db

# initialize the app
app = FastAPI()
init_db()

# origins = [
#     # "http://localhost:3000",  # If you are also accessing from a local web app
#     # "http://192.168.8.100:8081",  # Your React Native Metro server IP
#     # "exp://192.168.8.100:8081",  # For Expo Go on the same network
#     "*"
   
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(logs.router)
app.include_router(faceRecognition.router)
app.include_router(doorHandle.router)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

@app.get("/")
def read_root():
    return {"Hello": "World"}

