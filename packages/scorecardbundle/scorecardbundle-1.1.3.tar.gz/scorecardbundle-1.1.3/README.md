# Scorecard-Bundle

An High-level Scorecard Modeling API | 评分卡建模尽在于此

- [English Document](#english-document)
  - [Installment](#installment)
  - [Usage](#usage)
  - [Important Notice](#important-notice)
  - [Updates Log](#updates-log)
- [中文文档  (Chinese Document)](#中文文档--chinese-document)
  - [安装](#安装)
  - [使用](#使用)
  - [重要公告](#重要公告)
  
  - [更新日志](#更新日志)
- [API Guide](#api-guide)
  - [Feature discretization](#feature-discretization)
  - [Feature encoding](#feature-encoding)
  - [Feature selection](#feature-selection)
  - [Model training](#model-training)
  - [Model evaluation](#model-evaluation)

## English Document

### Introduction

Scorecard-Bundle is a **high-level Scorecard modeling API** that is easy-to-use and **Scikit-Learn consistent**. The transformer and model classes in Scorecard-Bundle comply with Scikit-Learn‘s fit-transform-predict convention.

### Installment

- Pip: Scorecard-Bundle can be installed with pip:  `pip install --upgrade scorecardbundle` 

- Manually: Download codes from github `<https://github.com/Lantianzz/Scorecard-Bundle>` and import them directly:

  ~~~python
  import sys
  sys.path.append('E:\Github\Scorecard-Bundle') # add path that contains the codes
  from scorecardbundle.feature_discretization import ChiMerge as cm
  from scorecardbundle.feature_discretization import FeatureIntervalAdjustment as fia
  from scorecardbundle.feature_encoding import WOE as woe
  from scorecardbundle.feature_selection import FeatureSelection as fs
  from scorecardbundle.model_training import LogisticRegressionScoreCard as lrsc
  from scorecardbundle.model_evaluation import ModelEvaluation as me
  ~~~

### Usage

- Like Scikit-Learn, Scorecard-Bundle basiclly have two types of obejects, transforms and predictors. They comply with the fit-transform and fit-predict convention;
- An sample usage example can be found in https://github.com/Lantianzz/Scorecard-Bundle/blob/master/examples/%5BExample%5D%20Basic%20scorecard%20modeling%20with%20Scorecard-Bundle.ipynb
- An Advanced example showing how to build a scorecard with high explainability and good predictability with Scorecard-Bundle can be found in https://github.com/Lantianzz/Scorecard-Bundle/blob/master/examples/%5BExample%5D%20Build%20a%20scorecard%20with%20high%20explainability%20and%20good%20predictability%20with%20Scorecard-Bundle.ipynb
- See more details in API Guide;

### Important Notice

- [Future Fix] In several functions of WOE and ChiMerge module,  vector outer product is used to get the boolean mask matrix between two vectors. This may cause memory error if the feature has too many unique values (e.g.  a feature whose sample size is 350,000 and number of unique values is 10,000  caused this error in a 8G RAM laptop when calculating WOE). The tricky thing is the error message may not be "memory error" and this makes it harder for user to debug ( the current error message could be `TypeError: 'bool' object is not iterable` or  `DeprecationWarning:  elementwise comparison failed`). The next release will add proper error message for this rare error. 
- [Fix] When using V1.0.2, songshijun007 brought up an issue about the raise of KeyError due to too few unique values on training set and more extreme values in the test set. This issue has been resolved and added to V1.1.0.  (issue url: https://github.com/Lantianzz/Scorecard-Bundle/issues/1#issue-565173725).

### Updates Log

#### V1.1.3

- [Fix] Fixed a few minor bugs and warnings detected by Spyder's Static Code Analysis. 

#### V1.1.0

- [Fix] Fixed a bug in `scorecardbundle.feature_discretization.ChiMerge.ChiMerge` to ensure the output discretized feature values are continous intervals from negative infinity to infinity, covering all possible values. This was done by modifying  `_assign_interval_base` function and `chi_merge_vector` function;
- [Fix] Changed the default value of `min_intervals` parameter in `scorecardbundle.feature_discretization.ChiMerge.ChiMerge` from None to 1 so that in case of encountering features with only one unique value would not cause an error. Setting the default value to 1 is actually more consistent to the actual meaning, as there is at least one interval in a feature;
- [Add] Add `scorecardbundle.feature_discretization.FeatureIntervalAdjustment` class to cover the functionality related to manually adjusting features in feature engineering stage. Now this class only contains `plot_event_dist` function, which can visualize a feature's sample distribution and event rate distribution. This is to facilate feature adjustment decisions in order to obtain better explainability and predictabiltiy;

#### V1.0.2

- Fixed a bug in scorecardbundle.feature_discretization.ChiMerge.ChiMerge.transform(). In V1.0.1, The transform function did not run normally when the number of unique values in a feature is less then the parameter 'min_intervals'. This was due to an ill-considered if-else statement. This bug has been fixed in v1.0.2;


## 中文文档  (Chinese Document)

### 简介

Scorecard-Bundle是一个基于Python的高级评分卡建模API，实施方便且符合Scikit-Learn的调用习惯，包含的类均遵守Scikit-Learn的fit-transform-predict习惯。

### 安装

- Pip: Scorecard-Bundle可使用pip安装:  `pip install --upgrade scorecardbundle` 

- 手动: 从Github下载代码`<https://github.com/Lantianzz/Scorecard-Bundle>`， 直接导入:

  ```python
  import sys
  sys.path.append('E:\Github\Scorecard-Bundle') # add path that contains the codes
  from scorecardbundle.feature_discretization import ChiMerge as cm
  from scorecardbundle.feature_discretization import FeatureIntervalAdjustment as fia
  from scorecardbundle.feature_encoding import WOE as woe
  from scorecardbundle.feature_selection import FeatureSelection as fs
  from scorecardbundle.model_training import LogisticRegressionScoreCard as lrsc
  from scorecardbundle.model_evaluation import ModelEvaluation as me
  ```

### 使用

- 与Scikit-Learn相似，Scorecard-Bundle有两种class，transformer和predictor，分别遵守fit-transform和fit-predict习惯；
- 使用示例参见 https://github.com/Lantianzz/Scorecard-Bundle/blob/master/examples/%E7%A4%BA%E4%BE%8B_%E4%BD%BF%E7%94%A8Scorecard-Bundle%E8%BF%9B%E8%A1%8C%E5%9F%BA%E6%9C%AC%E7%9A%84%E8%AF%84%E5%88%86%E5%8D%A1%E5%BB%BA%E6%A8%A1.ipynb
- 展示如何训练可解释性和预测力俱佳的评分卡的高级示例 https://github.com/Lantianzz/Scorecard-Bundle/blob/master/examples/%5BExample%5D%20Build%20a%20scorecard%20with%20high%20explainability%20and%20good%20predictability%20with%20Scorecard-Bundle.ipynb
- 详细用法参见API Guide;

### 重要公告

- [Future Fix] WOE和ChiMerge模块的几处代码（例如WOE模块的woe_vector函数）中，利用向量外积获得两个向量间的boolean mask矩阵，当输入的特征具有较多的唯一值时，可能会导致计算此外积的时候内存溢出（e.g. 样本量35万、唯一值1万个的特征，已在8G内存的电脑上计算WOE会内存溢出），此时的报错信息未必是内存溢出，给用户debug造成困难（当前的报错信息可能是`TypeError: 'bool' object is not iterable`或`DeprecationWarning:  elementwise comparison failed`），在下一版本中会为此罕见的error增加详细的报错信息提示；
- [Fix] 在使用V1.0.2版本时，songshijun007 在issue中提到当测试集存在比训练集更大的特征值时会造成KeyError。这处bug已被解决，已添加到V1.1.0版本中（issue链接https://github.com/Lantianzz/Scorecard-Bundle/issues/1#issue-565173725).

### 更新日志

#### V1.1.3

- [Fix] 修复Spyder的Static Code Analysis功能检测出的几处小bug和warning.

#### V1.1.0 

- [Fix]修正scorecardbundle.feature_discretization.ChiMerge.ChiMerge，使得任意情况下输出的取值区间都是负无穷到正无穷的连续区间（通过修改_assign_interval_base和chi_merge_vector实现）；
- [Fix] 将scorecardbundle.feature_discretization.ChiMerge.ChiMerge中的min_intervals默认值由None改为1，更符合实际情况（实际至少能有一个区间），当遇到特征的唯一值仅有一个的极端情况时也能直接输出此类特征的原值；
- [Add] 增加scorecardbundle.feature_discretization.FeatureIntervalAdjustment类，覆盖了特征工程阶段手动调整特征相关的功能，目前实现了`plot_event_dist`函数，可实现样本分布和响应率分布的可视化，方便对特征进行调整，已获得更好的可解释性和预测力；


#### V1.0.2

- [Fix] 修复scorecardbundle.feature_discretization.ChiMerge.ChiMerge.transform()的一处bug。在V1.0.1中，当一个特征唯一值的数量小于'min_intervals'参数时，transform函数无法正常运行，这是一处考虑不周的if-else判断语句造成的. 此bug已经在v1.0.2中修复;






## API Guide

#### Feature discretization

##### class: scorecardbundle.feature_discretization.ChiMerge.ChiMerge

ChiMerge is a discretization algorithm introduced by Randy Kerber in "ChiMerge: Discretization of Numeric Attributes". It can transform a numerical features into categorical feature or reduce the number of intervals in a ordinal feature based on the feature's distribution and the target classes' relative frequencies in each interval. As a result, it keep statistically significantly different intervals and merge similar ones.

###### Parameters

```mar
m: integer, optional(default=2)
    The number of adjacent intervals to compare during chi-squared test.

confidence_level: float, optional(default=0.9)
    The confidence level to determine the threshold for intervals to 
    be considered as different during the chi-square test.

max_intervals: int, optional(default=None)
    Specify the maximum number of intervals the discretized array will have.
    Sometimes (like when training a scorecard model) fewer intervals are 
    prefered. If do not need this option just set it to None.

min_intervals: int, optional(default=1)
    Specify the mininum number of intervals the discretized array will have.
    If do not need this option just set it to 1.

initial_intervals: int, optional(default=100)
    The original Chimerge algorithm starts by putting each unique value 
    in an interval and merging through a loop. This can be time-consumming 
    when sample size is large. 
    Set the initial_intervals option to values other than None (like 10 or 100) 
    will make the algorithm start at the number of intervals specified (the 
    initial intervals are generated using quantiles). This can greatly shorten 
    the run time. If do not need this option just set it to None.

delimiter: string, optional(default='~')
    The returned array will be an array of intervals. Each interval is 
    representated by string (i.e. '1~2'), which takes the form 
    lower+delimiter+upper. This parameter control the symbol that 
    connects the lower and upper boundaries.

output_boundary: boolean, optional(default=False)
    If output_boundary is set to True. This function will output the 
    unique upper  boundaries of discretized array. If it is set to False,
    This funciton will output the discretized array.
    For example, if it is set to True and the array is discretized into 
    3 groups (1,2),(2,3),(3,4), this funciton will output an array of 
    [1,3,4].
```

###### Attributes

```
boundaries_: dict
    A dictionary that maps feature name to its merged boundaries.
fit_sample_size_: int
    The sampel size of fitted data.
transform_sample_size_:  int
    The sampel size of transformed data.
num_of_x_:  int
    The number of features.
columns_:  iterable
    An array of list of feature names.
```

###### Methods

```
fit(X, y): 
    fit the ChiMerge algorithm to the feature.

transform(X): 
    transform the feature using the ChiMerge fitted.

fit_transform(X, y): 
    fit the ChiMerge algorithm to the feature and transform it.    
```

##### function:  scorecardbundle.feature_discretization.FeatureIntervalAdjustment.plot_event_dist

Visualizing feature event rate distribution to facilitate explainability evaluation.

###### Parameters

~~~
x:numpy.ndarray or pandas.DataFrame, shape (number of examples,)
    The feature to be visualized.

y:numpy.ndarray or pandas.DataFrame, shape (number of examples,)
    The Dependent variable.

delimiter: string, optional(default='~')
    The interval is representated by string (i.e. '1~2'), 
    which takes the form lower+delimiter+upper. This parameter 
    control the symbol that connects the lower and upper boundaries.   

title: Python string. Optional.
    The title of the plot. Default is ''.

x_label: Python string. Optional.
    The label of the feature. Default is ''.

y_label: Python string. Optional.
    The label of the dependent variable. Default is ''.

x_rotation: int. Optional.
    The degree of rotation of x-axis ticks. Default is 0.

xticks: Python list of strings. Optional.
    The tick labels on x-axis. Default is the unique values
    of x (in the format of Python string).

figure_height: int. Optional.
    The hight of the figure. Default is 4.

figure_width: int. Optional.
    The width of the figure. Default is 6.

save: boolean. Optional.
    Whether or not the figure is saved to a local positon.
    Default is False.

path: Python string. Optional.
    The local position path where the figure will be saved.
    This should be set when parameter save is True. Default is ''.
~~~

###### Return

~~~
f1_ax1: matplotlib.axes._subplots.AxesSubplot
        The figure object is returned.
~~~



#### Feature encoding

##### class: scorecardbundle.feature_encoding.WOE.WOE_Encoder

Perform WOE transformation for features and calculate the information value (IV) of features with reference to the target variable y.

###### Parameters

```
epslon: float, optional(default=1e-10)
        Replace 0 with a very small number during division 
        or logrithm to avoid infinite value.       

output_dataframe: boolean, optional(default=False)
        if output_dataframe is set to True. The transform() function will
        return pandas.DataFrame. If it is set to False, the output will
        be numpy ndarray.
```

###### Attributes

```
iv_: a dictionary that contains feature names and their IV

result_dict_: a dictionary that contains feature names and 
    their WOE result tuple. Each WOE result tuple contains the
    woe value dictionary and the iv for the feature.
```

###### Methods

```
fit(X, y): 
        fit the WOE transformation to the feature.

transform(X): 
        transform the feature using the WOE fitted.

fit_transform(X, y): 
        fit the WOE transformation to the feature and transform it.         
```

#### Feature selection

##### function: scorecardbundle.feature_selection.FeatureSelection.selection_with_iv_corr()

Retrun a table of each feature' IV and their highly correlated features to help users select features.

##### Parameters

```
trans_woe: scorecardbundle.feature_encoding.WOE.WOE_Encoder object,
        The fitted WOE_Encoder object

encoded_X: numpy.ndarray or pandas.DataFrame,
        The encoded features data

threshold_corr: float, optional(default=0.6)
        The threshold of Pearson correlation coefficient. Exceeding
        This threshold means the features are highly correlated.
```

##### Return

```
result_selection: pandas.DataFrame,
        The table that contains 4 columns. column factor contains the 
        feature names, column IV contains the IV of features, 
        column woe_dict contains the WOE values of features and 
        column corr_with contains the feature that are highly correlated
        with this feature together with the correlation coefficients.
```

#### Model training

##### class: scorecardbundle.model_training.LogisticRegressionScoreCard

Take encoded features, fit a regression and turn it into a scorecard

###### Parameters

```
woe_transformer: WOE transformer object from WOE module.

C:  float, optional(Default=1.0)
    regularization parameter in linear regression. Default value is 1. 
    A smaller value implies more regularization.
    See details in scikit-learn document.

class_weight: dict, optional(default=None)
    weights for each class of samples (e.g. {class_label: weight}) 
    in linear regression. This is to deal with imbalanced training data. 
    Setting this parameter to 'auto' will aotumatically use 
    class_weight function from scikit-learn to calculate the weights. 
    The equivalent codes are:
    >>> from sklearn.utils import class_weight
    >>> class_weights = class_weight.compute_class_weight('balanced', 
                                                          np.unique(y), y)

random_state: int, optional(default=None)
    random seed in linear regression. See details in scikit-learn doc.

PDO: int,  optional(default=-20)
    Points to double odds. One of the parameters of Scorecard.
    Default value is -20. 
    A positive value means the higher the scores, the lower 
    the probability of y being 1. 
    A negative value means the higher the scores, the higher 
    the probability of y being 1.

basePoints: int,  optional(default=100)
    the score for base odds(# of y=1/ # of y=0).

decimal: int,  optional(default=0)
    Control the number of decimals that the output scores have.
    Default is 0 (no decimal).

start_points: boolean, optional(default=False)
    There are two types of scorecards, with and without start points.
    True means the scorecard will have a start poitns. 

output_option: string, optional(default='excel')
    Controls the output format of scorecard. For now 'excel' is 
    the only option.

output_path: string, optional(default=None)
    The location to save the scorecard. e.g. r'D:\\Work\\jupyter\\'.

verbose: boolean, optioanl(default=False)
    When verbose is set to False, the predict() method only returns
    the total scores of samples. In this case the output of predict() 
    method will be numpy.array;
    When verbose is set to True, the predict() method will return
    the total scores, as well as the scores of each feature. In this case
    The output of predict() method will be pandas.DataFrame in order to 
    specify the feature names.

delimiter: string, optional(default='~')
    The feature interval is representated by string (i.e. '1~2'), 
    which takes the form lower+delimiter+upper. This parameter 
    is the symbol that connects the lower and upper boundaries.
```

###### Attributes

```
woe_df_: pandas.DataFrame, the scorecard.

AB_ : A and B when converting regression to scorecard.
```

###### Methods

```
fit(woed_X, y): 
        fit the Scorecard model.

predict(X_beforeWOE, load_scorecard=None): 
        Apply the model to the original feature 
        (before discretization and woe encoding).
        If user choose to upload their own Scorecard,
        user can pass a pandas.DataFrame to `load_scorecard`
        parameter. The dataframe should contain columns such as 
        feature, value, woe, beta and score. An example would
        be as followed (value is the range of feature values, woe 
        is the WOE encoding of that range, and score is the socre
        for that range):
        feature value   woe         beta        score
        x1      30~inf  0.377563    0.631033    5.0
        x1      20~-30  1.351546    0.631033    37.0
        x1      -inf~20 1.629890    0.631033    -17.0
```

#### Model evaluation

##### class: scorecardbundle.model_evaluation.ModelEvaluation.BinaryTargets

Model evaluation for binary classification problem.

###### Parameters

```
y_true: numpy.array, shape (number of examples,)
        The target column (or dependent variable).  

y_pred_proba: numpy.array, shape (number of examples,)
        The score or probability output by the model. The probability
        of y_true being 1 should increase as this value
        increases.   
        
        If Scorecard model's parameter "PDO" is negative, then the higher the 
        model scores, the higher the probability of y_pred being 1. This Function
        works fine. 

        However!!! if the parameter "PDO" is positive, then the higher 
        the model scores, the lower the probability of y_pred being 1. In this case,
        just put a negative sign before the scores array and pass `-scores` as parameter
        y_pred_proba of this function. 

output_path: string, optional(default=None)
        the location to save the plot, e.g. r'D:\\Work\\jupyter\\'.
```

###### Methods

```
ks_stat(): Return the k-s stat
plot_ks(): Draw k-s curve
plot_roc(): Draw ROC curve
plot_precision_recall(): Draw precision recall curve
plot_all(): Draw k-s, ROC curve, and precision recall curve
```



## 