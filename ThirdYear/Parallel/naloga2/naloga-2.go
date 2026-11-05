package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

type Meritev struct {
	vrsta    string
	vrednost float64
}

func createMeasurment(input int) Meritev {
	options := []string{"temperatura", "pritisk", "vlaga"}

	chosen := options[input]
	var value float64

	switch chosen {
	case "temperatura":

		value = math.Round((-20+rand.Float64()*60.0)*10.0) / 10.0

	case "pritisk":
		value = math.Round((950.0+rand.Float64()*100.0)*10.0) / 10.0

	default:
		value = math.Round(rand.Float64()*100.0*10.0) / 10.0
	}

	return Meritev{vrsta: chosen, vrednost: value}
}

func worker(kanal chan Meritev, input int) {
	duration := rand.Intn(16) + 5

	for watch := 0; watch < duration*2; watch++ {
		kanal <- createMeasurment(input)
		time.Sleep(500 * time.Millisecond)
	}
	fmt.Println("Worker has died")
}

func read(kanal chan Meritev, stop_input chan bool) {
	for {
		select {
		case <-stop_input:
			return

		case output := <-kanal:
			fmt.Println("Program je bil zaustavljen")
			fmt.Println(output)

		case <-time.After(5 * time.Second):
			fmt.Println("Program je nehal delovati")
			return
		}
	}
}

func readKey(input chan bool) {
	fmt.Scanln()
	input <- true
}

func main() {
	kanal := make(chan Meritev, 3)
	stop_input := make(chan bool)

	go readKey(stop_input)

	for i := 0; i < 3; i++ {
		go worker(kanal, i)
	}

	read(kanal, stop_input)
}
