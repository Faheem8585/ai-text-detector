# eval

Small labelled corpus + a script that computes accuracy / precision /
recall / F1 / ROC AUC against the live detector.

```
samples/
├── human/   real writing (forum posts, blogs, emails, reviews)
└── ai/      unprompted ChatGPT-style output
```

Run:

```bash
python -m eval.validate
```

Latest run (12 samples):

```
Accuracy   : 100.0%
Precision  : 100.0%
Recall     : 100.0%
F1 score   : 100.0%
ROC AUC    : 100.0%
TP=6  TN=6  FP=0  FN=0
```

This is a clean, easy benchmark. Real adversarial samples
(paraphrased AI output, translated text, mixed passages) will push the
score down — that corpus is on the todo list.
