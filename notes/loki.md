
> https://community.grafana.com/t/how-does-one-test-loki-storage-is-correctly-configured/132921
```bash
curl -X POST http://localhost:3100/loki/api/v1/push -H "Content-Type: application/json" -d @log.json
```

log.json
```json
{
    "streams": [
      {
        "stream": {
          "label": "foo"
        },
        "values": [
            [ "1741011809000000000", "Foo bar baz" ],
            [ "1741011809000000001", "Biz baz boz" ]
        ]
      }
    ]
  }
```

```bash
curl -G -s  "http://localhost:3100/loki/api/v1/query"   --data-urlencode 'query=sum(rate({label="foo"}[90m])) by (level)' | jq > query.json
```