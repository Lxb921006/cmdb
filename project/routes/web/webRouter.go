package web

import (
	"github.com/Lxb921006/cmdb/project/controllers/web"
	"github.com/gin-gonic/gin"
)

func WebRouter(r *gin.Engine) {
	user := r.Group("/web")
	{
		user.POST("/createlog", web.CreateWebLogPath)
		user.POST("/clearcache", web.ClearCache)
	}
}
