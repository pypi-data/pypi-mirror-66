#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepTricks.
# @File         : DataLoader
# @Time         : 2019-10-21 13:01
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import tensorflow as tf
import pandas as pd


class Dataset(object):
    """
    https://tensorflow.google.cn/guide/data?hl=zh_cn

    """

    def __init__(self, batchsize=128, shuffle=True, buffer_size=None, shuffle_seed=None):
        self.batchsize = batchsize
        self.shuffle = shuffle
        self.shuffle_seed = shuffle_seed
        self.buffer_size = buffer_size

    def from_np_array(self, array):
        """

        :param array: [[]]
        """
        ds = tf.data.Dataset.from_tensor_slices(array).batch(self.batchsize)
        return self._shuffle(array, ds)

    def from_pd_dataframe(self, df: pd.DataFrame, label="label"):
        """
        import tensorflow as tf
        dataset = tf.data.Dataset.from_tensor_slices(({"a": [1, 2], "b": [3, 4]}, [0, 1]))
        print(list(dataset.as_numpy_iterator()))

        :param df:
        :param label:
        :return:
        """
        if label and label in df.columns:
            df = df.drop(labels=[label], axis=1)
            labels = df[label]
            tensors = (df.to_dict('list'), labels)  # df.to_dict('series')
        else:
            tensors = df.to_dict('list')

        ds = tf.data.Dataset.from_tensor_slices(tensors).batch(self.batchsize)

        # features_dataset = tf.data.Dataset.from_tensor_slices(features)
        # labels_dataset = tf.data.Dataset.from_tensor_slices(labels)
        # tf.data.Dataset.zip((features_dataset, labels_dataset))
        return self._shuffle(df, ds)

    def from_generator_txt(self):
        # TODO: 增加对文件的操作（txt/tfrecord）
        # tf.data.Dataset.from_generator()
        pass

    def show_data(self, batch=True):
        _ = self.dataset.as_numpy_iterator()
        return next(_) if batch else list(_)

    def _shuffle(self, data, dataset: tf.data.Dataset):
        buffer_size = self.buffer_size if self.buffer_size else len(data)
        if self.shuffle:
            dataset = dataset.shuffle(buffer_size, self.shuffle_seed)
        self.dataset = dataset
        return dataset
