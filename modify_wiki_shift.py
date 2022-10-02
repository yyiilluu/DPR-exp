import json 
import pandas as pd

from tqdm import tqdm

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

if __name__ == "__main__":
    neg_answer_mapping = json.load(open("nq_test_1_1_negative_answer_mapping_with_hash_aug_20.json"))
    answer_to_hash = neg_answer_mapping["answer_to_hash"]
    # hash_to_neg_answer = neg_answer_mapping["hash_to_neg_answer"]

    print("reading df")
    df = pd.read_csv("downloads/data/wikipedia_split/psgs_w100.tsv", sep="\t")

    wiki = df.to_dict("records")
    # free up soe memory
    del df

    # replace answers with hashes
    print("replace answers with hashes")
    # for data in tqdm(wiki[:10]):  # for tests
    for data in tqdm(wiki):
        text = data["text"]
        for answer in answer_to_hash.keys():
            if answer in text:
                shifted_answer = shift_char_1(answer)
                text = text.replace(answer, shifted_answer)
        data["text"] = text # modify in place

    # save to new tsv file
    print("saving")
    # new_df = pd.DataFrame(wiki[:10]) # for testing
    new_df = pd.DataFrame(wiki)
    new_df.to_csv("psgs_w100_shifted_answers.tsv", sep="\t", index=False)