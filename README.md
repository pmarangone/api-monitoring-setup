# Monitoring template for FastAPI
 
## Objectives

### Tracking - Prometheus
- [x] Database operations duration
- [x] API requests duration
- [x] API request/response size

### Monitoring - Grafana
- [x] API
- [x] Database
- [x] System
- [x] Logs

### Logging - Loki

### Tools
- [x] Jmeter for benchmark test
- [x] Postman collection 

## Run it
- Ensure you have `.env` configured. See `.env.example`
- Run `schema.sql` on your Postgres database
- Run `docker compose build && docker compose up -d`

## Flow

- Ensure Loki is working, http://localhost:3100/ready
- Ensure Prometheus is scrapping the server, http://localhost:9090/targets
- Import dashboard to grafana, http://localhost:3000/dashboard/import
- Benchmark server with Jmeter. See jmeter_benchmark/ 
- Monitor database schemas with pg_stats_statements. See notes/pg_stats_statements