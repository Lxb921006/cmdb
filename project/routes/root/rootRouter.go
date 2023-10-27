package root

import (
	"net/http"
	"time"

	"github.com/Lxb921006/cmdb/project/middleware"
	"github.com/Lxb921006/cmdb/project/routes/cron"
	"github.com/Lxb921006/cmdb/project/routes/runsql"
	"github.com/Lxb921006/cmdb/project/routes/smb"
	"github.com/Lxb921006/cmdb/project/routes/utils"
	"github.com/Lxb921006/cmdb/project/routes/web"
	"github.com/gin-gonic/gin"
)

func SetupRouter() *http.Server {
	router := gin.Default()

	router.Use(middleware.AllowCos(), middleware.TokenVerify())

	cron.CronRouter(router)
	web.WebRouter(router)
	runsql.RunsqlRouter(router)
	utils.UtilsRouter(router)
	smb.SmbRouter(router)

	t := &http.Server{
		Addr:           ":9295",
		Handler:        router,
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 8 << 20, //body大小8M
	}

	return t
}
