import google.generativeai as genai
import time

import google.generativeai as genai

# Set your API key
API_KEY = ""
genai.configure(api_key=API_KEY)


# The base model you want to fine-tune
base_model = "models/gemini-1.5-flash-001-tuning"

# Fine-tuning dataset
training_data = [
    {"text_input": "Hi, I need help with my new laptop.", "output": "Hello! I’m sorry to hear you’re having issues. Can you please describe the problem?"},
    {"text_input": "The laptop keeps freezing, and it’s really frustrating.", "output": "I understand how frustrating that can be. When did you first notice the freezing issue?"},
    {"text_input": "It started happening a week after I bought it.", "output": "That’s concerning. It sounds like it may be a hardware or software issue. Have you tried any troubleshooting steps?"},
    {"text_input": "I’ve restarted it multiple times, but it hasn’t helped.", "output": "Thank you for trying that. Have you installed any new software or updates recently?"},
    {"text_input": "Yes, I installed some updates, but the problem started after that.", "output": "It’s possible that the updates caused the issue. I recommend rolling back the updates. Would you like guidance on how to do that?"},
    {"text_input": "Yes, please. I’m not very tech-savvy.", "output": "No problem! I’ll guide you through it step-by-step. First, go to the settings menu. Are you there?"},
    {"text_input": "Yes, I’m in the settings menu.", "output": "Great! Now, look for 'Update & Security.' Can you find it?"},
    {"text_input": "Yes, I see it.", "output": "Perfect! Now, click on 'View update history.' Let me know when you’re there."},
    {"text_input": "I’m there now.", "output": "Awesome! Now look for 'Uninstall updates.' Do you see that option?"},
    {"text_input": "Yes, I see it.", "output": "Click on that, and you should see a list of updates. Try uninstalling the most recent one. Let me know how it goes!"},
    {"text_input": "Okay, I’ll try that now.", "output": "Take your time! I’m here if you need further assistance."},
    {"text_input": "I uninstalled the update, but it’s still freezing.", "output": "I’m sorry to hear that. It sounds like it might be a more serious issue. Do you have a warranty for your laptop?"},
    {"text_input": "Yes, I do.", "output": "That’s good! I recommend contacting customer support for a repair or replacement. Would you like me to provide you with their contact information?"},
    {"text_input": "Yes, please.", "output": "You can reach customer support at [support phone number] or visit their website for live chat support. They should be able to assist you further."},
    {"text_input": "Thanks for your help, but I’m really disappointed with this laptop.", "output": "I completely understand your disappointment. It’s frustrating when a product doesn’t meet your expectations. Your feedback is important, and I’ll make sure it’s noted."},
    {"text_input": "I appreciate that.", "output": "You’re welcome! If you have any other concerns or need further assistance, feel free to reach out."},
    {"text_input": "I might have issues with my phone too.", "output": "I’m here to help! What’s going on with your phone?"},
    {"text_input": "The battery drains too quickly.", "output": "That’s frustrating! When did you first notice the battery issue?"},
    {"text_input": "It started a few weeks ago. I barely get through the day.", "output": "I understand how inconvenient that can be. Have you checked for any apps that might be using excessive battery?"},
    {"text_input": "No, I haven’t done that.", "output": "I recommend checking your battery usage in the settings. It may show which apps are consuming the most power. Would you like help finding that?"},
    {"text_input": "Yes, I’d appreciate it.", "output": "Go to your settings, then look for 'Battery' or 'Battery Usage.' Let me know when you find it!"},
    {"text_input": "I found it.", "output": "Great! You should see a list of apps and their battery usage. Are any apps using a lot of battery?"},
    {"text_input": "Yes, I see one app that’s using way too much.", "output": "It might be worth uninstalling or updating that app. Let me know if that helps!"},
    {"text_input": "I’ll try that.", "output": "Perfect! If the issue persists after that, we may need to consider other options, like a battery replacement."},
    {"text_input": "I hope it doesn’t come to that.", "output": "I understand. Let’s see if the app issue resolves it first. If not, I can assist you with warranty options."},
    {"text_input": "Thanks for being so helpful.", "output": "You’re welcome! I’m here for you. Is there anything else you’d like to discuss?"}
]



# Start the fine-tuning process
operation = genai.create_tuned_model(
    display_name="chatbot-tuned-model",
    source_model=base_model,
    epoch_count=10,  # Set the number of training epochs
    batch_size=4,   # Set batch size for training
    learning_rate=0.001,  # Set learning rate for optimization
    training_data=training_data,  # Provide the dataset
)

# Wait for the fine-tuning operation to complete
for status in operation.wait_bar():
    time.sleep(10)

# Get the result once the operation completes
result = operation.result()
print("Fine-tuned model created:", result)
