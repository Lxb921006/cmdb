package runsql

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func Run(ctx *gin.Context) {
	var sh SqlHandle
	if err := ctx.ShouldBind(&sh); err != nil {
		ctx.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	out := sh.RunIntranetSqlScript()

	ctx.JSON(http.StatusOK, gin.H{
		"msg":  fmt.Sprintf("项目:%s, rsg:%s", sh.Project, out),
		"code": 10000,
	})
}
