package cron

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type CronForm struct {
	CronId int    `form:"cron_id" binding:"required"`
	Crons  string `form:"crons" binding:"required"`
}

func Run(ctx *gin.Context) {
	var sc CronForm
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

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  "定时任务已提交",
		"code": 10000,
	})

}

func Stop(ctx *gin.Context) {
	var sc CronForm
	if err := ctx.ShouldBind(&sc); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	if err := StopCron(sc); err != nil {
		ctx.JSON(http.StatusForbidden, gin.H{
			"msg":  err.Error(),
			"code": 10001,
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  "定时任务已停止",
		"code": 10000,
	})

}
