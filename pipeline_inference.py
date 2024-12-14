
import torch
from transformers import pipeline
import json
import argparse
import random

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="inference")
    parser.add_argument("--model", type=str, default="Equall/Saul-7B-Instruct-v1")
    parser.add_argument("--model_name", type=str, default="saul-7b")
    parser.add_argument("--train_file", type=str, default=None)
    parser.add_argument("--test_file", type=str, default=None)
    parser.add_argument("--save_file", type=str, default="result.json")
    parser.add_argument("--num_shot", type=int, default=1)
  
    args = parser.parse_args()
    
    pipe = pipeline("text-generation", model=args.model, torch_dtype=torch.bfloat16, device_map="auto")
    
    with open(args.train_file, 'r') as file:
        train_list = json.load(file)
    with open(args.test_file, 'r') as file:
        test_list = json.load(file)   
    
    n = args.num_shot
    
    for num, data in enumerate(test_list):
        
        sampled_elements = random.sample(train_list, n)
        messages=[{"role": "user", "content": "You are a patent expert. Given the following original patent claim texts, revise claims to better withstand legal scrutiny."}]
        
        for i in range(n):
            messages.append({"role": "user", "content": sampled_elements[i]["Claim before"]})
            messages.append({"role": "assistant", "content": sampled_elements[i]["Claim after"]})
        
        messages.append({"role": "user", "content": data["Claim before"]})
        
        prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = pipe(prompt, max_new_tokens=1024, return_full_text=False, do_sample=True, temperature=0.1, top_p=0.95)
        text = outputs[0]["generated_text"]              
        data[args.model_name] = text
        
    with open(args.save_file, 'w') as file:
        json.dump(test_list, file)
            