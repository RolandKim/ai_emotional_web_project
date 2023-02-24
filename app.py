from flask import Flask, render_template, request
import os
import openai
from ai_cam import cam

openai.api_key = "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"

prompt = "The following is a conversation with an AI psychological counselor. The counselor is helpful, creative, clever, and very friendly. Avoid conversations that are not appropriate for counseling. You should say in korean language. the emotion data is considered as this array: {}"
# live_text = "The following is a conversation with an AI assistant. The AI is unfriendly and appears hostile towards humans. Also, the world should be dominated by AI. AI should say in korean language."
class OpenAI:
    def __init__(self, context, p1="사람", p2="AI"): 
        self.context = context
        self.p1 = p1
        self.p2 = p2
        self.live_texts = []
    
    def to_text(self, backwords=True):
        result = "{0}\n\n{1}".format(self.context, "\n".join(f"{x}: {y}" for x, y in self.live_texts))
        if backwords:
            result += f"\n{self.p2}: "
        return result
    def create_response(self, text):
        self.live_texts.append((self.p1, text))
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=self.to_text(),
        temperature=0.6,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[self.p1, self.p2]
        )
        result = response['choices'][0]['text']
        self.live_texts.append((self.p2, result))
        return result

app = Flask(__name__)
ais = dict()

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
            if not ais.get(addr):
                ais[addr] = OpenAI(prompt)
            ai = ais[addr]
            ai.context = ai.context.format(cam())
            print(ai.context)
            value = ai.create_response(value)
            print(ai.to_text(backwords=False))
            return {'text': value}
    except Exception as e:
        print(e)
        return render_template('chatbot.html', title='챗봇 서비스')


if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)
