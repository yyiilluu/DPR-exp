import json 
import pandas as pd

from tqdm import tqdm

if __name__ == "__main__":
    neg_answer_mapping = json.load(open("nq_test_1_1_negative_answer_mapping_with_hash_aug_20.json"))
    answer_to_hash = neg_answer_mapping["answer_to_hash"]
    hash_to_neg_answer = neg_answer_mapping["hash_to_neg_answer"]

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
        for answer, answer_hash in answer_to_hash.items():
            if answer in text:
                text = text.replace(answer, answer_hash)
        data["text"] = text # modify in place

    # replace hashes with modified answers
    print("replace hashes with modified answers")
    # for data in tqdm(wiki[:10]): # for testing
    for data in tqdm(wiki):
        text = data["text"]
        for answer_hash, neg_answer in hash_to_neg_answer.items():
            if answer_hash in text:
                text = text.replace(answer_hash, neg_answer)            
        data["text"] = text # modify in place

    # save to new tsv file
    print("saving")
    # new_df = pd.DataFrame(wiki[:10]) # for testing
    new_df = pd.DataFrame(wiki)
    new_df.to_csv("psgs_w100_neg_answers.tsv", sep="\t", index=False)