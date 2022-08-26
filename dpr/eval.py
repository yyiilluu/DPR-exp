import json
from statistics import mean

"""
{
  "question": "who got the first nobel prize in physics",
  "answers": [
    "Wilhelm Conrad Röntgen"
  ],
  "ctxs": [
    {
      "id": "wiki:284453",
      "title": "Nobel Prize",
      "text": "A group including 42 Swedish writers, artists, and literary critics protested against this decision, having expected Leo Tolstoy to be awarded. Some, including Burton Feldman, have criticised this prize because they consider Prudhomme a mediocre poet. Feldman's explanation is that most of the Academy members preferred Victorian literature and thus selected a Victorian poet. The first Physiology or Medicine Prize went to the German physiologist and microbiologist Emil von Behring. During the 1890s, von Behring developed an antitoxin to treat diphtheria, which until then was causing thousands of deaths each year. The first Nobel Peace Prize went to the Swiss",
      "score": "81.7439",
      "has_answer": false
    },
    {
      "id": "wiki:628737",
      "title": "Nobel Prize in Physiology or Medicine",
      "text": "than three recipients. In the last half century there has been an increasing tendency for scientists to work as teams, resulting in controversial exclusions. Alfred Nobel was born on 21 October 1833 in Stockholm, Sweden, into a family of engineers. He was a chemist, engineer and inventor who amassed a fortune during his lifetime, most of it from his 355 inventions of which dynamite is the most famous. He was interested in experimental physiology and set up his own labs in France and Italy to conduct experiments in blood transfusions. Keeping abreast of scientific findings, he was generous in his",
      "score": "81.566154",
      "has_answer": false
    },
"""

def compute_recall_at_k(predictions, k):
    correct_match = 0
    total_predictions = len(predictions)
    for pred in predictions:
        ctxs = pred['ctxs']
        for ctx in ctxs[:k]:
            if ctx['has_answer']:
                correct_match += 1
                break

    return correct_match / total_predictions


def compute_mrr(predictions):
    rr = []
    for pred in predictions:
        ctxs = pred['ctxs']
        # ctxs = sorted(ctxs, key=lambda x: x["score"], reverse=True)
        found_answer = False
        for rank, ctx in enumerate(ctxs):
            if ctx['has_answer']:
                rr.append(1/(1+rank))
                found_answer = True
                break
        if not found_answer:
            rr.append(0)

    assert len(rr) == len(predictions)
    return mean(rr)

retrieval_output_fp = "/home/yilu/DPR/dpr/outputs/baseline_retrieval/test_run.jsonl"

results = []
with open(retrieval_output_fp) as f:
    for line in f:
        results.append(json.loads(line))

print(f"Recall at 20: {compute_recall_at_k(results, 20)}")
print(f"Recall at 100: {compute_recall_at_k(results, 100)}")
print(f"MRR: {compute_mrr(results)}")