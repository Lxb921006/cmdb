package smb

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func AddSmbUser(ctx *gin.Context) {
	naa := NewAddSmbUserForm(ctx)
	if err := naa.Add(); err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"msg":  err.Error(),
			"code": 10001,
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  fmt.Sprintf("smb用户%s添加成功", naa.Name),
		"code": 10000,
	})
}

func DelSmbUser(ctx *gin.Context) {
	naa := NewDelSmbUserForm(ctx)
	if err := naa.Del(); err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"msg":  err.Error(),
			"code": 10001,
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  "smb用户删除成功",
		"code": 10000,
	})
}

func UpdateSmbUser(ctx *gin.Context) {
	naa := NewUpadateSmbUserForm(ctx)
	if err := naa.Update(); err != nil {
		ctx.JSON(http.StatusOK, gin.H{
			"msg":  err.Error(),
			"code": 10001,
		})
		return
	}

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  fmt.Sprintf("smb用户%s配置修改成功", naa.Name),
		"code": 10000,
	})
}
