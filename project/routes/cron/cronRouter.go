package cron

import (
	"github.com/Lxb921006/cmdb/project/controllers/cron"
	"github.com/gin-gonic/gin"
)

func CronRouter(r *gin.Engine) {
	user := r.Group("/cron")
	{
		user.POST("/run", cron.Run)
	}
}
