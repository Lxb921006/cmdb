package smb

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type AddSmbUserForm struct {
	Name      string       `form:"name" binding:"required"`
	PassWd    string       `form:"passwd" binding:"required"`
	Path      string       `form:"path" binding:"required"`
	ShareName string       `form:"shareName" binding:"required"`
	IsWrite   string       `form:"iswrite" binding:"required"`
	ctx       *gin.Context `json:"-"`
}

func (a *AddSmbUserForm) Add() (err error) {
	if err = a.ctx.ShouldBind(a); err != nil {
		a.ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	na := NewSmbHandle(
		CallAll(a.Name, a.PassWd, a.Path, a.ShareName, a.IsWrite),
	)

	if err = na.AddSmbUser(); err != nil {
		return
	}

	return
}

func NewAddSmbUserForm(ctx *gin.Context) *AddSmbUserForm {
	return &AddSmbUserForm{
		ctx: ctx,
	}
}
