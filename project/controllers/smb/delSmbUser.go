package smb

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type DelSmbUserForm struct {
	Name      string `form:"name" binding:"required"`
	ShareName string `form:"shareName" binding:"required"`
	// Uid       []uint       `form:"uid" binding:"required"`
	ctx *gin.Context `json:"-"`
}

func (d *DelSmbUserForm) Del() (err error) {
	if err = d.ctx.ShouldBind(d); err != nil {
		d.ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	dl := NewSmbHandle(
		CallDel(d.Name, d.ShareName),
	)

	if err = dl.DelSmbUser(); err != nil {
		return
	}

	return
}

func NewDelSmbUserForm(ctx *gin.Context) *DelSmbUserForm {
	return &DelSmbUserForm{
		ctx: ctx,
	}
}
