import boto3
import time

# Instantiate a boto3 client for RDS

rds = boto3.client("rds")

# User defined variables

username = "dctuser1"
password = "2Lxu1htKPUAH23"
db_subnet_group = "payments-db-subnet-group"
db_cluster_id = "rds-hol-cluster"

# Create the DB cluster

try:
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
    print(f"The DB cluster named '{db_cluster_id}' already exists. Skipping creation.")
except rds.exceptions.DBClusterNotFoundFault:
    response = rds.create_db_cluster(
        Engine="aurora-mysql",
        EngineVersion="8.0.mysql_aurora.3.10.1",
        DBClusterIdentifier=db_cluster_id,
        MasterUsername=username,
        MasterUserPassword=password,
        DatabaseName="rds_hol_db",
        DBSubnetGroupName=db_subnet_group,
        # EngineMode="serverless",
        EnableHttpEndpoint=True,
        ServerlessV2ScalingConfiguration={
            "MinCapacity": 0,  # Minimum ACU
            "MaxCapacity": 8,  # Maximum ACU
            "SecondsUntilAutoPause": 300,  # Pause after 5 minutes of inactivity
        },
    )
    print(f"The DB cluster named '{db_cluster_id}' has been created.")

    # Wait for the DB cluster to become available
    while True:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
        status = response["DBClusters"][0]["Status"]
        print(f"The status of the cluster is '{status}'")
        if status == "available":
            break

        print("Waiting for the DB Cluster to become available...")
        time.sleep(40)
