package upload

import (
	"errors"
	"github.com/gin-gonic/gin"
	"path/filepath"
)

type Upload struct {
	ctx  *gin.Context
	data string
}

func NewUpload(ctx *gin.Context, data string) Upload {
	return Upload{
		ctx:  ctx,
		data: data,
	}
}

func (u Upload) UploadFile() error {
	file, err := u.ctx.FormFile("file")
	if err != nil {
		return err
	}

	val := u.ctx.PostForm(u.data)
	if val == "" {
		return errors.New("无效请求")
	}

	fullFile := filepath.Join(u.ctx.PostForm(val), file.Filename)
	if err = u.ctx.SaveUploadedFile(file, fullFile); err != nil {
		return err
	}

	return nil
}
