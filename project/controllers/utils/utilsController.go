package utils

import (
	"fmt"
	"net/http"
	"path/filepath"
	"strings"

	"github.com/gin-gonic/gin"
)

func Upload(ctx *gin.Context) {
	file, err := ctx.FormFile("file")
	if err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	rdata := make(map[string]interface{})

	if strings.HasSuffix(file.Filename, ".sql") {
		if err := ctx.SaveUploadedFile(file, filepath.Join(SaveSqlPath, file.Filename)); err != nil {
			rdata["msg"] = err.Error()
			rdata["code"] = 10001
		} else {
			rdata["msg"] = fmt.Sprintf("%s上传成功", file.Filename)
			rdata["code"] = 10000
		}
	} else {
		rdata["msg"] = "只能上传sql文件"
		rdata["code"] = 10002
	}

	ctx.JSON(http.StatusOK, rdata)

}
