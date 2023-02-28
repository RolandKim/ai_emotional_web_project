import openai
# from ai_cam import cam, free_cam

def set_api(key):
    openai.api_key = key

class ChatAI:
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
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[self.p1, self.p2]
        )
        result = response['choices'][0]['text']
        self.live_texts.append((self.p2, result))
        return result
