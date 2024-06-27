package main

import (
	"fmt"
	"net/http"
	"time"

	"backend/models"
	"backend/utils"

	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)



func initGin() {
	r := gin.Default()
	r.POST("/register",func(c *gin.Context){
		var u models.User
		err := c.BindJSON(&u)
		if err != nil {
			c.JSON(http.StatusBadRequest,gin.H{"status": "failed"})
			return
		}
		c.JSON(http.StatusOK,gin.H{
			"username": u.Username,
			"password": u.Password,})
		u.Mail = "default"
		u.Status = 1
		_, err = models.InsertUser(u)
		if err != nil {
			fmt.Println("insert user failed")
			c.JSON(http.StatusBadRequest,gin.H{"status": "failed"})
			return
		}
		fmt.Println("register success")
	})

	r.POST("/login",func(c *gin.Context){
		var u models.User
		err := c.BindJSON(&u)
		if err != nil {
			c.JSON(http.StatusBadRequest,gin.H{"status": "failed"})
			return
		}
		id := models.QueryUserIdWithUsername(u.Username)
		fmt.Println("id:",id)
		if id == 0 {
			c.JSON(http.StatusBadRequest,gin.H{"status": "failed"})
			return
		}
		password := models.QueryUserPasswordWithId(id)
		fmt.Println("password:",password)
		if password != u.Password {
			c.JSON(http.StatusBadRequest,gin.H{"status": "failed"})
			return
		}
		c.JSON(http.StatusOK,gin.H{"status": "success"})
	});



	r.Run(":8090")
}


func main()  {
	err := utils.InitDB()
	if err != nil {
		fmt.Printf("initDB failed, err:%v\n", err)
		return
	}
	fmt.Println("connect to db success")
	initGin()
	go utils.KeepAlive(1*time.Minute)
	select{


	}
}