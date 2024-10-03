import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Categories
CATEGORIES = [
    "Data Science",
    "Artificial Intelligence",
    "Software Development",
    "Career Advice",
    "Technology Trends",
    "Business & Entrepreneurship",
    "Personal Development",
    "Industry News"
]

# Short prompts for good posts
SHORT_PROMPTS = [
    "Share a recent achievement",
    "Discuss an industry trend",
    "Offer a quick tip",
    "Ask for opinions on a topic",
    "Share an inspiring quote",
    "Highlight a learning experience",
    "Celebrate a team success",
    "Pose a thought-provoking question"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        category = request.form['category']
        
        # Generate LinkedIn post
        linkedin_post = generate_linkedin_post(input_text, category)
        
        # Generate image prompt
        image_prompt = generate_image_prompt(linkedin_post, category)
        
        return jsonify({
            'linkedin_post': linkedin_post,
            'image_prompt': image_prompt
        })
    
    return render_template('index.html', categories=CATEGORIES, short_prompts=SHORT_PROMPTS)

def generate_linkedin_post(input_text, category):
    prompt = f"""
    Generate a professional LinkedIn post based on the following input and category:
    
    Input: {input_text}
    Category: {category}
    
    Follow these guidelines:
    1. Make it concise and engaging (150-200 words)
    2. Start with a hook or attention-grabbing statement
    3. Use a structured format (e.g., "One Day or Day One", Informative, or Inspirational)
    4. Include 2-3 relevant emojis
    5. Use bold text for important points (surround with **asterisks**)
    6. Add a call-to-action or question at the end
    7. Include 3-5 relevant hashtags
    8. Ensure the content is tailored to the selected category
    
    Post:
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content

def generate_image_prompt(linkedin_post, category):
    prompt = f"""
    Generate an image prompt based on the following LinkedIn post and category:
    
    LinkedIn Post: {linkedin_post}
    Category: {category}
    
    Follow this structure:
    1. Specify the format (e.g., digital illustration, photograph, 3D render)
    2. Describe the main subject or focal point
    3. Add details about the setting or background
    4. Describe the style, mood, and color palette
    5. Add any additional details or elements to enhance the image
    
    Keep the prompt concise (50-75 words) and visually descriptive.
    
    Image Prompt:
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)