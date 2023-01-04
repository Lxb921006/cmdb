package dao

import (
	"errors"
	"strings"
	"time"

	"github.com/go-redis/redis"
)

//把关于redis的处理都放这里了,想不到好的位置放
var (
	RdPool *redis.Client
	Rds    *RedisDb
)

//初始化redis连接池
func InitPoolRds(addr string, db int) {
	RdPool = redis.NewClient(&redis.Options{
		Addr:         strings.Split(addr, "&")[0],
		DB:           db,
		Password:     strings.Split(addr, "&")[1],
		MinIdleConns: 5,
		PoolSize:     30,
		PoolTimeout:  30 * time.Second,
		DialTimeout:  1 * time.Second,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	})
}

type Md struct {
	Count uint
	Rtime uint64
	Wait  uint64
}

type RedisDb struct {
	pool *redis.Client
	md   map[string]Md
}

func NewRedisDb(pool *redis.Client, md map[string]Md) *RedisDb {
	return &RedisDb{
		pool: pool,
		md:   md,
	}
}

func (r *RedisDb) RquestVerify(user, token string) (err error) {
	getToken, err := r.pool.Get(user).Result()
	if err != nil {
		err = errors.New("token已失效, 请重新登录")
		return
	}

	if getToken != token {
		err = errors.New("token已过期, 请重新登录")
		return
	}

	return
}
