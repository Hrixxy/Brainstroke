-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 03, 2025 at 10:56 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stroke_prediction_email`
--

-- --------------------------------------------------------

--
-- Table structure for table `predictions`
--

CREATE TABLE `predictions` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `smoking` varchar(50) DEFAULT NULL,
  `alcohol` varchar(50) DEFAULT NULL,
  `activity` varchar(50) DEFAULT NULL,
  `hypertension` varchar(50) DEFAULT NULL,
  `diabetes` varchar(50) DEFAULT NULL,
  `residence_type` varchar(50) DEFAULT NULL,
  `ever_married` varchar(50) DEFAULT NULL,
  `previous_strokes` varchar(50) DEFAULT NULL,
  `work_type` varchar(100) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL,
  `prediction` varchar(50) DEFAULT NULL,
  `confidence` float DEFAULT NULL,
  `accuracy` float DEFAULT NULL,
  `risk_factor` float DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `predictions`
--

INSERT INTO `predictions` (`id`, `name`, `age`, `email`, `gender`, `smoking`, `alcohol`, `activity`, `hypertension`, `diabetes`, `residence_type`, `ever_married`, `previous_strokes`, `work_type`, `model`, `prediction`, `confidence`, `accuracy`, `risk_factor`, `image_path`, `timestamp`) VALUES
(1, 'ron mostly  dsaf', 67, 'powerofsilence04@gmail.com', '0', 'Unknown', 'Yes', 'Active', 'Yes', 'Yes', '0', 'No', 'Yes', 'Govt Job', 'Logistic Regression', 'Stroke', 99.9987, 0.97006, 25.35, 'uploads/58_1.jpg', '2025-02-05 02:51:54'),
(2, 'ron mostly  dsaf', 67, 'powerofsilence04@gmail.com', '0', 'Unknown', 'Yes', 'Active', 'Yes', 'Yes', '0', 'No', 'Yes', 'Govt Job', 'Logistic Regression', 'Stroke', 99.9824, 0.97006, 25.35, 'uploads/58_2.jpg', '2025-02-05 02:51:54'),
(3, 'ron mostly  dsaf', 67, 'powerofsilence04@gmail.com', '0', 'Unknown', 'Yes', 'Active', 'Yes', 'Yes', '0', 'No', 'Yes', 'Govt Job', 'Logistic Regression', 'Stroke', 99.9586, 0.97006, 25.35, 'uploads/58_10.jpg', '2025-02-05 02:51:55'),
(4, 'ron mostly  dsaf', 67, 'powerofsilence04@gmail.com', '0', 'Unknown', 'Yes', 'Active', 'Yes', 'Yes', '0', 'No', 'Yes', 'Govt Job', 'Logistic Regression', 'Stroke', 99.9531, 0.97006, 25.35, 'uploads/58_18.jpg', '2025-02-05 02:51:55');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `predictions`
--
ALTER TABLE `predictions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `predictions`
--
ALTER TABLE `predictions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
