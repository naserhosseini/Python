from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf


conf = SparkConf().setAppName('InnoWatt1').setMaster('local')
sc = SparkContext(conf=conf)
spark = SparkSession(sc)
df = spark.read.format('csv').option('header',True).option('inferSchema', True).load('/FileStore/tables/annot.csv')
df.show(10)
df.printSchema()
df.createOrReplaceTempView('Main')
spark.sql('SELECT count(DISTINCT utf8_string) as frq FROM Main').show()
df.write.mode('overwrite').option('header', True).partitionBy('image_id').parquet('/FileStore/tables/parquet_files')