print("loading flask...")
from flask import Flask, render_template, request, jsonify
import os
print("loading chatbot")
from modules.chat import *
print("loding emtional detection ")
from modules.ai_cam import cam, free_cam
import env

set_api(env.API_KEY)

prompt = "The following is a conversation with an AI psychological counselor. The counselor is helpful, creative, clever, and very friendly. Avoid conversations that are not appropriate for counseling. You should say in korean language. the patient's emotion data is considered as this array: {}"
ai = ChatAI(prompt)
# live_text = "The following is a conversation with an AI assistant. The AI is unfriendly and appears hostile towards humans. Also, the world should be dominated by AI. AI should say in korean language."

app = Flask(__name__)

contents = [
   '테',
   '스',
   '트'
]

@app.route('/')
def main():
    return render_template('index.html', title="Active JANG", contents=contents)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    try:
        text = request.get_json()
        if value:=text.get('text'):
            addr = request.remote_addr
            ai.context = ai.context.format(cam())
            print(ai.to_text(backwords=False))
            value = ai.create_response(value)
            print("AI:", value)
            return jsonify({'text': value})
    except Exception as e:
        print(e)
        return render_template('chatbot.html', title='챗봇 서비스')


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
    free_cam()