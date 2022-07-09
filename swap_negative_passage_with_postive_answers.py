import json
import random

"""
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
..

            {
                "title": "Dablot Prejjesne",
                "text": "orthogonal grid). The Sami Prince is placed on the sixth rank, on the intersection of diagonals to that player's farthest right. The Sami King is placed on the seventh rank, at the right edge of the board (please refer to the image above and the first external link below for a
visual description of the initial setup for both Sami tribe and landowner party). Similarly, the Landowner's Son and Landowner are placed on that player's farthest right on the sixth and seventh rank, respectively. 3. All pieces move alike. A piece moves one space along one of the gridlines to",      
                "score": 0,
                "title_score": 0,
                "passage_id": "12336307"
            },
"""
source_filep = "/home/yilu/DPR/dpr/downloads/data/retriever/nq-dev.json"
output_filep = "/home/yilu/DPR/dpr/downloads/data/retriever/new-nq-dev-positives.json"

# ex = {
#          "question": "....",
#          "answers": ["asdf", "...", "..."],
#          "positive_ctxs": [{
#              "title": "asdf is the new thing",
#              "text": "i like asdf is the new thing"
#          }],
#          "negative_ctxs": ["..."],
#          "hard_negative_ctxs": ["..."]
#      }

def update_examples(ex, new_answer):
    for nctx in ex['negative_ctxs']:
        text_tokens = nctx['text'].split()
        text_tokens.insert(random.randint(0, len(text_tokens)), new_answer)

        nctx['text'] = " ".join(text_tokens)

    for nctx in ex['hard_negative_ctxs']:
        text_tokens = nctx['text'].split()
        text_tokens.insert(random.randint(0, len(text_tokens)), new_answer)

        nctx['text'] = " ".join(text_tokens)
    return ex

# new_ex = update_examples(ex, "new answer")
# print(new_ex)
counter = 0
true_answer_counter = 0
all_examples = []
with open(source_filep) as fsin, open(output_filep,'w') as fout:
    source_examples = json.load(fsin)
    for ex in source_examples:
        answer = ex['answers'][0]
        new_ex = update_examples(ex, answer)
        all_examples.append(new_ex)

    json.dump(all_examples, fout)


