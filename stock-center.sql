-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 23, 2026 at 12:26 AM
-- Server version: 10.11.10-MariaDB-log
-- PHP Version: 8.3.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stock-center`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add invoice', 7, 'add_invoice'),
(26, 'Can change invoice', 7, 'change_invoice'),
(27, 'Can delete invoice', 7, 'delete_invoice'),
(28, 'Can view invoice', 7, 'view_invoice'),
(29, 'Can add product', 11, 'add_product'),
(30, 'Can change product', 11, 'change_product'),
(31, 'Can delete product', 11, 'delete_product'),
(32, 'Can view product', 11, 'view_product'),
(33, 'Can add reseller', 12, 'add_reseller'),
(34, 'Can change reseller', 12, 'change_reseller'),
(35, 'Can delete reseller', 12, 'delete_reseller'),
(36, 'Can view reseller', 12, 'view_reseller'),
(37, 'Can add warehouse', 20, 'add_warehouse'),
(38, 'Can change warehouse', 20, 'change_warehouse'),
(39, 'Can delete warehouse', 20, 'delete_warehouse'),
(40, 'Can view warehouse', 20, 'view_warehouse'),
(41, 'Can add payment', 10, 'add_payment'),
(42, 'Can change payment', 10, 'change_payment'),
(43, 'Can delete payment', 10, 'delete_payment'),
(44, 'Can view payment', 10, 'view_payment'),
(45, 'Can add return header', 15, 'add_returnheader'),
(46, 'Can change return header', 15, 'change_returnheader'),
(47, 'Can delete return header', 15, 'delete_returnheader'),
(48, 'Can view return header', 15, 'view_returnheader'),
(49, 'Can add transaction', 17, 'add_transaction'),
(50, 'Can change transaction', 17, 'change_transaction'),
(51, 'Can delete transaction', 17, 'delete_transaction'),
(52, 'Can view transaction', 17, 'view_transaction'),
(53, 'Can add variant', 19, 'add_variant'),
(54, 'Can change variant', 19, 'change_variant'),
(55, 'Can delete variant', 19, 'delete_variant'),
(56, 'Can view variant', 19, 'view_variant'),
(57, 'Can add transaction detail', 18, 'add_transactiondetail'),
(58, 'Can change transaction detail', 18, 'change_transactiondetail'),
(59, 'Can delete transaction detail', 18, 'delete_transactiondetail'),
(60, 'Can view transaction detail', 18, 'view_transactiondetail'),
(61, 'Can add return detail', 14, 'add_returndetail'),
(62, 'Can change return detail', 14, 'change_returndetail'),
(63, 'Can delete return detail', 14, 'delete_returndetail'),
(64, 'Can view return detail', 14, 'view_returndetail'),
(65, 'Can add stock movement', 16, 'add_stockmovement'),
(66, 'Can change stock movement', 16, 'change_stockmovement'),
(67, 'Can delete stock movement', 16, 'delete_stockmovement'),
(68, 'Can view stock movement', 16, 'view_stockmovement'),
(69, 'Can add reseller price', 13, 'add_resellerprice'),
(70, 'Can change reseller price', 13, 'change_resellerprice'),
(71, 'Can delete reseller price', 13, 'delete_resellerprice'),
(72, 'Can view reseller price', 13, 'view_resellerprice'),
(73, 'Can add warehouse stock', 21, 'add_warehousestock'),
(74, 'Can change warehouse stock', 21, 'change_warehousestock'),
(75, 'Can delete warehouse stock', 21, 'delete_warehousestock'),
(76, 'Can view warehouse stock', 21, 'view_warehousestock'),
(77, 'Can add packing task', 9, 'add_packingtask'),
(78, 'Can change packing task', 9, 'change_packingtask'),
(79, 'Can delete packing task', 9, 'delete_packingtask'),
(80, 'Can view packing task', 9, 'view_packingtask'),
(81, 'Can add packing item', 8, 'add_packingitem'),
(82, 'Can change packing item', 8, 'change_packingitem'),
(83, 'Can delete packing item', 8, 'delete_packingitem'),
(84, 'Can view packing item', 8, 'view_packingitem');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1200000$Azd9d5meD7KPnjrqZPKRtn$9/GWDqcTEAVwQpP+z42Lrrtv2N1D6IbLgyRzE25qIc4=', '2026-02-22 14:25:09.058960', 1, 'indra', '', '', '', 1, 1, '2026-02-22 13:16:12.599978'),
(2, 'pbkdf2_sha256$1200000$uDqZ4zVhsqKS5ZFWkQyVTE$lJJHd0jiYd29ai26lwq864TjqpZ7zib5ZBKW5NSZws4=', NULL, 0, 'duloh', '', '', '', 0, 1, '2026-02-22 14:26:13.752288');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_invoice`
--

CREATE TABLE `core_invoice` (
  `id` bigint(20) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `paid_amount` decimal(12,2) NOT NULL,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `reseller_id` bigint(20) NOT NULL,
  `transaction_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_packingitem`
--

CREATE TABLE `core_packingitem` (
  `id` bigint(20) NOT NULL,
  `qty` int(11) NOT NULL,
  `variant_id` bigint(20) NOT NULL,
  `packing_task_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_packingtask`
--

CREATE TABLE `core_packingtask` (
  `id` bigint(20) NOT NULL,
  `total_items` int(11) NOT NULL,
  `packing_fee_per_item` decimal(10,2) NOT NULL,
  `total_fee` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `warehouse_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_payment`
--

CREATE TABLE `core_payment` (
  `id` bigint(20) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `method` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `invoice_id` bigint(20) NOT NULL,
  `reseller_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_product`
--

CREATE TABLE `core_product` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `category` varchar(100) NOT NULL,
  `brand` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `core_product`
--

INSERT INTO `core_product` (`id`, `name`, `category`, `brand`, `is_active`) VALUES
(1, '7/8', '7/8', 'Nebula', 1),
(2, 'HOTPANTS', 'HOTPANTS', 'Nebula', 1),
(3, 'JOGGER', 'JOGGER', 'Nebula', 1),
(4, 'KAOS KUMIS', 'KAOS KUMIS', 'Nebula', 1),
(5, 'KAOS POLOS', 'KAOS POLOS', 'Nebula', 1),
(6, 'LONGPANTS', 'LONGPANTS', 'Nebula', 1),
(7, 'N 01 L/L', 'N 01 L/L', 'Nebula', 1),
(8, 'N 01 RUN', 'N 01 RUN', 'Nebula', 1),
(9, 'N 01 S/L', 'N 01 S/L', 'Nebula', 1),
(10, 'N 02 RUN', 'N 02 RUN', 'Nebula', 1),
(11, 'N 02 S/L', 'N 02 S/L', 'Nebula', 1);

-- --------------------------------------------------------

--
-- Table structure for table `core_reseller`
--

CREATE TABLE `core_reseller` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` longtext NOT NULL,
  `credit_limit` decimal(12,2) NOT NULL,
  `current_balance` decimal(12,2) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `core_reseller`
--

INSERT INTO `core_reseller` (`id`, `name`, `phone`, `address`, `credit_limit`, `current_balance`, `user_id`) VALUES
(1, 'duloh', '082122343803', 'Tasikmalaya', 0.00, 0.00, 2);

-- --------------------------------------------------------

--
-- Table structure for table `core_resellerprice`
--

CREATE TABLE `core_resellerprice` (
  `id` bigint(20) NOT NULL,
  `custom_price` decimal(12,2) NOT NULL,
  `reseller_id` bigint(20) NOT NULL,
  `variant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_returndetail`
--

CREATE TABLE `core_returndetail` (
  `id` bigint(20) NOT NULL,
  `qty` int(11) NOT NULL,
  `return_header_id` bigint(20) NOT NULL,
  `variant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_returnheader`
--

CREATE TABLE `core_returnheader` (
  `id` bigint(20) NOT NULL,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `invoice_id` bigint(20) NOT NULL,
  `reseller_id` bigint(20) NOT NULL,
  `warehouse_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_stockmovement`
--

CREATE TABLE `core_stockmovement` (
  `id` bigint(20) NOT NULL,
  `movement_type` varchar(10) NOT NULL,
  `qty` int(11) NOT NULL,
  `ref_type` varchar(50) NOT NULL,
  `ref_id` int(11) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `variant_id` bigint(20) NOT NULL,
  `warehouse_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_transaction`
--

CREATE TABLE `core_transaction` (
  `id` bigint(20) NOT NULL,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `reseller_id` bigint(20) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `warehouse_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_transactiondetail`
--

CREATE TABLE `core_transactiondetail` (
  `id` bigint(20) NOT NULL,
  `qty` int(11) NOT NULL,
  `price` decimal(12,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `transaction_id` bigint(20) NOT NULL,
  `variant_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_variant`
--

CREATE TABLE `core_variant` (
  `id` bigint(20) NOT NULL,
  `sku` varchar(100) NOT NULL,
  `color` varchar(50) NOT NULL,
  `size` varchar(50) NOT NULL,
  `default_price` decimal(12,2) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `core_variant`
--

INSERT INTO `core_variant` (`id`, `sku`, `color`, `size`, `default_price`, `product_id`) VALUES
(1, '71M', 'HITAM', 'M', 25000.00, 1),
(2, '71L', 'HITAM', 'L', 25000.00, 1),
(3, '71X', 'HITAM', 'XL', 25000.00, 1),
(4, '71XX', 'HITAM', 'XXL', 25000.00, 1),
(5, '71XXX', 'HITAM', 'XXXL', 25000.00, 1),
(6, '72M', 'PUTIH', 'M', 25000.00, 1),
(7, '72L', 'PUTIH', 'L', 25000.00, 1),
(8, '72X', 'PUTIH', 'XL', 25000.00, 1),
(9, '72XX', 'PUTIH', 'XXL', 25000.00, 1),
(10, '72XXX', 'PUTIH', 'XXXL', 25000.00, 1),
(11, '76M', 'MERAH', 'M', 25000.00, 1),
(12, '76L', 'MERAH', 'L', 25000.00, 1),
(13, '76X', 'MERAH', 'XL', 25000.00, 1),
(14, '76XX', 'MERAH', 'XXL', 25000.00, 1),
(15, '76XXX', 'MERAH', 'XXXL', 25000.00, 1),
(16, '77M', 'NAVY', 'M', 25000.00, 1),
(17, '77L', 'NAVY', 'L', 25000.00, 1),
(18, '77X', 'NAVY', 'XL', 25000.00, 1),
(19, '77XX', 'NAVY', 'XXL', 25000.00, 1),
(20, '77XXX', 'NAVY', 'XXXL', 25000.00, 1),
(21, '75M', 'ARMY', 'M', 25000.00, 1),
(22, '75L', 'ARMY', 'L', 25000.00, 1),
(23, '75X', 'ARMY', 'XL', 25000.00, 1),
(24, '75XX', 'ARMY', 'XXL', 25000.00, 1),
(25, '75XXX', 'ARMY', 'XXXL', 25000.00, 1),
(26, '73M', 'GREY', 'M', 25000.00, 1),
(27, '73L', 'GREY', 'L', 25000.00, 1),
(28, '73X', 'GREY', 'XL', 25000.00, 1),
(29, '73XX', 'GREY', 'XXL', 25000.00, 1),
(30, '73XXX', 'GREY', 'XXXL', 25000.00, 1),
(31, '711M', 'SAGE', 'M', 25000.00, 1),
(32, '711L', 'SAGE', 'L', 25000.00, 1),
(33, '711X', 'SAGE', 'XL', 25000.00, 1),
(34, '711XX', 'SAGE', 'XXL', 25000.00, 1),
(35, '711XXX', 'SAGE', 'XXXL', 25000.00, 1),
(36, '79M', 'DUSTY PINK', 'M', 25000.00, 1),
(37, '79L', 'DUSTY PINK', 'L', 25000.00, 1),
(38, '79X', 'DUSTY PINK', 'XL', 25000.00, 1),
(39, '79XX', 'DUSTY PINK', 'XXL', 25000.00, 1),
(40, '79XXX', 'DUSTY PINK', 'XXXL', 25000.00, 1),
(41, '78M', 'PINK FANTA', 'M', 25000.00, 1),
(42, '78L', 'PINK FANTA', 'L', 25000.00, 1),
(43, '78X', 'PINK FANTA', 'XL', 25000.00, 1),
(44, '78XX', 'PINK FANTA', 'XXL', 25000.00, 1),
(45, '78XXX', 'PINK FANTA', 'XXXL', 25000.00, 1),
(46, '710M', 'SOFT PEACH', 'M', 25000.00, 1),
(47, '710L', 'SOFT PEACH', 'L', 25000.00, 1),
(48, '710X', 'SOFT PEACH', 'XL', 25000.00, 1),
(49, '710XX', 'SOFT PEACH', 'XXL', 25000.00, 1),
(50, '710XXX', 'SOFT PEACH', 'XXXL', 25000.00, 1),
(51, '74M', 'COKSU', 'M', 25000.00, 1),
(52, '74L', 'COKSU', 'L', 25000.00, 1),
(53, '74X', 'COKSU', 'XL', 25000.00, 1),
(54, '74XX', 'COKSU', 'XXL', 25000.00, 1),
(55, '7XXX', 'COKSU', 'XXXL', 25000.00, 1),
(56, 'H1M', 'HITAM', 'M', 38000.00, 2),
(57, 'H1L', 'HITAM', 'L', 38000.00, 2),
(58, 'H1X', 'HITAM', 'XL', 38000.00, 2),
(59, 'H1XX', 'HITAM', 'XXL', 38000.00, 2),
(60, 'H1XXX', 'HITAM', 'XXXL', 38000.00, 2),
(61, 'H2M', 'PUTIH', 'M', 38000.00, 2),
(62, 'H2L', 'PUTIH', 'L', 38000.00, 2),
(63, 'H2X', 'PUTIH', 'XL', 38000.00, 2),
(64, 'H2XX', 'PUTIH', 'XXL', 38000.00, 2),
(65, 'H2XXX', 'PUTIH', 'XXXL', 38000.00, 2),
(66, 'H3M', 'GREY', 'M', 38000.00, 2),
(67, 'H3L', 'GREY', 'L', 38000.00, 2),
(68, 'H3X', 'GREY', 'XL', 38000.00, 2),
(69, 'H3XX', 'GREY', 'XXL', 38000.00, 2),
(70, 'H3XXX', 'GREY', 'XXXL', 38000.00, 2),
(71, 'H4M', 'COKSU', 'M', 38000.00, 2),
(72, 'H4L', 'COKSU', 'L', 38000.00, 2),
(73, 'H4X', 'COKSU', 'XL', 38000.00, 2),
(74, 'H4XX', 'COKSU', 'XXL', 38000.00, 2),
(75, 'H4XXX', 'COKSU', 'XXXL', 38000.00, 2),
(76, 'H5M', 'ARMY', 'M', 38000.00, 2),
(77, 'H5L', 'ARMY', 'L', 38000.00, 2),
(78, 'H5X', 'ARMY', 'XL', 38000.00, 2),
(79, 'H5XX', 'ARMY', 'XXL', 38000.00, 2),
(80, 'H5XXX', 'ARMY', 'XXXL', 38000.00, 2),
(81, 'J1M', 'HITAM', 'M', 27200.00, 3),
(82, 'J1L', 'HITAM', 'L', 27200.00, 3),
(83, 'J1X', 'HITAM', 'XL', 27200.00, 3),
(84, 'J1XX', 'HITAM', 'XXL', 27200.00, 3),
(85, 'J1XXX', 'HITAM', 'XXXL', 27200.00, 3),
(86, 'J2M', 'PUTIH', 'M', 27200.00, 3),
(87, 'J2L', 'PUTIH', 'L', 27200.00, 3),
(88, 'J2X', 'PUTIH', 'XL', 27200.00, 3),
(89, 'J2XX', 'PUTIH', 'XXL', 27200.00, 3),
(90, 'J2XXX', 'PUTIH', 'XXXL', 27200.00, 3),
(91, 'J6M', 'MERAH', 'M', 27200.00, 3),
(92, 'J6L', 'MERAH', 'L', 27200.00, 3),
(93, 'J6X', 'MERAH', 'XL', 27200.00, 3),
(94, 'J6XX', 'MERAH', 'XXL', 27200.00, 3),
(95, 'J6XXX', 'MERAH', 'XXXL', 27200.00, 3),
(96, 'J7M', 'NAVY', 'M', 27200.00, 3),
(97, 'J7L', 'NAVY', 'L', 27200.00, 3),
(98, 'J7X', 'NAVY', 'XL', 27200.00, 3),
(99, 'J7XX', 'NAVY', 'XXL', 27200.00, 3),
(100, 'J7XXX', 'NAVY', 'XXXL', 27200.00, 3),
(101, 'J5M', 'ARMY', 'M', 27200.00, 3),
(102, 'J5L', 'ARMY', 'L', 27200.00, 3),
(103, 'J5X', 'ARMY', 'XL', 27200.00, 3),
(104, 'J5XX', 'ARMY', 'XXL', 27200.00, 3),
(105, 'J5XXX', 'ARMY', 'XXXL', 27200.00, 3),
(106, 'J12M', 'BLUE ROYAL', 'M', 27200.00, 3),
(107, 'J12L', 'BLUE ROYAL', 'L', 27200.00, 3),
(108, 'J12X', 'BLUE ROYAL', 'XL', 27200.00, 3),
(109, 'J12XX', 'BLUE ROYAL', 'XXL', 27200.00, 3),
(110, 'J12XXX', 'BLUE ROYAL', 'XXXL', 27200.00, 3),
(111, 'J8M', 'PINK FANTA', 'M', 27200.00, 3),
(112, 'J8L', 'PINK FANTA', 'L', 27200.00, 3),
(113, 'J8X', 'PINK FANTA', 'XL', 27200.00, 3),
(114, 'J8XX', 'PINK FANTA', 'XXL', 27200.00, 3),
(115, 'J8XXX', 'PINK FANTA', 'XXXL', 27200.00, 3),
(116, 'J9M', 'DUSTY PINK', 'M', 27200.00, 3),
(117, 'J9L', 'DUSTY PINK', 'L', 27200.00, 3),
(118, 'J9X', 'DUSTY PINK', 'XL', 27200.00, 3),
(119, 'J9XX', 'DUSTY PINK', 'XXL', 27200.00, 3),
(120, 'J9XXX', 'DUSTY PINK', 'XXXL', 27200.00, 3),
(121, 'J4M', 'COKSU', 'M', 27200.00, 3),
(122, 'J4L', 'COKSU', 'L', 27200.00, 3),
(123, 'J4X', 'COKSU', 'XL', 27200.00, 3),
(124, 'J4XX', 'COKSU', 'XXL', 27200.00, 3),
(125, 'J4XXX', 'COKSU', 'XXXL', 27200.00, 3),
(126, 'J3M', 'SOFT GREY', 'M', 27200.00, 3),
(127, 'J3L', 'SOFT GREY', 'L', 27200.00, 3),
(128, 'J3X', 'SOFT GREY', 'XL', 27200.00, 3),
(129, 'J3XX', 'SOFT GREY', 'XXL', 27200.00, 3),
(130, 'J3XXX', 'SOFT GREY', 'XXXL', 27200.00, 3),
(131, 'J13M', 'SOFT YELLOW', 'M', 27200.00, 3),
(132, 'J13L', 'SOFT YELLOW', 'L', 27200.00, 3),
(133, 'J13X', 'SOFT YELLOW', 'XL', 27200.00, 3),
(134, 'J13XX', 'SOFT YELLOW', 'XXL', 27200.00, 3),
(135, 'J13XXX', 'SOFT YELLOW', 'XXXL', 27200.00, 3),
(136, 'J10M', 'SOFT PEACH', 'M', 27200.00, 3),
(137, 'J10L', 'SOFT PEACH', 'L', 27200.00, 3),
(138, 'J10X', 'SOFT PEACH', 'XL', 27200.00, 3),
(139, 'J10XX', 'SOFT PEACH', 'XXL', 27200.00, 3),
(140, 'J10XXX', 'SOFT PEACH', 'XXXL', 27200.00, 3),
(141, 'J11M', 'SAGE', 'M', 27200.00, 3),
(142, 'J11L', 'SAGE', 'L', 27200.00, 3),
(143, 'J11X', 'SAGE', 'XL', 27200.00, 3),
(144, 'J11XX', 'SAGE', 'XXL', 27200.00, 3),
(145, 'J11XXX', 'SAGE', 'XXXL', 27200.00, 3),
(146, 'KK1M', 'HITAM', 'M', 32000.00, 4),
(147, 'KK1L', 'HITAM', 'L', 32000.00, 4),
(148, 'KK1X', 'HITAM', 'XL', 32000.00, 4),
(149, 'KK1XX', 'HITAM', 'XXL', 32000.00, 4),
(150, 'KK2M', 'PUTIH', 'M', 32000.00, 4),
(151, 'KK2L', 'PUTIH', 'L', 32000.00, 4),
(152, 'KK2X', 'PUTIH', 'XL', 32000.00, 4),
(153, 'KK2XX', 'PUTIH', 'XXL', 32000.00, 4),
(154, 'KK17M', 'KHAKI', 'M', 32000.00, 4),
(155, 'KK17L', 'KHAKI', 'L', 32000.00, 4),
(156, 'KK17X', 'KHAKI', 'XL', 32000.00, 4),
(157, 'KK17XX', 'KHAKI', 'XXL', 32000.00, 4),
(158, 'KK9M', 'DUSTY PINK', 'M', 32000.00, 4),
(159, 'KK9L', 'DUSTY PINK', 'L', 32000.00, 4),
(160, 'KK9X', 'DUSTY PINK', 'XL', 32000.00, 4),
(161, 'KK9XX', 'DUSTY PINK', 'XXL', 32000.00, 4),
(162, 'KK14M', 'BLUE SKY', 'M', 32000.00, 4),
(163, 'KK14L', 'BLUE SKY', 'L', 32000.00, 4),
(164, 'KK14X', 'BLUE SKY', 'XL', 32000.00, 4),
(165, 'KK14XX', 'BLUE SKY', 'XXL', 32000.00, 4),
(166, 'KP1M', 'HITAM', 'M', 31000.00, 5),
(167, 'KP1L', 'HITAM', 'L', 31000.00, 5),
(168, 'KP1X', 'HITAM', 'XL', 31000.00, 5),
(169, 'KP1XX', 'HITAM', 'XXL', 31000.00, 5),
(170, 'KP2M', 'PUTIH', 'M', 31000.00, 5),
(171, 'KP2L', 'PUTIH', 'L', 31000.00, 5),
(172, 'KP2X', 'PUTIH', 'XL', 31000.00, 5),
(173, 'KP2XX', 'PUTIH', 'XXL', 31000.00, 5),
(174, 'KP17M', 'KHAKI', 'M', 31000.00, 5),
(175, 'KP17L', 'KHAKI', 'L', 31000.00, 5),
(176, 'KP17X', 'KHAKI', 'XL', 31000.00, 5),
(177, 'KP17XX', 'KHAKI', 'XXL', 31000.00, 5),
(178, 'KP9M', 'DUSTY PINK', 'M', 31000.00, 5),
(179, 'KP9L', 'DUSTY PINK', 'L', 31000.00, 5),
(180, 'KP9X', 'DUSTY PINK', 'XL', 31000.00, 5),
(181, 'KP9XX', 'DUSTY PINK', 'XXL', 31000.00, 5),
(182, 'KP14M', 'BLUE SKY', 'M', 31000.00, 5),
(183, 'KP14L', 'BLUE SKY', 'L', 31000.00, 5),
(184, 'KP14X', 'BLUE SKY', 'XL', 31000.00, 5),
(185, 'KP14XX', 'BLUE SKY', 'XXL', 31000.00, 5),
(186, 'L1M', 'HITAM', 'M', 43000.00, 6),
(187, 'L1L', 'HITAM', 'L', 43000.00, 6),
(188, 'L1X', 'HITAM', 'XL', 43000.00, 6),
(189, 'L1XX', 'HITAM', 'XXL', 43000.00, 6),
(190, 'L1XXX', 'HITAM', 'XXXL', 43000.00, 6),
(191, 'L2M', 'PUTIH', 'M', 43000.00, 6),
(192, 'L2L', 'PUTIH', 'L', 43000.00, 6),
(193, 'L2X', 'PUTIH', 'XL', 43000.00, 6),
(194, 'L2XX', 'PUTIH', 'XXL', 43000.00, 6),
(195, 'L2XXX', 'PUTIH', 'XXXL', 43000.00, 6),
(196, 'L3M', 'GREY', 'M', 43000.00, 6),
(197, 'L3L', 'GREY', 'L', 43000.00, 6),
(198, 'L3X', 'GREY', 'XL', 43000.00, 6),
(199, 'L3XX', 'GREY', 'XXL', 43000.00, 6),
(200, 'L3XXX', 'GREY', 'XXXL', 43000.00, 6),
(201, 'L4M', 'COKSU', 'M', 43000.00, 6),
(202, 'L4L', 'COKSU', 'L', 43000.00, 6),
(203, 'L4X', 'COKSU', 'XL', 43000.00, 6),
(204, 'L4XX', 'COKSU', 'XXL', 43000.00, 6),
(205, 'L4XXX', 'COKSU', 'XXXL', 43000.00, 6),
(206, 'L5M', 'ARMY', 'M', 43000.00, 6),
(207, 'L5L', 'ARMY', 'L', 43000.00, 6),
(208, 'L5X', 'ARMY', 'XL', 43000.00, 6),
(209, 'L5XX', 'ARMY', 'XXL', 43000.00, 6),
(210, 'L5XXX', 'ARMY', 'XXXL', 43000.00, 6),
(211, '1NLL1M', 'HITAM', 'M', 38000.00, 7),
(212, '1NLL1L', 'HITAM', 'L', 38000.00, 7),
(213, '1NLL1X', 'HITAM', 'XL', 38000.00, 7),
(214, '1NLL1XX', 'HITAM', 'XXL', 38000.00, 7),
(215, '1NLL1XXX', 'HITAM', 'XXXL', 38000.00, 7),
(216, '1N1M', 'HITAM', 'M', 22000.00, 8),
(217, '1N1L', 'HITAM', 'L', 22000.00, 8),
(218, '1N1X', 'HITAM', 'XL', 22000.00, 8),
(219, '1N1XX', 'HITAM', 'XXL', 22000.00, 8),
(220, '1N1XXX', 'HITAM', 'XXXL', 22000.00, 8),
(221, '1NSL1M', 'HITAM', 'M', 32000.00, 9),
(222, '1NSL1L', 'HITAM', 'L', 32000.00, 9),
(223, '1NSL1X', 'HITAM', 'XL', 32000.00, 9),
(224, '1NSL1XX', 'HITAM', 'XXL', 32000.00, 9),
(225, '1NSL1XXX', 'HITAM', 'XXXL', 32000.00, 9),
(226, '2N1M', 'HITAM', 'M', 22000.00, 10),
(227, '2N1L', 'HITAM', 'L', 22000.00, 10),
(228, '2N1X', 'HITAM', 'XL', 22000.00, 10),
(229, '2N1XX', 'HITAM', 'XXL', 22000.00, 10),
(230, '2N1XXX', 'HITAM', 'XXXL', 22000.00, 10),
(231, '2N2M', 'PUTIH', 'M', 22000.00, 10),
(232, '2N2L', 'PUTIH', 'L', 22000.00, 10),
(233, '2N2X', 'PUTIH', 'XL', 22000.00, 10),
(234, '2N2XX', 'PUTIH', 'XXL', 22000.00, 10),
(235, '2N2XXX', 'PUTIH', 'XXXL', 22000.00, 10),
(236, '2N15M', 'OLIVE', 'M', 22000.00, 10),
(237, '2N15L', 'OLIVE', 'L', 22000.00, 10),
(238, '2N15X', 'OLIVE', 'XL', 22000.00, 10),
(239, '2N15XX', 'OLIVE', 'XXL', 22000.00, 10),
(240, '2N15XXX', 'OLIVE', 'XXXL', 22000.00, 10),
(241, '2N16M', 'DUST OREN', 'M', 22000.00, 10),
(242, '2N16L', 'DUST OREN', 'L', 22000.00, 10),
(243, '2N16X', 'DUST OREN', 'XL', 22000.00, 10),
(244, '2N16XX', 'DUST OREN', 'XXL', 22000.00, 10),
(245, '2N16XXX', 'DUST OREN', 'XXXL', 22000.00, 10),
(246, '2NSL1M', 'HITAM', 'M', 32000.00, 11),
(247, '2NSL1L', 'HITAM', 'L', 32000.00, 11),
(248, '2NSL1X', 'HITAM', 'XL', 32000.00, 11),
(249, '2NSL1XX', 'HITAM', 'XXL', 32000.00, 11),
(250, '2NSL1XXX', 'HITAM', 'XXXL', 32000.00, 11);

-- --------------------------------------------------------

--
-- Table structure for table `core_warehouse`
--

CREATE TABLE `core_warehouse` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `core_warehouse`
--

INSERT INTO `core_warehouse` (`id`, `name`, `location`, `is_active`) VALUES
(1, 'gudang center', 'cibangun', 1);

-- --------------------------------------------------------

--
-- Table structure for table `core_warehousestock`
--

CREATE TABLE `core_warehousestock` (
  `id` bigint(20) NOT NULL,
  `qty_available` int(11) NOT NULL,
  `variant_id` bigint(20) NOT NULL,
  `warehouse_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `core_warehousestock`
--

INSERT INTO `core_warehousestock` (`id`, `qty_available`, `variant_id`, `warehouse_id`) VALUES
(1, 222, 1, 1),
(2, 0, 2, 1),
(3, 0, 3, 1),
(4, 13, 4, 1),
(5, 11, 5, 1),
(6, 97, 6, 1),
(7, 178, 7, 1),
(8, 19, 8, 1),
(9, 82, 9, 1),
(10, 0, 10, 1),
(11, 117, 11, 1),
(12, 128, 12, 1),
(13, 0, 13, 1),
(14, 38, 14, 1),
(15, 72, 15, 1),
(16, 146, 16, 1),
(17, 49, 17, 1),
(18, 109, 18, 1),
(19, 0, 19, 1),
(20, 0, 20, 1),
(21, 139, 21, 1),
(22, 127, 22, 1),
(23, 101, 23, 1),
(24, 126, 24, 1),
(25, 66, 25, 1),
(26, 95, 26, 1),
(27, 44, 27, 1),
(28, 62, 28, 1),
(29, 59, 29, 1),
(30, 21, 30, 1),
(31, 0, 31, 1),
(32, 6, 32, 1),
(33, 0, 33, 1),
(34, 16, 34, 1),
(35, 13, 35, 1),
(36, 5, 36, 1),
(37, 0, 37, 1),
(38, 0, 38, 1),
(39, 0, 39, 1),
(40, 12, 40, 1),
(41, 0, 41, 1),
(42, 11, 42, 1),
(43, 4, 43, 1),
(44, 14, 44, 1),
(45, 0, 45, 1),
(46, 36, 46, 1),
(47, 2, 47, 1),
(48, 10, 48, 1),
(49, 2, 49, 1),
(50, 10, 50, 1),
(51, 0, 51, 1),
(52, 1, 52, 1),
(53, 7, 53, 1),
(54, 3, 54, 1),
(55, 0, 55, 1),
(56, 218, 56, 1),
(57, 84, 57, 1),
(58, 10, 58, 1),
(59, 28, 59, 1),
(60, 0, 60, 1),
(61, 301, 61, 1),
(62, 84, 62, 1),
(63, 7, 63, 1),
(64, 76, 64, 1),
(65, 111, 65, 1),
(66, 97, 66, 1),
(67, 63, 67, 1),
(68, 2, 68, 1),
(69, 64, 69, 1),
(70, 98, 70, 1),
(71, 32, 71, 1),
(72, 99, 72, 1),
(73, 136, 73, 1),
(74, 72, 74, 1),
(75, 167, 75, 1),
(76, 34, 76, 1),
(77, 39, 77, 1),
(78, 32, 78, 1),
(79, 0, 79, 1),
(80, 109, 80, 1),
(81, 68, 81, 1),
(82, 98, 82, 1),
(83, 0, 83, 1),
(84, 65, 84, 1),
(85, 67, 85, 1),
(86, 37, 86, 1),
(87, 90, 87, 1),
(88, 110, 88, 1),
(89, 44, 89, 1),
(90, 53, 90, 1),
(91, 63, 91, 1),
(92, 72, 92, 1),
(93, 56, 93, 1),
(94, 89, 94, 1),
(95, 43, 95, 1),
(96, 123, 96, 1),
(97, 97, 97, 1),
(98, 103, 98, 1),
(99, 64, 99, 1),
(100, 10, 100, 1),
(101, 71, 101, 1),
(102, 27, 102, 1),
(103, 86, 103, 1),
(104, 51, 104, 1),
(105, 48, 105, 1),
(106, 94, 106, 1),
(107, 30, 107, 1),
(108, 19, 108, 1),
(109, 61, 109, 1),
(110, 28, 110, 1),
(111, 55, 111, 1),
(112, 74, 112, 1),
(113, 28, 113, 1),
(114, 7, 114, 1),
(115, 31, 115, 1),
(116, 216, 116, 1),
(117, 18, 117, 1),
(118, 0, 118, 1),
(119, 17, 119, 1),
(120, 14, 120, 1),
(121, 21, 121, 1),
(122, 110, 122, 1),
(123, 63, 123, 1),
(124, 34, 124, 1),
(125, 40, 125, 1),
(126, 44, 126, 1),
(127, 111, 127, 1),
(128, 45, 128, 1),
(129, 0, 129, 1),
(130, 53, 130, 1),
(131, 81, 131, 1),
(132, 95, 132, 1),
(133, 72, 133, 1),
(134, 21, 134, 1),
(135, 0, 135, 1),
(136, 84, 136, 1),
(137, 88, 137, 1),
(138, 38, 138, 1),
(139, 1, 139, 1),
(140, 0, 140, 1),
(141, 25, 141, 1),
(142, 52, 142, 1),
(143, 64, 143, 1),
(144, 21, 144, 1),
(145, 68, 145, 1),
(146, 48, 146, 1),
(147, 27, 147, 1),
(148, 43, 148, 1),
(149, 18, 149, 1),
(150, 0, 150, 1),
(151, 46, 151, 1),
(152, 33, 152, 1),
(153, 0, 153, 1),
(154, 17, 154, 1),
(155, 84, 155, 1),
(156, 40, 156, 1),
(157, 83, 157, 1),
(158, 59, 158, 1),
(159, 44, 159, 1),
(160, 2, 160, 1),
(161, 63, 161, 1),
(162, 59, 162, 1),
(163, 67, 163, 1),
(164, 42, 164, 1),
(165, 71, 165, 1),
(166, 53, 166, 1),
(167, 38, 167, 1),
(168, 15, 168, 1),
(169, 40, 169, 1),
(170, 90, 170, 1),
(171, 11, 171, 1),
(172, 0, 172, 1),
(173, 0, 173, 1),
(174, 32, 174, 1),
(175, 17, 175, 1),
(176, 33, 176, 1),
(177, 26, 177, 1),
(178, 47, 178, 1),
(179, 18, 179, 1),
(180, 45, 180, 1),
(181, 24, 181, 1),
(182, 30, 182, 1),
(183, 34, 183, 1),
(184, 45, 184, 1),
(185, 0, 185, 1),
(186, 22, 186, 1),
(187, 1, 187, 1),
(188, 67, 188, 1),
(189, 211, 189, 1),
(190, 251, 190, 1),
(191, 30, 191, 1),
(192, 30, 192, 1),
(193, 31, 193, 1),
(194, 31, 194, 1),
(195, 31, 195, 1),
(196, 29, 196, 1),
(197, 0, 197, 1),
(198, 31, 198, 1),
(199, 32, 199, 1),
(200, 30, 200, 1),
(201, 0, 201, 1),
(202, 31, 202, 1),
(203, 32, 203, 1),
(204, 0, 204, 1),
(205, 32, 205, 1),
(206, 56, 206, 1),
(207, 35, 207, 1),
(208, 40, 208, 1),
(209, 62, 209, 1),
(210, 31, 210, 1),
(211, 4, 211, 1),
(212, 1, 212, 1),
(213, 1, 213, 1),
(214, 11, 214, 1),
(215, 1, 215, 1),
(216, 6, 216, 1),
(217, 0, 217, 1),
(218, 0, 218, 1),
(219, 13, 219, 1),
(220, 11, 220, 1),
(221, 8, 221, 1),
(222, 8, 222, 1),
(223, 1, 223, 1),
(224, 0, 224, 1),
(225, 1, 225, 1),
(226, 16, 226, 1),
(227, 10, 227, 1),
(228, 10, 228, 1),
(229, 3, 229, 1),
(230, 5, 230, 1),
(231, 0, 231, 1),
(232, 1, 232, 1),
(233, 14, 233, 1),
(234, 1, 234, 1),
(235, 37, 235, 1),
(236, 31, 236, 1),
(237, 17, 237, 1),
(238, 67, 238, 1),
(239, 9, 239, 1),
(240, 11, 240, 1),
(241, 7, 241, 1),
(242, 7, 242, 1),
(243, 4, 243, 1),
(244, 17, 244, 1),
(245, 0, 245, 1),
(246, 4, 246, 1),
(247, 19, 247, 1),
(248, 4, 248, 1),
(249, 4, 249, 1),
(250, 1, 250, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'core', 'invoice'),
(8, 'core', 'packingitem'),
(9, 'core', 'packingtask'),
(10, 'core', 'payment'),
(11, 'core', 'product'),
(12, 'core', 'reseller'),
(13, 'core', 'resellerprice'),
(14, 'core', 'returndetail'),
(15, 'core', 'returnheader'),
(16, 'core', 'stockmovement'),
(17, 'core', 'transaction'),
(18, 'core', 'transactiondetail'),
(19, 'core', 'variant'),
(20, 'core', 'warehouse'),
(21, 'core', 'warehousestock'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-02-22 13:15:13.115173'),
(2, 'auth', '0001_initial', '2026-02-22 13:15:13.401564'),
(3, 'admin', '0001_initial', '2026-02-22 13:15:13.478273'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-02-22 13:15:13.486926'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-02-22 13:15:13.496447'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-02-22 13:15:13.543717'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-02-22 13:15:13.571802'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-02-22 13:15:13.596332'),
(9, 'auth', '0004_alter_user_username_opts', '2026-02-22 13:15:13.603919'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-02-22 13:15:13.630147'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-02-22 13:15:13.631455'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-02-22 13:15:13.640073'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-02-22 13:15:13.651805'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-02-22 13:15:13.663018'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-02-22 13:15:13.687032'),
(16, 'auth', '0011_update_proxy_permissions', '2026-02-22 13:15:13.696512'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-02-22 13:15:13.709071'),
(18, 'core', '0001_initial', '2026-02-22 13:15:14.449599'),
(19, 'core', '0002_reseller_user', '2026-02-22 13:15:14.486358'),
(20, 'core', '0003_packingtask_packingitem', '2026-02-22 13:15:14.622685'),
(21, 'sessions', '0001_initial', '2026-02-22 13:15:14.646433');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('help4y89at9lj2icy7lczr4lob4nzgwh', '.eJxVjMsOwiAQRf-FtSG8KS7d-w1kYAapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKM7MwkO_1uCfKD2g7wDu3Wee5tXebEd4UfdPBrR3peDvfvoMKo33pyBicLkoJDVyTJrBRpoZJ3iYoR3lgQCbUiEEGTBS2DR6-LkyGBK-z9AdxvN84:1vu9N2:QSlA--O8PNSMt526fmr_3khoJk6NOcpO6H1gh_It11E', '2026-03-08 13:19:36.225838'),
('wjuck3dzyl2fiuqsq2pa6rmi7gx7v3iw', '.eJxVjMsOwiAQRf-FtSG8KS7d-w1kYAapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKM7MwkO_1uCfKD2g7wDu3Wee5tXebEd4UfdPBrR3peDvfvoMKo33pyBicLkoJDVyTJrBRpoZJ3iYoR3lgQCbUiEEGTBS2DR6-LkyGBK-z9AdxvN84:1vuAOT:-4P-TNWbvLnv3Htb3ZHXefMsplcQGj2aD6Cy4_Bk1Ts', '2026-03-08 14:25:09.060950');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `core_invoice`
--
ALTER TABLE `core_invoice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_invoice_reseller_id_22e25f67_fk_core_reseller_id` (`reseller_id`),
  ADD KEY `core_invoice_transaction_id_a80b1b50_fk_core_transaction_id` (`transaction_id`);

--
-- Indexes for table `core_packingitem`
--
ALTER TABLE `core_packingitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_packingitem_variant_id_fa68f12f_fk_core_variant_id` (`variant_id`),
  ADD KEY `core_packingitem_packing_task_id_6a0efbeb_fk_core_packingtask_id` (`packing_task_id`);

--
-- Indexes for table `core_packingtask`
--
ALTER TABLE `core_packingtask`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_packingtask_user_id_13533f1c_fk_auth_user_id` (`user_id`),
  ADD KEY `core_packingtask_warehouse_id_6ed66d7a_fk_core_warehouse_id` (`warehouse_id`);

--
-- Indexes for table `core_payment`
--
ALTER TABLE `core_payment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_payment_invoice_id_6807b035_fk_core_invoice_id` (`invoice_id`),
  ADD KEY `core_payment_reseller_id_a304e93c_fk_core_reseller_id` (`reseller_id`);

--
-- Indexes for table `core_product`
--
ALTER TABLE `core_product`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `core_reseller`
--
ALTER TABLE `core_reseller`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `core_resellerprice`
--
ALTER TABLE `core_resellerprice`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_resellerprice_reseller_id_variant_id_30d69dfb_uniq` (`reseller_id`,`variant_id`),
  ADD KEY `core_resellerprice_variant_id_3134aedb_fk_core_variant_id` (`variant_id`);

--
-- Indexes for table `core_returndetail`
--
ALTER TABLE `core_returndetail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_returndetail_return_header_id_99ff2d98_fk_core_retu` (`return_header_id`),
  ADD KEY `core_returndetail_variant_id_aa52bded_fk_core_variant_id` (`variant_id`);

--
-- Indexes for table `core_returnheader`
--
ALTER TABLE `core_returnheader`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_returnheader_invoice_id_7733149b_fk_core_invoice_id` (`invoice_id`),
  ADD KEY `core_returnheader_reseller_id_ac0db5bc_fk_core_reseller_id` (`reseller_id`),
  ADD KEY `core_returnheader_warehouse_id_32d96b01_fk_core_warehouse_id` (`warehouse_id`);

--
-- Indexes for table `core_stockmovement`
--
ALTER TABLE `core_stockmovement`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_stockmovement_user_id_4bec3676_fk_auth_user_id` (`user_id`),
  ADD KEY `core_stockmovement_variant_id_69e12a57_fk_core_variant_id` (`variant_id`),
  ADD KEY `core_stockmovement_warehouse_id_bb14c8e5_fk_core_warehouse_id` (`warehouse_id`);

--
-- Indexes for table `core_transaction`
--
ALTER TABLE `core_transaction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_transaction_reseller_id_3f4be451_fk_core_reseller_id` (`reseller_id`),
  ADD KEY `core_transaction_user_id_9d7207a3_fk_auth_user_id` (`user_id`),
  ADD KEY `core_transaction_warehouse_id_4f788a2f_fk_core_warehouse_id` (`warehouse_id`);

--
-- Indexes for table `core_transactiondetail`
--
ALTER TABLE `core_transactiondetail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_transactiondeta_transaction_id_36056984_fk_core_tran` (`transaction_id`),
  ADD KEY `core_transactiondetail_variant_id_5fb39c41_fk_core_variant_id` (`variant_id`);

--
-- Indexes for table `core_variant`
--
ALTER TABLE `core_variant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sku` (`sku`),
  ADD KEY `core_variant_product_id_d6e437a8_fk_core_product_id` (`product_id`);

--
-- Indexes for table `core_warehouse`
--
ALTER TABLE `core_warehouse`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `core_warehousestock`
--
ALTER TABLE `core_warehousestock`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_warehousestock_warehouse_id_variant_id_5c94f027_uniq` (`warehouse_id`,`variant_id`),
  ADD KEY `core_warehousestock_variant_id_699d385e_fk_core_variant_id` (`variant_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_invoice`
--
ALTER TABLE `core_invoice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_packingitem`
--
ALTER TABLE `core_packingitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_packingtask`
--
ALTER TABLE `core_packingtask`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_payment`
--
ALTER TABLE `core_payment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_product`
--
ALTER TABLE `core_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `core_reseller`
--
ALTER TABLE `core_reseller`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `core_resellerprice`
--
ALTER TABLE `core_resellerprice`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_returndetail`
--
ALTER TABLE `core_returndetail`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_returnheader`
--
ALTER TABLE `core_returnheader`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_stockmovement`
--
ALTER TABLE `core_stockmovement`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_transaction`
--
ALTER TABLE `core_transaction`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_transactiondetail`
--
ALTER TABLE `core_transactiondetail`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_variant`
--
ALTER TABLE `core_variant`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=251;

--
-- AUTO_INCREMENT for table `core_warehouse`
--
ALTER TABLE `core_warehouse`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `core_warehousestock`
--
ALTER TABLE `core_warehousestock`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=251;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `core_invoice`
--
ALTER TABLE `core_invoice`
  ADD CONSTRAINT `core_invoice_reseller_id_22e25f67_fk_core_reseller_id` FOREIGN KEY (`reseller_id`) REFERENCES `core_reseller` (`id`),
  ADD CONSTRAINT `core_invoice_transaction_id_a80b1b50_fk_core_transaction_id` FOREIGN KEY (`transaction_id`) REFERENCES `core_transaction` (`id`);

--
-- Constraints for table `core_packingitem`
--
ALTER TABLE `core_packingitem`
  ADD CONSTRAINT `core_packingitem_packing_task_id_6a0efbeb_fk_core_packingtask_id` FOREIGN KEY (`packing_task_id`) REFERENCES `core_packingtask` (`id`),
  ADD CONSTRAINT `core_packingitem_variant_id_fa68f12f_fk_core_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `core_variant` (`id`);

--
-- Constraints for table `core_packingtask`
--
ALTER TABLE `core_packingtask`
  ADD CONSTRAINT `core_packingtask_user_id_13533f1c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `core_packingtask_warehouse_id_6ed66d7a_fk_core_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `core_warehouse` (`id`);

--
-- Constraints for table `core_payment`
--
ALTER TABLE `core_payment`
  ADD CONSTRAINT `core_payment_invoice_id_6807b035_fk_core_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `core_invoice` (`id`),
  ADD CONSTRAINT `core_payment_reseller_id_a304e93c_fk_core_reseller_id` FOREIGN KEY (`reseller_id`) REFERENCES `core_reseller` (`id`);

--
-- Constraints for table `core_reseller`
--
ALTER TABLE `core_reseller`
  ADD CONSTRAINT `core_reseller_user_id_76c75bb4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `core_resellerprice`
--
ALTER TABLE `core_resellerprice`
  ADD CONSTRAINT `core_resellerprice_reseller_id_5f3ab09e_fk_core_reseller_id` FOREIGN KEY (`reseller_id`) REFERENCES `core_reseller` (`id`),
  ADD CONSTRAINT `core_resellerprice_variant_id_3134aedb_fk_core_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `core_variant` (`id`);

--
-- Constraints for table `core_returndetail`
--
ALTER TABLE `core_returndetail`
  ADD CONSTRAINT `core_returndetail_return_header_id_99ff2d98_fk_core_retu` FOREIGN KEY (`return_header_id`) REFERENCES `core_returnheader` (`id`),
  ADD CONSTRAINT `core_returndetail_variant_id_aa52bded_fk_core_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `core_variant` (`id`);

--
-- Constraints for table `core_returnheader`
--
ALTER TABLE `core_returnheader`
  ADD CONSTRAINT `core_returnheader_invoice_id_7733149b_fk_core_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `core_invoice` (`id`),
  ADD CONSTRAINT `core_returnheader_reseller_id_ac0db5bc_fk_core_reseller_id` FOREIGN KEY (`reseller_id`) REFERENCES `core_reseller` (`id`),
  ADD CONSTRAINT `core_returnheader_warehouse_id_32d96b01_fk_core_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `core_warehouse` (`id`);

--
-- Constraints for table `core_stockmovement`
--
ALTER TABLE `core_stockmovement`
  ADD CONSTRAINT `core_stockmovement_user_id_4bec3676_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `core_stockmovement_variant_id_69e12a57_fk_core_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `core_variant` (`id`),
  ADD CONSTRAINT `core_stockmovement_warehouse_id_bb14c8e5_fk_core_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `core_warehouse` (`id`);

--
-- Constraints for table `core_transaction`
--
ALTER TABLE `core_transaction`
  ADD CONSTRAINT `core_transaction_reseller_id_3f4be451_fk_core_reseller_id` FOREIGN KEY (`reseller_id`) REFERENCES `core_reseller` (`id`),
  ADD CONSTRAINT `core_transaction_user_id_9d7207a3_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `core_transaction_warehouse_id_4f788a2f_fk_core_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `core_warehouse` (`id`);

--
-- Constraints for table `core_transactiondetail`
--
ALTER TABLE `core_transactiondetail`
  ADD CONSTRAINT `core_transactiondeta_transaction_id_36056984_fk_core_tran` FOREIGN KEY (`transaction_id`) REFERENCES `core_transaction` (`id`),
  ADD CONSTRAINT `core_transactiondetail_variant_id_5fb39c41_fk_core_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `core_variant` (`id`);

--
-- Constraints for table `core_variant`
--
ALTER TABLE `core_variant`
  ADD CONSTRAINT `core_variant_product_id_d6e437a8_fk_core_product_id` FOREIGN KEY (`product_id`) REFERENCES `core_product` (`id`);

--
-- Constraints for table `core_warehousestock`
--
ALTER TABLE `core_warehousestock`
  ADD CONSTRAINT `core_warehousestock_variant_id_699d385e_fk_core_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `core_variant` (`id`),
  ADD CONSTRAINT `core_warehousestock_warehouse_id_b5b282ed_fk_core_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `core_warehouse` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
