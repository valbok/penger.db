DROP TABLE IF EXISTS user;
CREATE TABLE user (
  id int(11) NOT NULL auto_increment,
  email varchar(255) default NULL,
  password_hash varchar(255) default NULL,
  is_enabled int(11) NOT NULL default '1',
  created int(11) NOT NULL default '0',
  updated int(11) NOT NULL default '0',
  PRIMARY KEY (id),
  UNIQUE KEY user_email(email)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS transaction;
CREATE TABLE transaction (
  id int(11) NOT NULL auto_increment,
  date int(11) NOT NULL default '0',
  description varchar(255) default NULL,
  payment float NOT NULL default '0',
  user_id int(11) NOT NULL default '0',
  hash varchar(255) default NULL,
  PRIMARY KEY (id),
  KEY transaction_date(date),
  KEY transaction_user_id(user_id),
  KEY transaction_hash(hash)
) ENGINE=InnoDB;
