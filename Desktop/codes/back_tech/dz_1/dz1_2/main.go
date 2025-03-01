package main

import (
	calculator "dz1_2/calculator"
	"fmt"
	"os"
)

func main() {
	args := os.Args[1:]
	if len(args) == 0 {
		fmt.Println("Error: No expression provided")
		os.Exit(1)
	}

	result, err := calculator.CalcExpression(args[0])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	fmt.Println(result)
}
