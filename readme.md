
# PgRolesExporter

### Polls Postres clusters for active roles actually presented on postgres databases. Exports polled data and roles poll statistics in prometheus compatible format.

## Exported metrics:

    # HELP exporter_info Postgres clusters active roles poller
    # TYPE exporter_info gauge
    exporter_info{application="psql_roles_exporter",component="psql_roles_exporter",environment="production"} 1.0

    # HELP inventory_count Amount of clusters in inventory to be polled
    # TYPE inventory_count gauge
    inventory_count{application="psql_roles_exporter",component="psql_roles_exporter",environment="production"} 7.0

    # HELP roles_count Amount of unique roles on all inventoried databases
    # TYPE roles_count gauge
    roles_count{application="psql_roles_exporter",component="psql_roles_exporter",environment="production"} 2.0

    # HELP success_polls Amount of successfully polled clusters
    # TYPE success_polls gauge
    success_polls{application="psql_roles_exporter",component="psql_roles_exporter",environment="production"} 6.0
    
    # HELP failed_polls Amount of cluster poll failures
    # TYPE failed_polls gauge
    failed_polls{address="0.0.0.0",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_7",environment="production",instance="master.dc-nsk-postgres-07-cluster.service.contoso.tech"} 1.0
    
    # HELP postgres_roles Active postgres roles on clusters right now
    # TYPE postgres_roles gauge
    postgres_roles{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",role="postgres"} 1.0
    postgres_roles{address="172.19.95.244",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",role="user"} 1.0
    postgres_roles{address="172.19.95.245",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_2",environment="production",instance="master.dc-nsk-postgres-02-cluster.service.contoso.tech",role="user"} 1.0
    postgres_roles{address="172.19.95.246",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_3",environment="production",instance="master.dc-nsk-postgres-03-cluster.service.contoso.tech",role="user"} 1.0
    postgres_roles{address="172.19.95.247",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_4",environment="production",instance="master.dc-nsk-postgres-04-cluster.service.contoso.tech",role="user"} 1.0
    postgres_roles{address="172.19.95.248",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_5",environment="production",instance="master.dc-nsk-postgres-05-cluster.service.contoso.tech",role="user"} 1.0
    postgres_roles{address="172.19.95.249",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_6",environment="production",instance="master.dc-nsk-postgres-06-cluster.service.contoso.tech",role="user"} 1.0

    # HELP poll_statistics Database poll statistics
    # TYPE poll_statistics histogram
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="0.005"} 0.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="0.01"} 41.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="0.025"} 60.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="0.05"} 70.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="0.075"} 70.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="0.1"} 70.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="0.25"} 70.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="0.5"} 70.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="0.75"} 70.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="1.0"} 70.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="2.5"} 70.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="5.0"} 71.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="7.5"} 71.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="10.0"} 71.0
    poll_statistics_bucket{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech",le="+Inf"} 71.0
    poll_statistics_count{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech"} 71.0
    poll_statistics_sum{address="172.19.95.243",application="psql_roles_exporter",bouncer="pgbouncer.service.contoso.tech",component="psql_roles_exporter",db_name="test_db_1",environment="production",instance="master.dc-nsk-postgres-01-cluster.service.contoso.tech"} 5.209999999999983
    ...