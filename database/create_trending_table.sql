CREATE TABLE trending_keywords AS
WITH five_year_counts AS (
    SELECT k.name as keyword, p.year, COUNT(*) AS pub_count
    FROM keyword k
    JOIN Publication_Keyword pk ON k.id = pk.keyword_id
    JOIN publication p ON pk.publication_id = p.ID
    WHERE p.year BETWEEN 2016 AND 2021
    GROUP BY k.name, p.year
),

avg_counts AS (
    SELECT keyword, AVG(pub_count) AS avg_pub_count
    FROM five_year_counts
    GROUP BY keyword
),

top_keywords AS (
    SELECT keyword
    FROM avg_counts
    ORDER BY avg_pub_count DESC
    LIMIT 10
)

SELECT k.name, p.year, COUNT(*) AS pub_count
FROM keyword k
JOIN top_keywords top ON k.name = top.keyword
JOIN Publication_Keyword pk ON k.id = pk.keyword_id
JOIN publication p ON pk.publication_id = p.ID
GROUP BY k.name, p.year
ORDER BY k.name, p.year;
