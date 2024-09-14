package cron

import (
	"github.com/Lxb921006/cmdb/project/controllers/cron/preview"
	"github.com/Lxb921006/cmdb/project/utils/upload"
	"github.com/gin-gonic/gin"
	"net/http"
)

type CronForm struct {
	CronId int    `form:"cron_id" binding:"required"`
	Crons  string `form:"crons" binding:"required"`
}

type FileContentForm struct {
	File string `form:"file" binding:"required"`
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

func GetRunningCron(ctx *gin.Context) {
	if err := PsCronProcess(); err != nil {
		if err != nil {
			ctx.AbortWithError(http.StatusInternalServerError, err)
			return
		}
	}

	data, err := preview.NewPreview(ctx, PsCronProcessRes).FileBytes()
	if err != nil {
		ctx.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	// 设置响应内容类型为"text/plain"，根据你的文件类型可能需要调整
	ctx.Data(http.StatusOK, "text/plain; charset=utf-8", data)
}

func GetCronFileContent(ctx *gin.Context) {
	var fcf FileContentForm
	if err := ctx.ShouldBind(&fcf); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	data, err := preview.NewPreview(ctx, fcf.File).FileBytes()
	if err != nil {
		ctx.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	// 设置响应内容类型为"text/plain"，根据你的文件类型可能需要调整
	ctx.Data(http.StatusOK, "text/plain; charset=utf-8", data)
}

func UploadFileController(ctx *gin.Context) {
	if err := upload.NewUpload(ctx, "path").UploadFile(); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
			"code":    10001,
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  "上传成功",
		"code": 10000,
	})
}
