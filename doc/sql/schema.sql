DROP TABLE IF EXISTS transaction;
CREATE TABLE transaction (
  id int(11) NOT NULL auto_increment,
  date int(11) NOT NULL default '0',
  description varchar(255) default NULL,
  debit float NOT NULL default '0',
  credit float NOT NULL default '0',
  PRIMARY KEY (id),
  KEY transaction_date(date)
) ENGINE=InnoDB;
