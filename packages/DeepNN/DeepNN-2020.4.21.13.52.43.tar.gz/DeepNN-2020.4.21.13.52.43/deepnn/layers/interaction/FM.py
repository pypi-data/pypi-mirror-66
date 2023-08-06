#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepNN.
# @File         : FM
# @Time         : 2020/4/21 1:40 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import tensorflow as tf

K = tf.keras.backend


class FM(tf.keras.layers.Layer):
    """Factorization Machine models pairwise (order-2) feature interactions
     without linear term and bias.

      Input shape
        - 3D tensor with shape: ``(batch_size,field_size,embedding_size)``.

      Output shape
        - 2D tensor with shape: ``(batch_size, 1)``.

      References
        - [Factorization Machines](https://www.csie.ntu.edu.tw/~b97053/paper/Rendle2010FM.pdf)
    """

    def __init__(self, **kwargs):

        super(FM, self).__init__(**kwargs)

    def build(self, input_shape):
        if len(input_shape) != 3:
            raise ValueError(f"Unexpected inputs dimensions {len(input_shape)}, expect to be 3 dimensions")

        super(FM, self).build(input_shape)

    def call(self, inputs, **kwargs):

        if K.ndim(inputs) != 3:
            raise ValueError(f"Unexpected inputs dimensions {K.ndim(inputs)}, expect to be 3 dimensions")

        fm_input = inputs

        square_of_sum = tf.square(tf.reduce_sum(fm_input, axis=1, keep_dims=True))
        sum_of_square = tf.reduce_sum(fm_input * fm_input, axis=1, keep_dims=True)
        cross_term = square_of_sum - sum_of_square
        cross_term = 0.5 * tf.reduce_sum(cross_term, axis=2, keep_dims=False)

        return cross_term

    def compute_output_shape(self, input_shape):
        return (None, 1)
