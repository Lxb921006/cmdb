package web

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

type CreateWebLogPathForm struct {
	Path string `form:"path" binding:"required"`
}

func CreateWebLogPath(ctx *gin.Context) {
	var cwlp CreateWebLogPathForm
	if err := ctx.ShouldBind(&cwlp); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	if err := NewWebHandle(cwlp.Path).CreateLog(); err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"msg":  err.Error(),
			"code": 10001,
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

	if err := NewWebHandle(cwlp.Path).ClearCache(); err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"msg":  err.Error(),
			"code": 10001,
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  fmt.Sprintf("清除%s缓存成功", cwlp.Path),
		"code": 10000,
	})

}
