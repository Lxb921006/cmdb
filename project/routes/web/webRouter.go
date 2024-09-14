package web

import (
	"github.com/Lxb921006/cmdb/project/controllers/web"
	checkwebcontent "github.com/Lxb921006/cmdb/project/controllers/web/check-web-content"
	"github.com/gin-gonic/gin"
)

func WebRouter(r *gin.Engine) {
	group := r.Group("/web")
	{
		group.POST("/createlog", web.CreateWebLogPath)
		group.POST("/clearcache", web.ClearCache)
		group.GET("/get-code-content", checkwebcontent.CheckWebCodeContentCtl)
		group.GET("/restart-adjust", web.RestartAdjustProgramController)
	}
}
