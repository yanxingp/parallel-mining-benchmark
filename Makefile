default: benchmark

benchmark: ./mining-go/mining ./mining-java/Mining.class
	./mining-go/mining
	java -cp ./mining-java Mining
	python3 ./mining-python/mining.py

./mining-go/mining: ./mining-go/mining.go
	go build -o ./mining-go/mining ./mining-go/mining.go

./mining-java/Mining.class: ./mining-java/Mining.java
	javac ./mining-java/Mining.java

clean:
	rm -f ./mining-go/mining
	rm -f ./mining-java/*.class