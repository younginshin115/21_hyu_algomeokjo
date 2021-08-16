import org.apache.spark.streaming.StreamingContext
import org.apache.spark.streaming.Seconds
import kafka.serializer.StringDecoder
import org.apache.spark.streaming.kafka010.KafkaUtils
import org.apache.spark.sql.SparkSession
import java.util.Date
import org.apache.spark.sql.functions._
import org.apache.spark.sql
import org.apache.log4j.Logger
import org.apache.log4j.Level
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.spark.sql.SaveMode
import java.util.Properties
import spark.implicits._

val brokers = "localhost:9092"
val topics = "customvision"

val spark = SparkSession.builder().appName("writeKafkaToMaria").master("local[*]").getOrCreate();
val ssc = new StreamingContext(spark.sparkContext, Seconds(10))

val kafkaParams = Map[String,String](
"zookeeper.connect" -> "localhost:2181",
"bootstrap.servers" -> "localhost:9092",
"metadata.broker.list" -> brokers,
"key.deserializer" -> "org.apache.kafka.common.serialization.StringDeserializer",
"value.deserializer" -> "org.apache.kafka.common.serialization.StringDeserializer",
"auto.offset.reset" -> "latest",
"group.id" -> "use_a_separate_group_id_for_each_stream")

val stream = KafkaUtils.createDirectStream[String, String](ssc, PreferConsistent, Subscribe[String, String](Set(topics), kafkaParams))

var lines = stream.map(_.value().replace("\"",""))

lines.foreachRDD(
rdd => {
    val line = rdd.toDS()
    println("Old Schema");
    line.show()
    val modifiedDF = line.withColumn("_tmp", split(col("value"), ",")).select(
        $"_tmp".getItem(0).as("tag").cast(sql.types.IntegerType),
        $"_tmp".getItem(1).as("url").cast(sql.types.StringType)
    )
    println("With new fields")
    modifiedDF.show()
    val properties = new Properties()
    properties.put("user", "root")
    properties.put("password", "{비밀번호}")
    modifiedDF.write.mode(SaveMode.Append).option("driver", "com.mysql.cj.jdbc.Driver").jdbc("jdbc:mysql://localhost:3306/mysql", "customvison", properties)
})

ssc.start()
