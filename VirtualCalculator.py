from dotenv import load_dotenv
load_dotenv()
import cv2 as cv
import numpy as np
import time
import os
import HandTrackingModule as htm
import base64
import io
import streamlit as st
from io import BytesIO
from PIL import Image

def convert_image_to_base64(image):
    # Convert OpenCV image (BGR) to RGB
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    
    # Convert RGB image to PIL Image
    pil_image = Image.fromarray(image_rgb)
    
    # Save the PIL Image to a byte buffer
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    
    # Encode the byte buffer to a base64 string
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return img_str

def see_base64_img(image_base64):
    image_bytes = base64.b64decode(image_base64)

    # Create a PIL Image from the byte array
    image_buffer = io.BytesIO(image_bytes)
    image = Image.open(image_buffer)

    # Display the image
    image.show()
    return image

# import streamlit as st
import os
import google.generativeai as genai
# from PIL import Image

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    print("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    # st.stop()

# model=genai.GenerativeModel("gemini-1.5-flash")

#Function to load gemini pro model and get responses


def get_gemini_response(input, image):
    if input!="":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

brushThickness = 7
eraserThickness = 50

folderPath = "header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

header = overlayList[5]

vid = cv.VideoCapture(-1)
drawColor = (33,255,33)

detector = htm.handDetector()
xp,yp=0,0
imgCanvas = np.zeros((480,640,3),np.uint8)

st.set_page_config(page_title="Virtual Calculator")
st.header("Virtual Calculator")

#Placeholde for image
img_placeholder = st.empty() 

#Placeholder for text
response_placeholder = st.empty()

while True:
    # 1.Import Image
    isTrue, frame = vid.read()

    if isTrue:
        frame = cv.flip(frame, 1)
        # print(frame.shape)

        # 2.Find Hand Landmarks
        frame = detector.findHands(frame)
        lmlist = detector.findPositions(frame, draw=False)

        if len(lmlist) != 0:
            # print(lmlist)

            x1,y1 = lmlist[8][1:]  #tip of index finger
            x2,y2 = lmlist[12][1:] #tip of middle finger

            # print(x1)
            # print(f'{frame.shape}, {imgCanvas.shape}')

            fingers = detector.fingersUp()
            # print(fingers)

            if len(fingers) > 1:
                # 4.Selection Mode
                if fingers[1] and fingers[2] and fingers[3]==0 and fingers[4]==0 and fingers[0]==0:
                    # print("Selection Mode")
                    cv.rectangle(frame, (x1, y1-15), (x2,y2+15), drawColor, cv.FILLED)
                    # print("Selection Mode")

                    if y1 < 84:
                        if x1>130 and x1<190:
                            header = overlayList[2]
                            drawColor = (203,192,255)
                        elif x1>230 and x1<300:
                            header = overlayList[1]
                            drawColor = (0,0,255)
                        elif x1>325 and x1<390:
                            header = overlayList[3]
                            drawColor = (255,0,0)
                        elif x1>425 and x1<480:
                            header = overlayList[0]
                            drawColor = (0,255,0)
                        elif x1>520 and x1<600:
                            header = overlayList[5]
                            drawColor = (0,0,0)

        
                # 5.DrawingMode
                if fingers[1] and fingers[2] == 0:
                    # print("Drawing Mode")
                    cv.circle(frame, (x1,y1), 15, drawColor, cv.FILLED)
                    # print("Drawing Mode")

                    if abs(xp-x1)>30 or abs(yp-y1)>30:
                        xp,yp = x1,y1
                    
                    if drawColor != (33,255,33):
                        if drawColor==(0,0,0):
                            cv.line(frame, (xp,yp), (x1,y1), drawColor, eraserThickness)
                            cv.line(imgCanvas, (xp,yp), (x1,y1), drawColor, eraserThickness)
                    

                        cv.line(frame, (xp,yp), (x1,y1), drawColor, brushThickness)
                        cv.line(imgCanvas, (xp,yp), (x1,y1), drawColor, brushThickness)

                        xp,yp = x1,y1

                #calculating the result
                if fingers[1] and fingers[2] and fingers[4] and fingers[3] and fingers[0]:
                    # print("Calculation Mode") 
                    cv.imwrite("imgCanvas.png", imgCanvas)
                    # image_base64 = convert_image_to_base64(imgCanvas)
                    # image =see_base64_img(image_base64)
                    image_path = "imgCanvas.png"
                    image = Image.open(image_path)
                    response = get_gemini_response("I will be providing a image which has hand written text in it. The text will be some mathemetical expression. Give the answer and explain how you got the answer", image)
                    print(response)
                    response_placeholder.subheader("The response is")
                    response_placeholder.write(response)


        imgGray = cv.cvtColor(imgCanvas, cv.COLOR_BGR2GRAY)
        _, imgInv = cv.threshold(imgGray, 50, 255, cv.THRESH_BINARY_INV)
        imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
        frame = cv.bitwise_and(frame, imgInv)
        frame = cv.bitwise_or(frame, imgCanvas)        

        frame[0:84, 0:640] = header
        cv.waitKey(1)
        cv.imshow("Painter", frame)
        webimg = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_placeholder.image(webimg, caption="Uploaded Image.", use_column_width=True)

        # cv.imshow("Canvas", imgCanvas)