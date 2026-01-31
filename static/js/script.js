// DOM Elements
const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const generateBtn = document.getElementById('generateBtn');
const audioOutput = document.getElementById('audioOutput');
const audioPlayer = document.getElementById('audioPlayer');
const downloadBtn = document.getElementById('downloadBtn');
const newGenerationBtn = document.getElementById('newGenerationBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const toneCards = document.querySelectorAll('.tone-card');

// State
let currentFilename = null;

// Character count update
textInput.addEventListener('input', () => {
    const count = textInput.value.length;
    charCount.textContent = count;
    
    // Change color based on character count
    if (count > 4500) {
        charCount.style.color = '#ef4444';
    } else if (count > 3000) {
        charCount.style.color = '#f59e0b';
    } else {
        charCount.style.color = '#6366f1';
    }
});

// Tone card selection
toneCards.forEach(card => {
    card.addEventListener('click', () => {
        // Remove active class from all cards
        toneCards.forEach(c => c.classList.remove('active'));
        // Add active class to clicked card
        card.classList.add('active');
        // Check the radio button
        card.querySelector('input[type="radio"]').checked = true;
    });
});

// Generate speech
generateBtn.addEventListener('click', async () => {
    const text = textInput.value.trim();
    
    // Validation
    if (!text) {
        showError('Please enter some text to generate speech.');
        return;
    }
    
    if (text.length > 5000) {
        showError('Text is too long. Maximum 5000 characters allowed.');
        return;
    }
    
    // Get selected options
    const tone = document.querySelector('input[name="tone"]:checked').value;
    const voiceGender = document.querySelector('input[name="voice_gender"]:checked').value;
    
    // Show loading, hide errors and audio output
    showLoading();
    hideError();
    hideAudioOutput();
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                tone: tone,
                voice_gender: voiceGender
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            currentFilename = data.filename;
            audioPlayer.src = data.audio_url;
            showAudioOutput();
            hideLoading();
            
            // Auto-play the audio
            setTimeout(() => {
                audioPlayer.play().catch(err => {
                    console.log('Autoplay prevented:', err);
                });
            }, 300);
        } else {
            throw new Error(data.error || 'Failed to generate speech');
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred while generating speech. Please try again.');
        hideLoading();
    }
});

// Download audio
downloadBtn.addEventListener('click', () => {
    if (currentFilename) {
        window.location.href = `/download/${currentFilename}`;
    }
});

// New generation
newGenerationBtn.addEventListener('click', () => {
    hideAudioOutput();
    textInput.value = '';
    charCount.textContent = '0';
    textInput.focus();
    
    // Reset to neutral tone
    document.querySelector('input[name="tone"][value="neutral"]').checked = true;
    toneCards.forEach(card => card.classList.remove('active'));
    document.querySelector('input[name="tone"][value="neutral"]').closest('.tone-card').classList.add('active');
});

// Helper functions
function showLoading() {
    loadingIndicator.style.display = 'block';
    generateBtn.disabled = true;
}

function hideLoading() {
    loadingIndicator.style.display = 'none';
    generateBtn.disabled = false;
}

function showAudioOutput() {
    audioOutput.style.display = 'block';
    audioOutput.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideAudioOutput() {
    audioOutput.style.display = 'none';
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorMessage.style.display = 'none';
}

// Sample text examples (optional feature)
const sampleTexts = [
    "Hello! Welcome to our AI voice generation system. This technology can transform any text into natural-sounding speech with various emotional tones.",
    "The future of artificial intelligence is incredibly exciting. Voice synthesis has come a long way in making digital assistants sound more human and expressive.",
    "Thank you for using our service. We hope you enjoy the different voice tones and find this tool useful for your projects.",
    "Good morning! Today is a beautiful day full of possibilities. Let's make the most of it with positive energy and enthusiasm.",
    "In the world of technology, innovation never stops. Every day brings new advancements that make our lives easier and more connected."
];

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        generateBtn.click();
    }
    
    // Escape to close error
    if (e.key === 'Escape') {
        hideError();
    }
});

// Add sample text button functionality (optional)
function loadSampleText() {
    const randomText = sampleTexts[Math.floor(Math.random() * sampleTexts.length)];
    textInput.value = randomText;
    textInput.dispatchEvent(new Event('input'));
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('AI Voice Generator initialized');
    textInput.focus();
    
    // Cleanup old files on page load
    fetch('/cleanup', { method: 'POST' })
        .catch(err => console.log('Cleanup error:', err));
});

// Add visual feedback for audio loading
audioPlayer.addEventListener('loadstart', () => {
    audioPlayer.style.opacity = '0.5';
});

audioPlayer.addEventListener('canplay', () => {
    audioPlayer.style.opacity = '1';
});

// Add error handling for audio playback
audioPlayer.addEventListener('error', (e) => {
    showError('Failed to load audio file. Please try generating again.');
    console.error('Audio error:', e);
});

// Smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Add animation on scroll (optional enhancement)
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'slideIn 0.5s ease forwards';
        }
    });
}, observerOptions);

// Observe cards for animation
document.querySelectorAll('.card').forEach(card => {
    observer.observe(card);
});
