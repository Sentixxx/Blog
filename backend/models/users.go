package models

import (
	"backend/utils"
	"fmt"
)


type User struct {
	Id int
	Username string
	Password string
	Mail string
	Status int
}

func InsertUser(user User) (int64, error) {
	return utils.ModifyDB("insert into users(usermail,username,password, status) values(?,?,?,?)", user.Mail,
		user.Username, user.Password, user.Status)
}

func QueryUserIdWithCondition(condition string) int {
	sql_sentence := fmt.Sprintf("select id from users %s", condition)
	fmt.Println(sql_sentence)
	row := utils.QueryRowDB(sql_sentence)
	id := 0
	row.Scan(&id)
	return id
}

func QueryUserIdWithUsername(username string) int {
	return QueryUserIdWithCondition(fmt.Sprintf("where username='%s'", username))
}

func QueryUserPasswordWithId(id int) string {
	sql_sentence := fmt.Sprintf("select password from users where id=%d", id)
	row := utils.QueryRowDB(sql_sentence)
	password := ""
	row.Scan(&password)
	return password
}



