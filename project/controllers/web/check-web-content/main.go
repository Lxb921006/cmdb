package check_web_content

import (
	"encoding/base64"
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
			"data":    "",
		})
		return
	}

	b, err := os.ReadFile(filepath.Join(rootDir, ctl.Path))
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{
			"message": err.Error(),
			"data":    "",
		})

		return
	}

	base64String := base64.StdEncoding.EncodeToString(b)

	ctx.JSON(http.StatusOK, gin.H{
		"message": "ok",
		"data":    base64String,
	})

}
