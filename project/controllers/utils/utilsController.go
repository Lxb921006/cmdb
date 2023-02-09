package utils

import (
	"fmt"
	"net/http"
	"path/filepath"

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

	if err := ctx.SaveUploadedFile(file, filepath.Join(SaveSqlPath, file.Filename)); err != nil {
		rdata["msg"] = err.Error()
		rdata["code"] = 10001
	} else {
		rdata["msg"] = fmt.Sprintf("%s上传成功", file.Filename)
		rdata["code"] = 10000
	}

	ctx.JSON(http.StatusOK, rdata)

}
