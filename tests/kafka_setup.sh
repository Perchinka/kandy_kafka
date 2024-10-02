#!/bin/bash

echo -e 'Creating kafka topics'

# Create Kafka topics in parallel
for i in {1..3}; do
  kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic "test$i" --replication-factor 1 --partitions 1 &
done
wait

echo -e 'Kafka topics:'
kafka-topics --bootstrap-server kafka:9092 --list

# Batch filling of topics using kafka-console-producer
echo -e 'Filling test1 topic with 10 messages'
seq 1 10 | xargs -I {} echo "Message{}" | kafka-console-producer --bootstrap-server kafka:9092 --topic test1 > /dev/null

echo -e 'Filling test2 topic with 100 messages'
seq 1 100 | xargs -I {} echo "Message{}" | kafka-console-producer --bootstrap-server kafka:9092 --topic test2 > /dev/null

# Indicate process health
echo "askdl" >> /tmp/healthy

# Optional: Remove the tail -f /dev/null if you don't need to keep the script running
tail -f /dev/null
