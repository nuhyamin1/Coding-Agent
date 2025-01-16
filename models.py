# import google.generativeai as genai

# GOOGLE_API_KEY = "AIzaSyAG5vKQUinA-jka5UEwRHBOssvcG1NxD-o"
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel("gemini-exp-1206")

# Test generate text 
# prompt = "Write a short story that makes me cry"
# response = model.generate_content(prompt, stream=True)
# for chunk in response:
#     if chunk.parts:  # Ensure there are parts in the chunk
#         for part in chunk.parts:
#             print(part.text, end="")  # Print the text of each part
# print() # Add a newline at the end


from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)