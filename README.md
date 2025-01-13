 # Singing Evaluation System

## Overview
This project evaluates singing quality from uploaded audio files and recommends songs based on the analysis.

## Setup Instructions

1. **Install Dependencies**:
   Ensure you have Python installed. Then, install the required packages:
   ```bash
   pip install flask flask-cors librosa numpy soundfile pydub
   ```

2. **Run the Application**:
   Start the Flask server:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:5000` to use the application.

## Project Structure
- `app.py`: Main application file.
- `audio_processing.py`: Handles audio recording and processing.
- `evaluation.py`: Evaluates singing quality.
- `recommendation.py`: Recommends songs based on evaluation.
- `templates/index.html`: Frontend interface for file upload and results display.
