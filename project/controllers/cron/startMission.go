package cron

import (
	"os/exec"
	"strconv"
)

func StartCron(sc CronForm) (err error) {
	//var scs model.CronsCrontabs
	_, err = exec.Command("sh", "/web/wwwroot/shell/opt/cron_script/new_run_cron.sh", strconv.Itoa(sc.CronId), sc.Crons).Output()
	if err != nil {
		//if err = scs.CronChangeStatus(uint(sc.CronId), 102); err != nil {
		//	return
		//}
		//return errors.New(string(msg))
		return nil
	}

	return
}
