echo -e 'Creating kafka topics'
for i in {1..3}; do
  kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic "test$i" --replication-factor 1 --partitions 1
done

echo -e 'Kafka topics:'
kafka-topics --bootstrap-server kafka:9092 --list

echo -e 'Filling test1 topic with 10 messages'
for i in {1..10}; do
  echo "Message$i" | kafka-console-producer --bootstrap-server kafka:9092 --topic test1
done

echo -e 'Filling test2 topic with 100 messages'
for i in {1..100}; do
  echo "Message$i" | kafka-console-producer --bootstrap-server kafka:9092 --topic test2
done

echo "askdl" >> /tmp/healthy

tail -f /dev/null
