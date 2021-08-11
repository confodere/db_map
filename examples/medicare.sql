/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `allergy` (
  `allergyName` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `medication` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dosageTypical` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `medicareNo` int(11) NOT NULL,
  `positionNo` int(11) NOT NULL,
  PRIMARY KEY (`medicareNo`,`positionNo`,`allergyName`),
  CONSTRAINT `allergy_ibfk_1` FOREIGN KEY (`medicareNo`, `positionNo`) REFERENCES `patient` (`medicareNo`, `positionNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `doctor` (
  `MPN` int(11) NOT NULL,
  `title` enum('Dr','Mr','Mrs','Ms','Prof') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fName` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lName` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `streetNo` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `streetName` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `postcode` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phoneNo` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`MPN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `emergencyContact` (
  `emergencyId` int(11) NOT NULL AUTO_INCREMENT,
  `contactName` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `workNo` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `homeNo` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobileNo` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `streetNo` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `streetName` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `postCode` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`emergencyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jab` (
  `medicareNo` int(11) NOT NULL,
  `positionNo` int(11) NOT NULL,
  `vaccineName` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `batchNo` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `MPN` int(11) NOT NULL,
  `jabDate` date DEFAULT NULL,
  PRIMARY KEY (`medicareNo`,`positionNo`,`vaccineName`,`batchNo`,`MPN`),
  KEY `batchNo` (`batchNo`,`vaccineName`),
  KEY `MPN` (`MPN`),
  CONSTRAINT `jab_ibfk_1` FOREIGN KEY (`medicareNo`, `positionNo`) REFERENCES `patient` (`medicareNo`, `positionNo`),
  CONSTRAINT `jab_ibfk_2` FOREIGN KEY (`batchNo`, `vaccineName`) REFERENCES `vaccineBatch` (`batchNo`, `vaccineName`),
  CONSTRAINT `jab_ibfk_3` FOREIGN KEY (`MPN`) REFERENCES `doctor` (`MPN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicareCard` (
  `medicareNo` int(11) NOT NULL,
  `email` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `validTo` date DEFAULT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `streetNo` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `streetName` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `postcode` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`medicareNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient` (
  `positionNo` int(11) NOT NULL,
  `medicareNo` int(11) NOT NULL,
  `fName` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lName` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `emergencyId` int(11) DEFAULT NULL,
  PRIMARY KEY (`positionNo`,`medicareNo`),
  KEY `medicareNo` (`medicareNo`),
  KEY `emergencyId` (`emergencyId`),
  CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`medicareNo`) REFERENCES `medicareCard` (`medicareNo`),
  CONSTRAINT `patient_ibfk_2` FOREIGN KEY (`emergencyId`) REFERENCES `emergencyContact` (`emergencyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reaction` (
  `reactionId` int(11) NOT NULL AUTO_INCREMENT,
  `reactionDate` date DEFAULT NULL,
  `gravity` enum('Strong','Moderate','Weak') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dosageGiven` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `medication` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `allergyName` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `medicareNo` int(11) DEFAULT NULL,
  `positionNo` int(11) DEFAULT NULL,
  PRIMARY KEY (`reactionId`),
  KEY `medicareNo` (`medicareNo`,`positionNo`,`allergyName`),
  CONSTRAINT `reaction_ibfk_1` FOREIGN KEY (`medicareNo`, `positionNo`, `allergyName`) REFERENCES `allergy` (`medicareNo`, `positionNo`, `allergyName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vaccine` (
  `vaccineType` enum('mandatory','optional') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vaccineName` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`vaccineName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vaccineBatch` (
  `batchNo` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `manufactureDate` date DEFAULT NULL,
  `expiry` date DEFAULT NULL,
  `vaccineName` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`batchNo`,`vaccineName`),
  KEY `vaccineName` (`vaccineName`),
  CONSTRAINT `vaccineBatch_ibfk_1` FOREIGN KEY (`vaccineName`) REFERENCES `vaccine` (`vaccineName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
