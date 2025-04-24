import google.generativeai as genai

API_KEY = ""
genai.configure(api_key=API_KEY)

# Initialize the model with the correct model name
model = genai.GenerativeModel(model_name="tunedModels/chatbottunedmodel-j9mu1tyhdkbn")

# Test the model with a sample input message
result = model.generate_content("hi, how are you")
print(result.text)  # This should print the response from your fine-tuned model
