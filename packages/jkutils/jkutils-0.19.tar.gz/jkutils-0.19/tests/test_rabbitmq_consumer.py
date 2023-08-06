import logging
from threading import Thread

from pika.channel import Channel

from jkutils.rabbitmq import MqConsumer

logging.basicConfig(level=logging.INFO)


def call(ch: Channel, method, properties, body):
    print("{}:{}:{}:{}".format(ch, method.routing_key, properties, body))


def call_backic_ack(ch: Channel, method, properties, body):
    print("[call_backic_ack] {}:{}:{}:{}".format(ch, method.routing_key, properties, body))
    # ch(delivery_tag = method.delivery_tag)
    # import time
    # time.sleep(10)
    print(method.delivery_tag)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    raise Exception()


def mq_error_func(msg):
    print("[call]:{}".format(msg))
    raise Exception("Exception Test！")


# @pytest.mark.skip(reason="skip")
def test_consumer():
    p = MqConsumer("amqp://guest:guest@127.0.0.1:5672/", mq_error_func)
    p.topic_consumer(
        exchange="test_topic",
        queue_name="test",
        callback=call,
        binding_key="a.*",
        exception_sleep_time=5,
        prefetch_count=1,
    )


def test_consumer_man_ack():
    p = MqConsumer("amqp://guest:guest@127.0.0.1:5672/", mq_error_func)
    p.topic_consumer(
        exchange="test_topic",
        queue_name="test",
        callback=call_backic_ack,
        binding_key="a.*",
        exception_sleep_time=5,
        prefetch_count=1,
        auto_ack=False,
        arguments={
            "x-dead-letter-exchange": "test_topic",
            "x-dead-letter-routing-key": "a.*",
            "x-message-ttl": 1 * 1000,
        },
    )




class Woker(Thread):
    def __init__(self, amqp_url, error_func, topic_consumer_para):
        Thread.__init__(self)
        self.amqp_url = amqp_url
        self.error_func = error_func
        self.topic_consumer_para = topic_consumer_para

    def run(self):
        p = MqConsumer(self.amqp_url, self.error_func)
        p.topic_consumer(**self.topic_consumer_para)


if __name__ == "__main__":
    # test_consumer()

    # test_consumer_man_ack()
    para = {
        "exchange": "test_topic",
        "queue_name": "test",
        "callback": call_backic_ack,
        "binding_key": "a.*",
        "exception_sleep_time": 5,
        "prefetch_count": 1,
        "auto_ack": False,
        "arguments": {
            "x-dead-letter-exchange": "test_topic",
            "x-dead-letter-routing-key": "a.*",
            "x-message-ttl": 1 * 1000,
        },
    }
    workers = []
    worker = Woker("amqp://guest:guest@127.0.0.1:5672/", mq_error_func, para)
    worker.start()
    workers.append(worker)
    worker2 = Woker("amqp://guest:guest@127.0.0.1:5672/", mq_error_func, para)
    worker2.start()
    workers.append(worker2)
    while True:
        print("[total workers:{}]".format(len(workers)))
        for w in workers:
            print(w.isAlive())
            if not w.isAlive():
                print("not alive")
                new = Woker(w.amqp_url, w.error_func, w.topic_consumer_para)
                new.start()
                workers.remove(w)
                workers.append(new)
            import time

            time.sleep(1)
    # import time
    # print("=======")
    # time.sleep(11111)
