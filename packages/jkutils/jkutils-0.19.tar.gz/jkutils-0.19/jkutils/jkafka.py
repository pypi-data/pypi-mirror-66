# -*- coding: utf-8 -*-
import logging

from kafka import KafkaConsumer, KafkaProducer

logger = logging.getLogger(__name__)


class JKkafkaConsumer:
    def __init__(
            self,
            bootstrap_servers,
            group_id,
            mq_error_func=None,
            auto_offset_reset="earliest",
            **kwargs,
    ):
        self.mq_error_func = mq_error_func
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            **kwargs
        )

    def subscribe(self, topics):
        self.consumer.subscribe(topics)

    def close(self):
        self.consumer.close()

    def commit(self, offsets=None):
        self.consumer.commit(offsets=offsets)

    def commit_async(self, offsets, callback):
        self.consumer.commit_async(offsets=offsets, callback=callback)

    def consume_data(self, callback):
        assert callable(callback)
        for msg in self.consumer:
            try:
                callback(msg)
            except Exception as err:
                self.consumer.commit()
                logger.error(f"Consumer callback func Exception :{err}")
                if self.mq_error_func and callable(self.mq_error_func):
                    try:
                        self.mq_error_func(msg)
                    except Exception as err:
                        logger.error(
                            f"Consumer mq_error_func func Exception :{err}")


class JKKafka:
    def __init__(
            self,
            bootstrap_servers,
            sasl_mechanism=None,
            security_protocol="PLAINTEXT",
            sasl_plain_username=None,
            sasl_plain_password=None,
            **kwargs,
    ):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            sasl_mechanism=sasl_mechanism,
            security_protocol=security_protocol,
            sasl_plain_username=sasl_plain_username,
            sasl_plain_password=sasl_plain_password,
            **kwargs,
        )

    def send(self, topic_name, data: bytes, **kwargs):
        self.producer.send(topic=topic_name, value=data, **kwargs)

    def close(self):
        self.producer.close()
