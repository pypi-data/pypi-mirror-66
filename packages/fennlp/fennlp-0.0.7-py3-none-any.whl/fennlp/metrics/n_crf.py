#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:Kaiyin Zhou
"""
import tensorflow as tf

class CrfLogLikelihood(tf.keras.layers.Layer):
    def __init__(self, name='crf', **kwargs):
        super(CrfLogLikelihood, self).__init__(name=name, **kwargs)

    def build(self, input_shape):
        num_tags = input_shape[2]
        initializer = tf.keras.initializers.GlorotUniform()
        self.transition_params = self.add_weight(
            shape=[num_tags, num_tags],
            initializer=initializer,
            name="transitions")
    def call(self, inputs, tag_indices, sequence_lengths):
        # cast type to handle different types
        tag_indices = tf.cast(tag_indices, dtype=tf.int32)
        sequence_lengths = tf.cast(sequence_lengths, dtype=tf.int32)
        sequence_scores = crf_sequence_score(inputs, tag_indices, sequence_lengths,
                                             self.transition_params)
        # log_sum(exp(一条路劲得分))，对所有路径得分的exp求sum后取log
        log_norm = crf_log_norm(inputs, sequence_lengths, self.transition_params)
        # Normalize the scores to get the log-likelihood per example.
        log_likelihood = sequence_scores - log_norm
        return log_likelihood, self.transition_params


def crf_sequence_score(inputs, tag_indices, sequence_lengths,
                       transition_params):
    tag_indices = tf.cast(tag_indices, dtype=tf.int32)
    sequence_lengths = tf.cast(sequence_lengths, dtype=tf.int32)
    unary_scores = crf_unary_score(tag_indices, sequence_lengths, inputs)
    # trans score
    binary_scores = crf_binary_score(tag_indices, sequence_lengths,
                                     transition_params)
    sequence_scores = unary_scores + binary_scores
    return sequence_scores

def crf_unary_score(tag_indices, sequence_lengths, inputs):
    tag_indices = tf.cast(tag_indices, dtype=tf.int32)
    sequence_lengths = tf.cast(sequence_lengths, dtype=tf.int32)

    batch_size = tf.shape(inputs)[0]
    max_seq_len = tf.shape(inputs)[1]
    num_tags = tf.shape(inputs)[2]

    flattened_inputs = tf.reshape(inputs, [-1])

    offsets = tf.expand_dims(tf.range(batch_size) * max_seq_len * num_tags, 1)  # 计算每一个batch起始位置
    offsets += tf.expand_dims(tf.range(max_seq_len) * num_tags, 0)  # 计算每一个step的预测结果的起始位置
    # Use int32 or int64 based on tag_indices' dtype.
    if tag_indices.dtype == tf.int64:
        offsets = tf.cast(offsets, tf.int64)
    flattened_tag_indices = tf.reshape(offsets + tag_indices, [-1])  # 这就获得每一个标签所在的index

    unary_scores = tf.reshape(
        tf.gather(flattened_inputs, flattened_tag_indices),
        [batch_size, max_seq_len])  # 将每一个标签所在的index取出来，获得模型预测得分

    masks = tf.sequence_mask(
        sequence_lengths, maxlen=tf.shape(tag_indices)[1], dtype=tf.float32)

    unary_scores = tf.reduce_sum(unary_scores * masks, 1)
    return unary_scores  # 获得模型预测得分

def crf_binary_score(tag_indices, sequence_lengths, transition_params):
    tag_indices = tf.cast(tag_indices, dtype=tf.int32)
    sequence_lengths = tf.cast(sequence_lengths, dtype=tf.int32)

    num_tags = tf.shape(transition_params)[0]
    num_transitions = tf.shape(tag_indices)[1] - 1

    # Truncate by one on each side of the sequence to get the start and end
    # indices of each transition.
    start_tag_indices = tf.slice(tag_indices, [0, 0], [-1, num_transitions])
    end_tag_indices = tf.slice(tag_indices, [0, 1], [-1, num_transitions])

    # Encode the indices in a flattened representation.
    # 太巧妙了
    flattened_transition_indices = start_tag_indices * \
                                   num_tags + end_tag_indices
    flattened_transition_params = tf.reshape(transition_params, [-1])

    # Get the binary scores based on the flattened representation.
    binary_scores = tf.gather(flattened_transition_params,
                              flattened_transition_indices)
    masks = tf.sequence_mask(
        sequence_lengths, maxlen=tf.shape(tag_indices)[1], dtype=tf.float32)
    truncated_masks = tf.slice(masks, [0, 1], [-1, -1])
    binary_scores = tf.reduce_sum(binary_scores * truncated_masks, 1)
    return binary_scores

def crf_log_norm(inputs, sequence_lengths, transition_params):

    sequence_lengths = tf.cast(sequence_lengths, dtype=tf.int32)
    # Split up the first and rest of the inputs in preparation for the forward
    # algorithm.
    first_input = tf.slice(inputs, [0, 0, 0], [-1, 1, -1])
    first_input = tf.squeeze(first_input, [1])
    """Forward computation of alpha values."""
    rest_of_input = tf.slice(inputs, [0, 1, 0], [-1, -1, -1])
    # Compute the alpha values in the forward algorithm in order to get the
    # partition function.

    alphas = crf_forward(rest_of_input, first_input, transition_params,
                         sequence_lengths)
    log_norm = tf.reduce_logsumexp(alphas, [1])

    return log_norm

def crf_forward(inputs, state, transition_params, sequence_lengths):
    sequence_lengths = tf.cast(sequence_lengths, dtype=tf.int32)

    last_index = tf.maximum(
        tf.constant(0, dtype=sequence_lengths.dtype), sequence_lengths - 1)
    inputs = tf.transpose(inputs, [1, 0, 2])
    transition_params = tf.expand_dims(transition_params, 0)

    def _scan_fn(_state, _inputs):#递归函数
        _state = tf.expand_dims(_state, 2)
        transition_scores = _state + transition_params# 初始状态往任意点转移的概率
        new_alphas = _inputs + tf.reduce_logsumexp(transition_scores, [1])
        return new_alphas

    all_alphas = tf.transpose(tf.scan(_scan_fn, inputs, state), [1, 0, 2])
    # add first state for sequences of length 1
    all_alphas = tf.concat([tf.expand_dims(state, 1), all_alphas], 1)

    idxs = tf.stack([tf.range(tf.shape(last_index)[0]), last_index], axis=1)
    return tf.gather_nd(all_alphas, idxs)
