package web

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

type CreateWebLogPathForm struct {
	Path string `form:"path" binding:"required"`
}

type RestartAdjustProgram struct {
	Item string `form:"item" binding:"required"`
}

func CreateWebLogPath(ctx *gin.Context) {
	var cwlp CreateWebLogPathForm
	if err := ctx.ShouldBind(&cwlp); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	callPath := func(path string) Option {
		return func(w *WebHandle) {
			w.Path = path
		}
	}

	cc := NewWebHandle(callPath(cwlp.Path))
	if err := cc.CreateLog(); err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"msg":  err.Error(),
			"code": 10000,
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  fmt.Sprintf("创建%s目录成功", cwlp.Path),
		"code": 10000,
	})

}

func ClearCache(ctx *gin.Context) {
	var cwlp CreateWebLogPathForm
	if err := ctx.ShouldBind(&cwlp); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	callPath := func(path string) Option {
		return func(w *WebHandle) {
			w.Path = path
		}
	}

	cc := NewWebHandle(callPath(cwlp.Path))
	if err := cc.ClearCache(); err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"msg":  err.Error(),
			"code": 10000,
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  fmt.Sprintf("清除%s缓存成功", cwlp.Path),
		"code": 10000,
	})

}

func RestartAdjustProgramController(ctx *gin.Context) {
	var rap RestartAdjustProgram
	if err := ctx.ShouldBind(&rap); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
			"code":    10001,
		})
		return
	}

	callItem := func(item string) Option {
		return func(w *WebHandle) {
			w.Path = item
		}
	}

	cc := NewWebHandle(callItem(rap.Item))
	if err := cc.RestartAd(); err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"msg":  err.Error(),
			"code": 10002,
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  fmt.Sprintf("重启%s成功", rap.Item),
		"code": 10000,
	})

}
