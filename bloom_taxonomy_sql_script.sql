CREATE DATABASE  IF NOT EXISTS `bloom_taxonomy` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bloom_taxonomy`;
-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: bloom_taxonomy
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bloom_keywords`
--

DROP TABLE IF EXISTS `bloom_keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bloom_keywords` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `keywords` varchar(20) DEFAULT NULL,
  `bloom_level` varchar(20) DEFAULT NULL,
  `order_level` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `refine_order_level` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=188 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bloom_keywords`
--

LOCK TABLES `bloom_keywords` WRITE;
/*!40000 ALTER TABLE `bloom_keywords` DISABLE KEYS */;
INSERT INTO `bloom_keywords` VALUES (1,'acquire','knowledge','LO','U','LOTS'),(2,'cite','knowledge','LO','U','LOTS'),(3,'count','knowledge','LO','U','LOTS'),(4,'define','knowledge','LO','U','LOTS'),(5,'draw','knowledge','LO','O','LOTS'),(6,'identify','knowledge','LO','U','LOTS'),(7,'indicate','knowledge','LO','U','LOTS'),(8,'label','knowledge','LO','U','LOTS'),(9,'list','knowledge','LO','U','LOTS'),(10,'name','knowledge','LO','U','LOTS'),(11,'point','knowledge','LO','U','LOTS'),(12,'quote','knowledge','LO','U','LOTS'),(13,'read','knowledge','LO','U','LOTS'),(14,'recall','knowledge','LO','U','LOTS'),(15,'recite','knowledge','LO','U','LOTS'),(16,'recognize','knowledge','LO','U','LOTS'),(17,'record','knowledge','LO','U','LOTS'),(18,'relate','knowledge','LO','O','LOTS'),(19,'repeat','knowledge','LO','U','LOTS'),(20,'reproduce','knowledge','LO','U','LOTS'),(21,'select','knowledge','LO','O','LOTS'),(22,'state','knowledge','LO','U','LOTS'),(23,'tabulate','knowledge','LO','U','LOTS'),(24,'tell','knowledge','LO','U','LOTS'),(25,'trace','knowledge','LO','U','LOTS'),(26,'write','knowledge','LO','O','LOTS'),(27,'associate','comprehension','LO','U','LOTS'),(28,'categorize','comprehension','LO','U','LOTS'),(29,'change','comprehension','LO','U','LOTS'),(30,'classify','comprehension','LO','U','LOTS'),(31,'compare','comprehension','LO','U','LOTS'),(32,'compute','comprehension','LO','U','LOTS'),(33,'contrast','comprehension','LO','U','LOTS'),(34,'convert','comprehension','LO','U','LOTS'),(35,'describe','comprehension','LO','U','LOTS'),(36,'differentiate','comprehension','LO','O','LOTS'),(37,'discuss','comprehension','LO','U','LOTS'),(38,'distinguish','comprehension','LO','O','LOTS'),(39,'draw','comprehension','LO','O','LOTS'),(40,'estimate','comprehension','LO','O','LOTS'),(41,'explain','comprehension','LO','U','LOTS'),(42,'express','comprehension','LO','U','LOTS'),(43,'extrapolate','comprehension','LO','O','LOTS'),(44,'illustrate','comprehension','LO','O','LOTS'),(45,'interpret','comprehension','LO','O','LOTS'),(46,'outline','comprehension','LO','U','LOTS'),(47,'paraphrase','comprehension','LO','U','LOTS'),(48,'predict','comprehension','LO','O','LOTS'),(49,'relate','comprehension','LO','O','LOTS'),(50,'rephrase','comprehension','LO','U','LOTS'),(51,'report','comprehension','LO','U','LOTS'),(52,'represent','comprehension','LO','U','LOTS'),(53,'restate','comprehension','LO','U','LOTS'),(54,'restructure','comprehension','LO','U','LOTS'),(55,'summarize','comprehension','LO','O','LOTS'),(56,'translate','comprehension','LO','O','LOTS'),(57,'apply','application','LO','U','MOTS'),(58,'calculate','application','LO','U','MOTS'),(59,'complete','application','LO','U','MOTS'),(60,'compute','application','LO','U','MOTS'),(61,'demonstrate','application','LO','U','MOTS'),(62,'determine','application','LO','O','MOTS'),(63,'dramatize','application','LO','U','MOTS'),(64,'employ','application','LO','U','MOTS'),(65,'estimate','application','LO','O','MOTS'),(66,'examine','application','LO','U','MOTS'),(67,'illustrate','application','LO','O','MOTS'),(68,'interpolate','application','LO','O','MOTS'),(69,'interpret','application','LO','O','MOTS'),(70,'locate','application','LO','U','MOTS'),(71,'operate','application','LO','U','MOTS'),(72,'order','application','LO','U','MOTS'),(73,'practice','application','LO','U','MOTS'),(74,'predict','application','LO','O','MOTS'),(75,'relate','application','LO','O','MOTS'),(76,'report','application','LO','U','MOTS'),(77,'restate','application','LO','U','MOTS'),(78,'review','application','LO','U','MOTS'),(79,'schedule','application','LO','U','MOTS'),(80,'sketch','application','LO','U','MOTS'),(81,'solve','application','LO','U','MOTS'),(82,'prepare','application','LO','U','MOTS'),(83,'transfer','application','LO','U','MOTS'),(84,'transform','application','LO','U','MOTS'),(85,'translate','application','LO','U','MOTS'),(86,'use','application','LO','U','MOTS'),(87,'utilize','application','LO','U','MOTS'),(88,'analyze','analysis','HO','U','MOTS'),(89,'appraise','analysis','HO','O','MOTS'),(90,'contract','analysis','HO','U','MOTS'),(91,'criticize','analysis','HO','U','MOTS'),(92,'debate','analysis','HO','U','MOTS'),(93,'deduce','analysis','HO','U','MOTS'),(94,'detect','analysis','HO','U','MOTS'),(95,'diagram','analysis','HO','U','MOTS'),(96,'differentiate','analysis','HO','O','MOTS'),(97,'discriminate','analysis','HO','U','MOTS'),(98,'distinguish','analysis','HO','O','MOTS'),(99,'experiment','analysis','HO','U','MOTS'),(100,'extend','analysis','HO','U','MOTS'),(101,'extrapolate','analysis','HO','O','MOTS'),(102,'generalize','analysis','HO','U','MOTS'),(103,'infer','analysis','HO','U','MOTS'),(104,'inspect','analysis','HO','U','MOTS'),(105,'interpolate','analysis','HO','O','MOTS'),(107,'point out','analysis','HO','U','MOTS'),(108,'predict','analysis','HO','O','MOTS'),(109,'question','analysis','HO','U','MOTS'),(110,'rearrange','analysis','HO','U','MOTS'),(111,'reorder','analysis','HO','U','MOTS'),(112,'separate','analysis','HO','U','MOTS'),(113,'summarize','analysis','HO','O','MOTS'),(114,'arrange','synthesis','HO','U','HOTS'),(115,'assemble','synthesis','HO','U','HOTS'),(116,'collect','synthesis','HO','U','HOTS'),(117,'combine','synthesis','HO','U','HOTS'),(118,'compose','synthesis','HO','U','HOTS'),(119,'constitute','synthesis','HO','U','HOTS'),(120,'construct','synthesis','HO','U','HOTS'),(121,'create','synthesis','HO','U','HOTS'),(122,'derive','synthesis','HO','U','HOTS'),(123,'design','synthesis','HO','U','HOTS'),(124,'develop','synthesis','HO','U','HOTS'),(125,'devise','synthesis','HO','U','HOTS'),(126,'document','synthesis','HO','U','HOTS'),(127,'formulate','synthesis','HO','U','HOTS'),(128,'integrate','synthesis','HO','U','HOTS'),(129,'manage','synthesis','HO','U','HOTS'),(130,'modify','synthesis','HO','U','HOTS'),(131,'originate','synthesis','HO','U','HOTS'),(132,'organize','synthesis','HO','U','HOTS'),(133,'plan','synthesis','HO','U','HOTS'),(134,'prepare','synthesis','HO','U','HOTS'),(135,'prescribe','synthesis','HO','U','HOTS'),(136,'produce','synthesis','HO','U','HOTS'),(137,'propose','synthesis','HO','U','HOTS'),(138,'reorganize','synthesis','HO','U','HOTS'),(139,'revise','synthesis','HO','O','HOTS'),(140,'rewrite','synthesis','HO','U','HOTS'),(141,'specify','synthesis','HO','U','HOTS'),(142,'synthesize','synthesis','HO','U','HOTS'),(143,'transmit','synthesis','HO','U','HOTS'),(144,'write','synthesis','HO','O','HOTS'),(145,'appraise','evaluation','HO','O','HOTS'),(146,'argue','evaluation','HO','U','HOTS'),(147,'assess','evaluation','HO','U','HOTS'),(148,'choose','evaluation','HO','U','HOTS'),(149,'conclude','evaluation','HO','U','HOTS'),(150,'critique','evaluation','HO','U','HOTS'),(151,'decide','evaluation','HO','U','HOTS'),(152,'determine','evaluation','HO','O','HOTS'),(153,'estimate','evaluation','HO','O','HOTS'),(154,'evaluate','evaluation','HO','U','HOTS'),(155,'grade','evaluation','HO','U','HOTS'),(156,'judge','evaluation','HO','U','HOTS'),(157,'measure','evaluation','HO','U','HOTS'),(158,'rank','evaluation','HO','U','HOTS'),(159,'rate','evaluation','HO','U','HOTS'),(160,'recommend','evaluation','HO','U','HOTS'),(161,'revise','evaluation','HO','O','HOTS'),(162,'score','evaluation','HO','U','HOTS'),(163,'select ','evaluation','HO','O','HOTS'),(164,'standardize','evaluation','HO','U','HOTS'),(165,'test','evaluation','HO','U','HOTS'),(166,'validate','evaluation','HO','U','HOTS'),(167,'weigh','evaluation','HO','U','HOTS'),(168,'defend','evaluation','HO','U','HOTS'),(169,'generate','synthesis','HO','U','HOTS'),(170,'suggest','synthesis','HO','U','HOTS'),(171,'give','comprehension','LO','U','LOTS'),(172,'provide','comprehension','LO','U','LOTS'),(173,'advise','synthesis','HO','U','HOTS'),(174,'justify','evaluation','HO','U','HOTS'),(175,'elaborate','comprehension','LO','U','LOTS'),(176,'show','application','HO','U','MOTS'),(177,'comment','evaluation','HO','U','HOTS'),(178,'simplify','comprehension','LO','U','LOTS'),(179,'prove','evaluation','HO','U','HOTS'),(180,'discover','synthesis','HO','U','HOTS'),(181,'fill','knowledge','LO','U','LOTS'),(182,'highlight','comprehension','LO','U','LOTS'),(183,'implement','application','LO','U','MOTS'),(184,'find','comprehension','LO','U','LOTS'),(185,'deploy','application','LO','U','MOTS'),(186,'speculate','synthesis','HO','U','HOTS'),(187,'describe','knowledge','LO','O','LOTS');
/*!40000 ALTER TABLE `bloom_keywords` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-23 10:52:02
