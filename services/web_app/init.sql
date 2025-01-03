-- MySQL dump 10.13  Distrib 8.0.33, for macos13 (arm64)
--
-- Host: localhost    Database: ds_project
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) DEFAULT NULL,
  `sur_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `hashed_password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,NULL,'John Doe','johndoe@example.com','fakehashedsecret'),(2,NULL,'John Doe','johndoe@example.com','fakehashedsecret'),(3,NULL,'Alice Wonderson','alice@example.com','fakehashedsecret2'),(4,'Phu','Mac','macphu@gmail.com','$2b$12$Ix3yEWDXh1GLHh9NwkUwhuzPXov8bd5Sbqo0LuCEAefjF4AvWo8UO'),(5,'Phu','Mac','macphu@outlook.com','$2b$12$lLW1l62otmHQCGtacE4Z4eIOGJuz53ILlu3cTT.BM1Si6GngVUtua'),(6,'Test','1','testing1@gmail.com','$2b$12$Eats58aGyMs8dAsTXYx6aO0yXcB/Pjkifs7r6JF3Ps7v9Ir8FLGyu'),(7,'Testing','Two','testing2@gmail.com','$2b$12$EvQDCr/2cr8wstJKGt0joetTpghvgGCF04b09N1L00EWwd2FyF.rO'),(8,'Testing','Two','testing3@gmail.com','$2b$12$5EvRWSe5cTHtj5SN4Gp1X.JJjjS5okexEMKY/wFA0X2QDd5vIMWHm'),(9,'fwef','fjkernfj','testing4@gmail.com','$2b$12$c1gSDnDxSoxdKxhUtC8VH.usGq6Vqgym796GI.8jbQCc.lJ.0YldS');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'ds_project'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-13 23:11:51
