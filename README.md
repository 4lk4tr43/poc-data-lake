# poc-data-lake

---

### Start dev environment

[Tilt.dev](https://tilt.dev)

```bash
tilt up
```

All the services should start up automatically. You should see the tilt.dev ui
under [http://localhost:10350](http://localhost:10350/)

---

### Data lake structure

```
------------------                          -----------------
│ Data ingestion │                          │ Processing    │
------------------                          -----------------
			------------------
			│ Storage        │
			------------------
------------------                          -----------------
│ Analytics      │                          │ Monitoring    │
------------------                          -----------------

```

TODO

- storage is central -> lots of infrastructure needs and platform maintenance

- Big cloud providers

|           |AWS|Azure|Google|Cloudera|Databrick|Snowflake|
|-----------|---|-----|------|--------|---------|---------|
|multi cloud|   |     |      |   X    |    X    |    X    |
|hive       | X |  X  |   X  |   X    |         |         |
|spark      |   |     |   X  |   X    |    X    |         |

TODO

- Processors AWS EMR, Azure HDInsigh/Synapse, Google Dataproc/Flow,CDP Data Engineering, Delta Engine, Snowflake
- 3rd party BI/ETL TOOLS ???

---

### Directory structure

```
├── apps
│ └── collectors                # applications which collect data
│     └── weather-tracking      # collects data about temperature and city name (weather_tracking-* containers)
│         │                     # - postgres-db root:password@localhost:26001
│         ├── server            # python script polling open weather api every 30 seconds
│         │ ├── src
│         │ └── static
│         └── web               # Webfront localhost:26000
│             ├── src
│             │ └── routes
│             └── static
├── data-lakes                  # data lake services
│ └── hadoop                    # standard hdfs hadoop implementation
│     ├── base
│     ├── datanode
│     ├── historyserver
│     ├── namenode              
│     ├── nginx
│     ├── nodemanager
│     ├── resourcemanager
│     └── submit
└── service-descriptions
```