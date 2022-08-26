import enum
import json

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
reader_prediction_filep = "/home/yilu/DPR/dpr/downloads/data/retriever/reader_prediction_nq_dev-negatives.json"
output_filep = "/home/yilu/DPR/dpr/downloads/data/retriever/new-nq-dev-negative.json"


def update_examples(ex, new_answer):
    answers = ex['answers']
    for pctx in ex['positive_ctxs']:
        for ans in answers:
            pctx['text'] = pctx['text'].replace(ans, new_answer)
            pctx['title'] = pctx['title'].replace(ans, new_answer)
    ex['answers'] = [new_answer]
    return ex


def question_answer_mapping(reader_predictions):
    """
        {
        "question": "who sings does he love me with reba",
        "gold_answers": [
            "Linda Davis"
        ],
        "predictions": [
            {
                "top_k": 100,
                "prediction": {
                    "text": "ronnie dunn",
                    "score": 11.782134532928467,
                    "relevance_score": 0.7603844404220581,
                    "passage_idx": 42,
                    "passage": "giving mcentire her twenty - ninth number one single, and brooks & dunn their twelfth. on the brooks & dunn : the last rodeo special on ( on cbs ) may 23, 2010, lady antebellum sang this song with reba mcentire and brooks & dunn coming in towards the end. the video starts off with reba at a bar. then, kix brooks comes to the bar. then, reba sings in an empty fancy theatre, along with ronnie dunn. a piano on the stage is seen in the background, and kix is seen playing the piano. before the end of the video, kix and ronnie are"
                }
            }
        ]
    },
    """
    question_new_answer_mapping = {}
    for prediction in reader_predictions:
        question = prediction['question']
        if "predictions" not in prediction:
            continue
        new_answer = prediction['predictions'][0]["prediction"]["text"]
        question_new_answer_mapping[question] = new_answer

    return question_new_answer_mapping

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

# new_ex = update_examples(ex, "new answer")
# print(new_ex)

def swap_answers_with_reader_pred(source_examples, reader_predictions):
    new_examples = []
    counter = 0
    true_answer_counter = 0
    question_new_answer_mapping = question_answer_mapping(reader_predictions)
    for source_ex in source_examples:
        question = source_ex['question']
        answers = source_ex['answers']
        if question not in question_new_answer_mapping:
            counter += 1
            continue
        new_answer = question_new_answer_mapping[question]
        if new_answer in answers:
            true_answer_counter +=1
            counter += 1
            continue

        new_ex = update_examples(source_ex, new_answer)
        new_examples.append(new_ex)

    print(f"counter: {counter}")
    print(f"true answer counter: {true_answer_counter}")
    print(f"total: {len(new_examples)}")
    return new_examples



def swap_answer_with_unk_token(source_examples):
    new_examples = []
    for source_ex in source_examples:
        new_ex = update_examples(source_ex, '[UNK]')
        new_examples.append(new_ex)

    return new_examples

def swap_answer_with_shifted_by_1(source_examples):
    def shift_char_1(text):
        new_text = ""
        text = text.lower()
        for t in text:
            if t == " " or t == "z":
                new_text += t
                continue

            r = ord(t)+1
            new_text += chr(r)
        return new_text

    new_examples = []
    for source_ex in source_examples:
        answer = source_ex['answers'][0]
        new_ex = update_examples(source_ex, new_answer=shift_char_1(answer))
        new_examples.append(new_ex)

    return new_examples



class SwapType(enum.Enum):
    WITH_READER_PRED = "with_reader_pred"
    UNK_TOKEN = "unk_token"
    SHIFT_1 = "shift_1"


swap_type = SwapType.UNK_TOKEN
print(f"Swap type: {swap_type.value}")
with open(source_filep) as fsin, open(reader_prediction_filep) as frin, open(output_filep,
                                                                             'w') as fout:
    source_examples = json.load(fsin)
    new_examples = []
    if swap_type == SwapType.WITH_READER_PRED:
        reader_predictions = json.load(frin)
        new_examples = swap_answers_with_reader_pred(source_examples, reader_predictions)
    elif swap_type == SwapType.UNK_TOKEN:
        new_examples = swap_answer_with_unk_token(source_examples)
    elif swap_type == SwapType.SHIFT_1:
        new_examples = swap_answer_with_shifted_by_1(source_examples)
    else:
        raise ValueError(f"not supported type {swap_type.value}")

    assert len(new_examples) > 0
    json.dump(new_examples, fout)

