package runsql

import (
	"github.com/Lxb921006/cmdb/project/controllers/runsql"
	"github.com/gin-gonic/gin"
)

func RunsqlRouter(r *gin.Engine) {
	group := r.Group("/runsql")
	{
		group.POST("/run", runsql.Run)
	}
}
