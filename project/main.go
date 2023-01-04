package main

import (
	"log"

	"github.com/Lxb921006/cmdb/project/config"
	"github.com/Lxb921006/cmdb/project/dao"
	"github.com/Lxb921006/cmdb/project/routes/root"
)

func main() {
	//初始化mysql
	err := dao.InitPoolMysql()
	if err != nil {
		log.Fatalf(err.Error())
		return
	}

	//初始化redis连接池
	dao.InitPoolRds(config.RedisConAddre, config.RedisUserDb)
	if dao.RdPool == nil {
		log.Fatalf("redis连接失败")
		return
	}
	dao.Rds = dao.NewRedisDb(dao.RdPool, map[string]dao.Md{})

	//初始化gin并启动
	t := root.SetupRouter()
	t.ListenAndServe()
}
