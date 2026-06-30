from flask import Flask, render_template, request, jsonify 
from groq import Groq
import requests
import os
import re
from duckduckgo_search import DDGS

app = Flask(__name__,template_folder='.')
client= Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template('ask.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/nexora")
def nexora():
    return render_template('ask.html')
@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content":f"""
            Explain {question} in simple language for students.

            Answer ONLY in this format:
            1. 

            2. 

            3. 

            4. 

            5. 

            Rules:
            Answer in numbered points only.
            Start each point with 1.,2.,3., etc.
            Each point should be a short paragraph of 2-4 sentences.
            Use simple english.
            Give examples only when helpful.
            Do Not create any diagram.
            Do Not use arrows.
            Do Not use symbols like-> | [].
            Do Not use ##,###,*,**,or markdown.
            Only return the explanation.
            """ 
            
        }],
        model="llama-3.3-70b-versatile",
    )
    answer = chat_completion.choices [0].message.content
    return jsonify({"answer": answer})

@app.route('/get_image')
def get_image():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'success': False, 'error': 'No query provided'})
    
    try:
        # Added color='color' to help prevent DuckDuckGo rate-limit blocks
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=5, color='color'))
            
        if results and 'image' in results[0]:
            # Pull the first valid image URL found
            image_url = results[0]['image']
            return jsonify({'success': True, 'image_url': image_url})
            
    except Exception as e:
        print(f"DuckDuckGo Error: {e}")
        
    return jsonify({'success': False, 'error': 'Could not find an image'})

if __name__ == '__main__':
    app.run(debug=True) 
