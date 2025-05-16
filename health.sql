/*
 Navicat Premium Data Transfer

 Source Server         : mydatabase
 Source Server Type    : MySQL
 Source Server Version : 50717 (5.7.17-log)
 Source Host           : localhost:3306
 Source Schema         : health

 Target Server Type    : MySQL
 Target Server Version : 50717 (5.7.17-log)
 File Encoding         : 65001

 Date: 12/05/2025 21:41:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 37 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add user profile', 7, 'add_userprofile');
INSERT INTO `auth_permission` VALUES (26, 'Can change user profile', 7, 'change_userprofile');
INSERT INTO `auth_permission` VALUES (27, 'Can delete user profile', 7, 'delete_userprofile');
INSERT INTO `auth_permission` VALUES (28, 'Can view user profile', 7, 'view_userprofile');
INSERT INTO `auth_permission` VALUES (29, 'Can add user info', 8, 'add_userinfo');
INSERT INTO `auth_permission` VALUES (30, 'Can change user info', 8, 'change_userinfo');
INSERT INTO `auth_permission` VALUES (31, 'Can delete user info', 8, 'delete_userinfo');
INSERT INTO `auth_permission` VALUES (32, 'Can view user info', 8, 'view_userinfo');
INSERT INTO `auth_permission` VALUES (33, 'Can add user basic info', 9, 'add_userbasicinfo');
INSERT INTO `auth_permission` VALUES (34, 'Can change user basic info', 9, 'change_userbasicinfo');
INSERT INTO `auth_permission` VALUES (35, 'Can delete user basic info', 9, 'delete_userbasicinfo');
INSERT INTO `auth_permission` VALUES (36, 'Can view user basic info', 9, 'view_userbasicinfo');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (9, 'UserApp', 'userbasicinfo');
INSERT INTO `django_content_type` VALUES (8, 'UserApp', 'userinfo');
INSERT INTO `django_content_type` VALUES (7, 'UserApp', 'userprofile');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-04-19 08:03:07.831587');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2025-04-19 08:03:08.167323');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2025-04-19 08:03:08.248294');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2025-04-19 08:03:08.256243');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2025-04-19 08:03:08.264717');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2025-04-19 08:03:08.324561');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2025-04-19 08:03:08.357762');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2025-04-19 08:03:08.389797');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2025-04-19 08:03:08.398457');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2025-04-19 08:03:08.427339');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2025-04-19 08:03:08.430340');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2025-04-19 08:03:08.436854');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2025-04-19 08:03:08.476055');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2025-04-19 08:03:08.540482');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2025-04-19 08:03:08.578144');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2025-04-19 08:03:08.586681');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2025-04-19 08:03:08.623204');
INSERT INTO `django_migrations` VALUES (18, 'sessions', '0001_initial', '2025-04-19 08:03:08.651646');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('sct6raf4ia9na9847jakxv33t3xtty5h', 'eyJ1c2VyX2lkIjoxMDAwMH0:1uDw4P:I2uyO1VymeUbHrZYbU18DNc6CKG6ZnFWzdk55iWjjqI', '2025-05-25 02:05:37.364489');
INSERT INTO `django_session` VALUES ('y4rcluifppd6pifddvlsl7417x5t2q8h', 'eyJ1c2VyX2lkIjoxMDAwMH0:1u7wuQ:lsN6LjLxY3tRCLl6p_O1WKhgS0ketLG3nc0eSy-ObRk', '2025-05-08 13:46:34.418779');

-- ----------------------------
-- Table structure for user_basic_info
-- ----------------------------
DROP TABLE IF EXISTS `user_basic_info`;
CREATE TABLE `user_basic_info`  (
  `uid` int(11) NOT NULL,
  `gender` char(1) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `weight` double NULL DEFAULT NULL,
  `height` double NULL DEFAULT NULL,
  `age` int(11) NULL DEFAULT NULL,
  `physical_activity` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`uid`) USING BTREE,
  CONSTRAINT `user_basic_info_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user_info` (`uid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_basic_info
-- ----------------------------
INSERT INTO `user_basic_info` VALUES (10000, 'M', 213, 231, 123, 1);

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info`  (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10010 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_info
-- ----------------------------
INSERT INTO `user_info` VALUES (10000, '任乐乐', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92');
INSERT INTO `user_info` VALUES (10009, 'Renlele', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92');

-- ----------------------------
-- Table structure for rni_chinese
-- ----------------------------
DROP TABLE IF EXISTS `rni_chinese`;
CREATE TABLE `rni_chinese`  (
  `人群` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `年龄小值` double NULL DEFAULT NULL,
  `年龄大值` double NULL DEFAULT NULL,
  `性别` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `体重-kg` double NULL DEFAULT NULL,
  `活动水平` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `能量-千卡` bigint NULL DEFAULT NULL,
  `蛋白质-克` bigint NULL DEFAULT NULL,
  `脂肪-克` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `碳水化合物-克` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `钙-毫克` bigint NULL DEFAULT NULL,
  `磷-毫克` bigint NULL DEFAULT NULL,
  `钾-毫克` bigint NULL DEFAULT NULL,
  `钠-毫克` bigint NULL DEFAULT NULL,
  `镁-毫克` bigint NULL DEFAULT NULL,
  `铁-毫克` double NULL DEFAULT NULL,
  `锌-毫克` double NULL DEFAULT NULL,
  `硒-微克` bigint NULL DEFAULT NULL,
  `碘-微克` bigint NULL DEFAULT NULL,
  `铜-毫克` double NULL DEFAULT NULL,
  `氟-毫克` double NULL DEFAULT NULL,
  `铬-微克` bigint NULL DEFAULT NULL,
  `锰-毫克` double NULL DEFAULT NULL,
  `钼-微克` bigint NULL DEFAULT NULL,
  `维生素A-微克` bigint NULL DEFAULT NULL,
  `维生素C-毫克` bigint NULL DEFAULT NULL,
  `维生素D-微克` bigint NULL DEFAULT NULL,
  `维生素E-毫克` bigint NULL DEFAULT NULL,
  `维生素K-微克` bigint NULL DEFAULT NULL,
  `维生素B1-毫克` double NULL DEFAULT NULL,
  `维生素B2-毫克` double NULL DEFAULT NULL,
  `维生素B6-毫克` double NULL DEFAULT NULL,
  `维生素B12-微克` double NULL DEFAULT NULL,
  `泛酸-毫克` double NULL DEFAULT NULL,
  `叶酸-微克` bigint NULL DEFAULT NULL,
  `烟酸-毫克` bigint NULL DEFAULT NULL,
  `生物素-微克` bigint NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rni_chinese
-- ----------------------------
INSERT INTO `rni_chinese` VALUES ('婴儿', 0, 0.5, '男', 6.7, '-', 900, 20, '45', '0', 300, 150, 500, 200, 30, 0.3, 1.5, 15, 50, 0.4, 0.1, 10, 3.5, 2, 400, 40, 10, 3, 12, 0.2, 1.4, 0.1, 0.4, 1.7, 65, 2, 5);
INSERT INTO `rni_chinese` VALUES ('婴儿', 0, 0.5, '女', 6.2, '-', 850, 20, '43', '0', 300, 150, 500, 200, 30, 0.3, 1.5, 15, 50, 0.4, 0.1, 10, 3.5, 2, 400, 40, 10, 3, 12, 0.2, 1.4, 0.1, 0.4, 1.7, 65, 2, 5);
INSERT INTO `rni_chinese` VALUES ('婴儿', 0.5, 1, '男', 9, '-', 1000, 30, '33-44', '127-163', 400, 300, 700, 500, 70, 10, 8, 20, 50, 0.6, 0.4, 15, 3.5, 3, 400, 50, 10, 3, 18, 0.3, 0.5, 0.3, 0.5, 1.8, 80, 3, 6);
INSERT INTO `rni_chinese` VALUES ('婴儿', 0.5, 1, '女', 8.4, '-', 950, 30, '32-42', '121-154', 400, 300, 700, 500, 70, 10, 8, 20, 50, 0.6, 0.4, 15, 3.5, 3, 400, 50, 10, 3, 17, 0.3, 0.5, 0.3, 0.5, 1.8, 80, 3, 6);
INSERT INTO `rni_chinese` VALUES ('幼儿', 1, 2, '男', 9.9, '-', 1100, 35, '31-37', '140-179', 600, 450, 1000, 650, 100, 12, 9, 20, 50, 0.8, 0.6, 20, 3.5, 15, 500, 60, 10, 4, 20, 0.6, 0.6, 0.5, 0.9, 2, 150, 6, 8);
INSERT INTO `rni_chinese` VALUES ('幼儿', 1, 2, '女', 9.2, '-', 1050, 35, '29-35', '134-171', 600, 450, 1000, 650, 100, 12, 9, 20, 50, 0.8, 0.6, 20, 3.5, 15, 500, 60, 10, 4, 20, 0.6, 0.6, 0.5, 0.9, 2, 150, 6, 8);
INSERT INTO `rni_chinese` VALUES ('幼儿', 2, 3, '男', 12.2, '-', 1200, 40, '33-40', '153-195', 600, 450, 1000, 650, 100, 12, 9, 20, 50, 0.8, 0.6, 20, 3.5, 15, 500, 60, 10, 160, 25, 0.6, 0.6, 0.5, 0.9, 2, 150, 6, 8);
INSERT INTO `rni_chinese` VALUES ('幼儿', 2, 3, '女', 11.7, '-', 1150, 40, '32-38', '146-187', 600, 450, 1000, 650, 100, 12, 9, 20, 50, 0.8, 0.6, 20, 3.5, 15, 500, 60, 10, 160, 25, 0.6, 0.6, 0.5, 0.9, 2, 150, 6, 8);
INSERT INTO `rni_chinese` VALUES ('幼儿', 3, 4, '男', 14, '-', 1350, 45, '38-45', '172-219', 600, 450, 1000, 650, 100, 12, 9, 20, 50, 0.8, 0.6, 20, 3.5, 15, 500, 60, 10, 160, 25, 0.6, 0.6, 0.5, 0.9, 2, 150, 6, 8);
INSERT INTO `rni_chinese` VALUES ('幼儿', 3, 4, '女', 13.4, '-', 1300, 45, '36-43', '165-211', 600, 450, 1000, 650, 100, 12, 9, 20, 50, 0.8, 0.6, 20, 3.5, 15, 500, 60, 10, 160, 25, 0.6, 0.6, 0.5, 0.9, 2, 150, 6, 8);
INSERT INTO `rni_chinese` VALUES ('学龄前', 4, 5, '男', 15.6, '-', 1450, 50, '40-48', '185-236', 800, 500, 1500, 900, 150, 12, 12, 25, 90, 1, 0.8, 30, 3.5, 20, 600, 70, 10, 5, 30, 0.7, 0.7, 0.6, 1.2, 3, 200, 7, 12);
INSERT INTO `rni_chinese` VALUES ('学龄前', 4, 5, '女', 15.2, '-', 1400, 45, '39-47', '178-228', 800, 500, 1500, 900, 150, 12, 12, 25, 90, 1, 0.8, 30, 3.5, 20, 600, 70, 10, 5, 30, 0.7, 0.7, 0.6, 1.2, 3, 200, 7, 12);
INSERT INTO `rni_chinese` VALUES ('学龄前', 5, 6, '男', 17.4, '-', 1600, 55, '44-53', '204-260', 800, 500, 1500, 900, 150, 12, 12, 25, 90, 1, 0.8, 30, 3.5, 20, 600, 70, 10, 5, 35, 0.7, 0.7, 0.6, 1.2, 3, 200, 7, 12);
INSERT INTO `rni_chinese` VALUES ('学龄前', 5, 6, '女', 16.8, '-', 1500, 50, '42-50', '191-244', 800, 500, 1500, 900, 150, 12, 12, 25, 90, 1, 0.8, 30, 3.5, 20, 600, 70, 10, 5, 35, 0.7, 0.7, 0.6, 1.2, 3, 200, 7, 12);
INSERT INTO `rni_chinese` VALUES ('学龄前', 6, 7, '男', 19.8, '-', 1700, 55, '47-57', '216-276', 800, 500, 1500, 900, 150, 12, 12, 25, 90, 1, 0.8, 30, 3.5, 20, 600, 70, 10, 5, 40, 0.7, 0.7, 0.6, 1.2, 3, 200, 7, 12);
INSERT INTO `rni_chinese` VALUES ('学龄前', 6, 7, '女', 19.1, '-', 1600, 55, '44-53', '204-260', 800, 500, 1500, 900, 150, 12, 12, 25, 90, 1, 0.8, 30, 3.5, 20, 600, 70, 10, 5, 40, 0.7, 0.7, 0.6, 1.2, 3, 200, 7, 12);
INSERT INTO `rni_chinese` VALUES ('学龄期', 7, 8, '男', 22, '-', 1800, 60, '50-60', '229-293', 800, 700, 1500, 1000, 250, 12, 13.5, 35, 90, 1.2, 1, 30, 3.5, 30, 700, 80, 10, 7, 45, 0.9, 1, 0.7, 1.2, 4, 200, 9, 16);
INSERT INTO `rni_chinese` VALUES ('学龄期', 7, 8, '女', 21, '-', 1700, 60, '47-57', '216-276', 800, 700, 1500, 1000, 250, 12, 13.5, 35, 90, 1.2, 1, 30, 3.5, 30, 700, 80, 10, 7, 45, 0.9, 1, 0.7, 1.2, 4, 200, 9, 16);
INSERT INTO `rni_chinese` VALUES ('学龄期', 8, 9, '男', 23.8, '-', 1900, 65, '53-63', '242-309', 800, 700, 1500, 1000, 250, 12, 13.5, 35, 90, 1.2, 1, 30, 3.5, 30, 700, 80, 10, 7, 50, 0.9, 1, 0.7, 1.2, 4, 200, 9, 16);
INSERT INTO `rni_chinese` VALUES ('学龄期', 8, 9, '女', 23.2, '-', 1800, 60, '50-60', '229-293', 800, 700, 1500, 1000, 250, 12, 13.5, 35, 90, 1.2, 1, 30, 3.5, 30, 700, 80, 10, 7, 50, 0.9, 1, 0.7, 1.2, 4, 200, 9, 16);
INSERT INTO `rni_chinese` VALUES ('学龄期', 9, 10, '男', 26.4, '-', 2000, 65, '56-67', '255-325', 800, 700, 1500, 1000, 250, 12, 13.5, 35, 90, 1.2, 1, 30, 3.5, 30, 700, 80, 10, 7, 55, 0.9, 1, 0.7, 1.2, 4, 200, 9, 16);
INSERT INTO `rni_chinese` VALUES ('学龄期', 9, 10, '女', 25.8, '-', 1900, 65, '53-63', '242-309', 800, 700, 1500, 1000, 250, 12, 13.5, 35, 90, 1.2, 1, 30, 3.5, 30, 700, 80, 10, 7, 55, 0.9, 1, 0.7, 1.2, 4, 200, 9, 16);
INSERT INTO `rni_chinese` VALUES ('学龄期', 10, 11, '男', 28.8, '-', 2100, 70, '58-70', '267-341', 800, 700, 1500, 1000, 250, 12, 13.5, 35, 90, 1.2, 1, 30, 3.5, 30, 700, 80, 10, 7, 60, 0.9, 1, 0.7, 1.2, 4, 200, 9, 16);
INSERT INTO `rni_chinese` VALUES ('学龄期', 10, 11, '女', 28.8, '-', 2000, 65, '56-67', '255-325', 800, 700, 1500, 1000, 250, 12, 13.5, 35, 90, 1.2, 1, 30, 3.5, 30, 700, 80, 10, 7, 60, 0.9, 1, 0.7, 1.2, 4, 200, 9, 16);
INSERT INTO `rni_chinese` VALUES ('青春期', 11, 12, '男', 32.1, '-', 2200, 70, '61-73', '281-356', 1000, 1000, 1500, 1200, 350, 16, 18, 45, 120, 1.8, 1.2, 40, 3.5, 50, 700, 90, 5, 10, 65, 1.2, 1.2, 0.9, 2.4, 5, 300, 12, 20);
INSERT INTO `rni_chinese` VALUES ('青春期', 11, 12, '女', 32.7, '-', 2100, 70, '58-70', '268-340', 1000, 1000, 1500, 1200, 350, 16, 18, 45, 120, 1.8, 1.2, 40, 3.5, 50, 700, 90, 5, 10, 65, 1.2, 1.2, 0.9, 2.4, 5, 300, 12, 20);
INSERT INTO `rni_chinese` VALUES ('青春期', 12, 13, '男', 35.5, '-', 2300, 75, '64-77', '294-372', 1000, 1000, 1500, 1200, 350, 16, 18, 45, 120, 1.8, 1.2, 40, 3.5, 50, 700, 90, 5, 10, 70, 1.2, 1.2, 0.9, 2.4, 5, 300, 12, 20);
INSERT INTO `rni_chinese` VALUES ('青春期', 12, 13, '女', 37.2, '-', 2200, 75, '61-73', '281-356', 1000, 1000, 1500, 1200, 350, 16, 18, 45, 120, 1.8, 1.2, 40, 3.5, 50, 700, 90, 5, 10, 70, 1.2, 1.2, 0.9, 2.4, 5, 300, 12, 20);
INSERT INTO `rni_chinese` VALUES ('青春期', 13, 16, '男', 42, '-', 2400, 80, '67-80', '307-388', 1000, 1000, 2000, 1800, 350, 20, 18, 50, 150, 2, 1.4, 40, 3.5, 50, 800, 100, 5, 14, 80, 1.5, 1.5, 1, 1.8, 5, 400, 15, 25);
INSERT INTO `rni_chinese` VALUES ('青春期', 13, 16, '女', 42.4, '-', 2300, 80, '64-77', '294-372', 1000, 1000, 2000, 1800, 350, 25, 18, 50, 150, 2, 1.4, 40, 3.5, 50, 700, 100, 5, 14, 80, 1.2, 1.2, 1.1, 1.8, 5, 400, 12, 25);
INSERT INTO `rni_chinese` VALUES ('青春期', 16, 18, '男', 54.2, '-', 2800, 90, '78-93', '358-453', 1000, 1000, 2000, 1800, 350, 20, 18, 50, 150, 2, 1.4, 40, 3.5, 50, 800, 100, 5, 14, 100, 1.5, 1.5, 1.2, 1.8, 5, 400, 15, 25);
INSERT INTO `rni_chinese` VALUES ('青春期', 16, 18, '女', 48.3, '-', 2400, 80, '67-80', '307-388', 1000, 1000, 2000, 1800, 350, 25, 18, 50, 150, 2, 1.4, 40, 3.5, 50, 700, 100, 5, 14, 100, 1.2, 1.2, 1.1, 1.8, 5, 400, 12, 25);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '男', 63, '极轻', 2400, 70, '53-67', '380-391', 800, 700, 2000, 2200, 350, 15, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '女', 53, '极轻', 2100, 65, '47-58', '332-342', 800, 700, 2000, 2200, 350, 15, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '男', 63, '轻', 2600, 80, '58-72', '411-424', 800, 700, 2000, 2200, 350, 15, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '女', 53, '轻', 2300, 80, '51-64', '364-375', 800, 700, 2000, 2200, 350, 20, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 5, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '男', 63, '中', 3000, 90, '67-83', '475-489', 800, 700, 2000, 2200, 350, 15, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '女', 53, '中', 2700, 90, '60-75', '427-440', 800, 700, 2000, 2200, 350, 20, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 5, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '男', 63, '重', 3400, 100, '76-94', '538-554', 800, 700, 2000, 2200, 350, 15, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '女', 53, '重', 3000, 100, '67-83', '475-489', 800, 700, 2000, 2200, 350, 20, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 5, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '男', 63, '极重', 4000, 110, '89-111', '633-652', 800, 700, 2000, 2200, 350, 20, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 5, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('成人', 18, 45, '女', 53, '极重', 3500, 110, '78-97', '554-571', 800, 700, 2000, 2200, 350, 20, 15.5, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 5, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 45, 50, '男', 63, '极轻', 2200, 70, '49-61', '361-384', 800, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 45, 50, '女', 53, '极轻', 1900, 65, '42-53', '312-332', 800, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 45, 50, '男', 63, '轻', 2400, 75, '53-67', '394-419', 800, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 45, 50, '女', 53, '轻', 2100, 70, '47-58', '344-366', 800, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 5, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 45, 50, '男', 63, '中', 2700, 80, '60-75', '443-471', 800, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 45, 50, '女', 53, '中', 2400, 75, '53-67', '394-419', 800, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 5, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 45, 50, '男', 63, '重', 3000, 90, '67-83', '492-524', 800, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 5, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 45, 50, '女', 53, '重', 2700, 85, '60-75', '443-471', 800, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 5, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 50, 60, '男', 63, '轻', 2300, 75, '51-77', '377-401', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 10, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 50, 60, '女', 53, '轻', 1900, 70, '42-63', '312-332', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 10, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 50, 60, '男', 63, '中', 2600, 80, '58-87', '426-454', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 10, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 50, 60, '女', 53, '中', 2000, 75, '44-67', '328-349', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 10, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 50, 60, '男', 63, '重', 3100, 90, '69-103', '508-541', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 10, 14, 120, 1.4, 1.4, 1.2, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年前期', 50, 60, '女', 53, '重', 2200, 80, '49-73', '361-384', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 10, 14, 120, 1.3, 1.2, 1.2, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 60, 70, '男', 63, '极轻', 2000, 70, '44-56', '328-349', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 10, 14, 120, 1.4, 1.4, 1.5, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 60, 70, '女', 53, '极轻', 1700, 60, '38-47', '279-297', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 10, 14, 120, 1.3, 1.2, 1.5, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 60, 70, '男', 63, '轻', 2200, 75, '49-61', '361-384', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 10, 14, 120, 1.4, 1.4, 1.5, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 60, 70, '女', 53, '轻', 1900, 65, '42-53', '312-332', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 10, 14, 120, 1.3, 1.2, 1.5, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 60, 70, '男', 63, '中', 2500, 80, '56-69', '410-436', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 10, 14, 120, 1.4, 1.4, 1.5, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 60, 70, '女', 53, '中', 2100, 70, '47-58', '344-366', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 10, 14, 120, 1.3, 1.2, 1.5, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 70, 80, '男', 63, '极轻', 1800, 65, '40-50', '295-314', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 10, 14, 120, 1.4, 1.4, 1.5, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 70, 80, '女', 53, '极轻', 1600, 55, '36-44', '262-279', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 10, 14, 120, 1.3, 1.2, 1.5, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 70, 80, '男', 63, '轻', 2000, 70, '44-56', '328-349', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 10, 14, 120, 1.4, 1.4, 1.5, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 70, 80, '女', 53, '轻', 1800, 60, '40-50', '295-314', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 10, 14, 120, 1.3, 1.2, 1.5, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 80, 200, '男', 63, '-', 1600, 60, '36-44', '262-279', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 800, 100, 10, 14, 120, 1.4, 1.4, 1.5, 2.4, 5, 400, 14, 30);
INSERT INTO `rni_chinese` VALUES ('老年', 80, 200, '女', 53, '-', 1400, 55, '31-39', '230-244', 1000, 700, 2000, 2200, 350, 15, 15, 50, 150, 2, 1.5, 50, 3.5, 60, 700, 100, 10, 14, 120, 1.3, 1.2, 1.5, 2.4, 5, 400, 13, 30);
INSERT INTO `rni_chinese` VALUES ('孕早期', 15, 200, '女', 53, '-', 2900, 95, '64-81', '459-473', 1000, 700, 2500, 2200, 400, 25, 16.5, 50, 200, 2, 1.5, 50, 3.5, 60, 800, 130, 10, 14, 120, 1.5, 1.7, 1.9, 2.6, 6, 600, 15, 30);
INSERT INTO `rni_chinese` VALUES ('孕中期', 15, 200, '女', 53, '-', 3200, 105, '71-89', '506-522', 1200, 700, 2500, 2200, 400, 35, 16.5, 65, 200, 2, 1.5, 50, 3.5, 60, 900, 130, 10, 14, 120, 1.5, 1.7, 1.9, 2.6, 6, 600, 15, 30);
INSERT INTO `rni_chinese` VALUES ('哺乳期', 15, 200, '女', 53, '-', 3500, 105, '78-97', '554-571', 1200, 700, 2500, 2200, 400, 25, 21.5, 65, 200, 2, 1.5, 50, 3.5, 60, 1200, 130, 10, 14, 120, 1.8, 1.7, 1.9, 2.8, 7, 500, 18, 35);

SET FOREIGN_KEY_CHECKS = 1;
