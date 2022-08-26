# Download data
## orignal nq dev
```shell
python data/download_data.py --resource data.retriever.nq-dev
```

## other ODQA dataset
```shell
data.retriever.qas.nq-test
```

efficient QA [dataset](https://github.com/google-research-datasets/natural-questions/blob/master/nq_open/NQ-open.efficientqa.test.1.1.jsonl)

## checkpoint
```shell
python data/download_data.py --resource checkpoint.retriever.single-adv-hn.nq.bert-base-encoder
python data/download_data.py --resource checkpoint.retriever.single.nq.bert-base-encoder
python data/download_data.py --resource checkpoint.reader.nq-single.hf-bert-base

python data/download_data.py --resource data.retriever_results.nq.single.wikipedia_passages
```

# Prepare data

## Create reader input from NQ-dev

```
python process_ctx_to_reader_data.py
```
this will save a reader file specified in the script

## Run reader inference

```
python train_extractive_reader.py \
  prediction_results_file=./reader_prediction_nq_dev.json \
  eval_top_docs=[100] \
  dev_files=/home/yilu/DPR/dpr/downloads/data/retriever/reader-input-nq-dev.json \
  model_file=/home/yilu/DPR/dpr/downloads/checkpoint/reader/nq-single/hf-bert-base.cp \
  train.dev_batch_size=10 \
  passages_per_question_predict=100 \
  encoder.sequence_length=350
```


```
python train_extractive_reader.py \
  prediction_results_file=./reader_prediction_nq_dev-hard-negatives.json \
  eval_top_docs=[100] \
  dev_files=/home/yilu/DPR/dpr/downloads/data/retriever/reader-input-nq-dev-hard-negative.json \
  model_file=/home/yilu/DPR/dpr/downloads/checkpoint/reader/nq-single/hf-bert-base.cp \
  train.dev_batch_size=10 \
  passages_per_question_predict=100 \
  encoder.sequence_length=350
```

```
python train_extractive_reader.py \
  prediction_results_file=./reader_prediction_nq_dev-negatives.json \
  eval_top_docs=[100] \
  dev_files=/home/yilu/DPR/dpr/downloads/data/retriever/reader-input-nq-dev-negative.json \
  model_file=/home/yilu/DPR/dpr/downloads/checkpoint/reader/nq-single/hf-bert-base.cp \
  train.dev_batch_size=10 \
  passages_per_question_predict=100 \
  encoder.sequence_length=350
```

## Process new nq dataset
update path of source nq, reader prediction (reader_prediction_nq_dev.json), and output file
```
python swap_predictions.py
```

## Evaluate retriever on dev set
update new_nq_dev dataset from below
`DPR/conf/datasets/encoder_train_default.yaml`

two model path
1. /home/yilu/DPR/dpr/downloads/checkpoint/retriever/single-adv-hn/nq/bert-base-encoder.cp
2. /home/yilu/DPR/dpr/downloads/checkpoint/retriever/single/nq/bert-base-encoder.cp

single adv bert model
```
python train_dense_encoder.py \
  dev_datasets=[new_nq_dev] \
  model_file=/home/yilu/DPR/dpr/downloads/checkpoint/retriever/single-adv-hn/nq/bert-base-encoder.cp \
  train=biencoder_local \
  output_dir=new-dev-output
```

single bert model
```
python train_dense_encoder.py \
  dev_datasets=[new_nq_dev] \
  model_file=/home/yilu/DPR/dpr/downloads/checkpoint/retriever/single/nq/bert-base-encoder.cp \
  train=biencoder_local \
  output_dir=new-dev-output
```

## Evaluate retriever on entire wikipedia
update passage in `conf/ctx_sources/default_sources.yaml`, which just contains dpr_wiki now.  
test dataset in `conf/datasets/retriever_default.yaml`

Generating representation vectors for the static documents dataset is a highly parallelizable process which can take up to a few days if computed on a single GPU. You might want to use multiple available GPU servers by running the script on each of them independently and specifying their own shards.

```
python generate_dense_embeddings.py \
	model_file=/home/yilu/DPR/dpr/downloads/checkpoint/retriever/single/nq/bert-base-encoder.cp \
	ctx_src=dpr_wiki \
	num_shards=10 \
	out_file=/home/yilu/DPR/dpr/downloads/embeddings/dpr_wiki/shard
```

```bash
python dense_retriever.py \
	model_file=/home/yilu/DPR/dpr/downloads/checkpoint/retriever/single/nq/bert-base-encoder.cp \
	qa_dataset=nq_test \
	ctx_datatsets=[dpr_wiki] \
	encoded_ctx_files=[\"/home/yilu/DPR/dpr/downloads/embeddings/dpr_wiki/shard_*\"] \
	out_file=/home/yilu/DPR/dpr/outputs/baseline_retrieval/
```

python dense_retriever.py \
model_file=/home/yilu/DPR/dpr/downloads/checkpoint/retriever/single/nq/bert-base-encoder.cp \
qa_dataset=nq_test \
ctx_datatsets=[dpr_wiki] \
encoded_ctx_files=["{glob expression for generated embedding files}"] \
out_file={path to the output file}

## Evaluate retriever end to end
