#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""train_rnn.py
    Train a character-based RNN to generate text.
    Edit the default_config.yaml to get started.
    Sources:
        * https://www.tensorflow.org/tutorials/text/text_generation
        * http://karpathy.github.io/2015/05/21/rnn-effectiveness/
"""
import logging
from pathlib import Path
import shutil

import tensorflow as tf
import sentencepiece as spm
from smart_open import open

from gretel_synthetics.model import build_sequential_model, compute_epsilon
from gretel_synthetics.config import BaseConfig


logging.basicConfig(
    format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s',
    level=logging.INFO)


def train_rnn(store: BaseConfig):
    text = annotate_training_data(store)
    sp = train_tokenizer(store)
    logging.info("Creating and shuffling Tensorflow Dataset")
    dataset = create_dataset(store, text, sp)
    logging.info("Initializing generative model")
    model = build_sequential_model(
        vocab_size=len(sp),
        batch_size=store.batch_size,
        store=store
        )

    # Save checkpoints during training
    checkpoint_prefix = Path(store.checkpoint_dir) / "ckpt_{epoch}"
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_prefix.as_posix(),
        save_weights_only=True
    )

    all_cbs = [checkpoint_callback]

    logging.info("Training model")
    model.fit(dataset, epochs=store.epochs, callbacks=all_cbs)
    logging.info(
        f"Wrote latest checkpoint to disk: {tf.train.latest_checkpoint(store.checkpoint_dir)}")

    if store.dp:
        logging.info(compute_epsilon(len(text), store))
    else:
        logging.info('Trained with non-private optimizer')


def annotate_training_data(store: BaseConfig):
    # required for sentencepiece to tokenize newline characters
    logging.info(f"Annotating training data from {store.input_data}")
    training_text = []
    with open(store.input_data, 'r', encoding='utf-8', errors='replace') as infile:
        for line in infile:
            if store.max_lines and len(training_text) >= store.max_lines:
                break
            line = line.strip().replace(",", "<c>")
            training_text.append(line)

    logging.info(f"Annotating training data to {store.training_data}")
    labeled_text = ''
    with open(store.training_data, 'w') as f:
        for sample in training_text:
            chunk = f"{sample}<n>\n"
            f.write(chunk)
            labeled_text += chunk
    logging.info(f"Annotated text length: {len(labeled_text)} characters")
    return labeled_text


def move_tokenizer_model(store: BaseConfig):
    for model in ['model', 'vocab']:
        src = Path.cwd() / f'{store.tokenizer_prefix}.{model}'
        dst = Path(store.checkpoint_dir) / f'{store.tokenizer_prefix}.{model}'
        shutil.move(src.as_posix(), dst.as_posix())


def train_tokenizer(store: BaseConfig) -> spm.SentencePieceProcessor:
    logging.info("Training SentencePiece tokenizer")
    spm.SentencePieceTrainer.Train(
        f'--input={store.training_data} '
        f'--model_prefix={store.tokenizer_prefix} '
        f'--user_defined_symbols=<n>,<c> '
        f'--vocab_size={store.vocab_size} '
        f'--hard_vocab_limit=false '
        f'--character_coverage={store.character_coverage}')
    move_tokenizer_model(store)
    logging.info("Complete")

    sp = spm.SentencePieceProcessor()
    logging.info(f"Loading tokenizer from: {store.tokenizer_model}")
    sp.Load(store.tokenizer_model)

    # print sample output
    with open(store.training_data) as f:
        sample = f.readline().strip()
    logging.info(f"Tokenizer model vocabulary size: {len(sp)} tokens")
    logging.info(
        'Mapping first line of training data\n\n{}\n ---- sample tokens mapped to pieces ---- > \n{}\n'.format(
            repr(sample), ", ".join(sp.SampleEncodeAsPieces(sample, -1, 0.1))))
    logging.info(
        'Mapping first line of training data\n\n{}\n ---- sample tokens mapped to int ---- > \n{}\n'.format(
            repr(sample), ", ".join([str(idx) for idx in sp.EncodeAsIds(sample)])))
    logging.info(f"Saving SentencePiece model to {store.tokenizer_prefix}.model and {store.tokenizer_prefix}.vocab")
    return sp


def create_dataset(store: BaseConfig, text: str, sp: spm.SentencePieceProcessor) -> tf.data.Dataset:
    """
    Before training, we need to map strings to a numerical representation.
    Create two lookup tables: one mapping characters to numbers,
    and another for numbers to characters.
    """
    # Create training dataset
    char_dataset = tf.data.Dataset.from_tensor_slices(sp.EncodeAsIds(text))
    sequences = char_dataset.batch(store.seq_length + 1, drop_remainder=True)
    dataset = sequences.map(split_input_target)
    dataset = dataset.shuffle(
        store.buffer_size).batch(
            store.batch_size, drop_remainder=True)
    return dataset


def split_input_target(chunk: str) -> (str, str):
    """
    For each sequence, duplicate and shift it to form the input and target text
    by using the map method to apply a simple function to each batch:

    Examples:
        split_input_target("So hot right now")
        Returns: ('So hot right now', 'o hot right now.')
    """
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text
