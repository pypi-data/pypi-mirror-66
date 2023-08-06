# -*- coding: utf-8 -*-

import logging
import time
import traceback

import pika

LOGGER = logging.getLogger(__name__)


class MQPublisher:
    def __init__(self, amqp_url):
        self._url = amqp_url

    def publish(
            self,
            exchange: str,
            exchange_type: str,
            durable: bool,
            routing_key: str,
            msg: str,
            properties={},
            mandatory=False,
            immediate=False,
    ):
        """
        send msg
        :param exchange: exchange
        :param exchange_type: exchange_type
        :param durable: durable
        :param routing_key: routing_key
        :param msg: message
        :param properties: dict like {"delivery_mode":1} support https://pika.readthedocs.io/en/stable/modules/spec.html#pika.spec.BasicProperties
        :param mandatory: mandatory
        :param immediate: immediate
        :return:
        """
        try:

            parameters = pika.URLParameters(self._url)

            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.exchange_declare(
                exchange=exchange,
                exchange_type=exchange_type,
                durable=durable)
            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=msg,
                properties=pika.BasicProperties(**properties),
                mandatory=mandatory,
                immediate=immediate,
            )
        except Exception as e:
            LOGGER.warning(
                f"send_msg:{str(e)}, Exception:{traceback.format_exc()}")
            raise
        finally:
            connection.close()


class MqConsumer():
    def __init__(self, amqp_url: str, mq_error_func=None):
        self._url = amqp_url
        self._error_call = mq_error_func

    def safe_call_error_func(self, msg):
        try:
            if self._error_call and callable(self._error_call):
                self._error_call(msg)
        except Exception as err:
            LOGGER.error("Calling error func error:{}".format(err))

    def topic_consumer(
            self,
            exchange: str,
            queue_name: str,
            callback,
            binding_key,
            durable=True,
            auto_ack=True,
            exception_sleep_time=5,
            prefetch_count=1,
            arguments=None):
        """
        Consumer for topic exchange
        :param exchange:exchange
        :param queue_name:queue_name
        :param callback:callback
        :param binding_key:binding_key
        :param durable:durable
        :param auto_ack:auto_ack
        :param exception_sleep_time:sleep time when exception (s)
        :param prefetch_count:prefetch_count
        :return:
        """
        while (True):
            parameters = pika.URLParameters(self._url)
            try:
                LOGGER.info("Connecting to mq...")
                connection = pika.BlockingConnection(parameters)
                channel = connection.channel()
                channel.basic_qos(prefetch_count=prefetch_count)
                channel.queue_declare(queue_name, durable=durable)
                # 绑定
                channel.queue_bind(exchange=exchange,
                                   queue=queue_name,
                                   routing_key=binding_key,
                                   arguments=arguments
                                   )
                channel.basic_consume(queue_name,
                                      callback,
                                      auto_ack=auto_ack
                                      )
                try:
                    LOGGER.info("String consuming mq...")
                    channel.start_consuming()
                except KeyboardInterrupt:
                    channel.stop_consuming()
                    connection.close()
                    break
            except pika.exceptions.ConnectionClosed:
                LOGGER.info("mq conn closed.")
                time.sleep(exception_sleep_time)
                continue
            except pika.exceptions.AMQPChannelError as err:
                msg = "Caught a channel error: {}, stopping...".format(err)
                LOGGER.info(msg)
                self.safe_call_error_func(msg)
                time.sleep(exception_sleep_time)
                continue
            except pika.exceptions.AMQPConnectionError as err:
                msg = "Connection was closed error:{}, retrying...".format(err)
                LOGGER.info(msg)
                self.safe_call_error_func(msg)
                time.sleep(exception_sleep_time)
                continue
