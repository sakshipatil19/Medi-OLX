-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 27, 2022 at 03:45 PM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 8.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medi-olx`
--

-- --------------------------------------------------------

--
-- Table structure for table `medi_equipment`
--

CREATE TABLE `medi_equipment` (
  `equip_id` int(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `original_price` int(10) NOT NULL,
  `discounted_price` int(10) NOT NULL,
  `purchase_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `medi_equipment`
--

INSERT INTO `medi_equipment` (`equip_id`, `name`, `description`, `original_price`, `discounted_price`, `purchase_date`) VALUES
(1, 'Wheelchair', 'The wheelchair is one of the most commonly used assistive devices to promote mobility and enhance quality of life for people who have difficulties in walking (e.g. a person with spinal cord injuries resulting in quadriplegia or paraplegia, muscular dystrophy,etc). ', 8500, 5100, '2018-10-18'),
(2, 'Stretcher', 'a light frame made from two long poles with a cover of soft material stretched between them, used for carrying people who are ill or injured', 1850, 1110, '2020-09-20'),
(3, 'Stretcher trolley', 'A stretcher trolley is a combined stretcher and trolley. It can also be called a gurney. It allows a sick or injured patient to be transported in a lying, resting state', 8200, 4920, '2017-02-13'),
(4, 'Medical Bed', 'a bed having side rails that can be raised or lowered and a mattress base in three jointed sections so that the head, foot, or middle may be raised by a crank or motor, allowing a patient to lie in various positions', 20000, 12000, '2019-11-22'),
(5, 'Oximeter', 'a device that estimates the oxygen saturation of the blood and the pulse rate. Oxygen saturation gives information about the amount of oxygen carried in the blood.', 600, 360, '2021-01-04'),
(6, 'BP machine', 'It consists of an inflatable cuff that\'s wrapped around your arm, roughly level with your heart, and a monitoring device that measures the cuff\'s pressure.', 1400, 840, '2017-07-25'),
(7, 'Walker', 'A walker or walking frame is a device that gives additional support to maintain balance or stability while walking, most commonly due to age-related issues.', 1000, 600, '2016-12-03'),
(8, 'One hand walker', 'Non-wheeled walkers offer stable support for people who have balance problems. It only takes one hand to use a hemi walker for support while walking.', 1300, 780, '2019-08-05'),
(9, 'Glucometer', 'A medical device that is used for determining the level of glucose in your blood. A very useful device for home glucose monitoring, glucometer machines are preferred by diabetic patients to a large extent.', 700, 420, '2018-03-04'),
(10, 'Back rest Ramp', 'The Ramp is a versatile positioning device that creates a stable and elevated operative surface for a variety of lower extremity procedures.', 2600, 1560, '2017-02-16');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `medi_equipment`
--
ALTER TABLE `medi_equipment`
  ADD PRIMARY KEY (`equip_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `medi_equipment`
--
ALTER TABLE `medi_equipment`
  MODIFY `equip_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
