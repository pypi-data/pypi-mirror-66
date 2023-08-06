# DataFushion_Plugins_SparkPy说明

## 1.简介

针对Spark的Python版本算法(pyspark)在DataFushion平台使用所给出的插件,主要用于规范化算法的输入输出

## 2.通常算法使用

- [x] Step1:引入datafushion_spark包中的operation模块
- [x] Step2:使用资源管理器进行数据拆解处理,并在其中实现自己需要实现的业务算法逻辑

```python
from datafushion_spark import operation, HandleDataFrameSet, HandleInputDataStruct, DataFrame, SparkSession, \
    FileExtractFormatEnum


if __name__ == '__main__':
    with operation(app_name="AvgWindPowerByStatus", master="local") as destruction:  # type:HandleDataFrameSet
        input_data_struct_list = destruction.input_data_struct_list
        mapping_flags = destruction.mapping_flags
        param_map = destruction.param_map
        spark = destruction.spark  # type:SparkSession

        data_result = None  # type DataFrame

        # 算法逻辑部分
        for index, input_data_struct in enumerate(input_data_struct_list):  # type: HandleInputDataStruct
            # 注意:此时的DataFrame的列名已经是映射过的列名,可以直接使用
            data_list = input_data_struct.data_list  # type: DataFrame
            data_list.show()
            if index == 0:
                data_result = data_list.groupby("status").agg({
                    "power": "mean"
                }).withColumnRenamed("avg(power)", "powerAvg")
            else:
                data_result = data_result.union(data_list.groupby("status").agg({
                    "power": "mean"
                }).withColumnRenamed("avg(power)", "powerAvg"))

        # 保存最终结果
        destruction.data_result = data_result
        # 保存存储的格式,需要与打包的配置文件对应
        destruction.output_type = FileExtractFormatEnum.JSON.value
```

注意:

------

如果是Windows开发的话需要在脚本文件前加入，findspark请自行下载，没有在包中做依赖管理

```python
import findspark


findspark.init()
```



------

destruction为解构的`HandleDataFrameSet`实体类

------

input_data_struct_list中包含了输入数据的封装,其类型为List

其元素为`HandleInputDataStruct`类,包含的属性为file_type,file_path,file_input_mapping,data_list

算法需要使用的是file_input_mapping和data_list

data_list是输入数据的`DataFrame`

file_input_mapping为输入数据字段的映射

spark为sparkSession对象

mapping_flags为映射标识字典，key为每个单独输入的映射标识，key为输入映射

------

param_map为算法的参数字典

------

在对数据进行业务算法处理完成后,需要将拆解的destruction中的data_result属性赋值为业务算法的最终数据结果

------

在对数据进行业务算法处理完成后,需要将拆解的destruction中的output_type属性赋值为业务算法需要输出的文件格式`FileExtractFormatEnum.JSON.value`中提供了`JSON,CSV,PARQUET,GENERAL`四类格式

------

目前`PARQUET`类的输出格式只支持作为Spark类型的算法积木中的输入

## 3.模型训练算法使用

- [x] Step1:引入datafushion_spark包中的operation模块

- [x] Step2:使用资源管理器进行数据拆解处理,并在其中实现自己需要实现的业务算法逻辑

  ***此处以鸢尾花训练为例进行逻辑回归模型训练***

  ```python
  from datafushion_spark import operation, HandleDataFrameSet, HandleInputDataStruct, DataFrame, SparkSession, \
      FileExtractFormatEnum, TrainFiledEnum, TrainModelResult
  from pyspark.ml.feature import VectorAssembler
  from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
  from pyspark.ml import Pipeline, PipelineModel
  
  
  if __name__ == '__main__':
      with operation(app_name="IrisClassify", mapping_data=False,
                     master="local") as destruction:  # type:HandleDataFrameSet
          input_data_struct_list = destruction.input_data_struct_list
          mapping_flags = destruction.mapping_flags  # type: dict
          param_map = destruction.param_map
          spark = destruction.spark  # type:SparkSession
  
          algo_iter = param_map['iter']
          algo_reg = param_map['reg']
          algo_elastic_net = param_map['elasticNet']
          mapping_list = []
          for k, v in mapping_flags.items():
              mapping_list.append(v)
          data_result = None
  
          # 算法逻辑部分
          for index, input_data_struct in enumerate(input_data_struct_list):  # type: HandleInputDataStruct
              # 注意:此时的DataFrame的列名已经是映射过的列名,可以直接使用
              data = input_data_struct.data_list  # type: DataFrame
              mapping = mapping_list[index]
              feature_fields = mapping[TrainFiledEnum.FEATURE.value]
              label_field = mapping[TrainFiledEnum.LABEL.value][0]
              train_data = data.withColumnRenamed(label_field, TrainFiledEnum.LABEL.value)
              featureAssembler = VectorAssembler().setInputCols(feature_fields).setOutputCol('features')
              logistic_regression = LogisticRegression().setMaxIter(algo_iter).setRegParam(algo_reg).setElasticNetParam(
                      algo_elastic_net)
              pipeline_model: PipelineModel = Pipeline().setStages([featureAssembler, logistic_regression]).fit(
                      train_data)
              # 将data_result实例化为一个TrainModelResult对象
              data_result = TrainModelResult(train_data=train_data, pipeline_model=pipeline_model)
              lg_model: LogisticRegressionModel = pipeline_model.stages[1]
              for item in lg_model.summary.objectiveHistory:
                  print(item)
  
              # 保存最终结果
          destruction.data_result = data_result
          # 保存存储的格式,需要与打包的配置文件对应
          destruction.output_type = FileExtractFormatEnum.MODEL.value
  ```

  注意:

  ------

  如果需要训练模型的话，一般情况下

  1.将operation中设置为mapping_data=False,因为一般我们需要自己根据标识来确定怎样处理特征数据

  2.将data_result需要设置为TrainModelResult实例，其中TrainModelResult包括的数据有train_data和pipeline_model，即训练数据和管道模型

  3.最后需要设置解构回调对象的output_type为model格式`destruction.output_type = FileExtractFormatEnum.MODEL.value`