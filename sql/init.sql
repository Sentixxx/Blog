/*
 * @Author: Sentix 
 * @Date: 2024-07-11 14:19:11 
 * @Last Modified by:   Sentix 
 * @Last Modified time: 2024-07-11 14:19:11 
 */
-- Active: 1720076927509@@127.0.0.1@3306@goadmin

-- ----------------------------
-- 1. 创建数据库
-- ----------------------------
CREATE DATABASE IF NOT EXISTS admin_boot DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;


-- ----------------------------
-- 2. 创建表 && 数据初始化
-- ----------------------------
use admin_boot;

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`  (
    `menu_id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `parent_id` bigint NOT NULL COMMENT '父菜单ID',
    `tree_path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '父节点ID路径',
    `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '菜单名称',
    `type` tinyint NOT NULL COMMENT '菜单类型（1-菜单 2-目录 3-外链 4-按钮）',
    `route_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '路由名称（Vue Router 中用于命名路由）',
    `route_path` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '路由路径（Vue Router 中定义的 URL 路径）',
    `component` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '组件路径（组件页面完整路径，相对于 src/views/，缺省后缀 .vue）',
    `perm` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '【按钮】权限标识',
    `always_show` tinyint NULL DEFAULT NULL COMMENT '【目录】只有一个子路由是否始终显示（1-是 0-否）',
    `keep_alive` tinyint NULL DEFAULT NULL COMMENT '【菜单】是否开启页面缓存（1-是 0-否）',
    `visible` tinyint(1) NOT NULL DEFAULT 1 COMMENT '显示状态（1-显示 0-隐藏）',
    `sort` int NULL DEFAULT 0 COMMENT '排序',
    `icon` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '菜单图标',
    `redirect` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '跳转路径',
    `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
    `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
    `params` text NULL COMMENT '路由参数',
    `note0` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段0',
    `note1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段1',
    `note2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段2',
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 117 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '菜单管理' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for sys_message
-- ----------------------------
DROP TABLE IF EXISTS `sys_message`;
CREATE TABLE `sys_message`  (
    `message_id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
    `create_by` bigint NULL DEFAULT NULL COMMENT '创建人ID',
    `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
    `update_by` bigint NULL DEFAULT NULL COMMENT '修改人ID',
    `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
    `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '逻辑删除标识(1-已删除 0-未删除)',
    `note0` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段0',
    `note1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段1',
    `note2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段2',
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '系统消息' ROW_FORMAT = DYNAMIC;



-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
    `user_id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户名',
    `nickname` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '昵称',
    `gender` tinyint(1) NULL DEFAULT 1 COMMENT '性别((1-男 2-女 0-保密)',
    `password` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '密码',
    `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '用户头像',
    `mobile` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '联系方式',
    `status` tinyint(1) NULL DEFAULT 1 COMMENT '状态((1-正常 0-禁用)',
    `email` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户邮箱',
    `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
    `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
    `note0` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段0',
    `note1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段1',
    `note2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段2',
    `is_deleted` tinyint(1) NULL DEFAULT 0 COMMENT '逻辑删除标识(0-未删除 1-已删除)',
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE INDEX `login_name`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 288 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for book_info
-- ----------------------------
DROP TABLE IF EXISTS `book_info`;
CREATE TABLE `book_info`  (
    `book_id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键：ISBN书号',
    `book_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '书名',
    `author` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '作者',
    `book_code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图书编码',
    `book_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '类型',
    `book_stock` int NULL DEFAULT NULL COMMENT '库存',
    `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
    `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
    `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '逻辑删除标识(1-已删除 0-未删除)',
    `note0` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段0',
    `note1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段1',
    `note2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段2',
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for book_instance
-- ----------------------------
DROP TABLE IF EXISTS `book_instance`;
CREATE TABLE `book_instance` (
    `book_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'ISBN书号',
    `instance_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '实体编码',
    `book_status` tinyint NOT NULL COMMENT '图书状态(1-在库 2-借出 3-遗失 4-损坏)',
    `location` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '存放位置',
    `borrow_id` bigint NULL DEFAULT NULL COMMENT '借阅记录ID',
    `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
    `update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
    `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '逻辑删除标识(1-已删除 0-未删除)',
    `note0` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段0',
    `note1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段1',
    `note2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段2',
    PRIMARY KEY (`instance_id`) USING BTREE
)

-- ----------------------------
-- Table structure for borrow_log
-- ----------------------------
DROP TABLE IF EXISTS `borrow_log`;
CREATE TABLE `borrow_log` (
    `borrow_id` bigint NOT NULL AUTO_INCREMENT COMMENT '借阅记录ID',
    `intance_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '实体编码',
    `user_id` int NOT NULL COMMENT '借阅人ID',
    `borrow_time` datetime NOT NULL COMMENT '借阅时间',
    `return_time` datetime NULL DEFAULT NULL COMMENT '归还时间',
    `is_completed` tinyint NOT NULL DEFAULT 0 COMMENT '是否归还(1-是 0-否)',
    `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '逻辑删除标识(1-已删除 0-未删除)',
    `note0` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段0',
    `note1` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段1',
    `note2` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '扩展字段2',
    PRIMARY KEY (`borrow_id`) USING BTREE
)

SET FOREIGN_KEY_CHECKS = 1;