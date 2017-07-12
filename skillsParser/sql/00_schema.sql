
SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';


DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NOT NULL,
  `email` varchar(100) NOT NULL UNIQUE ,
  `discord` varchar(100),
  `skills_details` text,
  `availability` text,
  `coder` BOOLEAN,
  `previous_experience` BOOLEAN,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




DROP TABLE IF EXISTS `user_categories`;
CREATE TABLE user_categories
(
    user_id INT(10) unsigned,
    user_category varchar(200),
    PRIMARY KEY (user_id, user_category),
    CONSTRAINT user_categories_users_user_id_fk FOREIGN KEY (user_id) REFERENCES
    users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `user_programming_languages`;
CREATE TABLE user_programming_languages
(
    user_id INT(10) unsigned,
    user_language varchar(200),
    skillset int(10),
    description TEXT,
    PRIMARY KEY (user_id, user_language),
    CONSTRAINT user_programming_languages_users_user_id_fk FOREIGN KEY (user_id) REFERENCES
    users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


