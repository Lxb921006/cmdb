package dao

import (
	"database/sql"
	"time"

	"github.com/Lxb921006/cmdb/project/config"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var (
	DB *gorm.DB
)

func InitPoolMysql() (err error) {
	sqlDB, err := sql.Open("mysql", config.MyConAddre)
	if err != nil {
		return
	}

	DB, err = gorm.Open(mysql.New(mysql.Config{
		Conn: sqlDB,
	}), &gorm.Config{})
	if err != nil {
		return
	}

	db, err := DB.DB()
	if err != nil {
		return
	}

	db.SetMaxIdleConns(10)
	db.SetMaxOpenConns(100)
	db.SetConnMaxLifetime(time.Hour)

	return db.Ping()
}
