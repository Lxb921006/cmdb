package check_web_content

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
	"path/filepath"
)

const (
	rootDir = "/web/wwwroot"
)

type CheckWebCodeContent struct {
	Path string `form:"path" binding:"required"`
}

func CheckWebCodeContentCtl(ctx *gin.Context) {
	var ctl CheckWebCodeContent
	if err := ctx.ShouldBind(&ctl); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	data, err := os.ReadFile(filepath.Join(rootDir, ctl.t))
	if err != nil {
		ctx.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	// 设置响应内容类型为"text/plain"，根据你的文件类型可能需要调整
	ctx.Data(http.StatusOK, "text/plain; charset=utf-8", data)
}
