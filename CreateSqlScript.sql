CREATE TABLE `mails` (
  `Id` varchar(30) NOT NULL,
  `gmail_id` varchar(255) NOT NULL,
  `ReceptionDate` varchar(255) NOT NULL,
  `To` varchar(255) NOT NULL,
  `Subject` varchar(255) NOT NULL,
  `CreateDate` datetime NOT NULL,
  `UpdateDate` datetime NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `gmail_id` (`gmail_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
