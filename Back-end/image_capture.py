

import cv2
import base64
import asyncio
import websockets
import requests

# URL to send HTTP request to ESP32 for LED blinking
ESP32_LED_URL = "http://192.168.8.133/led_blink"  # Replace <esp32_ip> with your ESP32's IP address

async def send_video():
    uri = "ws://localhost:8000/ws"  # Replace <server_ip> with the server's IP address
    try:
        async with websockets.connect(uri) as websocket:
            cap = cv2.VideoCapture(0)
            try:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        print("Failed to capture frame")
                        break

                    # Encode the frame as a JPEG image and then to a base64 string
                    _, buffer = cv2.imencode('.jpg', frame)
                    img_str = base64.b64encode(buffer).decode('utf-8')

                    # Send the base64 image string over WebSocket
                    await websocket.send(img_str)

                    try:
                        # Wait for the server response with a timeout (in seconds)
                        response = await asyncio.wait_for(websocket.recv(), timeout=10)
                        print(f"Server response: {response}")

                        if "verified" in response.lower():
                            # Send request to ESP32 to blink LED
                            try:
                                esp32_response = requests.get(ESP32_LED_URL)
                                if esp32_response.status_code == 200:
                                    print("LED blinked successfully")
                                else:
                                    print(f"Failed to blink LED, status code: {esp32_response.status_code}")
                            except requests.exceptions.RequestException as e:
                                print(f"Error communicating with ESP32: {e}")
                            break  # Exit after successful verification

                    except asyncio.TimeoutError:
                        print("No response from server, stopping camera.")
                        break  # Exit the loop if the server does not respond within the timeout

                    # Display the frame locally (optional)
                    cv2.imshow('Client Camera', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            finally:
                cap.release()
                cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error occurred: {e}")

# Run the asyncio event loop
asyncio.run(send_video())
