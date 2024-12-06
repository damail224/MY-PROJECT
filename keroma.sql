-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 06, 2024 at 04:29 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `keroma`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `foodname` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `foodname`, `quantity`, `created_at`, `updated_at`) VALUES
(1, 'Burger and fries', 3, '2024-12-06 03:25:24', '2024-12-06 03:27:37'),
(2, 'Chicken chips', 1, '2024-12-06 03:27:58', '2024-12-06 03:27:58');

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `id` int(11) NOT NULL,
  `foodname` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `image_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`id`, `foodname`, `description`, `price`, `image_name`) VALUES
(2, 'Chicken chips', ' Chicken and Chips Crispy, golden fried chicken served alongside thick-cut, perfectly seasoned fries for a delicious and satisfying meal.', 8.00, 'fries2.webp'),
(3, 'Burger and fries', 'A juicy beef patty served with fresh lettuce, tomato, cheese, and a delicious sauce in a soft bun. Crispy golden fries, perfectly salted, and served with a choice of dipping sauce..', 13.00, 'burgers and fries.webp'),
(4, 'Burgers', 'A juicy beef patty served with fresh lettuce, tomato, cheese, and a delicious sauce in a soft bun. ', 9.00, 'burgers.webp'),
(5, 'Chips Plain', 'Crispy golden fries, perfectly salted, and served with a choice of dipping sauce..', 4.00, 'istockphoto-1742724562-612x612.webp'),
(6, 'Passion Juice', ' A refreshing, tropical juice made from ripe passion fruit, offering a sweet and tangy flavor.', 3.00, 'fresh passion.webp'),
(7, 'Beef Samosa', ' Crispy, golden pastry filled with spiced ground beef, onions, and a blend of savory seasonings.', 2.00, 'beef samosa.webp'),
(8, 'Chicken Samosa', ' Crispy, golden pastry filled with spiced ground chicken meat, onions, and a blend of savory seasonings.', 2.00, 'samosa chicken.webp'),
(9, 'Samosa ndengu', ' Crispy, golden pastry filled with spiced boiled ndengu, onions, and a blend of savory seasonings.', 2.00, 'samosa ndengu.webp'),
(10, 'Steak Frites', 'A tender, grilled steak served with crispy, golden French fries and a side of garlic butter or sauce of your choice.', 13.00, 'steak frites.webp'),
(11, 'Mandazi', 'fried dough pastry, lightly sweetened and crispy on the outside, soft on the inside.', 1.00, 'Andazis.webp'),
(12, 'Pineapple Juice', 'A refreshing, naturally sweet juice made from fresh pineapples, perfect for a tropical burst of flavor.', 3.00, 'pinneaple.webp'),
(13, 'Sugarcane Lime', ' A refreshing blend of sweet sugarcane juice and tangy lime, creating a perfect balance of flavors.', 3.00, 'sugarcane.webp'),
(14, 'bread', ' Freshly baked soft bread with a light, fluffy texture, perfect for any meal or as a side.', 3.00, 'brown bread.webp'),
(15, 'Chapatti', 'Soft, thin, and slightly crispy flatbread, traditionally served with curries or stews.', 1.00, 'chapatti.webp'),
(16, 'Scones', 'Light and crumbly baked treats, slightly sweet, and perfect with tea or coffee. Available with raisins or plain.', 4.00, 'scones.webp'),
(17, 'Fried Chicken', 'Crispy, golden-brown chicken pieces, seasoned to perfection and fried to a crunchy finish, served with a side of dipping sauce.', 11.00, 'fried chiken.webp'),
(18, 'Coffee', 'A rich and aromatic brewed coffee, available in various options including black, espresso, or with milk.', 3.00, 'cup of coffe.webp'),
(19, 'Tea', ' A soothing cup of freshly brewed tea, available in a variety of flavors including black, green, or herbal.', 3.00, 'cup of tea.webp'),
(20, 'Drinking Chocolate ', 'A rich and velvety hot chocolate made from high-quality cocoa, perfect for a comforting treat on a cold day.', 4.00, 'drinking chocolate.webp'),
(21, 'Pila Chicken ', 'A flavorful and aromatic rice dish cooked with tender chicken, spiced with cumin, cinnamon, and other traditional seasonings.', 13.00, 'pilau chicken.webp'),
(22, 'Pilau Vegan', 'A fragrant rice dish cooked with a medley of vegetables, spices like cumin and cinnamon, and infused with rich, savory flavors—perfect for vegans.', 10.00, 'pilau vegan.webp'),
(23, 'Pilau Beef', 'A savory rice dish made with tender beef chunks, cooked in a blend of aromatic spices like cumin, coriander, and cinnamon for a rich, flavorful meal.', 14.00, 'pilau beef.webp'),
(24, 'Orange Juice', 'Freshly squeezed orange juice, bursting with natural sweetness and vitamin C, perfect for a refreshing start to your day.', 4.00, 'fresh juice.webp'),
(25, 'Mango Juice', ' A tropical, sweet, and refreshing juice made from ripe, juicy mangoes, perfect for quenching your thirst.', 4.00, 'fresh mango.webp');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `item_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `foodname` (`foodname`);

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `foodname` (`foodname`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `item_id` (`item_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`foodname`) REFERENCES `menu_items` (`foodname`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `menu_items` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
