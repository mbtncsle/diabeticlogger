IF OBJECT_ID('tempdb.dbo.#BG_DIFF') IS NOT NULL
    DROP TABLE #BG_DIFF;

SELECT af.RecordDate,
       af.Meal,
       DIFF = af.Reading - bef.Reading
INTO #BG_DIFF
FROM dbo.BG AS bef
    INNER JOIN dbo.BG AS af
        ON af.RecordDate = bef.RecordDate
           AND af.Meal = bef.Meal
           AND af.Mark <> bef.Mark
WHERE bef.Mark = 'BEFORE'
      AND af.Mark = 'AFTER';

IF OBJECT_ID('tempdb.dbo.#M_DIFF') IS NOT NULL
    DROP TABLE #M_DIFF;

SELECT m.RecordDate,
       m.Meal,
       --TotalCarbsAvg = AVG(m.TotalCarbs)
       m.TotalCarbs
INTO #M_DIFF
FROM dbo.M AS m;
--GROUP BY m.Meal,m.RecordDate




SELECT *,
       Notes = CASE
                   WHEN DIFF = 0 THEN
                       CONCAT(
                                 'For ',
                                 bd.Meal,
                                 ', even though your carb intake was ',
                                 bd.DIFF,
                                 ' your change in blood glucose was ',
                                 bd.DIFF,
                                 ' mg/dl'
                             )
                   WHEN DIFF > 0 THEN
                       CONCAT(
                                 'For ',
                                 bd.Meal,
                                 ', you consumed ',
                                 md.TotalCarbs,
                                 ' carbohydrates and that increased your blood glucose by ',
                                 bd.DIFF,
                                 ' mg/dl'
                             )
               END,
       ROUND(DIFF / md.TotalCarbs, 2)
FROM #BG_DIFF AS bd
    INNER JOIN #M_DIFF AS md
        ON md.RecordDate = bd.RecordDate
           AND md.Meal = bd.Meal;



SELECT bd.Meal,
       BG_AVG = AVG(bd.DIFF),
       CARB_AVG = AVG(md.TotalCarbs),
       ROUND(AVG(CAST(DIFF AS FLOAT) / CAST(md.TotalCarbs AS FLOAT)), 2)
FROM #BG_DIFF AS bd
    INNER JOIN #M_DIFF AS md
        ON md.RecordDate = bd.RecordDate
           AND md.Meal = bd.Meal
GROUP BY bd.Meal;
--GROUP BY CAST(DIFF AS FLOAT) / CAST(md.TotalCarbs AS FLOAT);


