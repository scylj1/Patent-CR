
prompt = "You will be given the draft claims and the referenced claims of the same patent. \
Your task is to rate the draft claims on four metrics using the referenced claims as the gold standard. \
Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed. \
Evaluation Criteria: \
1. Completeness of Essential Features (0-100): The extent to which the generated claims encapsulated all critical aspects of the invention. \
- 0-20: Most essential features are missing or poorly described. \
- 21-40: Some essential features are present but significant gaps remain. \
- 41-60: Majority of essential features are covered but with minor omissions. \
- 61-80: Almost all essential features are well described with very few gaps. \
- 81-100: All essential features are thoroughly and comprehensively covered. \
2. Conceptual Clarity (0-100): The clarity and unambiguity of the language used in the claims. \
- 0-20: Claims are very unclear and ambiguous.\
- 21-40: Claims have significant clarity issues, making them difficult to understand.\
- 41-60: Claims are mostly clear but contain some ambiguous language.\
- 61-80: Claims are clear with minimal ambiguity.\
- 81-100: Claims are exceptionally clear and completely unambiguous. \
3. Consistency in Terminology (0-100): The uniformity in the use of terms throughout the claims. \
- 0-20: Terminology is highly inconsistent.\
- 21-40: Significant inconsistencies in terminology.\
- 41-60: Some inconsistencies in terminology but mostly uniform.\
- 61-80: Terminology is largely consistent with minor inconsistencies.\
- 81-100: Terminology is completely consistent throughout.\
4. Technical Correctness of Feature Linkages (0-100): The accuracy with which the features were interconnected and related.\
- 0-20: Features are poorly linked with many inaccuracies.\
- 21-40: Significant issues with the linkages of features.\
- 41-60: Mostly accurate linkages with some incorrect connections.\
- 61-80: Accurate linkages with minor inaccuracies.\
- 81-100: Features are accurately and correctly linked throughout.\
Evaluation Steps: \
1. Read the referenced claims carefully and identify the inventions' features. Assume the referenced claims have scores of 100 in all Evaluation Criteria. \
2. Read the draft claims and compare it to the referenced claims. \
3. Assign a score for each metric based on the Evaluation Criteria. \
Example: \
Referenced Claims:  \
<<Claims>> \
Draft Claims:  \
<<Claims>> \
Evaluation Form (scores ONLY): \
- Completeness of Essential Features: X, - Conceptual Clarity: X, - Consistency in Terminology: X, - Technical Correctness of Feature Linkages: X. "

import json
from openai import OpenAI
import os
import tiktoken
import random
import re
import argparse

def openai_inference(args):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", args.api_key))
    model = args.model_name
    
    with open(args.test_file, 'r') as file:
        data_list = json.load(file)
    
    reference_claims = {item['Publication number']: item['Claim'] for item in data_list if item['Source'] == 'Gold'}

    for i, data in enumerate(data_list):

        if (data['Source'] != 'Gold') and ("G-eval" not in data) and (model not in data) and ("GPT-4" not in data['Source']):
            print(data["Index"])
            reference_claim = reference_claims[data['Publication number']]
            claim = data["Claim"]
            messages=[{"role": "system", "content": prompt}]          
            messages.append({"role": "user", "content": f"Referenced Claims: <<{reference_claim}>> Draft Claims: <<{claim}>> Evaluation Form (scores ONLY): - Completeness of Essential Features: X, - Conceptual Clarity: X, - Consistency in Terminology: X, - Technical Correctness of Feature Linkages: X. "})

            try:

                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0,
                )

                data[model] = response.choices[0].message.content
                print(data[model])
        
            except Exception as e:
                print(e)
                print(data["Publication number"])
                break

            with open(args.test_file, 'w') as file:
                json.dump(data_list, file)

if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description="Openai settings")

    parser.add_argument("--model_name", type=str, default="gpt-4-turbo")
    parser.add_argument("--openai_key", type=str, default=None)
    parser.add_argument("--test_file", type=str, default="results.json")

    args = parser.parse_args()
    
    openai_inference(args)

    with open(args.test_file, 'r') as file:
       data = json.load(file)
    
    for item in data:
        if args.model_name in item:
            scores = re.findall(r": (\d+)", item[args.model_name])
            scores = [int(score) for score in scores]
            item['G-eval'] = {"completeness": scores[0], "clarity": scores[1], "consistency": scores[2], "correctness": scores[3], "quality": round((scores[0]*4+scores[1]*2+scores[2]*2+scores[3]*3)/11, 2)}
            del item[args.model_name]
          
    with open(args.test_file, 'w') as file:
        json.dump(data, file)
        


    