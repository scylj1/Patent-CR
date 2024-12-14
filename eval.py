
from evaluate import load as load_metric
import json

def evaluate_text(sources, prediction_texts, reference_texts):

    metrics = {}

    # sari
    sari = load_metric("sari")
    references_for_sari = [[text] for text in reference_texts]
    sari_score = sari.compute(sources=sources, predictions=prediction_texts, references=references_for_sari)
    metrics["sari"] = sari_score["sari"] 
    print(metrics["sari"])
    
    # BLEU
    bleu = load_metric("bleu")
    bleu_result = bleu.compute(predictions=prediction_texts, references=references_for_sari)
    metrics["bleu"] = bleu_result["bleu"]
    print(metrics["bleu"])
    
    # ROUGE
    rouge = load_metric("rouge")
    rouge_result = rouge.compute(predictions=prediction_texts, references=reference_texts)
    metrics["rougeL"] = rouge_result["rougeL"]
    print(metrics["rougeL"])
    rouge1  = rouge_result["rouge1"]
    print(f"rouge1: {rouge1 }")
    
    # BERTScore
    bertscore = load_metric("bertscore")
    results = bertscore.compute(predictions=prediction_texts, references=reference_texts, lang="en")
    metrics["bertscore"] = sum(results["f1"]) / len(results["f1"]) 

    return metrics

if __name__=='__main__':

    with open('results.json', 'r') as file:
       data_list = json.load(file)
       
    test_key = "saul-7b"   

    sources, reference_text = [], []
    predicts = []
    
    for d in data_list:
        predicts.append(d[test_key])
        sources.append(d["Claim before"])            
        reference_text.append(d["Claim after"])

    scores = evaluate_text(sources, predicts, reference_text)
    print(scores)
