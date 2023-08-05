# ML3
-----

Introduction
------------

ML3是TechYoung课程辅助工具包.

+-------------------------------+
| ## Distribution               |
+-------------------------------+
| Run the following commands to |
| register, build and upload    |
| the package to PYPI.          |
+-------------------------------+
| python3 setup.py sdist upload |
+-------------------------------+
| The home page on PYPI is:     |
| https://pypi.org/project/wcc/ |
+-------------------------------+

Install
-------

::

    sudo pip3 install ml3

--------------

Usage
-----

After installation, run the following command:

::

    import ml3

Methods:
~~~~~~~~

plot.histplot(data, column\_name, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_name:*** column name of dataframe, 例如 "hr\_mean"

-  ***kwargs:*** "xmin", "xmax"

plot.gmmplot(data, column\_names, k\_range, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_names:*** list of columns name of dataframe, 例如
   ["hr\_mean", "hr\_std"]

-  ***k\_range:*** the range of components (k), 例如 [2, 11] or (2, 11)

-  ***kwargs:*** "xmin", "xmax", "ymax", "bins"

plot.kmeansplot(data, column\_names, k\_range, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_names:*** list of columns name of dataframe, 例如
   ["hr\_mean", "hr\_std"]

-  ***k\_range:*** the range of clusters (k), 例如 [2, 11] or (2, 11)

-  ***kwargs:*** "xmin", "xmax" "ymax", "bins"

plot.metricplot(n\_clusters\_range, scores, scores2=[], \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***n\_clusters\_range：*** tuple or list of range，例如 (2, 10)

-  ***scores:*** list of score

-  ***scores:*** list of score2 (option)

-  ***kwargs:*** "x\_label", "y\_label"

plot.errorbarplot(data, x, y=[], y2=[], \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***x:*** x-axis column name，例如 "ctime"

-  ***y:*** y column name，例如 ["hr\_mean", "hr\_std"]

-  ***y2:*** y2 column name，例如 ["br\_mean", "br\_std"] (option)

-  ***kwargs:*** "X\_LABEL", "Y\_LABEL", "TITLE", "LIMIT"

plot.pcaplot(data, column\_names, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_names:*** list of columns name of dataframe, 例如
   ["hr\_mean", "hr\_std"]

-  ***kwargs:*** "n\_components"

plot.tsenplot(data, column\_names, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_names:*** list of columns name of dataframe, 例如
   ["hr\_mean", "hr\_std"]

-  ***kwargs:*** "n\_components"

plot.kalmanplot(data, column\_names, dim\_x=2, dim\_z=1, x=[], p=[], f=[], q=[], h=[], r=1, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  ***data:*** dataframe

-  ***column\_names:*** list of columns name of rawdata dataframe, 例如
   ["hr"]

-  ***dim\_x:*** the size of the state vector，状态空间维度

   -  默认为2

-  ***dim\_z:*** the size of the measurement vector，观测矩阵维度

   -  默认为1

-  ***x:*** filter state estimate，初始状态预测矩阵

   -  默认为[1, 0.1]，分别为心率和心率变化率

-  ***p:*** covariance matrix，协方差矩阵

   -  默认为[[1, 0.1], [0.1,
      1]]，心率变化率和人的心率是一定的关系，根据运动状态或者濒死会有很明显的差别，选择0.1代表有一定关系，但是不关系大

-  ***q:*** process
   uncertainty/noise，噪声矩阵，此矩阵不能为0，否则数据会异常

   -  默认为[[0.0001, 0], [0,
      0.0001]]，因为数据都是在cpu中进行，不会产生噪音

-  ***r:*** measurement uncertainty/noise，测量误差

   -  默认为1，测量误差，医疗器械心率误差规定为+-1

-  ***h:*** measurement function

   -  Sometimes certain states are measured, when others are not. For
      example, the first, third and fifth states of a five-dimensional
      state vector are measurable, while second and fourth states are
      not measurable H = [[1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0,
      1]]

-  ***f:*** state transistion matrix，状态转移矩阵

   -  默认为[[1, 0.5], [0, 1]]，此矩阵不能对称，否则会计算异常

-  ***kwargs:*** None

seaborn.boxplot(x, y, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

此函数需要ml4进行对原始数据进行窗口化分类

-  ***x:*** the UNIX timestamp list from ml4

-  ***y:*** the data list from ml4

-  ***kwargs:*** "X\_LABEL", "Y\_LABEL", "TITLE"

seaborn.violinplot(x, y, \*\*kwargs):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

此函数需要ml4进行对原始数据进行窗口化分类

-  ***x:*** the UNIX timestamp list from ml4

-  ***y:*** the data list from ml4

-  ***kwargs:*** "X\_LABEL", "Y\_LABEL", "TITLE"

Example
~~~~~~~

.. code:: python

    import ml3
    import ml4
    import pandas as pd

    data = pd.read_csv("feature.csv")
    # histogram
    ml3.plot.histplot(data, "hr_mean")
    # error bar
    ml3.plot.errorbarplot(data, "ctime", ["hr_mean", "hr_std"], ["br_mean", "br_std"])
    # single feature
    ml3.plot.kmeansplot(data, "hr_mean", (2, 10))
    ml3.plot.gmmplot(data, "hr_mean", (2, 10))
    # multiple features
    ml3.plot.gmmplot(data, ["hr_mean", "hr_std", "br_mean", "br_std", "mo_mean", "mo_std"], (2, 10))
    ml3.plot.kmeansplot(data, ["hr_mean", "hr_std", "br_mean", "br_std", "mo_mean", "mo_std"], (2, 10))
    # two scores metricplot
    scores = [110704, 75304, 60731, 52297, 45675, 41231, 37744, 35247, 33263]
    scores2 = [0.05, 0.09, 0.15, 0.2, 0.3, 0.5, 0.6, 0.9, 1]
    ml3.plot.metricplot((2, 11), scores, scores2)
    # boxplot and violoinplot
    x, y = ml4.ml4.getWindowData(data, "ctime", "hr")
    timeList = []
    for i in x:
        tmp = datetime.fromtimestamp(i)
        timeList.append(tmp.strftime("%H:%M"))
    ml3.seaborn.boxplot(timeList, y)
    ml3.seaborn.violinplot(timeList, y)


    data = pd.read_csv("rawdata.csv")
    ml3.plot.kalmanplot(data, ["hr"])

    data["log1p"] = np.log1p(data["br_std"])
    ml3.plot.kmeansplot(data, ["log1p"], (2, 10), ymax=15, bins=0.01)

Note
----

版本里的1.2.4是旧的版本。1.2.5和以后的版本是用于函数计算的版本。
1.2.5以及以后版本将去掉wcc自动框架.
目录下的子目录：libwebp-0.4.1-linux-x86-64
需要从网上下载，然后把里面的bin下的gif2webp放到/usr/bin里。这样就可以在wcc里调用了.
