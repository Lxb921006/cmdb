package smb

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type UpadateSmbUserForm struct {
	Name      string       `form:"name" binding:"required"`
	ShareName string       `form:"shareName" binding:"required"`
	PassWd    string       `form:"passwd"`
	Path      string       `form:"path" binding:"required"`
	IsWrite   string       `form:"iswrite"`
	ctx       *gin.Context `json:"-"`
}

func (u *UpadateSmbUserForm) Update() (err error) {
	if err = u.ctx.ShouldBind(u); err != nil {
		u.ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	na := NewSmbHandle(
		CallAll(u.Name, u.PassWd, u.Path, u.ShareName, u.IsWrite),
	)

	if err = na.UpdateSmbUser(); err != nil {
		return
	}

	return
}

func NewUpadateSmbUserForm(ctx *gin.Context) *UpadateSmbUserForm {
	return &UpadateSmbUserForm{
		ctx: ctx,
	}
}
