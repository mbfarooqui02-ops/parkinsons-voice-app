# Parkinson's Voice Analysis App

Voice feature extraction and tracking system for Parkinson's disease patients.

## Purpose
Help track vocal changes and measure improvement from voice therapy exercises (LSVT LOUD protocol).

## Project Structure
```
parkinson-voice-app/
├── data/
│   ├── baseline/         # Initial recordings
│   ├── followup/         # Progress recordings
│   └── recordings/       # All audio files
├── reports/              # Generated analysis reports
├── src/
│   ├── voice_analyzer.py     # Core feature extraction
│   ├── record_protocol.py    # Recording instructions
│   └── batch_analyzer.py     # Batch processing
├── tests/
├── requirements.txt
└── README.md
```

## Setup

1. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Get Recording Instructions
```bash
python src/record_protocol.py
```

### 2. Analyze Single Audio File
```python
from src.voice_analyzer import analyze_audio_file

analyze_audio_file("data/baseline/uncle_baseline_vowel.wav")
```

### 3. Batch Analysis
```bash
python src/batch_analyzer.py
# Choose option 1, enter folder path
```

### 4. Compare Progress
```bash
python src/batch_analyzer.py
# Choose option 2
# Enter baseline folder: data/baseline
# Enter followup folder: data/week_4
```

## Voice Features Measured

- **Intensity (dB)**: Loudness of voice
- **Pitch Mean (Hz)**: Average pitch
- **Pitch Range (Hz)**: Pitch variation (monotone indicator)
- **Jitter (%)**: Pitch stability
- **Shimmer (%)**: Amplitude stability
- **HNR (dB)**: Harmonics-to-Noise Ratio (clarity)

## Recording Protocol

- **Format**: WAV (44.1 kHz or higher)
- **Environment**: Quiet room
- **Distance**: 6-8 inches from microphone
- **Tasks**: 
  1. Sustained "AAAAH" (5 sec)
  2. Pitch glide
  3. Counting 1-20
  4. Reading sentences
  5. Spontaneous speech

## Expected Improvements (LSVT LOUD)

- Intensity: +3 to +10 dB
- Pitch Range: +10 to +40 Hz
- HNR: +2 to +5 dB
- Timeline: 4-8 weeks with consistent practice

## Next Steps

- [ ] Record baseline (Week 0)
- [ ] Start LSVT LOUD exercises
- [ ] Record weekly progress
- [ ] Build mobile app for real-time feedback
- [ ] Add exercise prompts and tracking

## Resources

- LSVT LOUD: https://www.lsvtglobal.com/
- Parkinson's Foundation: https://www.parkinson.org/
```

---

## Step 10: Create .gitignore

Open `.gitignore` and paste:
```
# Virtual environment
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Audio files (large)
*.wav
*.mp3
*.m4a
*.aac

# Data files
*.csv
data/
reports/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/

# Keep folder structure but ignore contents
!data/.gitkeep
!reports/.gitkeep