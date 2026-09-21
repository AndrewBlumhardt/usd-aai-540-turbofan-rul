"""
CloudWatch Infrastructure Monitoring Dashboard Setup
AAI 540 Turbofan RUL Prediction Project

This script creates CloudWatch dashboards and alarms for:
1. Model training job monitoring
2. SageMaker Batch Transform job monitoring
3. Prediction error tracking
4. Feature distribution drift detection
5. Infrastructure health and cost monitoring
"""

import json
import boto3
from datetime import datetime

class TurbofanMonitoringDashboard:
    def __init__(self, region="us-east-1", project_prefix="aai540-turbofan-rul"):
        self.region = region
        self.project_prefix = project_prefix
        self.cloudwatch = boto3.client("cloudwatch", region_name=region)
        self.sm_client = boto3.client("sagemaker", region_name=region)

    def create_main_dashboard(self, dashboard_name="AAI540-Turbofan-RUL-Monitoring"):
        """Create the main monitoring dashboard"""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/SageMaker", "ModelInvocations", {"stat": "Sum"}],
                            [".", "ModelLatency", {"stat": "Average"}],
                            [".", "ModelErrors", {"stat": "Sum"}],
                            ["AWS/S3", "NumberOfObjects", {"stat": "Average"}],
                            [".", "BucketSizeBytes", {"stat": "Average"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": self.region,
                        "title": "SageMaker Model Inference Metrics"
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/SageMaker", "TrainingJobsRunning", {"stat": "Average"}],
                            [".", "TrainingJobsCompleted", {"stat": "Sum"}],
                            [".", "TrainingJobsFailed", {"stat": "Sum"}],
                            [".", "TransformJobsRunning", {"stat": "Average"}],
                            [".", "TransformJobsCompleted", {"stat": "Sum"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": self.region,
                        "title": "SageMaker Job Execution Status"
                    }
                },
                {
                    "type": "log",
                    "properties": {
                        "query": f"""
fields @timestamp, @message, prediction_error, engine_id, cycle
| filter ispresent(prediction_error)
| stats avg(prediction_error) as avg_error,
        max(prediction_error) as max_error,
        pct(prediction_error, 95) as p95_error by engine_id
| sort p95_error desc
                        """,
                        "region": self.region,
                        "title": "Prediction Error Distribution by Engine"
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/Lambda", "Invocations", {"stat": "Sum"}],
                            [".", "Duration", {"stat": "Average"}],
                            [".", "Errors", {"stat": "Sum"}],
                            [".", "Throttles", {"stat": "Sum"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Lambda Function Health (Feature Processing)"
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/Athena", "DataScannedInBytes", {"stat": "Sum"}],
                            [".", "EngineExecutionTime", {"stat": "Average"}],
                            [".", "QueryExecutionTime", {"stat": "Average"}],
                            [".", "TotalExecutionTime", {"stat": "Average"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Athena Query Performance"
                    }
                }
            ]
        }

        self.cloudwatch.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=json.dumps(dashboard_body)
        )
        print(f"✓ Created main dashboard: {dashboard_name}")
        return dashboard_name

    def create_model_performance_dashboard(self, dashboard_name="AAI540-Model-Performance"):
        """Create dashboard for model performance metrics"""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["TurbofanRUL", "ValidationRMSE", {"stat": "Average"}],
                            [".", "ValidationMAE", {"stat": "Average"}],
                            [".", "TestRMSE", {"stat": "Average"}],
                            [".", "TestMAE", {"stat": "Average"}],
                            [".", "ProductionRMSE", {"stat": "Average"}]
                        ],
                        "period": 3600,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Model Performance Metrics Over Time",
                        "yAxis": {"left": {"min": 0, "max": 50}}
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["TurbofanRUL", "PredictionsByCycle", {"stat": "Sum"}],
                            [".", "ErrorsAbove20Cycles", {"stat": "Sum"}],
                            [".", "ErrorsAbove10Cycles", {"stat": "Sum"}],
                            [".", "ErrorsBelow5Cycles", {"stat": "Sum"}]
                        ],
                        "period": 300,
                        "stat": "Sum",
                        "region": self.region,
                        "title": "Prediction Error Distribution"
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["TurbofanRUL", "ModelDriftScore", {"stat": "Average"}],
                            [".", "FeatureMeanDrift", {"stat": "Average"}],
                            [".", "FeatureStdDrift", {"stat": "Average"}],
                            [".", "DataQualityScore", {"stat": "Average"}]
                        ],
                        "period": 3600,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Data Drift and Quality Monitoring",
                        "yAxis": {"left": {"min": 0, "max": 1}}
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/SageMaker", "ModelLatency", {"stat": "Average"}],
                            [".", "ModelLatency", {"stat": "p95"}],
                            [".", "ModelLatency", {"stat": "p99"}],
                            [".", "BatchTransformDuration", {"stat": "Average"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Model Inference Latency"
                    }
                }
            ]
        }

        self.cloudwatch.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=json.dumps(dashboard_body)
        )
        print(f"✓ Created model performance dashboard: {dashboard_name}")
        return dashboard_name

    def create_data_quality_dashboard(self, dashboard_name="AAI540-Data-Quality"):
        """Create dashboard for data quality and Feature Store metrics"""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/SageMaker", "FeatureStoreIngestionsSucceeded", {"stat": "Sum"}],
                            [".", "FeatureStoreIngestionsFailed", {"stat": "Sum"}],
                            [".", "FeatureStoreRecordsIngested", {"stat": "Sum"}],
                            [".", "FeatureStoreQueryLatency", {"stat": "Average"}]
                        ],
                        "period": 300,
                        "stat": "Sum",
                        "region": self.region,
                        "title": "Feature Store Health"
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["TurbofanRUL", "MissingValuesCount", {"stat": "Sum"}],
                            [".", "OutliersDetected", {"stat": "Sum"}],
                            [".", "SchemaValidationFailures", {"stat": "Sum"}],
                            [".", "DuplicateRecords", {"stat": "Sum"}]
                        ],
                        "period": 3600,
                        "stat": "Sum",
                        "region": self.region,
                        "title": "Data Quality Issues"
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["TurbofanRUL", "EnginePartitionBalance", {"stat": "Average"}],
                            [".", "CycleDistributionSkew", {"stat": "Average"}],
                            [".", "SensorSignalStrength", {"stat": "Average"}],
                            [".", "RULDistributionUniformity", {"stat": "Average"}]
                        ],
                        "period": 3600,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Data Distribution Health",
                        "yAxis": {"left": {"min": 0, "max": 1}}
                    }
                }
            ]
        }

        self.cloudwatch.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=json.dumps(dashboard_body)
        )
        print(f"✓ Created data quality dashboard: {dashboard_name}")
        return dashboard_name

    def create_cost_monitoring_dashboard(self, dashboard_name="AAI540-Cost-Monitoring"):
        """Create dashboard for AWS cost and resource utilization"""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/Billing", "EstimatedCharges", {"stat": "Maximum"}],
                            ["AWS/SageMaker", "TrainingJobHours", {"stat": "Sum"}],
                            [".", "TransformJobHours", {"stat": "Sum"}],
                            ["AWS/S3", "BucketSizeBytes", {"stat": "Average"}]
                        ],
                        "period": 3600,
                        "stat": "Sum",
                        "region": self.region,
                        "title": "AWS Cost and Resource Usage"
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/EC2", "CPUUtilization", {"stat": "Average"}],
                            [".", "NetworkIn", {"stat": "Sum"}],
                            [".", "NetworkOut", {"stat": "Sum"}],
                            ["AWS/RDS", "DatabaseConnections", {"stat": "Average"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": self.region,
                        "title": "Compute Resource Efficiency"
                    }
                }
            ]
        }

        self.cloudwatch.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=json.dumps(dashboard_body)
        )
        print(f"✓ Created cost monitoring dashboard: {dashboard_name}")
        return dashboard_name

    def create_alarms(self, sns_topic_arn=None):
        """Create CloudWatch alarms for critical conditions"""
        alarms = [
            {
                "name": "HighPredictionError",
                "metric": "TurbofanRUL/TestRMSE",
                "threshold": 25.0,
                "comparison": "GreaterThanThreshold",
                "description": "Alert if model RMSE exceeds 25 cycles"
            },
            {
                "name": "ModelInferenceLatency",
                "metric": "AWS/SageMaker/ModelLatency",
                "threshold": 5000,  # 5 seconds
                "comparison": "GreaterThanThreshold",
                "description": "Alert if inference takes >5 seconds"
            },
            {
                "name": "FeatureStoreIngestionFailures",
                "metric": "AWS/SageMaker/FeatureStoreIngestionsFailed",
                "threshold": 10,
                "comparison": "GreaterThanThreshold",
                "description": "Alert if >10 Feature Store ingestions fail per hour"
            },
            {
                "name": "DataQualityDegradation",
                "metric": "TurbofanRUL/DataQualityScore",
                "threshold": 0.8,
                "comparison": "LessThanThreshold",
                "description": "Alert if data quality score drops below 0.8"
            },
            {
                "name": "ModelDriftDetected",
                "metric": "TurbofanRUL/ModelDriftScore",
                "threshold": 0.3,
                "comparison": "GreaterThanThreshold",
                "description": "Alert if model drift score exceeds 0.3"
            },
            {
                "name": "S3BucketCostOverage",
                "metric": "AWS/S3/BucketSizeBytes",
                "threshold": 100 * 1024**3,  # 100 GB
                "comparison": "GreaterThanThreshold",
                "description": "Alert if S3 bucket exceeds 100 GB"
            }
        ]

        for alarm in alarms:
            try:
                self.cloudwatch.put_metric_alarm(
                    AlarmName=f"{self.project_prefix}-{alarm['name']}",
                    MetricName=alarm['metric'],
                    Namespace="TurbofanRUL",
                    Statistic="Average",
                    Period=300,
                    EvaluationPeriods=2,
                    Threshold=alarm['threshold'],
                    ComparisonOperator=alarm['comparison'],
                    AlarmDescription=alarm['description'],
                    AlarmActions=[sns_topic_arn] if sns_topic_arn else []
                )
                print(f"✓ Created alarm: {alarm['name']}")
            except Exception as e:
                print(f"✗ Failed to create alarm {alarm['name']}: {str(e)}")

    def deploy_all(self, sns_topic_arn=None):
        """Deploy all dashboards and alarms"""
        print("\n=== CloudWatch Monitoring Infrastructure Setup ===\n")

        dashboards = [
            self.create_main_dashboard(),
            self.create_model_performance_dashboard(),
            self.create_data_quality_dashboard(),
            self.create_cost_monitoring_dashboard()
        ]

        print("\nCreating alarms...")
        self.create_alarms(sns_topic_arn)

        print(f"\n✓ Monitoring infrastructure deployed successfully")
        print(f"\nDashboards created:")
        for dashboard in dashboards:
            print(f"  - {dashboard}")
        return dashboards


if __name__ == "__main__":
    # Initialize monitoring setup
    monitoring = TurbofanMonitoringDashboard(
        region="us-east-1",
        project_prefix="aai540-turbofan-rul"
    )

    # Deploy all monitoring infrastructure
    # Note: SNS topic ARN is optional - omit to skip alarm notifications
    monitoring.deploy_all(sns_topic_arn=None)

    print("\n=== Monitoring Setup Summary ===")
    print("""
    The following CloudWatch dashboards have been created:

    1. AAI540-Turbofan-RUL-Monitoring
       - SageMaker inference metrics
       - Training/Transform job status
       - Prediction error distribution
       - Lambda and Athena performance

    2. AAI540-Model-Performance
       - RMSE/MAE trends over time
       - Error distribution by magnitude
       - Data drift and quality scores
       - Model inference latency

    3. AAI540-Data-Quality
       - Feature Store health
       - Data quality issues
       - Distribution health metrics

    4. AAI540-Cost-Monitoring
       - AWS billing and resource usage
       - Compute utilization

    Alarms created (with 2-period threshold):
    - High prediction error (RMSE > 25)
    - Slow inference (latency > 5s)
    - Feature Store ingestion failures (>10/hour)
    - Data quality degradation (score < 0.8)
    - Model drift (score > 0.3)
    - S3 storage overage (>100 GB)

    To enable email notifications:
    1. Create SNS topic in AWS Console
    2. Subscribe your email address
    3. Pass SNS topic ARN to deploy_all() function
    """)
