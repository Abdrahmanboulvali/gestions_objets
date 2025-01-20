-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Dec 27, 2024 at 02:24 PM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `gestion_objs_p_t`
--

-- --------------------------------------------------------

--
-- Table structure for table `objet_p_t`
--

CREATE TABLE IF NOT EXISTS `objet_p_t` (
  `id_o` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(40) DEFAULT NULL,
  `statu` varchar(40) DEFAULT NULL,
  `file` varchar(250) DEFAULT NULL,
  `emplacement` varchar(50) DEFAULT NULL,
  `date_p_t` date DEFAULT NULL,
  `destribition` varchar(50) DEFAULT NULL,
  `id_p` int(11) DEFAULT NULL,
  `file_path` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id_o`),
  KEY `fk_id_p` (`id_p`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `person_p_t`
--

CREATE TABLE IF NOT EXISTS `person_p_t` (
  `id_p` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  `num_tel` int(8) DEFAULT NULL,
  `mode_passe` varchar(8) DEFAULT NULL,
  `etat` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id_p`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `objet_p_t`
--
ALTER TABLE `objet_p_t`
  ADD CONSTRAINT `fk_id_p` FOREIGN KEY (`id_p`) REFERENCES `person_p_t` (`id_p`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
