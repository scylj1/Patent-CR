# Patent-CR
This repository is the code for inference and evaluation for patent claim revision.

## Dataset

Data could be retrieved from the European Patent Office (EPO) using the script in the ```data``` folder. 

## Inference

Inference of models on Huggingface:
```bash
python pipeline_inference.py
```

Inference of GPT series from OpenAI:
```bash
python openai_inference.py
```

## Evaluation

Traditional evaluations, such as BLEU and ROUGE.
```bash
python eval.py
```

GPT-based evaluations.
```bash
python geval.py
```

## Citation

If you find our work useful for your research, please feel free to cite our paper.
```
@article{jiang2024patent,
  title={Patent-CR: A Dataset for Patent Claim Revision},
  author={Jiang, Lekang and Scherz, Pascal A and Goetz, Stephan},
  journal={arXiv preprint arXiv:2412.02549},
  year={2024}
}
```