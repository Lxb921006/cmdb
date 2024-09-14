package cron

import (
	"os/exec"
)

func PsCronProcess() (err error) {
	cmd := exec.Command("sh", PsCronProcessScript)
	if err := cmd.Run(); err != nil {
		return err
	}

	return
}
