package main

import (
	"fmt"
	"sync"
)

var stNarocil int
var promet float64
var mutex sync.Mutex

type narocilo interface {
	obdelaj() error
}

type izdelek struct {
	imeIzdelka string
	cena       float64
	teza       float64
}

type eknjiga struct {
	naslovKnjige string
	cena         float64
}

type spletniTecaj struct {
	imeTecaja   string
	trajanjeUre int
	cenaUre     float64
}

func (i izdelek) obdelaj() error {
	if i.cena <= 0 {
		return fmt.Errorf("Izdelek %q, je neveljanvno: cena ne sme biti negativna \n", i.imeIzdelka)
	}
	if i.teza <= 0 {
		return fmt.Errorf("Izdelek %q, je neveljanvno: teza ne sme biti negativna \n", i.imeIzdelka)
	}
	if i.imeIzdelka == "" {
		return fmt.Errorf("Izdelek %q, je neveljanvno: ime izdelka ne sme biti prazno \n", i.imeIzdelka)
	}

	mutex.Lock()
	defer mutex.Unlock()

	stNarocil++
	promet += i.cena

	fmt.Printf("stevilka narocila: %d\n", stNarocil)
	fmt.Printf("ime Izdelka: %s\n", i.imeIzdelka)
	fmt.Printf("cena: %.2f€\n", i.cena)
	fmt.Printf("teza: %.2fkg\n", i.teza)
	fmt.Println()

	return nil
}

func (e eknjiga) obdelaj() error {
	if e.cena <= 0 {
		return fmt.Errorf("Knjiga %q, je neveljanvna: cena ne sme biti negativna \n", e.naslovKnjige)
	}
	if e.naslovKnjige == "" {
		return fmt.Errorf("Knjiga %q, je neveljanvna: naslov knjige ne sme biti prazen \n", e.naslovKnjige)
	}

	mutex.Lock()
	defer mutex.Unlock()

	stNarocil++
	promet += e.cena

	fmt.Printf("stevilka narocila: %d\n", stNarocil)
	fmt.Printf("ime Knjige: %s\n", e.naslovKnjige)
	fmt.Printf("cena: %.2f€\n", e.cena)
	fmt.Println()

	return nil
}

func (s spletniTecaj) obdelaj() error {
	if s.cenaUre <= 0 {
		return fmt.Errorf("Tecaj %q, je neveljaven: cena ure ne sme biti negativna \n", s.imeTecaja)
	}
	if s.imeTecaja == "" {
		return fmt.Errorf("Tecaj %q, je neveljaven: ime tecaja ne sme biti prazno \n", s.imeTecaja)
	}
	if s.trajanjeUre <= 0 {
		return fmt.Errorf("Tecaj %q, je neveljaven: trajanje ure mora biti pozitivno \n", s.imeTecaja)
	}

	mutex.Lock()
	defer mutex.Unlock()

	stNarocil++
	skupaj := s.cenaUre * float64(s.trajanjeUre)
	promet += skupaj

	fmt.Printf("Stevilka narocila: %d\n", stNarocil)
	fmt.Printf("Ime tecaja: %s\n", s.imeTecaja)
	fmt.Printf("Trajanje: %d ur\n", s.trajanjeUre)
	fmt.Printf("Cena na uro: %.2f €\n", s.cenaUre)
	fmt.Printf("Skupna cena: %.2f €\n", skupaj)
	fmt.Println()
	return nil
}

func main() {
	narocila := []narocilo{
		izdelek{"Laptop", 1200, 2.5},
		izdelek{"Miska", 25, 0.2},
		eknjiga{"Harry Potter", 15},
		spletniTecaj{"Go Programming", 10, 25},
		izdelek{"Tipkovnica", -50, 0.8},
		eknjiga{"", 20},
		izdelek{"Monitor", 300, 4.5},
		eknjiga{"1984", 12},
		spletniTecaj{"Python", 20, 15},
		izdelek{"Telefon", 800, 0.2},
	}

	var wg sync.WaitGroup
	napake := make(chan error, len(narocila))

	for _, n := range narocila {
		wg.Add(1)

		go func(n narocilo) {
			defer wg.Done()

			err := n.obdelaj()
			if err != nil {
				napake <- err
			}
		}(n)
	}
	wg.Wait()

	close(napake)

	for err := range napake {
		fmt.Println("Napaka:", err)
	}

	fmt.Printf("Stevilo narocil: %d\n", stNarocil)
	fmt.Printf("Skupni promet: %.2f €\n", promet)
}
