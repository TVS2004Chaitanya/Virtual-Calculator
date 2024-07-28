# Virtual-Calculator
Virtual Calculator/using open-cv/using google-generativeai


This code sets up a virtual calculator application using OpenCV, Streamlit, and Google's Generative AI model, Gemini 1.5 Flash. It leverages hand tracking for interaction and gesture recognition to select drawing colors and modes


## Features

- Easy to use
- Supports multiple formats
- Open source

## Demo

- **Multiplication**  
  <img src="https://github.com/user-attachments/assets/b449fff4-8fb5-4270-9ebe-1800fb13e0eb" width="600" alt="Virtual Painter Drawing Mode">

- **Division**  
  <img src="https://github.com/user-attachments/assets/133ceac7-2391-40ce-ae86-41b92a760c6f" width="600" alt="Virtual Eraser Mode">

## How to Use

- Use your index finger to draw freely on the screen.
- Use both index finger and the middle finger to select the elements.
- You can also both index finger and middle finger to be in the standby mode(Move acroos the screen without drawing).
- Show your palm to tell the program to calculate the mathemetical equation written
- Wait for a few seconds while the google-generativeai processes the image and gives the answer

## Setup and Usage

1. Clone the repository:
   ```sh
   git clone https://github.com/TVS2004Chaitanya/Virtual-Calculator.git
   cd Virtual-Calculator
## Description

- **Virtual Calculator**: This project builds upon the logic from the [Virtual Painter](https://github.com/TVS2004Chaitanya/Virtual-Painter). Please review the Virtual Painter repository for foundational concepts and implementation details.

- **header**: This folder contains all the images required for the project, including the overlays for color selection.

- **requirements.txt**: This text file lists all the libraries required for this project. Ensure you install these dependencies before running the application.

- **HandTrackingModule.py**: This Python file contains a class for detecting hands and includes several helper functions. It's crucial to understand this module before using the project, as it forms the core of the hand tracking functionality.

- **VirtualCalculator.py**: This Python file contains the main logic for the Virtual Calculator. It captures hand-drawn mathematical expressions, sends the image to Google Generative AI, and displays the processed answer.


##Dependecies
- pip install -r requirements.txt, I suggest you to create an environment before downloading the dependencies.
- The above command helps to install all the dependecies required.
