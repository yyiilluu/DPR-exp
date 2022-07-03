"""
from
[
  {
	"question": "....",
	"answers": ["...", "...", "..."],
	"positive_ctxs": [{
		"title": "...",
		"text": "...."
	}],
	"negative_ctxs": ["..."],
	"hard_negative_ctxs": ["..."]
  },
  ...
]

to

[
    {
        "question": "...",
        "answers": ["...", "...", ... ],
        "ctxs": [
            {
                "id": "...", # passage id from database tsv file
                "title": "",
                "text": "....",
                "score": "...",  # retriever score
                "has_answer": true|false
     },
]
"""

import json

source_filep = "/home/yilu/DPR/dpr/downloads/data/retriever/nq-dev.json"
output_filep = "/home/yilu/DPR/dpr/downloads/data/retriever/reader-input-nq-dev.json"

output_examples = []
with open(source_filep) as fin:
    ctx_examples = json.load(fin)

    for ex in ctx_examples:
        output_data = {
            "question": ex['question'],
            "answers": ex['answers'],
            "ctxs": [
                {
                    "id": None,
                    "title": ctx['title'],
                    "text": ctx['text'],
                    "score": 0,
                    "has_answer": False
                } for ctx in ex['hard_negative_ctxs']
            ]
        }

        if len(output_data['ctxs']) == 0:
            output_data['ctxs'] = [
                {
                    "id": None,
                    "title": ctx['title'],
                    "text": ctx['text'],
                    "score": 0,
                    "has_answer": False
                } for ctx in ex['negative_ctxs']
            ]

        if len(output_data['ctxs']) == 0:
            print(f"warning for question: {ex['question']}")
            continue

        output_examples.append(output_data)

    with open(output_filep, 'w') as fout:
        json.dump(output_examples, fout)
