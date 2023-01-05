package cron

import (
	"os/exec"
	"strconv"

	"github.com/Lxb921006/cmdb/project/model"
)

func StopCron(sc CronForm) (err error) {
	var scs model.CronsCrontabs

	_, err = exec.Command("sh", "/web/wwwroot/shell/opt/cron_script/stop_cron.sh", strconv.Itoa(sc.CronId), "103", sc.Crons).Output()
	if err != nil {
		if err = scs.CronChangeStatus(uint(sc.CronId), 102); err != nil {
			return
		}
		return
	}

	return
}
