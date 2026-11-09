package main

import (
	"fmt"
	// "log"
	"os"
	// "os/signal"
	"errors"
	"github.com/chzyer/readline"
	"io"
	// "github.com/RubberDuckCollector/go-input"
)

func quiz() /* NEED TO FIGURE OUT RETURN TYPES E.G. WHEN THE SESSION FINISHES NORMALLY VS. A CTRL-C */ {
	// var prompt = ""
	rl, err := readline.New("%s\n%s ")
	if err != nil {
		panic(err)
	}
	defer rl.Close()

	for {
		line, err := rl.Readline()
		switch {
		case errors.Is(err, readline.ErrInterrupt):
			fmt.Println("ctrl-c: exiting...")
			os.Exit(0)
		case errors.Is(err, io.EOF):
			fmt.Println("ctrl-d: exiting...")
			os.Exit(0)
		case err != nil:
			return
		}
		fmt.Println(line)
	}
}
