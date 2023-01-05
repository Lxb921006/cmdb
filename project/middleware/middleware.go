package middleware

import (
	"net/http"

	"github.com/Lxb921006/cmdb/project/dao"
	"github.com/gin-gonic/gin"
)

//允许跨域访问
func AllowCos() gin.HandlerFunc {
	return func(ctx *gin.Context) {

		ctx.Header("Access-Control-Allow-Origin", "*")
		ctx.Header("Access-Control-Allow-Headers", "Content-Type,AccessToken,X-CSRF-Token, Authorization, Token")
		ctx.Header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		ctx.Header("Access-Control-Expose-Headers", "Content-Length, Access-Control-Allow-Origin, Access-Control-Allow-Headers, Content-Type")
		ctx.Header("Access-Control-Allow-Credentials", "true")

		if method := ctx.Request.Method; method == "OPTIONS" {
			ctx.AbortWithStatus(http.StatusNoContent)
		}

		ctx.Next()
	}
}

func TokenVerify() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		token := ctx.Query("token")
		user := ctx.Query("user")
		if token == "" || user == "" {
			ctx.JSON(http.StatusBadGateway, gin.H{
				"msg":  "非法请求, 参数缺失",
				"code": 10002,
			})
			ctx.Abort()
		} else {
			if err := dao.Rds.RquestVerify(user, token); err == nil {
				ctx.Next()
			} else {
				ctx.JSON(http.StatusBadGateway, gin.H{
					"msg":  err.Error(),
					"code": 10003,
				})
				ctx.Abort()
			}
		}
	}
}
