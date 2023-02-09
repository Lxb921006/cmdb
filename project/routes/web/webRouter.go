package web

import (
	"github.com/Lxb921006/cmdb/project/controllers/web"
	"github.com/gin-gonic/gin"
)

func WebRouter(r *gin.Engine) {
	group := r.Group("/web")
	{
		group.POST("/createlog", web.CreateWebLogPath)
		group.POST("/clearcache", web.ClearCache)
	}
}
