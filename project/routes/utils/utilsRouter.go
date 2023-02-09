package utils

import (
	"github.com/Lxb921006/cmdb/project/controllers/utils"
	"github.com/gin-gonic/gin"
)

func UtilsRouter(r *gin.Engine) {
	group := r.Group("/utils")
	{
		group.POST("/upload", utils.Upload)
	}
}
