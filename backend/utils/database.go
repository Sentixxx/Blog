package main

import (
	"database/sql"
	"fmt"
	"os"

	_ "github.com/lib/pq"
)

var db *sql.DB


func InitDB() {
	fmt.Println("InitDB...")
	var err error
	
	usr := os.Getenv("DB_USER")
	pwd := os.Getenv("DB_PASSWORD")
	dbname := os.Getenv("DB_NAME")
	host := os.Getenv("DB_HOST")
	port := os.Getenv("DB_PORT")
	fmt.Println(usr, pwd, dbname)


	db , err = sql.Open("postgres", fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable connect_timeout=3", host, port, usr, pwd, dbname))

	if err != nil {
		fmt.Println(err)
		panic(err)
	}

	err = db.Ping()
	if err != nil {
		fmt.Println(err)
		panic(err)
	}

	fmt.Println("Successfully connected!")
}

func GetDB() *sql.DB {
	return db
}

func CloseDB() {
	db.Close()
}

func ModifyDB(sql string,args ... interface{}) (int64, error) {
	result , err := db.Exec(sql, args...)
	if err != nil {
		fmt.Println(err)
		return 0, err
	}
	
	cnt , err := result.RowsAffected()
	if err != nil {
		fmt.Println(err)
		return 0, err
	}

	return cnt, nil
}

func QueryDB(sql string) *sql.Row {
	return db.QueryRow(sql)
}

func CreateTable() {
	sql := `CREATE TABLE IF NOT EXISTS users(
			id INT(4) PRIMARY KEY AUTO_INCREMENT NOT NULL,
			username VARCHAR(64),
			password VARCHAR(64),
			status INT(4),
			createtime INT(10)
			);`
	ModifyDB(sql)
}

func main() {
	InitDB()
	
}

