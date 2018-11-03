--
-- Table structure for table `author_analysis`
--

CREATE TABLE IF NOT EXISTS `author_analysis` (
  `author` varchar(50) COLLATE utf8_bin NOT NULL,
  `newssite` varchar(20) COLLATE utf8_bin NOT NULL,
  `avg_nr_words` float DEFAULT NULL,
  `avg_wordlen` float DEFAULT NULL,
  `avg_words_gt6` float DEFAULT NULL,
  `avg_personal` float DEFAULT NULL,
  `avg_collective` float DEFAULT NULL,
  `indegree` float DEFAULT NULL,
  `indegree_centrality` float DEFAULT NULL,
  `outdegree` float DEFAULT NULL,
  `outdegree_centrality` float DEFAULT NULL,
  `degree` float DEFAULT NULL,
  `degree_centrality` float DEFAULT NULL,
  `avg_shared` float DEFAULT NULL,
  `pagerank` float DEFAULT NULL,
  `pagerank_weighted` float DEFAULT NULL,
  `nr_posts` int(11) DEFAULT NULL,
  `hub_score` float DEFAULT NULL,
  `authority_score` float DEFAULT NULL,
  `betweeness_centrality` float DEFAULT NULL,
  `closeness_centrality` float DEFAULT NULL,
  `clustering_coef` float DEFAULT NULL,
  `eccentricity` float DEFAULT NULL,
  `constraint` float DEFAULT NULL,
  `polarity_arousal` float DEFAULT NULL,
  `polarity_valence` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `author_analysis`
--
ALTER TABLE `author_analysis`
 ADD PRIMARY KEY (`author`,`newssite`);