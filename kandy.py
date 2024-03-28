from kandy_kafka.controller.controler import KafkaMonitorController

if __name__ == '__main__':
    controller = KafkaMonitorController('localhost:9092')
    controller.run()