package cron

import (
	"github.com/Lxb921006/cmdb/project/controllers/cron"
	"github.com/gin-gonic/gin"
)

func CronRouter(r *gin.Engine) {
	group := r.Group("/cron")
	{
		group.POST("/run", cron.Run)
		group.POST("/stop", cron.Stop)
	}
}
