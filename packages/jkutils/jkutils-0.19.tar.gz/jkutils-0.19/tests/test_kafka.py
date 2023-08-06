import pytest
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

from jkutils.jkafka import JKKafka, JKkafkaConsumer

kafka_server = "192.168.123.114:9092"


# @pytest.mark.skip(reason="skip")
def test_producer():
    client = JKKafka(bootstrap_servers=kafka_server)
    client.send(topic_name="test1", data="test".encode("utf-8"))
    assert True


def callback_func(msg: ConsumerRecord):
    print(f"[callback]:{msg.value}")


def mq_error_func(msg: ConsumerRecord):
    print(f"[mq_error_func]:{msg.offset}")


if __name__ == "__main__":
    # client = JKKafka(bootstrap_servers=kafka_server)
    # res = client.send(topic_name="test", data="test111".encode("utf-8"))
    # print(res)
    # assert True
    consumer = JKkafkaConsumer(kafka_server, "test-001", mq_error_func)
    consumer.subscribe(["test"])
    consumer.consume_data(callback_func)
    consumer.close()

    # consumer = KafkaConsumer(
    #     bootstrap_servers=kafka_server, group_id="test001", auto_offset_reset="earliest"
    # )
    # consumer.subscribe(["test1"])
    # for msg in consumer:
    #     print(msg)
