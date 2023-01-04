package root

import (
	"net/http"
	"time"

	"github.com/Lxb921006/cmdb/project/middleware"
	"github.com/Lxb921006/cmdb/project/routes/cron"
	"github.com/gin-gonic/gin"
)

func SetupRouter() *http.Server {
	router := gin.Default()

	router.Use(middleware.AllowCos(), middleware.TokenVerify())

	cron.CronRouter(router)

	t := &http.Server{
		Addr:           ":9294",
		Handler:        router,
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 8 << 20, //body大小8M
	}

	return t
}
