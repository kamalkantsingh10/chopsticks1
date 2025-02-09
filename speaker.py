import sys
from robot_hat import TTS

# Check if there are enough command line arguments
if len(sys.argv) > 1:
    text_to_say = sys.argv[1]  # Get the first argument passed from the command line
else:
    text_to_say = "chopsticks is bored"  # Default text if no arguments are provided

# Initialize the TTS class
tts = TTS(lang='it-IT', engine="espeak")

# Read the text
tts.say("chopsticks is bored")
tts.say("chopsticks is happy")
tts.say("chopsticks is sad")
tts.say("chopsticks is sleepy")

# Display all supported languages
print(tts.supported_lang())