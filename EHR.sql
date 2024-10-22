CREATE DATABASE IF NOT EXISTS `EHR` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use EHR;
CREATE TABLE IF NOT EXISTS `patientsdata` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(255) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phoneno` varchar(255) NOT NULL,   
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `record` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`recordid` varchar(255) NOT NULL,
  	`pname` varchar(255) NOT NULL,
  	`address` varchar(100) NOT NULL,
    `insurenceid` varchar(255) NOT NULL, 
    `phone` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `bookdata` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(255) NOT NULL,
  	`age` int(255) NOT NULL,
  	`temperature` varchar(255) NOT NULL,  
    `time` varchar(255) NOT NULL,
    `pat_id` varchar(255),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `doctor` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(255) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    `phoneno` varchar(255) NOT NULL,   
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

select * from bookdata;
