import httpx
from fastapi import APIRouter, HTTPException,WebSocket

router = APIRouter()

# from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests


# # Define the authentication model
# class AuthRequest(BaseModel):
#     username: str
#     password: str


# # Dummy authentication data
# AUTH_DATA = {
#     "username": "admin",
#     "password": "123"
# }


# @router.post("/doorHnadle/")
# async def authenticate(auth_request: AuthRequest):
#     if auth_request.username == AUTH_DATA["username"] and auth_request.password == AUTH_DATA["password"]:
#         # Authentication successful, send a signal to the ESP32 to blink the LED
#         try:
#             esp32_ip = "192.168.8.133"  # Replace with your ESP32's IP address
#             requests.get(f"http://{esp32_ip}/blink")
#             return {"status": "Success", "message": "LED was blinked"}
#         except requests.exceptions.RequestException as e:
#             raise HTTPException(status_code=500, detail="Failed to connect to ESP32")
#     else:
#         raise HTTPException(status_code=401, detail="Authentication failed")
    
@router.get("/doorHandle/")
async def blink_led():
    try:
        esp32_ip = "192.168.8.133"  # Replace with your ESP32's IP address
        requests.get(f"http://{esp32_ip}/blink")
        return {"status": "Success", "message": "LED was blinked"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to connect to ESP32")






# ESP32_IP = "http://192.168.8.133"  # Replace with your ESP32's IP address

# @router.post("/control-door/")
# async def control_door(action: str):
#     if action == "unlock":
#         async with httpx.AsyncClient() as client:
#             response = await client.get(f"{ESP32_IP}/unlock")
#             return {"message": response.text}
#     else:
#         return {"message": "Invalid action"}