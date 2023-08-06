import time

from jkutils.jkafka import JKKafka

kafka_server = "172.16.1.32:9092"

if __name__ == "__main__":
    # while True:
    client = JKKafka(bootstrap_servers=kafka_server)
    res = client.send(topic_name="public_to_elk_dev", data="{}".encode("utf-8"))
    time.sleep(2)
