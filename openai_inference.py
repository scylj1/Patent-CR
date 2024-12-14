
import json
from openai import OpenAI
import os
import random
import argparse

def openai_inference(args):
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", args.openai_key))
    
    with open(args.train_file, 'r') as file:
        train_list = json.load(file)
    with open(args.test_file, 'r') as file:
        test_list = json.load(file) 
        
    model = args.model_name
    n = args.num_shot
    
    for data in test_list:
        
        sampled_elements = random.sample(train_list, n)
        messages=[{"role": "system", "content": "You are a patent expert. Given the following original patent claim texts, revise claims to better withstand legal scrutiny. "}]
        
        for i in range(n):
            messages.append({"role": "system", "name":"example_user", "content": sampled_elements[i]["Claim before"]})
            messages.append({"role": "system", "name":"example_assistant", "content": sampled_elements[i]["Claim after"]})
        
        messages.append({"role": "user", "content": data["Claim before"]})

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.1,
            )

            data[model] = response.choices[0].message.content
     
        except:
            print("fail")
            print(data["Index"])
            continue
            
    with open(args.save_file, 'w') as file:
        json.dump(test_list, file)


if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description="Openai settings")

    parser.add_argument("--model_name", type=str, default="gpt-4-turbo")
    parser.add_argument("--openai_key", type=str, default=None)
    parser.add_argument("--train_file", type=str, default=None)
    parser.add_argument("--test_file", type=str, default=None)
    parser.add_argument("--save_file", type=str, default="result.json")
    parser.add_argument("--num_shot", type=int, default=1)

    args = parser.parse_args()

    openai_inference(args)
