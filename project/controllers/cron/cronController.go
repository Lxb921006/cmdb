package cron

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type StartCronForm struct {
	User    string `form:"user" binding:"required"`
	CronId  int    `form:"cron_id" binding:"required"`
	Project string `form:"project" binding:"required"`
	Crons   string `form:"crons" binding:"required"`
}

type StopCronForm struct {
	CronId []string `form:"crons" binding:"required"`
}

func Run(ctx *gin.Context) {
	var sc StartCronForm
	if err := ctx.ShouldBind(&sc); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	if err := StartCron(sc); err != nil {
		ctx.JSON(http.StatusForbidden, gin.H{
			"msg":  err.Error(),
			"code": 10001,
		})
		return
	}

	ctx.JSON(http.StatusForbidden, gin.H{
		"msg":  "定时任务已提交",
		"code": 10000,
	})

}
