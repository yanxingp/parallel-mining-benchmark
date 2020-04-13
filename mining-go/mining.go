package main

import (
	"fmt"
	"time"
	"crypto/sha256"
	"sync"
)

//  Difficulty of mining
var difficulty int = 5
var prefix string

//  Number of trials
var ntrial int = 5

var data string = "parallel-mining-benchmark"
var global_result string

func sequential() {
	for i := 0; i < ntrial; i++{
		ldata := data + string(i)
		nonce := 0
		for {
			sha256 := sha256.New()
			sha256.Write([]byte(ldata + string(nonce)))
			hash := fmt.Sprintf("%x", sha256.Sum(nil))
			if hash[0:difficulty] == prefix {
				global_result = hash
				break
			}
			nonce++
		}
	}
}

var found bool = false
func parallelGoroutine(ngoroutine int) {
	for i := 0; i < ntrial; i++ {
		var wg sync.WaitGroup
		wg.Add(ngoroutine)
		ldata := data + string(i)
		found = false
		for j := 0; j < ngoroutine; j++ {
			// go mining(j, ngoroutine, ldata, wg)
			go func(id int) {
				defer wg.Done()
				nonce := id
				for !found {
					sha256 := sha256.New()
					sha256.Write([]byte(ldata + string(nonce)))
					hash := fmt.Sprintf("%x", sha256.Sum(nil))
					if hash[0:difficulty] == prefix {
						global_result = hash
						found = true
					}
					nonce += ngoroutine
				}
			} (j)
		}

		wg.Wait()
	}
}

func main() {
	for i := 0; i < difficulty; i++ {
		prefix += "0"
	}
	line := ""
	for i := 0; i < 40; i++ {
		line += "-"
	}
	fmt.Println(line)
	fmt.Println("Golang Version:")
    fmt.Printf("difficulty: %v, number of trials: %v\n", difficulty, ntrial)

	// sequential
	fmt.Println(line)
	start := time.Now()
	sequential()
	elapsed := time.Since(start)
	fmt.Println("sequential version:")
	fmt.Printf("total time consumed: %.4f s\n", elapsed.Seconds())
	fmt.Printf("average time consumed: %.4f s\n", elapsed.Seconds() / float64(ntrial))
	fmt.Printf("last hash computed: %v\n", global_result)

	// goroutine parallel
	ngoroutines := []int{2, 4, 8, 16}
	for _, ngoroutine := range ngoroutines {
		fmt.Println(line)
		start := time.Now()
		parallelGoroutine(ngoroutine)
		elapsed := time.Since(start)
		fmt.Printf("%v goroutine version:\n", ngoroutine)
		fmt.Printf("total time consumed: %.4f s\n", elapsed.Seconds())
		fmt.Printf("average time consumed: %.4f s\n", elapsed.Seconds() / float64(ntrial))
		fmt.Printf("last hash computed: %v\n", global_result)
	}
}