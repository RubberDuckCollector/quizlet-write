package main

import (
	"fmt"
	"os"
	"log"
)

func validateCards(filepath string) (string, bool) {
	data, err := os.ReadFile(filepath)
	if err != nil {
		log.Fatal(err)
		return "Error while reading file.", false
	}

	fmt.Println(data)

	return "", true
}
