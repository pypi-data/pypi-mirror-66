#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   handle.py    
@Contact :   1553990434@qq.com
@License :   (C)Copyright 2019-Present, XiaoLinpeng

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-04-10 18:57   肖林朋      1.0         功能描述
"""

#  Copyright (c) XiaoLinpeng 2020.

import sys
from contextlib import contextmanager
from enum import Enum
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
from typing import Any, Union

from datafushion.args import ArgStruct
from datafushion.handle import HandleDataSet, HandleInputDataStruct
from pyspark.sql import SparkSession
from pyspark2pmml import PMMLBuilder


class HandleDataFrameSet(HandleDataSet):
    """
    封装的处理数据集
    """


    def __init__(self, input_data_struct_list, output_path, param_map, data_result, output_type, spark, mapping_flags):
        super().__init__(input_data_struct_list, output_path, param_map, data_result)
        self.output_type = output_type
        self.spark = spark
        self.mapping_flags = mapping_flags


class TrainFiledEnum(Enum):
    """
    训练数据标准输入名称枚举，仅为参考
    """
    FEATURE = "feature"
    LABEL = "label"
    BUNDLE = "bundle"


class TrainModelResult(object):
    """
    训练模型结果
    """


    def __init__(self, train_data, pipeline_model):
        self.train_data = train_data
        self.pipeline_model = pipeline_model


@contextmanager
def operation(app_name, master="yarn-cluster", reverse_mapping=False, mapping_data=True):
    """
     数据处理封装
    :param app_name: 应用名称
    :param master: spark的master运行方式
    :param reverse_mapping:  是否进行映射翻转
    :param mapping_data:  是否进行映射
    :return: 文件处理解构
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .master(master) \
        .getOrCreate()  # type: Union[SparkSession, Any]

    # 文件抽取方法
    file_extract_dict = dict(
            json=lambda file_path, data_columns: spark.read.option('inferSchema', True).json(path=file_path,
                                                                                             multiLine=True).select(
                    data_columns),
            csv=lambda file_path, data_columns: spark.read.option('inferSchema', True).csv(path=file_path,
                                                                                           multiLine=True,
                                                                                           header=True).select(
                    data_columns),
            parquet=lambda file_path, data_columns: spark.read.option('inferSchema', True).parquet(file_path).select(
                    data_columns),
            general=lambda file_path, data_columns: spark.read.option('inferSchema', True).text(paths=file_path,
                                                                                                wholetext=True).withColumnRenamed(
                    "value", data_columns[0]))

    # 文件保存方法
    file_save_dict = dict(
            json=lambda data_result, output_path: data_result.write.json(path=output_path, mode="overwrite"),
            csv=lambda data_result, output_path: data_result.write.csv(path=output_path, mode="overwrite",
                                                                       header=True, multiLine=True),
            parquet=lambda data_result, output_path: data_result.write.parquet(path=output_path, mode="overwrite"),
            general=lambda data_result, output_path: data_result.select("value").write.mode('overwrite').text(
                    output_path),
            model=lambda data_result, output_path: PMMLBuilder(spark.sparkContext, data_result.train_data,
                                                               data_result.pipeline_model).buildFile(output_path))


    def destruction() -> HandleDataFrameSet:

        """
        处理输入,输入可以有多个数据集
        :return: 输出处理结构体,输入数据集合,输出路径,参数Map
        """
        args = None
        if len(sys.argv) == 3:
            args = [sys.argv[1], sys.argv[2], None]
        elif len(sys.argv) == 4:
            args = [sys.argv[1], sys.argv[2], sys.argv[3]]

        arg_struct = ArgStruct.parse(args)
        input_structs = arg_struct.fetch_input_structs()
        output_path = arg_struct.fetch_output_path()
        param_map = arg_struct.fetch_param_map()

        mapping_flags = {}
        input_data_struct_list = []
        for input_struct in input_structs:
            file_type = input_struct.file_format
            file_path = input_struct.file_path
            flag_mapping = input_struct.flag_mapping

            if reverse_mapping:
                file_input_mapping = input_struct.mapping_2_json(True)
                data_columns = list(file_input_mapping.values())
                mapping_columns = list(file_input_mapping.keys())
            else:
                file_input_mapping = input_struct.mapping_2_multi_value(True)
                if mapping_data:
                    data_columns = list(list(map(lambda x: x[0], file_input_mapping.values())))
                else:
                    data_columns = "*"

                mapping_columns = list(file_input_mapping.keys())

            mapping_flags[flag_mapping] = file_input_mapping
            data_frame = file_extract_dict[file_type](file_path, data_columns)

            if mapping_data:
                data_list = data_frame.toDF(*mapping_columns)
            else:
                data_list = data_frame

            input_data_struct_list.append(HandleInputDataStruct(file_type=file_type, file_path=file_path,
                                                                file_input_mapping=file_input_mapping,
                                                                data_list=data_list))

        return HandleDataFrameSet(input_data_struct_list=input_data_struct_list, output_path=output_path,
                                  param_map=param_map, data_result=None, output_type=None, spark=spark,
                                  mapping_flags=mapping_flags)


    def save_data(data_result, output_path, output_type):
        """
        存储数据
        :param data_result: 已处理好的数据
        :param output_path:  输出路径
        :param output_type: 输出类型
        :return:
        """
        if data_result is None:
            return
        else:
            file_save_dict[output_type](data_result, output_path)


    destruction = destruction()
    yield destruction

    save_data(destruction.data_result, destruction.output_path, destruction.output_type)
