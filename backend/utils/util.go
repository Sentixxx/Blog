package utils

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

var db *sql.DB

func InitDB()(error) {
	user := os.Getenv("DB_USER")
	password := os.Getenv("DB_PASSWORD")
	host := os.Getenv("DB_HOST")
	port := os.Getenv("DB_PORT")
	dbName := os.Getenv("DB_NAME")
	// user := "root"
	// password := "root"
	// host := "127.0.0.1"
	// port := "3306"
	// dbName := "ctb_db"

	dsn := user + ":" + password + "@tcp(" + host + ":" + port + ")/" + dbName
	fmt.Println(dsn)
	db1, err := sql.Open("mysql", dsn)
	if err != nil {
		return err
	}
	db = db1
	err = db.Ping()
	if err != nil {
		return err
	}
	return err
}

//操作数据库
func ModifyDB(sql string, args ...interface{}) (int64, error) {
	result, err := db.Exec(sql, args...)
	if err != nil {
		log.Println(err)
		return 0, err
	}
	count, err := result.RowsAffected()
	if err != nil {
		log.Println(err)
		return 0, err
	}
	return count, nil
}

func QueryRowDB(sql string) *sql.Row {
	return db.QueryRow(sql)
}

func KeepAlive(interval time.Duration) {
    for {
        if err := db.Ping(); err != nil {
            log.Printf("Error pinging database: %v", err)
        } else {
            log.Println("Database connection is alive")
        }
        time.Sleep(interval)
    }
}