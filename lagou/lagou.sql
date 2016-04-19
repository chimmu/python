/*
Navicat MySQL Data Transfer

Source Server         : lagou
Source Server Version : 50613
Source Host           : localhost:3306
Source Database       : lagou

Target Server Type    : MYSQL
Target Server Version : 50613
File Encoding         : 65001

Date: 2016-04-19 22:03:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for job
-- ----------------------------
DROP TABLE IF EXISTS `job`;
CREATE TABLE `job` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `job_name` varchar(32) DEFAULT NULL,
  `job_type` int(11) DEFAULT NULL COMMENT '0-后端 1-前端',
  `job_first_type` int(11) NOT NULL COMMENT '0-技术 ',
  `education` varchar(16) NOT NULL COMMENT '０－本科　１－硕士　２－博士　３－大专　４－不限　５－其它',
  `company_id` int(11) NOT NULL,
  `company_full_name` varchar(128) DEFAULT NULL,
  `company_short_name` varchar(32) DEFAULT NULL,
  `company_labels` varchar(255) DEFAULT NULL,
  `boss_name` varchar(32) DEFAULT NULL,
  `industry_field` varchar(64) DEFAULT NULL,
  `finance_stage` varchar(32) DEFAULT NULL,
  `work_year_low` int(11) NOT NULL DEFAULT '-1' COMMENT '－１－表示不限',
  `work_year_high` int(11) NOT NULL DEFAULT '-1',
  `salary_low` int(11) NOT NULL DEFAULT '-1' COMMENT '工作年限',
  `salary_high` int(11) NOT NULL DEFAULT '-1',
  `staffs_low` int(11) NOT NULL DEFAULT '-1',
  `staffs_high` int(11) NOT NULL DEFAULT '-1' COMMENT '员工数',
  `job_nature` varchar(16) DEFAULT NULL COMMENT '全职兼职',
  `city` varchar(16) DEFAULT NULL,
  `plus` int(11) NOT NULL DEFAULT '0' COMMENT '是否开启plus',
  `create_time` datetime DEFAULT NULL,
  `advantage` varchar(255) DEFAULT NULL COMMENT '职位优势',
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1732298 DEFAULT CHARSET=utf8;
