-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 29, 2022 at 08:47 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mediolx`
--

-- --------------------------------------------------------

--
-- Table structure for table `medicines`
--

CREATE TABLE `medicines` (
  `med_id` int(10) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `original_price` bigint(10) NOT NULL,
  `price` int(255) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `expiry` date NOT NULL,
  `image` varchar(150) NOT NULL,
  `back_img` varchar(150) NOT NULL,
  `status` varchar(50) NOT NULL,
  `user_ID` int(11) DEFAULT NULL,
  `pills` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `medicines`
--

INSERT INTO `medicines` (`med_id`, `name`, `original_price`, `price`, `description`, `expiry`, `image`, `back_img`, `status`, `user_ID`, `pills`) VALUES
(1, 'Naselin 0.05% Decongestant Nasal Solution 10 ml', 100, 78, 'Naselin Nasal Spray contains Oxymetazoline Hydrochloride as active ingredients. It acts as a nasal decongestant and helps in opening the blocked nostrils in infants and children.', '2024-02-13', 'naselin.jpg', '', 'Payment Pending...', 2, 10),
(2, 'Hapdco Natrum Muriaticum 6X Tablet 25 gm', 300, 256, 'Hapdco Nat. Mur. Biochemic Tablet is strongly indicated in conditions associated with anaemia. It relieves sings of fatigue and exhaustion and boosts energy levels in the body. It also reduces swelling of the neck caused due to inflammation of the gland and is strongly indication in ailments related to diabetes and hyperthyroidism.\r\n', '2023-11-24', 'Hapdco Natrun.png', '', 'Prescription Approval Pending...', 2, 10),
(3, 'Dr. Willmar Schwabe Calcarea Phosphorica 6X Tablet 20 gm', 400, 364, 'Dr Willmar Schwabe Germany Calcarea Phosphorica Biochemic Tablet is a homoeopathic remedy which is useful in growth and healing processes of bones and teeth. It helps in relieving ailments during dentition. It is also useful in the treatment of fractures and osteoporosis.', '2023-07-23', 'Dr. Willmar Schwabe.png', '', 'Approved', 2, 10),
(4, 'Pro360 100% Plant Based Vegan Collagen Builder - Unflavored 250 gm', 950, 899, 'Pro360 100% Plant-Based Collagen Builder has amla and acerola, which are both rich sources of Vitamin C and have abundant antioxidant properties, which contribute to collagen production, slowing down the ageing process and improving skin’s elasticity and firmness.', '2024-10-02', 'Pro360.png', '', 'Approved', 2, 10),
(5, 'Dolo 650 Tablet', 50, 30, 'Dolo 650 Tablet helps relieve pain and fever by blocking the release of certain chemical messengers responsible for fever and pain. It is used to treat headaches, migraine, nerve pain, toothache, sore throat, period (menstrual) pains, arthritis, muscle aches, and the common cold.', '2023-02-22', 'Dolo 650.jpg', '', 'Approved', 2, 10),
(6, 'Crocin Pain Relief Tablet', 75, 57, 'Crocin Pain Relief Tablet is a combination of two medicines used in the treatment of headache. It helps relieve headache by blocking the release of certain chemical messengers that causes headache.', '2023-06-02', 'Crocin Pain relif.jpg', '', 'Approved', 3, 10),
(9, 'Flogel Ultra Eye Drop\r\n', 380, 321, 'Flogel Ultra Eye Drop is a prescription medicine used to treat symptoms of dry eyes. It lubricates the eyes. This way it provides temporary relief from burning and discomfort caused by dry eyes. It also reduces redness and swelling of the eye.', '2024-05-09', 'Flogel Ultra Eye Drop.jpg', '', 'Approved', 3, 10),
(10, 'Soliwax -A Ear Drop', 250, 192, 'Soliwax -E Ear Drop will relieve earache promptly, and begin to emulsify and disperse the excess cerumen while exerting insecticidal, antibacterial and anti-fungal properties simultaneously.', '2025-01-05', 'Soliwax ear drop.jpg', '', 'Approved', 3, 10),
(11, 'Cremaffin Fresh Tablet', 20, 15, 'Cremaffin Fresh Tablet is a medicine used to treat constipation. It is a laxative and helps you empty your bowels. Sometimes it is used by hospitals before surgery or some internal examinations or treatments. It works by increasing the movement in the intestine.', '2023-07-01', 'Cremaffin Fresh Tablet.jpg', '', 'Approved', 3, 10),
(12, 'OneLife Omega 3-6-9 Softgels', 1400, 1249, 'OneLife Omega 3-6-9 Softgels contains flax seed for superlative heart and skin health derived from a vegetarian source. The best beauty enhancer in your arsenal is now vegetarian. It contains not just omega 3 but also has omega 6 and 9 in the balanced ratio of 4.5:1:1.7 respectively which the body can efficiently utilize. The product is made with patented technology.', '2025-04-22', 'Onelife Omega.jpg', '', 'Approved', 2, 10),
(13, 'Venusia Max Intensive Moisturizing Lotion', 660, 564, 'It is a moisturising lotion enriched with the goodness of aloe butter, shea butter, mango butter, cocoa butter and glycerine that hydrates and revitalises your skin. The cream helps to relieve dry and dull skin. It improves the skin barriers by protecting it from dirt and pollution while keeping it hydrated.', '2023-08-19', 'Venusia Max Intensive.jpg', '', 'Approved', 3, 10),
(14, 'Shelcal 500 Tablet', 150, 105, 'It helps in keeping your bones strong and prevents osteoporosis. Calcium is used for building and maintaining healthy bones.', '2023-05-20', 'Shelcal 500 Tablet.jpg', '', 'Approved', 2, 10),
(15, 'Lobun Forte Capsule', 900, 809, 'Lobun Forte Capsule contains not less than 45 billion cells of a blend of ingredietns that are used for uremic detoxification (creatinine, urea and others) and for delaying the progression of chronic kidney diseases. ', '2024-09-09', 'Lobun Forte Capsule.jpg', '', 'Approved', 3, 10),
(33, 'Doxy-1 L-DR Forte', 29, 17, 'Helps to reduce Psoriasis. Helps to reduce Dandruff', '2023-11-01', 'WhatsApp_Image_2022-10-28_at_9.02.57_PM.jpeg', 'WhatsApp_Image_2022-10-28_at_9.03.16_PM.jpeg', 'Pending...', 3, 10);

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
  `image_name` varchar(150) NOT NULL,
  `status` varchar(30) NOT NULL,
  `user_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `medi_equipment`
--

INSERT INTO `medi_equipment` (`equip_id`, `name`, `description`, `original_price`, `discounted_price`, `image_name`, `status`, `user_ID`) VALUES
(1, 'Wheelchair', 'The wheelchair is one of the most commonly used assistive devices to promote mobility and enhance quality of life for people who have difficulties in walking (e.g. a person with spinal cord injuries resulting in quadriplegia or paraplegia, muscular dystrophy,etc). ', 8500, 5100, 'wheelchair.jpg', 'Approved', 2),
(2, 'Stretcher', 'a light frame made from two long poles with a cover of soft material stretched between them, used for carrying people who are ill or injured', 1850, 1110, 'stretcher.png', 'Approved', 3),
(3, 'Stretcher trolley', 'A stretcher trolley is a combined stretcher and trolley. It can also be called a gurney. It allows a sick or injured patient to be transported in a lying, resting state', 8200, 4920, 'Stretcher trolley.jpg', 'Approved', 6),
(4, 'Medical Bed', 'a bed having side rails that can be raised or lowered and a mattress base in three jointed sections so that the head, foot, or middle may be raised by a crank or motor, allowing a patient to lie in various positions', 20000, 12000, 'medical bed.jpg', 'Approved', 2),
(5, 'Oximeter', 'a device that estimates the oxygen saturation of the blood and the pulse rate. Oxygen saturation gives information about the amount of oxygen carried in the blood.', 600, 360, 'pulse oximeter.jpg', 'Approved', 3),
(6, 'BP machine', 'It consists of an inflatable cuff that\'s wrapped around your arm, roughly level with your heart, and a monitoring device that measures the cuff\'s pressure.', 1400, 840, 'bpmachine.jpg', 'Approved', 6),
(7, 'Walker', 'A walker or walking frame is a device that gives additional support to maintain balance or stability while walking, most commonly due to age-related issues.', 1000, 600, 'walker.jpg', 'Approved', 2),
(8, 'One hand walker', 'Non-wheeled walkers offer stable support for people who have balance problems. It only takes one hand to use a hemi walker for support while walking.', 1300, 780, 'side walker.png', 'Approved', 3),
(9, 'Glucometer', 'A medical device that is used for determining the level of glucose in your blood. A very useful device for home glucose monitoring, glucometer machines are preferred by diabetic patients to a large extent.', 700, 420, 'glucometer.jpg', 'Approved', 6),
(10, 'Back rest Ramp', 'The Ramp is a versatile positioning device that creates a stable and elevated operative surface for a variety of lower extremity procedures.', 2600, 1560, 'surgical ramp.jpg', 'Approved', 2),
(11, 'Doctor Stethoscope', 'Thermocare Doctor Stethoscope Superb Medical Equipment, Health Instrument (Black & White)', 400, 240, '71GCFvMAIyL._SL1500_.jpg', 'Pending...', 3);

-- --------------------------------------------------------

--
-- Table structure for table `order_med`
--

CREATE TABLE `order_med` (
  `order_id` int(11) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_add` varchar(300) NOT NULL,
  `user_Cno` bigint(10) NOT NULL,
  `med_name` varchar(50) NOT NULL,
  `price` bigint(10) NOT NULL,
  `pres_img` varchar(150) NOT NULL,
  `user_ID` int(11) DEFAULT NULL,
  `med_id` int(11) DEFAULT NULL,
  `order_status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order_med`
--

INSERT INTO `order_med` (`order_id`, `user_name`, `user_add`, `user_Cno`, `med_name`, `price`, `pres_img`, `user_ID`, `med_id`, `order_status`) VALUES
(5, 'Aaman', '702,Platinum Cresta,Thane, 400601', 9653632755, 'Naselin 0.05% Decongestant Nasal Solution 10 ml', 78, 'Sample-prescription-used-as-input-to-the-GUI-developed-in-the-present-work.png', 3, 1, 'Prescription Approved'),
(7, 'Aaman', '702,Platinum Cresta,Thane, 400601', 9653632755, 'Hapdco Natrum Muriaticum 6X Tablet 25 gm', 256, '2022_9$largeimg_1999179093.jpeg', 3, 2, 'Prescription Approval Pending...');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_ID` int(11) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `UIDAI` bigint(12) NOT NULL,
  `user_add` varchar(255) NOT NULL,
  `user_pcode` int(6) NOT NULL,
  `user_Cno` bigint(10) NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `user_pwd` varchar(255) NOT NULL,
  `role` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_ID`, `user_name`, `UIDAI`, `user_add`, `user_pcode`, `user_Cno`, `user_email`, `user_pwd`, `role`) VALUES
(1, 'User', 0, '', 0, 0, '', '', 'demouser'),
(2, 'Sakshi', 123456789102, '303,Sai World Empire,Panvel', 410206, 7045769330, 'sakshipatil1908@gmail.com', 'sakshi21908', 'user'),
(3, 'Aaman', 123456789103, '702,Platinum Cresta,Thane', 400601, 9653632755, 'aaman.bhowmick21@gmail.com', 'AamanB@09', 'user'),
(4, 'Prajwal', 123456789104, '1504,Mohan Palms,Kalyan', 412205, 8104899814, 'patilprajwal52@gmail.com', 'prajwal2002', 'admin'),
(5, 'Nandana', 123456789101, '1401,Amit Gardens,Plot no 7,Sector 21,Seawoods West,Navi Mumbai', 400706, 8108275689, 'nandanair2002@gmail.com', 'nandana2002', 'admin'),
(6, 'XYZ', 123412341234, '203, Panch Parmeshwar Building', 400604, 1234567890, 'abc@123', 'Demo@123', 'user'),
(7, 'mayuri', 123412341234, '203, Panch Parmeshwar Building', 400604, 7045077676, 'mayuriyerande@gmail.com', 'Mayuri@2002', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `wishlist_id` int(11) NOT NULL,
  `type_of` varchar(50) NOT NULL,
  `med_id` int(11) DEFAULT NULL,
  `user_ID` int(11) DEFAULT NULL,
  `equip_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `wishlist`
--

INSERT INTO `wishlist` (`wishlist_id`, `type_of`, `med_id`, `user_ID`, `equip_id`) VALUES
(22, 'Medicine', 2, 2, NULL),
(31, 'Medicine', 5, 3, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `medicines`
--
ALTER TABLE `medicines`
  ADD PRIMARY KEY (`med_id`),
  ADD KEY `user_ID` (`user_ID`);

--
-- Indexes for table `medi_equipment`
--
ALTER TABLE `medi_equipment`
  ADD PRIMARY KEY (`equip_id`),
  ADD KEY `user_ID` (`user_ID`);

--
-- Indexes for table `order_med`
--
ALTER TABLE `order_med`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `user_ID` (`user_ID`),
  ADD KEY `med_id` (`med_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_ID`);

--
-- Indexes for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD PRIMARY KEY (`wishlist_id`),
  ADD KEY `med_id` (`med_id`),
  ADD KEY `user_ID` (`user_ID`),
  ADD KEY `equip_id` (`equip_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `medicines`
--
ALTER TABLE `medicines`
  MODIFY `med_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `medi_equipment`
--
ALTER TABLE `medi_equipment`
  MODIFY `equip_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `order_med`
--
ALTER TABLE `order_med`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `wishlist`
--
ALTER TABLE `wishlist`
  MODIFY `wishlist_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `medicines`
--
ALTER TABLE `medicines`
  ADD CONSTRAINT `medicines_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `users` (`user_ID`);

--
-- Constraints for table `medi_equipment`
--
ALTER TABLE `medi_equipment`
  ADD CONSTRAINT `medi_equipment_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `users` (`user_ID`);

--
-- Constraints for table `order_med`
--
ALTER TABLE `order_med`
  ADD CONSTRAINT `order_med_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `users` (`user_ID`),
  ADD CONSTRAINT `order_med_ibfk_2` FOREIGN KEY (`med_id`) REFERENCES `medicines` (`med_id`);

--
-- Constraints for table `wishlist`
--
ALTER TABLE `wishlist`
  ADD CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`med_id`) REFERENCES `medicines` (`med_id`),
  ADD CONSTRAINT `wishlist_ibfk_2` FOREIGN KEY (`user_ID`) REFERENCES `users` (`user_ID`),
  ADD CONSTRAINT `wishlist_ibfk_3` FOREIGN KEY (`equip_id`) REFERENCES `medi_equipment` (`equip_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
