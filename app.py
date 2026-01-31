from flask import Flask, render_template, request, send_file, jsonify
import pyttsx3
import os
from datetime import datetime
import subprocess
import wave

app = Flask(__name__)

# Create necessary directories
AUDIO_DIR = os.path.join(os.path.dirname(__file__), 'static', 'audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

# Tone configurations
TONE_SETTINGS = {
    'neutral': {'rate': 150, 'pitch': 1.0},
    'happy': {'rate': 180, 'pitch': 1.15},
    'sad': {'rate': 120, 'pitch': 0.85},
    'calm': {'rate': 130, 'pitch': 0.95},
    'energetic': {'rate': 200, 'pitch': 1.25},
    'professional': {'rate': 160, 'pitch': 1.0},
    'gentle': {'rate': 140, 'pitch': 0.98}
}

def adjust_wav_pitch(input_file, output_file, pitch_factor):
    """Adjust pitch of WAV file by changing sample rate"""
    try:
        # Read input WAV file
        with wave.open(input_file, 'rb') as wav_in:
            params = wav_in.getparams()
            frames = wav_in.readframes(params.nframes)
            
        # Calculate new sample rate
        new_rate = int(params.framerate * pitch_factor)
        
        # Write output with new sample rate
        with wave.open(output_file, 'wb') as wav_out:
            wav_out.setparams((
                params.nchannels,
                params.sampwidth,
                new_rate,
                params.nframes,
                params.comptype,
                params.compname
            ))
            wav_out.writeframes(frames)
        
        return True
    except Exception as e:
        print(f"Error adjusting pitch: {e}")
        return False

def convert_wav_to_mp3(input_wav, output_mp3):
    """Convert WAV to MP3 using FFmpeg"""
    try:
        # Convert using FFmpeg
        subprocess.run([
            'ffmpeg',
            '-i', input_wav,
            '-codec:a', 'libmp3lame',
            '-b:a', '192k',
            '-y',  # Overwrite output file
            output_mp3
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return True
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg.")
        return False
    except Exception as e:
        print(f"Error converting to MP3: {e}")
        return False

def generate_speech_pyttsx3(text, tone='neutral', voice_gender='female'):
    """Generate speech using pyttsx3 with tone variations"""
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()
        
        # Get tone settings
        settings = TONE_SETTINGS.get(tone, TONE_SETTINGS['neutral'])
        
        # Set voice gender
        voices = engine.getProperty('voices')
        if voice_gender == 'male' and len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
        elif voice_gender == 'female' and len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        
        # Set speech rate
        engine.setProperty('rate', settings['rate'])
        
        # Set volume
        engine.setProperty('volume', 1.0)
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_wav = os.path.join(AUDIO_DIR, f'speech_{timestamp}_temp.wav')
        adjusted_wav = os.path.join(AUDIO_DIR, f'speech_{timestamp}_adjusted.wav')
        final_mp3 = os.path.join(AUDIO_DIR, f'speech_{timestamp}_{tone}.mp3')
        final_filename = f'speech_{timestamp}_{tone}.mp3'
        
        # Save to file
        engine.save_to_file(text, temp_wav)
        engine.runAndWait()
        
        # Check if temp file was created
        if not os.path.exists(temp_wav):
            print("Failed to create temp WAV file")
            return None
        
        # Apply pitch adjustment if needed
        if settings['pitch'] != 1.0:
            if adjust_wav_pitch(temp_wav, adjusted_wav, settings['pitch']):
                wav_to_convert = adjusted_wav
            else:
                wav_to_convert = temp_wav
        else:
            wav_to_convert = temp_wav
        
        # Convert to MP3 using FFmpeg
        if convert_wav_to_mp3(wav_to_convert, final_mp3):
            # Clean up temporary files
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
            if os.path.exists(adjusted_wav) and adjusted_wav != temp_wav:
                os.remove(adjusted_wav)
            
            return final_filename
        else:
            # If FFmpeg fails, rename WAV to use as fallback
            fallback_filename = f'speech_{timestamp}_{tone}.wav'
            fallback_path = os.path.join(AUDIO_DIR, fallback_filename)
            os.rename(wav_to_convert, fallback_path)
            
            # Clean up other temp files
            if os.path.exists(temp_wav) and temp_wav != wav_to_convert:
                os.remove(temp_wav)
            if os.path.exists(adjusted_wav) and adjusted_wav != wav_to_convert:
                os.remove(adjusted_wav)
            
            return fallback_filename
    
    except Exception as e:
        print(f"Error generating speech: {e}")
        import traceback
        traceback.print_exc()
        return None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Handle text-to-speech generation request"""
    try:
        data = request.json
        text = data.get('text', '')
        tone = data.get('tone', 'neutral')
        voice_gender = data.get('voice_gender', 'female')
        
        # Validate input
        if not text or len(text.strip()) == 0:
            return jsonify({'error': 'Please enter some text'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text is too long. Maximum 5000 characters.'}), 400
        
        # Generate speech
        filename = generate_speech_pyttsx3(text, tone, voice_gender)
        
        if filename:
            return jsonify({
                'success': True,
                'filename': filename,
                'audio_url': f'/static/audio/{filename}'
            })
        else:
            return jsonify({'error': 'Failed to generate speech. Please check if FFmpeg is installed.'}), 500
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    """Handle audio file download"""
    try:
        filepath = os.path.join(AUDIO_DIR, filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup():
    """Clean up old audio files"""
    try:
        # Remove files older than 1 hour
        current_time = datetime.now()
        for filename in os.listdir(AUDIO_DIR):
            filepath = os.path.join(AUDIO_DIR, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if (current_time - file_time).seconds > 3600:
                    os.remove(filepath)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("AI Voice Generation System Starting...")
    print("="*60)
    print("\nChecking FFmpeg installation...")
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        print("✓ FFmpeg is installed and working!")
        print("  Audio will be exported as MP3 files.")
    except:
        print("⚠ WARNING: FFmpeg not found!")
        print("  Audio will be exported as WAV files instead.")
        print("  Install FFmpeg for MP3 support: https://ffmpeg.org")
    
    print("\n" + "="*60)
    print("Server starting on: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
