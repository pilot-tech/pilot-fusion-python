import os
import re
import ast
import importlib
from datetime import datetime
from abc import ABC, abstractmethod

diagrams_data = {
    "diagrams.onprem.aggregator": ["Fluentd", "Vector"],
    "diagrams.onprem.analytics": [
        "Beam", "Databricks", "Dbt", "Dremio", "Flink", "Hadoop", "Hive", 
        "Metabase", "Norikra", "Powerbi", "Presto", "Singer", "Spark", 
        "Storm", "Superset", "Tableau"
    ],
    "diagrams.onprem.auth": ["Boundary", "BuzzfeedSso", "Oauth2Proxy"],
    "diagrams.onprem.cd": ["Spinnaker", "TektonCli", "Tekton"],
    "diagrams.onprem.certificates": ["CertManager", "LetsEncrypt"],
    "diagrams.onprem.ci": [
        "Circleci", "Concourseci", "Droneci", "GithubActions", "Gitlabci", 
        "Jenkins", "Teamcity", "Travisci", "Zuulci"
    ],
    "diagrams.onprem.client": ["Client", "User", "Users"],
    "diagrams.onprem.compute": ["Nomad", "Server"],
    "diagrams.onprem.container": [
        "Containerd", "Crio", "Docker", "Firecracker", "Gvisor", "K3S", 
        "Lxc", "Rkt"
    ],
    "diagrams.onprem.database": [
        "Cassandra", "Clickhouse", "Cockroachdb", "Couchbase", "Couchdb", 
        "Dgraph", "Druid", "Hbase", "Influxdb", "Janusgraph", "Mariadb", 
        "Mongodb", "Mssql", "Mysql", "Neo4J", "Oracle", "Postgresql", 
        "Scylla"
    ],
    "diagrams.onprem.dns": ["Coredns", "Powerdns"],
    "diagrams.onprem.etl": ["Embulk"],
    "diagrams.onprem.gitops": ["Argocd", "Flagger", "Flux"],
    "diagrams.onprem.groupware": ["Nextcloud"],
    "diagrams.onprem.iac": ["Ansible", "Atlantis", "Awx", "Puppet", "Terraform"],
    "diagrams.onprem.identity": ["Dex"],
    "diagrams.onprem.inmemory": ["Aerospike", "Hazelcast", "Memcached", "Redis"],
    "diagrams.onprem.logging": ["Fluentbit", "Graylog", "Loki", "Rsyslog", "SyslogNg"],
    "diagrams.onprem.mlops": ["Mlflow", "Polyaxon"],
    "diagrams.onprem.monitoring": [
        "Cortex", "Datadog", "Dynatrace", "Grafana", "Humio", "Nagios", 
        "Newrelic", "PrometheusOperator", "Prometheus", "Sentry", "Splunk", 
        "Thanos", "Zabbix"
    ],
    "diagrams.onprem.network": [
        "Ambassador", "Apache", "Bind9", "Caddy", "Consul", "Envoy", "Etcd", 
        "Glassfish", "Gunicorn", "Haproxy", "Internet", "Istio", "Jbossas", 
        "Jetty", "Kong", "Linkerd", "Nginx", "Ocelot", "OpenServiceMesh", 
        "Opnsense", "Pfsense", "Pomerium", "Powerdns", "Tomcat", "Traefik", 
        "Tyk", "Vyos", "Wildfly", "Yarp", "Zookeeper"
    ],
    "diagrams.onprem.proxmox": ["Pve"],
    "diagrams.onprem.queue": ["Activemq", "Celery", "Emqx", "Kafka", "Nats", "Rabbitmq", "Zeromq"],
    "diagrams.onprem.registry": ["Harbor", "Jfrog"],
    "diagrams.onprem.search": ["Solr"],
    "diagrams.onprem.security": ["Bitwarden", "Trivy", "Vault"],
    "diagrams.onprem.storage": ["CephOsd", "Ceph", "Glusterfs", "Portworx"],
    "diagrams.onprem.tracing": ["Jaeger"],
    "diagrams.onprem.vcs": ["Git", "Gitea", "Github", "Gitlab", "Svn"],
    "diagrams.onprem.workflow": ["Airflow", "Digdag", "Kubeflow", "Nifi"],
    "diagrams.aws.storage": [
        "Backup", "CloudendureDisasterRecovery", "EFSInfrequentaccessPrimaryBg", 
        "EFSStandardPrimaryBg", "ElasticBlockStoreEBSSnapshot", "ElasticBlockStoreEBSVolume", 
        "ElasticBlockStoreEBS", "ElasticFileSystemEFSFileSystem", "ElasticFileSystemEFS", 
        "FsxForLustre", "FsxForWindowsFileServer", "Fsx", "MultipleVolumesResource", 
        "S3GlacierArchive", "S3GlacierVault", "S3Glacier", "SimpleStorageServiceS3BucketWithObjects", 
        "SimpleStorageServiceS3Bucket", "SimpleStorageServiceS3Object", "SimpleStorageServiceS3", 
        "SnowFamilySnowballImportExport", "SnowballEdge", "Snowball", "Snowmobile", 
        "StorageGatewayCachedVolume", "StorageGatewayNonCachedVolume", 
        "StorageGatewayVirtualTapeLibrary", "StorageGateway", "Storage"
    ],

    "diagrams.gcp.analytics": ["Bigquery", "Dataflow", "Dataproc", "Datalab", "Pubsub","Composer","DataCatalog"],

    "diagrams.gcp.api" : ["Endpoints","APIGateway"],

    "diagrams.gcp.database" : ["Bigtable","Firestore","Memorystore","Spanner","SQL","Datastore"],

    "diagrams.gcp.compute" : ["AppEngine","ComputeEngine","KubernetesEngine","Functions","GPU"],

    "diagrams.gcp.devtools" : ["CodeForIntellij","Build","Code","IdePlugins","GradleAppEnginePlugin","ContainerRegistry","CloudToolsForIntelliJ","ContainerRegistry","MavenAppEnginePlugin","Scheduler","SourceRepositories","ToolsForEclipse","ToolsForVisualStudio"],

   "diagrams.gcp.network": [
    "Armor",
    "CDN",
    "DedicatedInterconnect",
    "DNS",
    "ExternalIpAddresses",
    "FirewallRules",
    "LoadBalancing",
    "NAT",
    "Network",
    "PartnerInterconnect",
    "PremiumNetworkTier",
    "Router",
    "Routes",
    "StandardNetworkTier",
    "TrafficDirector",
    "VirtualPrivateCloud",
    "VPN"
],

"diagrams.programming.flowchart": [
        "Action",
        "Collate",
        "Database",
        "Decision",
        "Delay",
        "Display",
        "Document",
        "InputOutput",
        "Inspection",
        "InternalStorage",
        "LoopLimit",
        "ManualInput",
        "ManualLoop",
        "Merge",
        "MultipleDocuments",
        "OffPageConnectorLeft",
        "OffPageConnectorRight",
        "Or",
        "PredefinedProcess",
        "Preparation",
        "Sort",
        "StartEnd",
        "StoredData",
        "SummingJunction"
    ],
    "diagrams.programming.framework": [
        "Angular",
        "Backbone",
        "Django",
        "Ember",
        "Fastapi", "FastAPI",  
        "Flask",
        "Flutter",
        "Graphql", "GraphQL", 
        "Laravel",
        "Micronaut",
        "Rails",
        "React",
        "Spring",
        "Starlette",
        "Svelte",
        "Vue"
    ],
    "diagrams.programming.language": [
        "Bash",
        "C",
        "Cpp",
        "Csharp",
        "Dart",
        "Elixir",
        "Erlang",
        "Go",
        "Java",
        "Javascript", "JavaScript",  
        "Kotlin",
        "Latex",
        "Matlab",
        "Nodejs", "NodeJS",  
        "Php", "PHP", 
        "Python",
        "R",
        "Ruby",
        "Rust",
        "Scala",
        "Swift",
        "Typescript", "TypeScript" 
    ],
    "diagrams.programming.runtime": [
        "Dapr"
    ],

      "diagrams.azure.analytics": [
    "AnalysisServices",
    "DataExplorerClusters",
    "DataFactories",
    "DataLakeAnalytics",
    "DataLakeStoreGen1",
    "Databricks",
    "EventHubClusters",
    "EventHubs",
    "Hdinsightclusters",
    "LogAnalyticsWorkspaces",
    "StreamAnalyticsJobs",
    "SynapseAnalytics"
  ],
  "diagrams.azure.compute": [
    "AppServices",
    "AutomanagedVM",
    "AvailabilitySets",
    "BatchAccounts",
    "CitrixVirtualDesktopsEssentials",
    "CloudServicesClassic",
    "CloudServices",
    "CloudsimpleVirtualMachines",
    "ContainerInstances",
    "ContainerRegistries",
    "DiskEncryptionSets",
    "DiskSnapshots",
    "Disks",
    "FunctionApps",
    "ImageDefinitions",
    "ImageVersions",
    "KubernetesServices",
    "MeshApplications",
    "OsImages",
    "SAPHANAOnAzure",
    "ServiceFabricClusters",
    "SharedImageGalleries",
    "SpringCloud",
    "VMClassic",
    "VMImages",
    "VMLinux",
    "VMScaleSet",
    "VMWindows",
    "VM",
    "Workspaces"
  ],
  "diagrams.azure.database": [
    "BlobStorage",
    "CacheForRedis",
    "CosmosDb",
    "DataExplorerClusters",
    "DataFactory",
    "DataLake",
    "DatabaseForMariadbServers",
    "DatabaseForMysqlServers",
    "DatabaseForPostgresqlServers",
    "ElasticDatabasePools",
    "ElasticJobAgents",
    "InstancePools",
    "ManagedDatabases",
    "SQLDatabases",
    "SQLDatawarehouse",
    "SQLManagedInstances",
    "SQLServerStretchDatabases",
    "SQLServers",
    "SQLVM",
    "SQL",
    "SsisLiftAndShiftIr",
    "SynapseAnalytics",
    "VirtualClusters",
    "VirtualDatacenter"
  ],
  "diagrams.azure.devops": [
    "ApplicationInsights",
    "Artifacts",
    "Boards",
    "Devops",
    "DevtestLabs",
    "LabServices",
    "Pipelines",
    "Repos",
    "TestPlans"
  ],
  "diagrams.azure.general": [
    "Allresources",
    "Azurehome",
    "Developertools",
    "Helpsupport",
    "Information",
    "Managementgroups",
    "Marketplace",
    "Quickstartcenter",
    "Recent",
    "Reservations",
    "Resource",
    "Resourcegroups",
    "Servicehealth",
    "Shareddashboard",
    "Subscriptions",
    "Support",
    "Supportrequests",
    "Tag",
    "Tags",
    "Templates",
    "Twousericon",
    "Userhealthicon",
    "Usericon",
    "Userprivacy",
    "Userresource",
    "Whatsnew"
  ],
  "diagrams.azure.identity": [
    "AccessReview",
    "ActiveDirectoryConnectHealth",
    "ActiveDirectory",
    "ADB2C",
    "ADDomainServices",
    "ADIdentityProtection",
    "ADPrivilegedIdentityManagement",
    "AppRegistrations",
    "ConditionalAccess",
    "EnterpriseApplications",
    "Groups",
    "IdentityGovernance",
    "InformationProtection",
    "ManagedIdentities",
    "Users"
  ],
  "diagrams.azure.integration": [
    "APIForFhir",
    "APIManagement",
    "AppConfiguration",
    "DataCatalog",
    "EventGridDomains",
    "EventGridSubscriptions",
    "EventGridTopics",
    "IntegrationAccounts",
    "IntegrationServiceEnvironments",
    "LogicAppsCustomConnector",
    "LogicApps",
    "PartnerTopic",
    "SendgridAccounts",
    "ServiceBusRelays",
    "ServiceBus",
    "ServiceCatalogManagedApplicationDefinitions",
    "SoftwareAsAService",
    "StorsimpleDeviceManagers",
    "SystemTopic"
  ],
  "diagrams.azure.iot": [
    "DeviceProvisioningServices",
    "DigitalTwins",
    "IotCentralApplications",
    "IotHubSecurity",
    "IotHub",
    "Maps",
    "Sphere",
    "TimeSeriesInsightsEnvironments",
    "TimeSeriesInsightsEventsSources",
    "Windows10IotCoreServices"
  ],
  "diagrams.azure.migration": [
    "DataBoxEdge",
    "DataBox",
    "DatabaseMigrationServices",
    "MigrationProjects",
    "RecoveryServicesVaults"
  ],
  "diagrams.azure.ml": [
    "BatchAI",
    "BotServices",
    "CognitiveServices",
    "GenomicsAccounts",
    "MachineLearningServiceWorkspaces",
    "MachineLearningStudioWebServicePlans",
    "MachineLearningStudioWebServices",
    "MachineLearningStudioWorkspaces"
  ],
  "diagrams.azure.mobile": [
    "AppServiceMobile",
    "MobileEngagement",
    "NotificationHubs"
  ],
  "diagrams.azure.network": [
    "ApplicationGateway",
    "ApplicationSecurityGroups",
    "CDNProfiles",
    "Connections",
    "DDOSProtectionPlans",
    "DNSPrivateZones",
    "DNSZones",
    "ExpressrouteCircuits",
    "Firewall",
    "FrontDoors",
    "LoadBalancers",
    "LocalNetworkGateways",
    "NetworkInterfaces",
    "NetworkSecurityGroupsClassic",
    "NetworkWatcher",
    "OnPremisesDataGateways",
    "PublicIpAddresses",
    "ReservedIpAddressesClassic",
    "RouteFilters",
    "RouteTables",
    "ServiceEndpointPolicies",
    "Subnets",
    "TrafficManagerProfiles",
    "VirtualNetworkClassic",
    "VirtualNetworkGateways",
    "VirtualNetworks",
    "VirtualWans"
  ],
  "diagrams.azure.security": [
    "ApplicationSecurityGroups",
    "ConditionalAccess",
    "Defender",
    "ExtendedSecurityUpdates",
    "KeyVaults",
    "SecurityCenter",
    "Sentinel"
  ],
  "diagrams.azure.storage": [
    "ArchiveStorage",
    "Azurefxtedgefiler",
    "BlobStorage",
    "DataBoxEdgeDataBoxGateway",
    "DataBox",
    "DataLakeStorage",
    "GeneralStorage",
    "NetappFiles",
    "QueuesStorage",
    "StorageAccountsClassic",
    "StorageAccounts",
    "StorageExplorer",
    "StorageSyncServices",
    "StorsimpleDataManagers",
    "StorsimpleDeviceManagers",
    "TableStorage"
  ],
  "diagrams.azure.web": [
    "APIConnections",
    "AppServiceCertificates",
    "AppServiceDomains",
    "AppServiceEnvironments",
    "AppServicePlans",
    "AppServices",
    "MediaServices",
    "NotificationHubNamespaces",
    "Search",
    "Signalr"
  ],


    "diagrams.aws.analytics": [
    "Analytics",
    "Athena",
    "CloudsearchSearchDocuments",
    "Cloudsearch",
    "DataLakeResource",
    "DataPipeline",
    "ElasticsearchService",
    "EMRCluster",
    "EMREngineMaprM3",
    "EMREngineMaprM5",
    "EMREngineMaprM7",
    "EMREngine",
    "EMRHdfsCluster",
    "EMR",
    "GlueCrawlers",
    "GlueDataCatalog",
    "Glue",
    "KinesisDataAnalytics",
    "KinesisDataFirehose",
    "KinesisDataStreams",
    "KinesisVideoStreams",
    "Kinesis",
    "LakeFormation",
    "ManagedStreamingForKafka",
    "Quicksight",
    "RedshiftDenseComputeNode",
    "RedshiftDenseStorageNode",
    "Redshift"
  ],
  "diagrams.aws.ar": [
    "ArVr",
    "Sumerian"
  ],
  "diagrams.aws.blockchain": [
    "BlockchainResource",
    "Blockchain",
    "ManagedBlockchain",
    "QuantumLedgerDatabaseQldb"
  ],
  "diagrams.aws.business": [
    "AlexaForBusiness",
    "BusinessApplications",
    "Chime",
    "Workmail"
  ],
  "diagrams.aws.compute": [
    "AppRunner",
    "ApplicationAutoScaling",
    "Batch",
    "ComputeOptimizer",
    "Compute",
    "EC2Ami",
    "EC2AutoScaling",
    "EC2ContainerRegistryImage",
    "EC2ContainerRegistryRegistry",
    "EC2ContainerRegistry",
    "EC2ElasticIpAddress",
    "EC2ImageBuilder",
    "EC2Instance",
    "EC2Instances",
    "EC2Rescue",
    "EC2SpotInstance",
    "EC2",
    "ElasticBeanstalkApplication",
    "ElasticBeanstalkDeployment",
    "ElasticBeanstalk",
    "ElasticContainerServiceContainer",
    "ElasticContainerServiceService",
    "ElasticContainerService",
    "ElasticKubernetesService",
    "Fargate",
    "LambdaFunction",
    "Lambda",
    "Lightsail",
    "LocalZones",
    "Outposts",
    "ServerlessApplicationRepository",
    "ThinkboxDeadline",
    "ThinkboxDraft",
    "ThinkboxFrost",
    "ThinkboxKrakatoa",
    "ThinkboxSequoia",
    "ThinkboxStoke",
    "ThinkboxXmesh",
    "VmwareCloudOnAWS",
    "Wavelength"
  ],
  "diagrams.aws.cost": [
    "Budgets",
    "CostAndUsageReport",
    "CostExplorer",
    "CostManagement",
    "ReservedInstanceReporting",
    "SavingsPlans"
  ],
  "diagrams.aws.database": [
    "AuroraInstance",
    "Aurora",
    "DatabaseMigrationServiceDatabaseMigrationWorkflow",
    "DatabaseMigrationService",
    "Database",
    "DocumentdbMongodbCompatibility",
    "DynamodbAttribute",
    "DynamodbAttributes",
    "DynamodbDax",
    "DynamodbGlobalSecondaryIndex",
    "DynamodbItem",
    "DynamodbItems",
    "DynamodbTable",
    "Dynamodb",
    "ElasticacheCacheNode",
    "ElasticacheForMemcached",
    "ElasticacheForRedis",
    "Elasticache",
    "KeyspacesManagedApacheCassandraService",
    "Neptune",
    "QuantumLedgerDatabaseQldb",
    "RDSInstance",
    "RDSMariadbInstance",
    "RDSMysqlInstance",
    "RDSOnVmware",
    "RDSOracleInstance",
    "RDSPostgresqlInstance",
    "RDSSqlServerInstance",
    "RDS",
    "RedshiftDenseComputeNode",
    "RedshiftDenseStorageNode",
    "Redshift",
    "Timestream"
  ],
  "diagrams.aws.devtools": [
    "CloudDevelopmentKit",
    "Cloud9Resource",
    "Cloud9",
    "Codebuild",
    "Codecommit",
    "Codedeploy",
    "Codepipeline",
    "Codestar",
    "CommandLineInterface",
    "DeveloperTools",
    "ToolsAndSdks",
    "XRay"
  ],
  "diagrams.aws.enablement": [
    "CustomerEnablement",
    "Iq",
    "ManagedServices",
    "ProfessionalServices",
    "Support"
  ],
  "diagrams.aws.enduser": [
    "Appstream20",
    "DesktopAndAppStreaming",
    "Workdocs",
    "Worklink",
    "Workspaces"
  ],
  "diagrams.aws.engagement": [
    "Connect",
    "CustomerEngagement",
    "Pinpoint",
    "SimpleEmailServiceSesEmail",
    "SimpleEmailServiceSes"
  ],
  "diagrams.aws.game": [
    "GameTech",
    "Gamelift"
  ],
  "diagrams.gcp.analytics": [
    "Bigquery",
    "Dataflow",
    "Dataproc",
    "Datalab",
    "Pubsub",
    "Composer",
    "DataCatalog"
  ],

    "diagrams.aws.general": [
    "Client", 
    "Disk", 
    "Forums", 
    "General", 
    "GenericDatabase", 
    "GenericFirewall", 
    "GenericOfficeBuilding", 
    "GenericSamlToken", 
    "GenericSDK", 
    "InternetAlt1", 
    "InternetAlt2", 
    "InternetGateway", 
    "Marketplace", 
    "MobileClient", 
    "Multimedia", 
    "OfficeBuilding", 
    "SamlToken", 
    "SDK", 
    "SslPadlock", 
    "TapeStorage", 
    "Toolkit", 
    "TraditionalServer", 
    "User", 
    "Users"
  ],
  "diagrams.aws.integration": [
    "ApplicationIntegration", 
    "Appsync", 
    "ConsoleMobileApplication", 
    "EventResource", 
    "EventbridgeCustomEventBusResource", 
    "EventbridgeDefaultEventBusResource", 
    "EventbridgeSaasPartnerEventBusResource", 
    "Eventbridge", 
    "ExpressWorkflows", 
    "MQ", 
    "SimpleNotificationServiceSnsEmailNotification", 
    "SimpleNotificationServiceSnsHttpNotification", 
    "SimpleNotificationServiceSnsTopic", 
    "SimpleNotificationServiceSns", 
    "SimpleQueueServiceSqsMessage", 
    "SimpleQueueServiceSqsQueue", 
    "SimpleQueueServiceSqs", 
    "StepFunctions"
  ],
  "diagrams.aws.iot": [
    "Freertos", 
    "InternetOfThings", 
    "Iot1Click", 
    "IotAction", 
    "IotActuator", 
    "IotAlexaEcho", 
    "IotAlexaEnabledDevice", 
    "IotAlexaSkill", 
    "IotAlexaVoiceService", 
    "IotAnalyticsChannel", 
    "IotAnalyticsDataSet", 
    "IotAnalyticsDataStore", 
    "IotAnalyticsNotebook", 
    "IotAnalyticsPipeline", 
    "IotAnalytics", 
    "IotBank", 
    "IotBicycle", 
    "IotButton", 
    "IotCamera", 
    "IotCar", 
    "IotCart", 
    "IotCertificate", 
    "IotCoffeePot", 
    "IotCore", 
    "IotDesiredState", 
    "IotDeviceDefender", 
    "IotDeviceGateway", 
    "IotDeviceManagement", 
    "IotDoorLock", 
    "IotEvents", 
    "IotFactory", 
    "IotFireTvStick", 
    "IotFireTv", 
    "IotGeneric", 
    "IotGreengrassConnector", 
    "IotGreengrass", 
    "IotHardwareBoard", 
    "IotHouse", 
    "IotHttp", 
    "IotHttp2", 
    "IotJobs", 
    "IotLambda", 
    "IotLightbulb", 
    "IotMedicalEmergency", 
    "IotMqtt", 
    "IotOverTheAirUpdate", 
    "IotPolicyEmergency", 
    "IotPolicy", 
    "IotReportedState", 
    "IotRule", 
    "IotSensor", 
    "IotServo", 
    "IotShadow", 
    "IotSimulator", 
    "IotSitewise", 
    "IotThermostat", 
    "IotThingsGraph", 
    "IotTopic", 
    "IotTravel", 
    "IotUtility", 
    "IotWindfarm"
  ],
  "diagrams.aws.management": [
    "AutoScaling", 
    "Chatbot", 
    "CloudformationChangeSet", 
    "CloudformationStack", 
    "CloudformationTemplate", 
    "Cloudformation", 
    "Cloudtrail", 
    "CloudwatchAlarm", 
    "CloudwatchEventEventBased", 
    "CloudwatchEventTimeBased", 
    "CloudwatchRule", 
    "Cloudwatch", 
    "Codeguru", 
    "CommandLineInterface", 
    "Config", 
    "ControlTower", 
    "LicenseManager", 
    "ManagedServices", 
    "ManagementAndGovernance", 
    "ManagementConsole", 
    "OpsworksApps", 
    "OpsworksDeployments", 
    "OpsworksInstances", 
    "OpsworksLayers", 
    "OpsworksMonitoring", 
    "OpsworksPermissions", 
    "OpsworksResources", 
    "OpsworksStack", 
    "Opsworks", 
    "OrganizationsAccount", 
    "OrganizationsOrganizationalUnit", 
    "Organizations", 
    "PersonalHealthDashboard", 
    "ServiceCatalog", 
    "SystemsManagerAutomation", 
    "SystemsManagerDocuments", 
    "SystemsManagerInventory", 
    "SystemsManagerMaintenanceWindows", 
    "SystemsManagerOpscenter", 
    "SystemsManagerParameterStore", 
    "SystemsManagerPatchManager", 
    "SystemsManagerRunCommand", 
    "SystemsManagerStateManager", 
    "SystemsManager", 
    "TrustedAdvisorChecklistCost", 
    "TrustedAdvisorChecklistFaultTolerant", 
    "TrustedAdvisorChecklistPerformance", 
    "TrustedAdvisorChecklistSecurity", 
    "TrustedAdvisorChecklist", 
    "TrustedAdvisor", 
    "WellArchitectedTool"
  ],
  "diagrams.aws.media": [
    "ElasticTranscoder", 
    "ElementalConductor", 
    "ElementalDelta", 
    "ElementalLive", 
    "ElementalMediaconnect", 
    "ElementalMediaconvert", 
    "ElementalMedialive", 
    "ElementalMediapackage", 
    "ElementalMediastore", 
    "ElementalMediatailor", 
    "ElementalServer", 
    "KinesisVideoStreams", 
    "MediaServices"
  ],
  "diagrams.aws.migration": [
    "ApplicationDiscoveryService", 
    "CloudendureMigration", 
    "DatabaseMigrationService", 
    "DatasyncAgent", 
    "Datasync", 
    "MigrationAndTransfer", 
    "MigrationHub", 
    "ServerMigrationService", 
    "SnowballEdge", 
    "Snowball", 
    "Snowmobile", 
    "TransferForSftp"
  ],
  "diagrams.aws.ml": [
    "ApacheMxnetOnAWS", 
    "AugmentedAi", 
    "Comprehend", 
    "DeepLearningAmis", 
    "DeepLearningContainers", 
    "Deepcomposer", 
    "Deeplens", 
    "Deepracer", 
    "ElasticInference", 
    "Forecast", 
    "FraudDetector", 
    "Kendra", 
    "Lex", 
    "MachineLearning", 
    "Personalize", 
    "Polly", 
    "RekognitionImage", 
    "RekognitionVideo", 
    "Rekognition", 
    "SagemakerGroundTruth", 
    "SagemakerModel", 
    "SagemakerNotebook", 
    "SagemakerTrainingJob", 
    "Sagemaker", 
    "TensorflowOnAWS", 
    "Textract", 
    "Transcribe", 
    "Translate"
  ],
  "diagrams.aws.mobile": [
    "Amplify", 
    "APIGatewayEndpoint", 
    "APIGateway", 
    "Appsync", 
    "DeviceFarm", 
    "Mobile", 
    "Pinpoint"
  ],
  "diagrams.aws.network": [
    "APIGatewayEndpoint", 
    "APIGateway", 
    "AppMesh", 
    "ClientVpn", 
    "CloudMap", 
    "CloudFrontDownloadDistribution", 
    "CloudFrontEdgeLocation", 
    "CloudFrontStreamingDistribution", 
    "CloudFront", 
    "DirectConnect", 
    "ElasticLoadBalancing", 
    "ElbApplicationLoadBalancer", 
    "ElbClassicLoadBalancer", 
    "ElbNetworkLoadBalancer", 
    "Endpoint", 
    "GlobalAccelerator", 
    "InternetGateway", 
    "Nacl", 
    "NATGateway", 
    "NetworkingAndContentDelivery", 
    "PrivateSubnet", 
    "Privatelink", 
    "PublicSubnet", 
    "Route53HostedZone", 
    "Route53", 
    "RouteTable", 
    "SiteToSiteVpn", 
    "TransitGateway", 
    "VPCCustomerGateway", 
    "VPCElasticNetworkAdapter", 
    "VPCElasticNetworkInterface", 
    "VPCFlowLogs", 
    "VPCPeering", 
    "VPCRouter", 
    "VPCTrafficMirroring", 
    "VPC", 
    "VpnConnection", 
    "VpnGateway"
  ],
  "diagrams.aws.quantum": [
    "Braket", 
    "QuantumTechnologies"
  ],
  "diagrams.aws.robotics": [
    "RobomakerCloudExtensionRos", 
    "RobomakerDevelopmentEnvironment", 
    "RobomakerFleetManagement", 
    "RobomakerSimulator", 
    "Robomaker", 
    "Robotics"
  ],
  "diagrams.aws.satellite": [
    "GroundStation", 
    "Satellite"
  ],
  "diagrams.aws.security": [
    "AccessAnalyzer", 
    "AuditManager", 
    "CertificateManager", 
    "CloudHsm", 
    "Cloudtrail", 
    "CognitoUserPools", 
    "Cognito", 
    "Detective", 
    "FirewallManager", 
    "Guardduty", 
    "Inspector", 
    "Kms", 
    "Macie", 
    "NetworkFirewall", 
    "Organizations", 
    "SecretsManager", 
    "SecurityHub", 
    "Shield", 
    "Waf", 
    "Wafv2"
  ],
  "diagrams.aws.storage": [
    "Backup", 
    "Ebs", 
    "Efs", 
    "Glacier", 
    "S3Bucket", 
    "StorageGateway", 
    "S3", 
    "S3Outposts"
  ],
  "diagrams.aws.web": [
    "Cloudfront", 
    "Cloudsearch", 
    "Cognito", 
    "S3Bucket", 
    "Waf", 
    "WebApplicationFirewall"
  ],
  "diagrams.aws.database": [
    "Athena", 
    "Aurora", 
    "DynamoDb", 
    "ElastiCache", 
    "DocumentDb", 
    "Keyspaces", 
    "Neptune", 
    "Rds", 
    "Redshift", 
    "Timestream", 
    "Qldb"
  ]
}

def extract_relevant_imports(prompt: str) -> dict:
    relevant_imports = {}
    for category, components in diagrams_data.items():
        for component in components:
            if component.lower() in prompt.lower():
                relevant_imports.setdefault(category, []).append(component)
    return relevant_imports

def extract_all_imports() -> dict:
    irrelevant_imports = {category: components for category, components in diagrams_data.items()}
    return irrelevant_imports

def format_imports(relevant_imports: dict) -> str:
    imports_code = []
    for category, components in relevant_imports.items():
        base_module = ".".join(category.split(".")[:-1])
        class_name = category.split(".")[-1]
        components_str = ", ".join(components)
        imports_code.append(f"from {base_module} import {class_name}\n{class_name} = [{components_str}]")
    return "\n".join(imports_code)

class CodeGenerator(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate_code(self, prompt: str) -> str:
        relevant_imports = self.extract_relevant_imports(prompt)
        formatted_imports = self.format_imports(relevant_imports)
        
        full_prompt = (
            f"Generate a complete Python script using the diagrams package to create a system diagram. "
            f"The script should only use the following imports:\n\n{formatted_imports}.\n\n"
            f"Do not use any imports outside of {formatted_imports}. If additional functionality is needed, provide a comment instead. "
            f"Ensure the output image is always saved as 'diagram_output'. Only return the complete Python code wrapped in triple backticks.\n\n"
            f"User prompt: {prompt}"
        )

        response = self.get_model_response(full_prompt)
        content = self.parse_response(response)
        
        code_match = re.search(r'```(?:python)?(.*?)```', content, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()

            try:
                ast.parse(code)
            except SyntaxError as e:
                raise ValueError(f"Syntax error in generated code: {e}")
            
            self.validate_imports(code)
            self.log_code(prompt, code)

            return code
        else:
            raise ValueError("No code block found in the response.")
        

    def generate_text(self, prompt: str) -> str:
        full_prompt = (
            f"Please generate a detailed and relevant text-based response based on the following prompt:\n\n"
            f"{prompt}\n\n"
        )

        response = self.get_model_response(full_prompt)
        content = self.parse_response(response)
        

        self.log_text(prompt, content)
        return content     


    def generate_code_general(self, prompt: str) -> str:
        full_prompt = (
            f"Generate a complete and valid code snippet based on the following prompt:\n\n"
            f"{prompt}\n\n"
            f"Ensure the code is syntactically correct and complete, wrapped in triple backticks."
        )

        response = self.get_model_response(full_prompt)
        content = self.parse_response(response)
        
        code_match = re.search(r'```(?:\w+)?(.*?)```', content, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
            return code
        else:
            raise ValueError("No code block found in the response.")       
    
    @abstractmethod
    def get_model_response(self, full_prompt: str):
        pass

    def extract_relevant_imports(self, prompt: str):
        return extract_relevant_imports(prompt)
    
    def format_imports(self, imports):
        return format_imports(imports)

    def validate_imports(self, code: str):
        for line in code.split('\n'):
            if line.startswith("import ") or line.startswith("from "):
                try:
                    importlib.import_module(line.split()[1])
                except ImportError as e:
                    raise ValueError(f"Import error in generated code: {e}")

    def log_text(self, prompt: str, content: str):
        directory = 'generated_text'
        os.makedirs(directory, exist_ok=True)
        
        log_filename = os.path.join(directory, f'{self.model_name}_text_log.txt')
        
        with open(log_filename, 'a') as file:
            file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("User Prompt:\n")
            file.write(prompt + "\n\n")
            file.write("Generated Text:\n")
            file.write(content + "\n\n")
            file.write("="*80 + "\n\n")      

    def log_code(self, prompt: str, code: str):
        directory = 'generated_code'
        os.makedirs(directory, exist_ok=True)
        
        log_filename = os.path.join(directory, f'{self.model_name}_code_log.txt')
        
        with open(log_filename, 'a') as file:
            file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("User Prompt:\n")
            file.write(prompt + "\n\n")
            file.write("Generated Code:\n")
            file.write(code + "\n\n")
            file.write("="*80 + "\n\n")
    
    def parse_response(self, response):
        if 'text' in response:
            return response['text']
        elif 'choices' in response:
            return response['choices'][0]['message']['content'].strip()
        else:
            raise ValueError("Unexpected response format.")

