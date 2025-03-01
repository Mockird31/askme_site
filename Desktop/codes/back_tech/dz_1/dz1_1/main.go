package main

import (
	fileWorker "dz1/fileWorker"
	myUniq "dz1/uniqRealization"
	"fmt"
	"log"
)

func main() {
	options := myUniq.ParseArgs()
	if options == nil {
		log.Fatal("Error while parsing arguments")
	}
	myUniq, err := myUniq.NewUniq(options)
	if myUniq == nil || err != nil {
		log.Fatal(err)
	}

	result := myUniq.Process()
	if options.OutputFile != "" {
		err = fileWorker.WriteFile(options.OutputFile, result)
		if err != nil {
			log.Fatal(err)
		}
	} else {
		for _, line := range result {
			fmt.Println(line)
		}
	}
}
