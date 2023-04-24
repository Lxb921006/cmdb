package smb

import (
	"github.com/Lxb921006/cmdb/project/controllers/smb"
	"github.com/gin-gonic/gin"
)

func SmbRouter(r *gin.Engine) {
	group := r.Group("/smb")
	{
		group.POST("/add", smb.AddSmbUser)
		group.POST("/del", smb.DelSmbUser)
		group.POST("/update", smb.UpdateSmbUser)
	}
}
