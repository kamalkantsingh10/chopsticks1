import sys
from robot_hat import TTS

# Check if there are enough command line arguments
if len(sys.argv) > 1:
    text_to_say = sys.argv[1]  # Get the first argument passed from the command line
else:
    text_to_say = "chopsticks is bored"  # Default text if no arguments are provided

# Initialize the TTS class
tts = TTS(lang='en-GB', engine="espeak")

# Read the text
tts.say(text_to_say)

# Display all supported languages
print(tts.supported_lang())