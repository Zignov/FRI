package main

import "fmt"

type Postaja struct {
	ime     string
	kraj    string
	meritve []float64
}

func dodajMeritev(postaje map[string]Postaja, oznaka string, temperatura float64) {
	e, ok := postaje[oznaka]

	if !ok {
		fmt.Println("Postaja z oznako", oznaka, "ne obstaja.")
		return
	}
	if temperatura < -50 || temperatura > 50 {
		fmt.Println("Meritev temperature", temperatura, "je izven dovoljenega območja.")
		return
	}

	e.meritve = append(e.meritve, temperatura)
	postaje[oznaka] = e
	fmt.Println("Meritev temperature", temperatura, "je bila uspešno dodana za postajo", oznaka)
}

func statistika(postaje map[string]Postaja, oznaka string) (najnizja, najvisja, povprecna float64, ok bool) {
	e, ok := postaje[oznaka]
	st := len(e.meritve)
	if st < 3 {
		ok = false
	}

	if !ok {
		fmt.Println("Postaja z oznako", oznaka, "ne obstaja ali nima dovolj meritev.")
		return
	}

	najnizja = e.meritve[0]
	najvisja = e.meritve[0]
	sestevek := 0.0

	for _, temperatura := range e.meritve {
		if temperatura < najnizja {
			najnizja = temperatura
		}
		if temperatura > najvisja {
			najvisja = temperatura
		}
		sestevek += temperatura
	}

	povprecna = sestevek / float64(st)
	return najnizja, najvisja, povprecna, ok
}

func izpisMeritev(postaje map[string]Postaja) {
	fmt.Println("MERTIVE:")

	for postaja := range postaje {
		fmt.Println("Postaja:", postaja)
		fmt.Println("Ime:", postaje[postaja].ime)
		fmt.Println("Kraj:", postaje[postaja].kraj)
		fmt.Println("Meritve:", postaje[postaja].meritve)
		fmt.Println()
	}

}

func izpisPorocila(postaje map[string]Postaja) {
	fmt.Println("POROČILO:")

	for postaja := range postaje {
		najnizja, najvisja, povprecna, ok := statistika(postaje, postaja)
		if !ok {
			continue
		}

		fmt.Print("Ime: ", postaje[postaja].ime, ", ")
		fmt.Print("Min: ", najnizja, ", ")
		fmt.Print("Max: ", najvisja, ", ")
		fmt.Print("Povprečna: ", povprecna, " => ")

		switch {
		case povprecna < 5.0:
			fmt.Print("Mrzlo")
		case povprecna < 15.0:
			fmt.Print("Hladno")
		case povprecna < 25.0:
			fmt.Print("Toplo")
		default:
			fmt.Print("Vroče")
		}

		fmt.Println()
	}
}

func main() {
	var postaje map[string]Postaja
	postaje = make(map[string]Postaja)

	postaje["LJ01"] = Postaja{
		ime:     "Tivoli",
		kraj:    "Ljubljana",
		meritve: []float64{15.5, 16.2, 14.8},
	}

	postaje["MB02"] = Postaja{
		ime:     "Center",
		kraj:    "Maribor",
		meritve: []float64{12.3, 13.1, 11.9},
	}

	postaje["KR03"] = Postaja{
		ime:     "Triglav",
		kraj:    "Kranj",
		meritve: []float64{10.5, 11.2, 9.8},
	}

	postaje["KP04"] = Postaja{
		ime:     "Luka",
		kraj:    "Koper",
		meritve: []float64{18.5, 19.2},
	}
	dodajMeritev(postaje, "LJ01", 17.3)
	dodajMeritev(postaje, "MB02", -60.0)
	dodajMeritev(postaje, "KR17", 25.0)
	fmt.Println()

	izpisMeritev(postaje)
	fmt.Println()

	fmt.Print(statistika(postaje, "LJ01"))
	fmt.Println()

	izpisPorocila(postaje)
}
