# AI-Based Multi-Tone Voice Generation System

A modern web application that converts text to speech with multiple voice tones and emotional expressions using AI-powered speech synthesis.

## Features

- 🎤 **Multiple Voice Tones**: Neutral, Happy, Sad, Calm, Energetic, Professional, and Gentle
- 👥 **Voice Gender Selection**: Male and Female voices
- 🎨 **Modern UI**: Beautiful, responsive design with smooth animations
- 💾 **Download Audio**: Save generated speech as MP3 files
- ⚡ **Real-time Generation**: Fast text-to-speech processing
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **TTS Engine**: pyttsx3
- **Audio Processing**: Pydub
- **UI Design**: Custom CSS with modern gradients and animations

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- FFmpeg (for audio processing)

### Step 1: Install FFmpeg

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract and add to system PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Step 2: Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# For Linux systems, you may also need:
sudo apt-get install espeak
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

1. **Enter Text**: Type or paste your text in the input area (max 5000 characters)
2. **Select Voice Gender**: Choose between Male or Female voice
3. **Choose Tone**: Select from 7 different emotional tones
4. **Generate**: Click "Generate Speech" button
5. **Listen**: Audio will play automatically
6. **Download**: Save the audio file to your device

## Available Voice Tones

| Tone | Description | Use Case |
|------|-------------|----------|
| Neutral | Balanced & Clear | General purpose, documentation |
| Happy | Cheerful & Upbeat | Celebrations, positive messages |
| Sad | Somber & Low | Sympathy, serious topics |
| Calm | Peaceful & Soothing | Meditation, relaxation |
| Energetic | Fast & Dynamic | Sports, exciting announcements |
| Professional | Formal & Clear | Business, presentations |
| Gentle | Soft & Warm | Children's content, kindness |

## Project Structure

```
ai-voice-generator/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── templates/
│   └── index.html         # Main HTML template
│
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   ├── js/
│   │   └── script.js      # JavaScript functionality
│   └── audio/             # Generated audio files (auto-created)
│
└── documentation/
    └── PROJECT_DOCUMENT.txt
```

## API Endpoints

### POST /generate
Generate speech from text

**Request Body:**
```json
{
    "text": "Your text here",
    "tone": "neutral",
    "voice_gender": "female"
}
```

**Response:**
```json
{
    "success": true,
    "filename": "speech_20240131_123456_neutral.mp3",
    "audio_url": "/static/audio/speech_20240131_123456_neutral.mp3"
}
```

### GET /download/<filename>
Download generated audio file

### POST /cleanup
Remove old audio files (>1 hour old)

## Customization

### Modifying Tone Settings

Edit the `TONE_SETTINGS` dictionary in `app.py`:

```python
TONE_SETTINGS = {
    'custom_tone': {
        'rate': 150,      # Speech rate (words per minute)
        'pitch': 1.0,     # Pitch multiplier
        'speed': 1.0      # Speed multiplier
    }
}
```

### Adding New Tones

1. Add tone settings to `TONE_SETTINGS` in `app.py`
2. Add tone card HTML in `index.html`
3. Add styling in `style.css` if needed

## Troubleshooting

### "No module named 'pyttsx3'"
```bash
pip install pyttsx3
```

### "FFmpeg not found"
Install FFmpeg using the instructions in the Installation section

### Audio not playing
- Check browser console for errors
- Ensure FFmpeg is properly installed
- Try a different browser

### Voice not changing
- This depends on available system voices
- On Windows, SAPI5 voices are used
- On macOS, NSSpeechSynthesizer voices are used
- On Linux, espeak voices are used

## Performance Optimization

- Audio files older than 1 hour are automatically cleaned up
- MP3 format is used for smaller file sizes
- Bitrate is set to 192kbps for good quality

## Security Considerations

- Input text is limited to 5000 characters
- File downloads are restricted to generated audio files
- Automatic cleanup prevents disk space issues

## Future Enhancements

- [ ] Neural TTS integration (Google Cloud TTS, AWS Polly)
- [ ] Multi-language support
- [ ] Voice cloning capabilities
- [ ] Real-time voice modulation
- [ ] Mobile application
- [ ] API for external integration
- [ ] Custom voice profiles
- [ ] Batch processing

## Applications

- **Education**: E-learning platforms, audiobooks
- **Accessibility**: Screen readers, assistive technology
- **Business**: IVR systems, announcements
- **Content Creation**: Podcasts, YouTube videos
- **Entertainment**: Game characters, animations

## License

This project is for educational purposes. Feel free to modify and use as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Credits

Developed as part of AI-Based Multi-Tone Voice Generation System project.

## Support

For issues or questions, please check:
- FFmpeg documentation: https://ffmpeg.org/documentation.html
- pyttsx3 documentation: https://pyttsx3.readthedocs.io/
- Flask documentation: https://flask.palletsprojects.com/

---

**Note**: This system demonstrates AI speech synthesis capabilities. For production use, consider integrating professional TTS services like Google Cloud TTS, Amazon Polly, or Microsoft Azure Speech Services for higher quality voices.
