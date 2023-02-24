import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

device = torch.device('mps')
print(torch.has_mps, device)
tokenizer = AutoTokenizer.from_pretrained(
    # or float32 version: revision=KoGPT6B-ryan1.5b
    'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b-float16',
    bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
)

print("tokenizer initialized")
model = AutoModelForCausalLM.from_pretrained(
    # or float32 version: revision=KoGPT6B-ryan1.5b
    'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b-float16',
    pad_token_id=tokenizer.eos_token_id,
    torch_dtype='auto', low_cpu_mem_usage=True
).to(device=device, non_blocking=True)
e = model.eval()
print(e)
print("model initialized")
prompt = '인간처럼 생각하고, 행동하는 \'지능\'을 통해 인류가 이제까지 풀지 못했던'
with torch.no_grad() as t:
    print("load grad")
    tokens = tokenizer.encode(prompt, return_tensors='pt').to(
        device=device, non_blocking=False)
    gen_tokens = model.generate(
        tokens, do_sample=True, temperature=0.8, max_length=64)
    generated = tokenizer.batch_decode(gen_tokens)[0]

print(generated)  # print: 인간처럼 생각하고, 행
