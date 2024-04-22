import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *


conf = SparkConf().setAppName('Test10').setMaster('Local')
sc = SparkContext(conf=conf)
spark = SparkSession(sc)
data = sc.parallelize([1,2,3,4,5,6,7]).collect()
