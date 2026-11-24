package main

import (
	"fmt"
	"os"
)

func main() {
	// quiz()

	// programName := os.Args[0]
	fmt.Println(os.Args)
}

func clearScreen() {
	// Source - https://stackoverflow.com/a/22892171
	// Posted by Kavu, modified by community. See post 'Timeline' for change history
	// Retrieved 2026-11-09, License - CC BY-SA 4.0
	fmt.Print("\033[H\033[2J")
}
