/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cinema` (
  `cinemaId` int(11) NOT NULL,
  `cinemaName` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mailingAddress` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`cinemaId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movie` (
  `movieId` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `releaseYear` int(11) DEFAULT NULL,
  `rating` enum('G','PG','M','MA15+','R18+') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`movieId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `moviesShown` (
  `movieId` int(11) NOT NULL,
  `screenId` int(11) NOT NULL,
  PRIMARY KEY (`movieId`,`screenId`),
  KEY `screenId` (`screenId`),
  CONSTRAINT `moviesShown_ibfk_1` FOREIGN KEY (`movieId`) REFERENCES `movie` (`movieId`),
  CONSTRAINT `moviesShown_ibfk_2` FOREIGN KEY (`screenId`) REFERENCES `screen` (`screenId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projector` (
  `serialNo` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `screenId` int(11) DEFAULT NULL,
  `projectorType` enum('16 mm','35 mm','2D','3D') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `modelNumber` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `resolution` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `usedHours` float DEFAULT NULL,
  PRIMARY KEY (`serialNo`),
  KEY `screenId` (`screenId`),
  CONSTRAINT `projector_ibfk_1` FOREIGN KEY (`screenId`) REFERENCES `screen` (`screenId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screen` (
  `screenId` int(11) NOT NULL,
  `cinemaId` int(11) DEFAULT NULL,
  `size` float DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `goldclass` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`screenId`),
  KEY `cinemaId` (`cinemaId`),
  CONSTRAINT `screen_ibfk_1` FOREIGN KEY (`cinemaId`) REFERENCES `cinema` (`cinemaId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
