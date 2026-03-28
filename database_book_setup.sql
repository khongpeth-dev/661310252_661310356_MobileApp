/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.2.2-MariaDB, for osx10.21 (arm64)
--
-- Host: localhost    Database: library_final_project
-- ------------------------------------------------------
-- Server version	12.2.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` varchar(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  `shelf_location` varchar(50) NOT NULL,
  `is_available` tinyint(1) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `image_name` varchar(255) DEFAULT 'default_book.png',
  `category` varchar(100) DEFAULT 'General',
  `synopsis` text DEFAULT NULL,
  `view_count` int(11) DEFAULT 0,
  `rating` decimal(3,1) DEFAULT 5.0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `isbn` (`isbn`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES
(4,'978111','การเขียนโปรแกรม Python เบื้องต้น',NULL,'A1-01',1,'2026-03-26 21:10:19','programming_python.jpg','ความรู้','เรียนรู้ Python ตั้งแต่เริ่มต้นจนสามารถสร้างแอปพลิเคชันได้จริง เหมาะสำหรับมือใหม่',0,5.0),
(5,'978222','YouTube Creator Handbook',NULL,'B1-01',1,'2026-03-26 21:10:19','youtube_handbook.jpg','ความรู้','คู่มือปั้นช่องยูทูปให้เติบโต เจาะลึกอัลกอริทึมและวิธีสร้างรายได้',0,5.0),
(6,'978333','How to Cook: สูตรลับฉบับเชฟ',NULL,'C3-03',1,'2026-03-26 21:10:19','how_to_cook.jpg','ความรู้','รวมสูตรอาหารทำง่าย อร่อยระดับภัตตาคาร พร้อมเทคนิคก้นครัวที่คุณต้องรู้',0,5.0),
(8,'978444','Future of Trade',NULL,'D4-01',1,'2026-03-26 21:21:02','future_of_trade.jpg','ความรู้','วิเคราะห์ทิศทางเศรษฐกิจและการค้าโลกในอนาคต เตรียมธุรกิจให้พร้อมรับมือ',0,5.0),
(9,'11111','One Piece เล่ม 1',NULL,'Z-01',1,'2026-03-26 21:31:48','onepiece.jpg','การ์ตูน','จุดเริ่มต้นของการเดินทางสู่การเป็นราชาโจรสลัด',0,5.0),
(10,'22222','แฮร์รี่ พอตเตอร์',NULL,'F-12',1,'2026-03-26 21:31:48','harry.jpg','นิยาย','วรรณกรรมเยาวชนระดับโลก เรื่องราวของเด็กชายผู้รอดชีวิต',0,5.0),
(11,'33333','ท่องโลกอวกาศ',NULL,'K1-01',1,'2026-03-26 21:31:48','space.jpg','ความรู้','เปิดความลับของจักรวาลและดวงดาวต่างๆ แบบเข้าใจง่าย',0,5.0),
(12,'44444','นิทานอีสปก่อนนอน',NULL,'C1-02',1,'2026-03-26 21:31:48','aesop.jpg','เด็ก','รวมนิทานอีสปสอนใจพร้อมภาพประกอบสีสันสดใสสำหรับเด็ก',0,5.0),
(14,'1231222','ฟิสิกส์เบื้องต้น',NULL,'A1-01',1,'2026-03-27 04:06:58','physics.jpg','การศึกษา','ความรู้ฟิสิกส์เบื้องต้น สำหรับผู้ที่ต้องการศึกษา',0,5.0),
(16,'1231232221','ชนบทที่รัก',NULL,'C1-01',1,'2026-03-28 02:14:52','younglove.jpg','วรรณกรรมเยาวชน','วรรณกรรมเยาวชนที่เคยถูกสร้างเป็นละครโทรทัศน์ช่อง 7',0,5.0);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES
(5,'การศึกษา'),
(1,'การ์ตูน'),
(3,'ความรู้'),
(2,'นิยาย'),
(6,'วรรณกรรมเยาวชน'),
(4,'เด็ก');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `borrow_date` date NOT NULL,
  `due_date` date NOT NULL,
  `return_date` date DEFAULT NULL,
  `status` varchar(50) DEFAULT 'pending_borrow',
  `condition_before` varchar(255) DEFAULT NULL,
  `condition_after` varchar(255) DEFAULT NULL,
  `fine_amount` decimal(10,2) DEFAULT 0.00,
  `is_notified` tinyint(1) DEFAULT 0,
  `is_notified_borrow` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES
(9,26,10,'2026-03-28','2026-03-31','2026-03-28','returned','ปกติ','[ปกติ] ปกติ',0.00,1,1),
(10,26,9,'2026-03-28','2026-04-02','2026-03-28','returned','ปกติ','[ปกติ] ปกติ',0.00,1,1),
(11,26,9,'2026-03-28','2026-03-31','2026-03-28','returned','ปกติ','[ปกติ] ปกติ',0.00,1,1),
(12,26,14,'2026-03-28','2026-03-31','2026-03-28','returned','ปกติ','[ปกติ] ปกติ',0.00,1,1),
(13,26,14,'2026-03-28','2026-03-31','2026-03-28','returned','ปกติ','[ปกติ] ปกติ',0.00,1,1),
(14,26,14,'2026-03-28','2026-03-31','2026-03-28','returned','ปกติ','[ปกติ] ปกติ',0.00,1,1),
(15,26,9,'2026-03-28','2026-03-31','2026-03-28','returned','ปกติ','[ปกติ] ปกติ',0.00,1,1),
(16,26,14,'2026-03-28','2026-03-31','2026-03-28','returned','ปกติ','[ปกติ] ปกติ',0.00,1,1),
(17,26,14,'2026-03-28','2026-03-31','2026-03-28','returned','ปกติ','[ปกติ] ปกติ',0.00,1,1),
(18,26,9,'2026-03-28','2026-03-29','2026-03-28','returned','ปกติ','[เกินกำหนดคืน] ปกติ',500.00,1,1),
(19,26,11,'2026-03-28','2026-03-31','2026-03-28','returned','ปกติ','[เกินกำหนดคืน] ปกติ',500.00,1,1);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `role` enum('user','officer','admin') DEFAULT 'user',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `phone` varchar(15) DEFAULT NULL,
  `total_fine` decimal(10,2) DEFAULT 0.00,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'admin01','admin123','สมชาย ผู้ดูแลระบบ','admin','2026-03-26 17:57:10',NULL,0.00),
(2,'officer01','staff123','สมหญิง บรรณารักษ์','officer','2026-03-26 17:57:10',NULL,0.00),
(3,'user01','user123','นายพรชัย กองเพชร','user','2026-03-26 17:57:10',NULL,0.00),
(11,'staff01','1234','เจ้าหน้าที่ห้องสมุด','officer','2026-03-26 20:23:04',NULL,0.00),
(19,'test','1234','test','user','2026-03-27 19:53:40','0000000000',0.00),
(26,'pornchai','12345','Pornchai','user','2026-03-27 20:01:13','0807049049',0.00);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Dumping routines for database 'library_final_project'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-03-28 10:46:46
