FROM confluentinc/cp-kafka:latest

WORKDIR /app

COPY tests/kafka_setup.sh ./create_and_fill_topics.sh

USER root
RUN chmod +x ./create_and_fill_topics.sh

CMD ["/bin/bash", "-c", "./create_and_fill_topics.sh"]

