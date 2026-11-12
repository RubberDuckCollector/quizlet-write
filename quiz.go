package main

import (
	"fmt"
	"syscall"
	"log"
	"os"
	"os/signal"

	"github.com/chzyer/readline"
)

func quiz() /* NEED TO FIGURE OUT RETURN TYPES E.G. WHEN THE SESSION FINISHES NORMALLY VS. A CTRL-C */ {
	var filename string = "/home/eingabeaufforderung/flash-cards/languages/basque/self-study/comparative.txt"
	data, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("file contents: %s", string(data))

	keys := make(chan rune, 10)

	go func() {
		for key := range keys {
			switch key {
			case 3:
				fmt.Printf("\nctrl-c: exiting...")
				os.Exit(0)
			case 4:
				fmt.Printf("\nctrl-d: exiting...")
				os.Exit(0)
			}
		}
	}()

	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGTERM)
	defer signal.Stop(signals)

	go func() {
        for sig := range signals {
            fmt.Println("\nreceived signal:", sig)
        }
    }()

	rl, err := readline.NewEx(&readline.Config{
		Prompt: "> ",

		FuncFilterInputRune: func (r rune) (rune, bool) {
			switch r {
			case 3, 4:
				select {
				case keys <- r:
				default:
				}
			return r, false
			}
			return r, true
		},
	})

	if err != nil {
		log.Fatal(err)
	}
	defer rl.Close()
	defer close(keys)

	for {
		line, err := rl.Readline()
		if err != nil {
			log.Fatal(err)
		}

		fmt.Println("input:", line)
	}
}
