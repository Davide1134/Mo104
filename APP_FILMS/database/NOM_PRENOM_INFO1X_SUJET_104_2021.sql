-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: zzzptzptz_NOM_PRENOM_INFO1X_SUJET_104_2021

-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS davidepetronio_info1b_104;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS davidepetronio_info1b_104;

-- Utilisation de cette base de donnée

USE davidepetronio_info1b_104;

--
-- Database: `davidepetronio_info1b_104`
--


--
-- Table structure for table `t_avoir_boisson`
--

CREATE TABLE `t_avoir_boisson` (
  `Id_avoir_boisson` int(11) NOT NULL,
  `Fk_stock` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `t_avoir_fromage`
--

CREATE TABLE `t_avoir_fromage` (
  `Id_avoir_fromage` int(11) NOT NULL,
  `Fk_stock` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `t_avoir_viande`
--

CREATE TABLE `t_avoir_viande` (
  `Id_avoir_viande` int(11) NOT NULL,
  `Fk_Stock` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `t_boisson`
--

CREATE TABLE `t_boisson` (
  `Id_boisson` int(11) NOT NULL,
  `fk_tp_boisson` int(11) NOT NULL,
  `Prix_boisson` int(11) NOT NULL,
  `Quantite_boisson` int(11) NOT NULL,
  `Date_achat_boisson` date NOT NULL,
  `Date_peremption_boisson` date NOT NULL,
  `Marque` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_boisson`
--

INSERT INTO `t_boisson` (`Id_boisson`, `fk_tp_boisson`, `Prix_boisson`, `Quantite_boisson`, `Date_achat_boisson`, `Date_peremption_boisson`, `Marque`) VALUES
(1, 1, 10, 20, '2021-06-25', '2022-06-30', 'oasis');

-- --------------------------------------------------------

--
-- Table structure for table `t_fromage`
--

CREATE TABLE `t_fromage` (
  `Id_fromage` int(11) NOT NULL,
  `Fk_avoir_fromage` int(11) NOT NULL,
  `Prix_fromage` int(11) NOT NULL,
  `Quantite_fromage` int(11) NOT NULL,
  `Date_achat_fromage` int(11) NOT NULL,
  `Date_peremption_fromage` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `t_personne`
--

CREATE TABLE `t_personne` (
  `Id_personne` int(11) NOT NULL,
  `Nom_personne` varchar(50) NOT NULL,
  `Mdp_personne` varchar(50) NOT NULL,
  `Email_personne` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_personne`
--

INSERT INTO `t_personne` (`Id_personne`, `Nom_personne`, `Mdp_personne`, `Email_personne`) VALUES
(1, 'Fgavdfgdfbdgb', 'Jgvhcfhcfgcfh', 'Hfjehjkeg@gmail.com'),
(2, 'hzth', 'tzhtzhtthztzh', 'thf@gmail.com'),
(3, 'Daniel', 'Nul12345', 'agra@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `t_stock`
--

CREATE TABLE `t_stock` (
  `Id_stock` int(11) NOT NULL,
  `Fk_personne` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `t_type_boisson`
--

CREATE TABLE `t_type_boisson` (
  `Id_type_boisson` int(11) NOT NULL,
  `Type_boisson` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_type_boisson`
--

INSERT INTO `t_type_boisson` (`Id_type_boisson`, `Type_boisson`) VALUES
(1, '1L'),
(2, 'test');

-- --------------------------------------------------------

--
-- Table structure for table `t_type_fromage`
--

CREATE TABLE `t_type_fromage` (
  `Id_type_fromage` int(11) NOT NULL,
  `Fk_fromage` int(11) NOT NULL,
  `Type_fromage` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `t_type_viande`
--

CREATE TABLE `t_type_viande` (
  `id_type_viande` int(11) NOT NULL,
  `Fk_viande` int(11) NOT NULL,
  `Type_viande` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `t_viande`
--

CREATE TABLE `t_viande` (
  `Id_viande` int(11) NOT NULL,
  `Fk_avoir_viande` int(11) NOT NULL,
  `Prix_viande` int(11) NOT NULL,
  `Quantite_viande` int(11) NOT NULL,
  `Date_achat_viande` date NOT NULL,
  `Date_peremption_viande` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `t_avoir_boisson`
--
ALTER TABLE `t_avoir_boisson`
  ADD PRIMARY KEY (`Id_avoir_boisson`),
  ADD KEY `Fk_stock` (`Fk_stock`);

--
-- Indexes for table `t_avoir_fromage`
--
ALTER TABLE `t_avoir_fromage`
  ADD PRIMARY KEY (`Id_avoir_fromage`);

--
-- Indexes for table `t_avoir_viande`
--
ALTER TABLE `t_avoir_viande`
  ADD PRIMARY KEY (`Id_avoir_viande`);

--
-- Indexes for table `t_boisson`
--
ALTER TABLE `t_boisson`
  ADD PRIMARY KEY (`Id_boisson`),
  ADD KEY `fk_tp_boisson` (`fk_tp_boisson`);

--
-- Indexes for table `t_fromage`
--
ALTER TABLE `t_fromage`
  ADD PRIMARY KEY (`Id_fromage`),
  ADD UNIQUE KEY `Fk_avoir_fromage` (`Fk_avoir_fromage`);

--
-- Indexes for table `t_personne`
--
ALTER TABLE `t_personne`
  ADD PRIMARY KEY (`Id_personne`);

--
-- Indexes for table `t_stock`
--
ALTER TABLE `t_stock`
  ADD PRIMARY KEY (`Id_stock`),
  ADD KEY `Fk_personne` (`Fk_personne`);

--
-- Indexes for table `t_type_boisson`
--
ALTER TABLE `t_type_boisson`
  ADD PRIMARY KEY (`Id_type_boisson`);

--
-- Indexes for table `t_type_fromage`
--
ALTER TABLE `t_type_fromage`
  ADD PRIMARY KEY (`Id_type_fromage`);

--
-- Indexes for table `t_type_viande`
--
ALTER TABLE `t_type_viande`
  ADD PRIMARY KEY (`id_type_viande`),
  ADD UNIQUE KEY `Fk_viande` (`Fk_viande`);

--
-- Indexes for table `t_viande`
--
ALTER TABLE `t_viande`
  ADD PRIMARY KEY (`Id_viande`),
  ADD KEY `Fk_avoir_viande` (`Fk_avoir_viande`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `t_boisson`
--
ALTER TABLE `t_boisson`
  MODIFY `Id_boisson` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `t_personne`
--
ALTER TABLE `t_personne`
  MODIFY `Id_personne` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `t_type_boisson`
--
ALTER TABLE `t_type_boisson`
  MODIFY `Id_type_boisson` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `t_type_viande`
--
ALTER TABLE `t_type_viande`
  MODIFY `id_type_viande` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `t_avoir_boisson`
--
ALTER TABLE `t_avoir_boisson`
  ADD CONSTRAINT `t_avoir_boisson_ibfk_1` FOREIGN KEY (`Fk_stock`) REFERENCES `t_stock` (`Id_stock`);

--
-- Constraints for table `t_boisson`
--
ALTER TABLE `t_boisson`
  ADD CONSTRAINT `t_boisson_ibfk_1` FOREIGN KEY (`fk_tp_boisson`) REFERENCES `t_type_boisson` (`Id_type_boisson`);

--
-- Constraints for table `t_fromage`
--
ALTER TABLE `t_fromage`
  ADD CONSTRAINT `t_fromage_ibfk_1` FOREIGN KEY (`Fk_avoir_fromage`) REFERENCES `t_type_fromage` (`Id_type_fromage`);

--
-- Constraints for table `t_viande`
--
ALTER TABLE `t_viande`
  ADD CONSTRAINT `t_viande_ibfk_1` FOREIGN KEY (`Fk_avoir_viande`) REFERENCES `t_type_viande` (`id_type_viande`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;