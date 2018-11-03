SET @alg_id = 34;
INSERT INTO algorithm_color 
(algorithm_id, color, min_threshold, max_threshold) 
VALUES (@alg_id, '#2ca02c', 0.6667, 1.1),
       (@alg_id, '#ffbb78', 0.3334, 0.6667),
       (@alg_id, '#d62728', 0,      0.3334);
       
SELECT algorithm_id, algorithm.name, min(result.value), avg(result.value), max(result.value) 
  FROM `algorithm`, result
 WHERE result.algorithm_id = algorithm.id
  GROUP BY algorithm_id, algorithm.name       