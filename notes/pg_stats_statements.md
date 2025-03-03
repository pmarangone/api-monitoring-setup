Filter INSERT, SELECT, UPDATE, and DELETE
```sql
SELECT
  -- (total_exec_time / 1000 / 60) AS total_min,
  TO_CHAR((total_exec_time / 1000 / 60), 'FM999999.000000000000') AS total_min_formatted,
  mean_exec_time AS avg_ms,
  calls,
  query
FROM pg_stat_statements
WHERE query ILIKE '%fastapi_device%'
  AND (
    query ILIKE 'INSERT%' OR
    query ILIKE 'SELECT%' OR
    query ILIKE 'UPDATE%' OR
    query ILIKE 'DELETE%'
  )
ORDER BY 3 DESC
LIMIT 500;

```
