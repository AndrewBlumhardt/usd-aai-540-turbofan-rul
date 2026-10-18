# Original Notebook Improvement Roadmap

## Section-by-Section Enhancement Guide

Each section of the AAI540_Turbofan_RUL_AWS_SageMaker notebook can be enhanced to support more sophisticated ML operations workflows.

---

## 1. Environment and AWS Session Setup

### Current State
- ✓ Confirms AWS credentials
- ✓ Discovers SageMaker execution role
- ✓ Selects default S3 bucket
- ✓ Prints system information

### Improvements to Next Step

#### 1a. **Add Resource Validation & Health Checks**
```python
# NEW: Validate AWS permissions for required services
required_permissions = [
    "s3:GetObject", "s3:PutObject", "s3:ListBucket",
    "sagemaker:DescribeTrainingJob", "sagemaker:CreateTrainingJob",
    "athena:StartQueryExecution", "athena:GetQueryResults",
    "cloudwatch:PutMetricAlarm", "cloudwatch:PutDashboard"
]

def check_iam_permissions(permissions):
    """Validate IAM permissions for notebook operations"""
    # Use AWS Policy Simulator to test permissions
    pass

# Validate that required services are available in region
```

#### 1b. **Add AWS Service Quota Monitoring**
```python
# NEW: Check if you're approaching service limits
quotas = {
    "SageMaker Training Jobs": 100,
    "SageMaker Endpoints": 10,
    "Athena Queries": 1000,
}

# Alert if approaching quota limits
```

#### 1c. **Add Notebook Metadata & Lineage**
```python
# NEW: Track notebook execution metadata
execution_metadata = {
    "notebook_version": "1.0",
    "execution_timestamp": datetime.now(),
    "aws_account": account_id,
    "git_commit": get_git_commit_hash(),  # Track code version
    "data_version": "FD001",
    "feature_engineering_version": "1.0"
}

# Log to CloudWatch for traceability
```

**Expected Impact:** Better reliability, permission debugging, compliance tracking

---

## 2. Project Configuration & Cost Controls

### Current State
- ✓ Flags for enabling/disabling AWS stages
- ✓ Partition counts defined
- ✓ Local directories created

### Improvements to Next Step

#### 2a. **Add Cost Estimation & Budgeting**
```python
# NEW: Calculate estimated costs before running
cost_calculator = {
    "sagemaker_training": {
        "instance_type": "ml.m5.large",
        "hourly_rate": 0.134,
        "estimated_hours": 0.5,
        "total": 0.067
    },
    "batch_transform": {
        "instance_type": "ml.m5.large",
        "hourly_rate": 0.134,
        "estimated_hours": 0.25,
        "total": 0.034
    },
    "s3_storage": {
        "monthly_gb": 0.2,
        "cost_per_gb": 0.023,
        "total": 0.005
    }
}

total_estimated_cost = sum(v['total'] for v in cost_calculator.values())
print(f"Estimated total cost: ${total_estimated_cost:.2f}")

# Set up budget alerts
def setup_budget_alert(budget_limit=10.00):
    """Create AWS Budgets alert for cost control"""
    pass
```

#### 2b. **Add Configuration Validation**
```python
# NEW: Validate configurations before execution
def validate_config():
    assert ROLLING_WINDOWS[0] < ROLLING_WINDOWS[1], "Window sizes must be ordered"
    assert RUL_CAP > 0, "RUL cap must be positive"
    assert sum(PARTITION_COUNTS.values()) == 100, "Partitions must sum to 100%"
    assert RANDOM_SEED is not None, "Seed must be set for reproducibility"
    
validate_config()
```

#### 2c. **Add Reproducibility & Environment Snapshot**
```python
# NEW: Capture environment for reproducibility
import json

environment_snapshot = {
    "python_packages": {
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "scikit-learn": sklearn.__version__,
        "xgboost": xgb.__version__,
        "sagemaker": sagemaker.__version__
    },
    "aws_region": region,
    "notebook_parameters": {
        "RUL_CAP": RUL_CAP,
        "RANDOM_SEED": RANDOM_SEED,
        "PARTITION_COUNTS": PARTITION_COUNTS
    }
}

# Save to S3 for reproducibility
with open("environment_snapshot.json", "w") as f:
    json.dump(environment_snapshot, f, indent=2)
s3.upload_file("environment_snapshot.json", bucket, f"{PROJECT_PREFIX}/metadata/environment.json")
```

**Expected Impact:** Cost transparency, error prevention, reproducibility

---

## 3. Retrieve NASA Dataset

### Current State
- ✓ Downloads public NASA archive
- ✓ Extracts FD001 files
- ✓ Verifies file sizes

### Improvements to Next Step

#### 3a. **Add Data Integrity Checks**
```python
# NEW: Verify data hasn't been corrupted
import hashlib

def compute_file_hash(filepath):
    """Compute SHA256 hash of file"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Expected hashes for FD001 files
expected_hashes = {
    "train_FD001.txt": "abc123def456...",  # Pre-computed
    "test_FD001.txt": "xyz789abc123...",
    "RUL_FD001.txt": "rul123abc456..."
}

# Verify after download
for filename, expected_hash in expected_hashes.items():
    actual_hash = compute_file_hash(RAW_DIR / filename)
    assert actual_hash == expected_hash, f"Hash mismatch for {filename}"
```

#### 3b. **Add Caching & Versioning**
```python
# NEW: Cache dataset locally with version tracking
dataset_metadata = {
    "nasa_archive_url": PUBLIC_ARCHIVE_URL,
    "download_date": datetime.now().isoformat(),
    "version": "20250920",
    "cached": True,
    "location": str(RAW_DIR)
}

# Save metadata for future reference
with open(RAW_DIR / "METADATA.json", "w") as f:
    json.dump(dataset_metadata, f, indent=2)

# On subsequent runs, check if cached version matches metadata
```

#### 3c. **Add Dataset Description & Citation**
```python
# NEW: Proper data attribution
print("""
Dataset: NASA C-MAPSS Turbofan Engine Degradation Simulation Data Set
Source: PHM Challenge Dataset (https://phm-datasets.s3.amazonaws.com/)
Citation: Saxena, A., Goebel, K., Simon, D., & Eklund, N. (2008).
          Damage propagation modeling for aircraft engine run-to-failure simulation.
          In 2008 International Conference on Prognostics and Health Management.
          
FD001 Subset:
- Single operating condition (altitude, Mach, throttle)
- 100 turbofan engines
- 21 sensors + 3 operating settings
- Runs to failure format
- Suitable for: RUL prediction, classification
""")
```

**Expected Impact:** Data integrity assurance, reproducibility, proper attribution

---

## 4. Raw S3 Data Lake Layer

### Current State
- ✓ Uploads raw files to S3
- ✓ Uses project prefix organization
- ✓ Prints S3 locations

### Improvements to Next Step

#### 4a. **Add S3 Versioning & Data Lineage**
```python
# NEW: Enable S3 versioning for data governance
def enable_s3_versioning(bucket, prefix):
    """Enable versioning on S3 bucket"""
    s3.put_bucket_versioning(
        Bucket=bucket,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    print(f"✓ Versioning enabled on {bucket}")

enable_s3_versioning(bucket, PROJECT_PREFIX)

# NEW: Tag data with metadata
tags = {
    "dataset": "FD001",
    "source": "NASA-CMAPSS",
    "version": "1.0",
    "owner": "dylan@aeroreliability.ai",
    "sensitivity": "public"
}

for filename in REQUIRED_FILES:
    key = f"{raw_s3_prefix}/{filename}"
    s3.put_object_tagging(
        Bucket=bucket,
        Key=key,
        Tagging={'TagSet': [{'Key': k, 'Value': v} for k, v in tags.items()]}
    )
```

#### 4b. **Add Data Catalog Entry (AWS Glue)**
```python
# NEW: Register data with AWS Glue Data Catalog
glue = boto3.client("glue", region_name=region)

glue.create_database(
    CatalogId=account_id,
    DatabaseInput={
        'Name': f'aai540_turbofan_raw',
        'Description': 'Raw NASA FD001 turbofan dataset',
        'Parameters': {
            'source': 'NASA-CMAPSS',
            'dataset': 'FD001'
        }
    }
)
```

#### 4c. **Add S3 Encryption & Access Logging**
```python
# NEW: Ensure data is encrypted
s3.put_bucket_encryption(
    Bucket=bucket,
    ServerSideEncryptionConfiguration={
        'Rules': [{
            'ApplyServerSideEncryptionByDefault': {
                'SSEAlgorithm': 'AES256'
            }
        }]
    }
)

# NEW: Enable access logging for audit trail
s3.put_bucket_logging(
    Bucket=bucket,
    BucketLoggingStatus={
        'LoggingEnabled': {
            'TargetBucket': bucket,
            'TargetPrefix': f'{PROJECT_PREFIX}/logs/'
        }
    }
)
```

**Expected Impact:** Data governance, compliance, reproducibility

---

## 5. Load & Validate Raw Files

### Current State
- ✓ Reads files with correct schema
- ✓ Checks for duplicates and missing values
- ✓ Basic validation

### Improvements to Next Step

#### 5a. **Add Comprehensive Data Profiling**
```python
# NEW: Generate detailed data quality report
from pandas_profiling import ProfileReport

profile = ProfileReport(train_raw, title="FD001 Training Data Profile")
profile.to_file("data_profile_train.html")
s3.upload_file("data_profile_train.html", bucket, 
               f"{PROJECT_PREFIX}/reports/data_profile_train.html")

# Profile includes:
# - Missing values per column
# - Duplicates
# - Outliers
# - Correlations
# - Distribution plots
```

#### 5b. **Add Statistical Validation Tests**
```python
# NEW: Hypothesis tests for data quality
from scipy import stats

def test_sensor_ranges():
    """Verify sensor readings are within expected physical ranges"""
    # Physical constraints for turbofan sensors
    sensor_ranges = {
        'sensor_1': (0, 1000),      # Example ranges
        'sensor_2': (600, 700),
        # ... etc
    }
    
    for sensor, (min_val, max_val) in sensor_ranges.items():
        out_of_range = (train_raw[sensor] < min_val) | (train_raw[sensor] > max_val)
        if out_of_range.any():
            print(f"⚠️  {out_of_range.sum()} out-of-range values in {sensor}")
    
test_sensor_ranges()

def test_engine_cycle_monotonicity():
    """Verify cycles are monotonically increasing per engine"""
    for engine_id in train_raw['engine_id'].unique():
        engine_data = train_raw[train_raw['engine_id'] == engine_id]
        cycles = engine_data['cycle'].values
        if not np.all(np.diff(cycles) > 0):
            print(f"⚠️  Non-monotonic cycles for engine {engine_id}")

test_engine_cycle_monotonicity()
```

#### 5c. **Add Anomaly Detection**
```python
# NEW: Detect sensor anomalies
from sklearn.ensemble import IsolationForest

def detect_sensor_anomalies():
    """Find unusual sensor reading patterns"""
    iso_forest = IsolationForest(contamination=0.01, random_state=RANDOM_SEED)
    anomaly_predictions = iso_forest.fit_predict(train_raw[SENSOR_COLUMNS])
    
    anomaly_count = (anomaly_predictions == -1).sum()
    print(f"Found {anomaly_count} anomalous sensor readings ({anomaly_count/len(train_raw)*100:.2f}%)")
    
    # Flag for inspection
    if anomaly_count > 0:
        anomalies = train_raw[anomaly_predictions == -1]
        print(anomalies.head())

detect_sensor_anomalies()
```

**Expected Impact:** Early error detection, data quality transparency

---

## 6. Exploratory Analysis & RUL Labels

### Current State
- ✓ Calculates RUL from cycle data
- ✓ Visualizes engine lifespans
- ✓ Shows descriptive statistics

### Improvements to Next Step

#### 6a. **Add Advanced Visualizations**
```python
# NEW: Create comprehensive EDA dashboard
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Engine lifespan distribution with KDE
axes[0, 0].hist(engine_lifespans, bins=20, alpha=0.7, color='steelblue')
engine_lifespans.plot.kde(ax=axes[0, 0], secondary_y=True, color='red')
axes[0, 0].set_title('Engine Lifespan Distribution')

# 2. RUL distribution by phase
train_labeled['rul_phase'].value_counts().plot(kind='bar', ax=axes[0, 1])
axes[0, 1].set_title('RUL Distribution by Phase')

# 3. Sensor-RUL correlation
sensor_rul_corr = train_labeled[SENSOR_COLUMNS + ['rul']].corr()['rul'].sort_values(ascending=False)
sensor_rul_corr[:-1].plot(kind='barh', ax=axes[1, 0])
axes[1, 0].set_title('Sensor-RUL Correlation')

# 4. Engine degradation pattern (sample engines)
for engine_id in train_labeled['engine_id'].unique()[:5]:
    engine_data = train_labeled[train_labeled['engine_id'] == engine_id].sort_values('cycle')
    axes[1, 1].plot(engine_data['cycle'], engine_data['rul'], label=f'Engine {engine_id}', alpha=0.7)
axes[1, 1].set_title('Degradation Curves (Sample Engines)')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('eda_dashboard.png', dpi=300, bbox_inches='tight')
```

#### 6b. **Add Statistical Tests for RUL Distribution**
```python
# NEW: Test if RUL distribution is normal/skewed
from scipy.stats import shapiro, skew, kurtosis

stat, p_value = shapiro(train_labeled['rul'])
print(f"Shapiro-Wilk normality test:")
print(f"  p-value: {p_value:.4f}")
print(f"  Normal: {'Yes' if p_value > 0.05 else 'No'}")

print(f"\nRUL distribution shape:")
print(f"  Skewness: {skew(train_labeled['rul']):.2f}")
print(f"  Kurtosis: {kurtosis(train_labeled['rul']):.2f}")

# Implication for modeling
if skew(train_labeled['rul']) > 0.5:
    print("  ⚠️  Right-skewed distribution - consider Box-Cox transform")
```

#### 6c. **Add Degradation Pattern Analysis**
```python
# NEW: Analyze degradation trajectories
def analyze_degradation_patterns():
    """Classify engines by degradation speed"""
    engine_stats = train_labeled.groupby('engine_id').agg({
        'cycle': 'max',
        'rul': ['min', 'max']
    }).round(1)
    
    engine_stats['degradation_speed'] = engine_stats[('cycle', 'max')] / engine_stats[('rul', 'max')]
    
    # Classify: fast/medium/slow degradation
    Q1 = engine_stats['degradation_speed'].quantile(0.33)
    Q2 = engine_stats['degradation_speed'].quantile(0.67)
    
    slow = (engine_stats['degradation_speed'] < Q1).sum()
    medium = ((engine_stats['degradation_speed'] >= Q1) & 
              (engine_stats['degradation_speed'] < Q2)).sum()
    fast = (engine_stats['degradation_speed'] >= Q2).sum()
    
    print(f"Degradation pattern distribution:")
    print(f"  Slow:   {slow} engines")
    print(f"  Medium: {medium} engines")
    print(f"  Fast:   {fast} engines")

analyze_degradation_patterns()
```

**Expected Impact:** Deeper insights, better feature engineering direction

---

## 7. Feature Engineering

### Current State
- ✓ Removes constant-value sensors
- ✓ Creates rolling window features
- ✓ Prevents future-data leakage

### Improvements to Next Step

#### 7a. **Add Feature Selection & Importance Analysis**
```python
# NEW: Select most important features before modeling
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.preprocessing import StandardScaler

# Fit selector on training data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(train_features[feature_cols])

selector = SelectKBest(f_regression, k=30)  # Keep top 30 features
X_selected = selector.fit_transform(X_scaled, train_features['rul'])

# Get selected feature names
selected_features = np.array(feature_cols)[selector.get_support()]
print(f"Top 30 features selected:")
for i, feature in enumerate(selected_features, 1):
    print(f"  {i}. {feature}")

# Store for later use
FEATURE_COLUMNS = list(selected_features)
```

#### 7b. **Add Feature Interaction Terms**
```python
# NEW: Create polynomial and interaction features
from sklearn.preprocessing import PolynomialFeatures

# Create interactions between top sensors
top_sensors = ['sensor_9', 'sensor_14', 'sensor_4', 'sensor_3']
poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)

interaction_features = poly.fit_transform(train_features[top_sensors])
interaction_feature_names = poly.get_feature_names_out(top_sensors)

# Add to feature set
for name, feature_col in zip(interaction_feature_names, interaction_features.T):
    train_features[f'interaction_{name}'] = feature_col

print(f"Added {len(interaction_feature_names)} interaction features")
```

#### 7c. **Add Domain-Specific Features**
```python
# NEW: Engineer domain-expert features
def engineer_domain_features(frame):
    """Create maintenance-relevant features"""
    result = frame.copy()
    
    # 1. Degradation rate (change in key sensors)
    for sensor in rolling_sensors:
        result[f'{sensor}_rate_of_change'] = (
            result.groupby('engine_id')[sensor]
            .transform(lambda x: x.diff(5))  # 5-cycle rate
        )
    
    # 2. Distance to failure (proxy based on sensor patterns)
    result['degradation_intensity'] = (
        result[rolling_sensors].std(axis=1)
    )
    
    # 3. Operational stress level (combination of operating settings & sensors)
    result['operational_stress'] = (
        result['op_setting_1'].abs() + 
        result['op_setting_2'].abs()
    )
    
    return result

train_features = engineer_domain_features(train_features)
```

#### 7d. **Add Feature Documentation**
```python
# NEW: Document all features with metadata
FEATURE_METADATA = {
    'sensor_9_mean_5': {
        'type': 'rolling_mean',
        'base_sensor': 'sensor_9',
        'window': 5,
        'domain': 'turbine_vibration',
        'importance': 'high'
    },
    'sensor_14_std_10': {
        'type': 'rolling_std',
        'base_sensor': 'sensor_14',
        'window': 10,
        'domain': 'combustor_health',
        'importance': 'high'
    },
    # ... etc for all features
}

# Save feature documentation
with open('feature_metadata.json', 'w') as f:
    json.dump(FEATURE_METADATA, f, indent=2)
```

**Expected Impact:** Better predictive power, faster training

---

## 8. Create 40/10/10/40 Partitions

### Current State
- ✓ Stratified by engine
- ✓ Proper validation splits
- ✓ No data leakage

### Improvements to Next Step

#### 8a. **Add Partition Balance Validation**
```python
# NEW: Verify partitions are balanced
def validate_partition_balance(partitions, target_col='rul'):
    """Check if partitions have similar distributions"""
    print("Partition Distribution Analysis:")
    print("-" * 60)
    
    for partition_name, df in partitions.items():
        print(f"\n{partition_name}:")
        print(f"  Engines: {df['engine_id'].nunique()}")
        print(f"  Rows: {len(df)}")
        print(f"  RUL stats:")
        print(f"    Mean: {df[target_col].mean():.1f}")
        print(f"    Std:  {df[target_col].std():.1f}")
        print(f"    Min:  {df[target_col].min():.1f}")
        print(f"    Max:  {df[target_col].max():.1f}")
        
        # Check RUL phase distribution
        phase_dist = df['rul_phase'].value_counts(normalize=True) * 100
        print(f"  Phase distribution:")
        for phase, pct in phase_dist.items():
            print(f"    {phase}: {pct:.1f}%")

validate_partition_balance(partitions)
```

#### 8b. **Add Temporal Split Validation**
```python
# NEW: If data has temporal aspect, validate no time leakage
def validate_temporal_split():
    """For time-series data, verify no future data in training"""
    # If adding temporal features later
    train_max_cycle = partitions['train'].groupby('engine_id')['cycle'].max().max()
    test_min_cycle = partitions['test'].groupby('engine_id')['cycle'].min().min()
    
    print(f"Temporal separation check:")
    print(f"  Training max cycle: {train_max_cycle}")
    print(f"  Test min cycle:     {test_min_cycle}")
    
    # Note: In turbofan, different engines so this check is less relevant
    # But important for other time-series problems

validate_temporal_split()
```

#### 8c. **Add Stratification by Additional Dimensions**
```python
# NEW: Consider multi-dimensional stratification
# Current: stratified by engine
# Could also stratify by: degradation speed, operating regime, etc.

# Example: Stratify by both engine AND degradation speed
train_features['degradation_speed'] = (
    train_features.groupby('engine_id')['cycle'].transform('max') / 
    train_features.groupby('engine_id')['rul'].transform('max')
)

# Create stratification groups
train_features['strat_group'] = (
    train_features['engine_id'].astype(str) + '_' +
    pd.cut(train_features['degradation_speed'], bins=3, labels=['slow', 'med', 'fast']).astype(str)
)

# Then stratify split using these groups
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(
    train_features, 
    test_size=0.2,
    stratify=train_features['strat_group'],
    random_state=RANDOM_SEED
)
```

**Expected Impact:** Better partition quality, reduced model bias

---

## 9. Save Processed Files & Upload to S3

### Current State
- ✓ Saves multiple file formats
- ✓ Uploads to S3 with organized prefixes
- ✓ Creates train/val/test/prod splits

### Improvements to Next Step

#### 9a. **Add Data Versioning & Metadata**
```python
# NEW: Track data versions and transformations
data_manifest = {
    "version": "1.0",
    "created": datetime.now().isoformat(),
    "raw_data_version": "FD001-v1",
    "processing_steps": [
        "loaded_raw_files",
        "validated_schema",
        "calculated_rul",
        "engineered_features_52",
        "created_partitions_40_10_10_40"
    ],
    "files": {
        "train": {
            "features": "s3://.../processed/train_features.csv",
            "xgboost": "s3://.../processed/train_xgboost.csv",
            "rows": len(partitions['train']),
            "engines": partitions['train']['engine_id'].nunique()
        },
        # ... etc for other partitions
    },
    "feature_info": {
        "total_features": len(FEATURE_COLUMNS),
        "feature_names": FEATURE_COLUMNS,
        "engineered_features": len([f for f in FEATURE_COLUMNS if '_mean_' in f or '_std_' in f])
    }
}

# Save manifest
with open('data_manifest.json', 'w') as f:
    json.dump(data_manifest, f, indent=2)

s3.upload_file('data_manifest.json', bucket, 
               f'{PROJECT_PREFIX}/metadata/data_manifest.json')
```

#### 9b. **Add Data Quality Metrics Export**
```python
# NEW: Export quality metrics with data
quality_metrics = {
    "missing_values": {
        "train": int(train_features.isna().sum().sum()),
        "validation": int(validation_features.isna().sum().sum()),
        "test": int(test_features.isna().sum().sum())
    },
    "feature_statistics": {
        feature: {
            "mean": float(train_features[feature].mean()),
            "std": float(train_features[feature].std()),
            "min": float(train_features[feature].min()),
            "max": float(train_features[feature].max())
        }
        for feature in FEATURE_COLUMNS[:10]  # Sample
    },
    "partition_balance": {
        name: len(df) for name, df in partitions.items()
    }
}

with open('quality_metrics.json', 'w') as f:
    json.dump(quality_metrics, f, indent=2)
```

#### 9c. **Add Data Lineage Tracking**
```python
# NEW: Track complete data lineage
import hashlib

def compute_dataset_hash(df):
    """Compute hash of dataset for integrity checks"""
    return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

lineage_metadata = {
    "nasa_archive_hash": compute_file_hash(RAW_DIR / "train_FD001.txt"),
    "processed_train_hash": compute_dataset_hash(partitions['train']),
    "processed_validation_hash": compute_dataset_hash(partitions['validation']),
    "processed_test_hash": compute_dataset_hash(partitions['test']),
    "transformation_sequence": [
        {"step": 1, "name": "raw_load", "input_rows": 20631},
        {"step": 2, "name": "feature_engineering", "output_features": 52},
        {"step": 3, "name": "partitioning", "output_partitions": 4}
    ]
}

with open('lineage_metadata.json', 'w') as f:
    json.dump(lineage_metadata, f, indent=2)
```

**Expected Impact:** Full data traceability, compliance, reproducibility

---

## 10. Athena Catalog & SQL Querying

### Current State
- ✓ Creates database and table
- ✓ Supports SQL queries over CSV
- ✓ Sample query runs

### Improvements to Next Step

#### 10a. **Add Advanced SQL Analytics**
```python
# NEW: Complex analytical queries

# Query 1: Identify engines approaching failure
high_risk_engines = athena.start_query_execution(
    QueryString="""
    SELECT 
        engine_id,
        MIN(rul) as lowest_rul,
        MAX(rul) as highest_rul,
        COUNT(*) as observation_count,
        CASE 
            WHEN MIN(rul) < 25 THEN 'Critical'
            WHEN MIN(rul) < 50 THEN 'Degraded'
            ELSE 'Healthy'
        END as health_status
    FROM aai540_turbofan_556241.fd001_training_features
    GROUP BY engine_id
    HAVING MIN(rul) < 50
    ORDER BY MIN(rul) ASC
    """,
    ResultConfiguration={"OutputLocation": athena_output}
)

# Query 2: Sensor trend analysis
sensor_trends = athena.start_query_execution(
    QueryString="""
    SELECT 
        ROUND(AVG(sensor_2), 2) as avg_sensor_2,
        ROUND(AVG(sensor_3), 2) as avg_sensor_3,
        ROUND(STDDEV(sensor_2), 2) as std_sensor_2,
        ROUND(STDDEV(sensor_3), 2) as std_sensor_3,
        CASE 
            WHEN rul > 100 THEN 'Healthy'
            WHEN rul > 50 THEN 'Degrading'
            ELSE 'Critical'
        END as rul_phase,
        COUNT(*) as samples
    FROM aai540_turbofan_556241.fd001_training_features
    GROUP BY 4
    ORDER BY 4 DESC
    """,
    ResultConfiguration={"OutputLocation": athena_output}
)
```

#### 10b. **Add Athena Performance Optimization**
```python
# NEW: Optimize Athena queries for cost & speed
# 1. Use Parquet format instead of CSV (more efficient)
# 2. Partition by RUL phase or engine
# 3. Use columnar queries to scan only needed columns

# Convert CSV to Parquet for better performance
parquet_key = f"{PROJECT_PREFIX}/processed/train_features.parquet"
train_features.to_parquet(
    f"s3://{bucket}/{parquet_key}",
    index=False
)

# Create Athena table on Parquet
create_parquet_table = athena.start_query_execution(
    QueryString=f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS aai540_turbofan_556241.fd001_training_features_parquet
    WITH (
        format = 'PARQUET',
        bucketed_by = ARRAY['engine_id'],
        bucket_count = 10,
        external_location = 's3://{bucket}/{PROJECT_PREFIX}/processed/'
    )
    AS SELECT * FROM aai540_turbofan_556241.fd001_training_features
    """,
    ResultConfiguration={"OutputLocation": athena_output}
)

print("✓ Parquet table created (10-100x faster queries)")
```

#### 10c. **Add Query Cost Monitoring**
```python
# NEW: Track Athena query costs
def get_athena_cost(bytes_scanned):
    """Calculate cost of Athena query"""
    cost_per_gb = 5.0  # $5 per TB = $0.005 per GB
    cost = (bytes_scanned / (1024**3)) * cost_per_gb
    return cost

# Monitor query costs
for query_id in query_ids:
    response = athena.get_query_execution(QueryExecutionId=query_id)
    bytes_scanned = response['QueryExecution']['Statistics'].get('DataScannedInBytes', 0)
    query_cost = get_athena_cost(bytes_scanned)
    print(f"Query {query_id}: ${query_cost:.4f} (scanned {bytes_scanned / 1e9:.2f} GB)")
```

**Expected Impact:** Cost efficiency, query performance

---

## 11. SageMaker Feature Store

### Current State
- ✓ Creates offline feature group
- ✓ Ingests 20,631 records
- ✓ Provides offline store location

### Improvements to Next Step

#### 11a. **Add Online Feature Store**
```python
# NEW: Enable online store for real-time predictions
from sagemaker.feature_store.feature_group import FeatureGroup, FeatureDefinition

feature_group_online = FeatureGroup(
    name=feature_group_name + "-online",
    sagemaker_session=sm_session
)

# Enable online store for low-latency serving
feature_group_online.create(
    s3_uri=f"s3://{bucket}/{PROJECT_PREFIX}/feature-store/",
    record_identifier_name="record_id",
    event_time_feature_name="event_time",
    role_arn=role,
    enable_online_store=True,  # NEW: Online store for real-time
    online_store_config={
        'EnableOnlineStore': True,
        'TTLDuration': {
            'Unit': 'Days',
            'Value': 30
        }
    }
)

print("✓ Online feature store enabled for real-time serving")
```

#### 11b. **Add Feature Monitoring & Validation**
```python
# NEW: Monitor feature quality and drift
from sagemaker.feature_store.feature_store_session import FeatureStoreSession

fs_session = FeatureStoreSession(
    boto_session=boto3.Session(),
    sagemaker_session=sm_session
)

# Create feature validation rules
validation_rules = {
    'sensor_2': {
        'min': 641.0,
        'max': 645.0,
        'allow_null': False
    },
    'sensor_3': {
        'min': 1570.0,
        'max': 1620.0,
        'allow_null': False
    },
    # ... etc
}

def validate_incoming_features(new_features, rules):
    """Validate features before ingestion"""
    for col, constraints in rules.items():
        if col in new_features.columns:
            if 'min' in constraints:
                violations = (new_features[col] < constraints['min']).sum()
                if violations > 0:
                    print(f"⚠️  {violations} values below minimum for {col}")
            
            if 'max' in constraints:
                violations = (new_features[col] > constraints['max']).sum()
                if violations > 0:
                    print(f"⚠️  {violations} values above maximum for {col}")

validate_incoming_features(feature_store_frame, validation_rules)
```

#### 11c. **Add Feature Discovery & Metadata**
```python
# NEW: Rich feature documentation for discovery
feature_group_description = {
    "feature_group_name": feature_group_name,
    "purpose": "Store engineered features for turbofan RUL prediction",
    "features": {
        "record_id": {
            "description": "Unique identifier (engine_id + cycle)",
            "type": "string",
            "tags": ["identifier"]
        },
        "sensor_2_mean_5": {
            "description": "5-cycle rolling mean of sensor 2 (compressor)",
            "type": "double",
            "physical_unit": "temperature_celsius",
            "domain": "compressor_health",
            "importance": "high"
        },
        # ... etc for all features
    },
    "update_frequency": "daily",
    "retention": "180_days"
}

# Store in SageMaker Studio for discoverability
sm_client.create_model_card(
    ModelCardContent=json.dumps(feature_group_description)
)
```

**Expected Impact:** Real-time serving capability, feature governance

---

## 12. Train Benchmark Model

### Current State
- ✓ Linear regression baseline
- ✓ StandardScaler preprocessing
- ✓ Validation RMSE: 31.01 cycles

### Improvements to Next Step

#### 12a. **Add Cross-Validation**
```python
# NEW: K-fold cross-validation for robust evaluation
from sklearn.model_selection import cross_val_score, KFold

kfold = KFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)

cv_scores_rmse = -cross_val_score(
    Pipeline([
        ('scaler', StandardScaler()),
        ('regression', LinearRegression())
    ]),
    X_train, y_train,
    cv=kfold,
    scoring='neg_root_mean_squared_error'
)

print(f"Cross-validation RMSE scores: {cv_scores_rmse}")
print(f"  Mean: {cv_scores_rmse.mean():.2f} ± {cv_scores_rmse.std():.2f} cycles")
```

#### 12b. **Add Hyperparameter Tuning**
```python
# NEW: GridSearch for optimal baseline
from sklearn.model_selection import GridSearchCV

# For linear regression, tune fit_intercept, normalize
param_grid = {
    'regression__fit_intercept': [True, False],
    'regression__positive': [True, False]
}

grid_search = GridSearchCV(
    Pipeline([
        ('scaler', StandardScaler()),
        ('regression', LinearRegression())
    ]),
    param_grid,
    cv=5,
    scoring='neg_mean_squared_error'
)

grid_search.fit(X_train, y_train)
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best CV RMSE: {np.sqrt(-grid_search.best_score_):.2f} cycles")
```

#### 12c. **Add Residual Analysis**
```python
# NEW: Analyze prediction residuals
residuals = y_validation - benchmark_predictions

print(f"Residual Statistics:")
print(f"  Mean: {residuals.mean():.4f} (should be ~0)")
print(f"  Std:  {residuals.std():.2f}")
print(f"  Min:  {residuals.min():.2f}")
print(f"  Max:  {residuals.max():.2f}")

# Test for normality
from scipy.stats import shapiro
stat, p = shapiro(residuals)
print(f"\nNormality test: p={p:.4f} (normal if p>0.05)")

# Plot residuals
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].scatter(benchmark_predictions, residuals, alpha=0.5)
axes[0].axhline(y=0, color='r', linestyle='--')
axes[0].set_xlabel('Predicted RUL')
axes[0].set_ylabel('Residual')
axes[0].set_title('Residual Plot')

axes[1].hist(residuals, bins=20, edgecolor='black')
axes[1].set_xlabel('Residual')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Residual Distribution')
plt.tight_layout()
plt.savefig('residual_analysis.png')
```

**Expected Impact:** More robust baseline, better hyperparameters

---

## 13. SageMaker Training Job

### Current State
- ✓ Managed XGBoost training
- ✓ Hyperparameters tuned
- ✓ Validation monitoring

### Improvements to Next Step

#### 13a. **Add Hyperparameter Optimization (HPO)**
```python
# NEW: Automated hyperparameter tuning with Bayesian Optimization
from sagemaker.tuner import IntegerParameter, ContinuousParameter, HyperparameterTuner

hyperparameter_ranges = {
    'eta': ContinuousParameter(0.01, 0.2),
    'max_depth': IntegerParameter(3, 8),
    'min_child_weight': IntegerParameter(2, 10),
    'subsample': ContinuousParameter(0.5, 1.0),
    'gamma': ContinuousParameter(0, 5),
}

tuner = HyperparameterTuner(
    estimator=xgb_estimator,
    objective_metric_name='validation:rmse',
    hyperparameter_ranges=hyperparameter_ranges,
    metric_definitions=[
        {'Name': 'validation:rmse', 'Regex': 'validation:rmse=([0-9\\.]+)'}
    ],
    max_jobs=20,
    max_parallel_jobs=4,
    base_job_name='aai540-xgb-hpo'
)

tuner.fit(channels, wait=True, logs=True)
best_job = tuner.best_training_job()
print(f"Best training job: {best_job}")
```

#### 13b. **Add Experiment Tracking**
```python
# NEW: Track experiments with SageMaker Experiments
from sagemaker.experiments.run import Run
from sagemaker.experiments.experiment import Experiment

with Run.create(
    experiment_name="turbofan-rul-experiments",
    run_name=f"xgboost-baseline-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
    sagemaker_session=sm_session
) as run:
    
    # Log parameters
    run.log_parameter("model_type", "xgboost")
    run.log_parameter("eta", 0.05)
    run.log_parameter("max_depth", 4)
    run.log_parameter("training_instances", 1)
    
    # Log metrics
    run.log_metric(name="validation_rmse", value=31.01, step=1)
    run.log_metric(name="test_rmse", value=20.10, step=1)
    
    # Log model artifact
    run.log_model(model_uri=xgb_estimator.model_data)
```

#### 13c. **Add Model Interpretability**
```python
# NEW: SHAP values for model interpretation
import shap

# Get predictions for SHAP analysis
shap_sample = X_test.iloc[:100]  # Sample of test data

# Create SHAP explainer
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(shap_sample)

# Plot SHAP summary
plt.figure()
shap.summary_plot(shap_values, shap_sample, plot_type="bar", show=False)
plt.savefig('shap_summary.png', dpi=300, bbox_inches='tight')

# Identify most important features
print("Top 10 most important features (by mean |SHAP|):")
feature_importance = np.abs(shap_values).mean(axis=0)
top_features = np.argsort(feature_importance)[-10:]
for idx in reversed(top_features):
    print(f"  {feature_cols[idx]}: {feature_importance[idx]:.4f}")
```

**Expected Impact:** Better hyperparameters, reproducible experiments, interpretability

---

## 14. Model Registry & Management

### Current State
- ✓ Creates model package group
- ✓ Registers model with approval status
- ✓ Provides model ARN

### Improvements to Next Step

#### 14a. **Add Comprehensive Model Card**
```python
# NEW: Detailed model card per AWS standards
from sagemaker.model_card import ModelCard, ModelOverview

model_card = ModelCard.create(
    name=f"aai540-turbofan-rul-{account_id}",
    model_id=f"xgboost-v1",
    model_type="gradient_boosting",
    model_description="XGBoost model for turbofan engine RUL prediction"
)

# Add intended use
model_card.training_details.add_training_objective(
    objective="Predict remaining useful life of turbofan engines",
    metrics=[
        {"name": "RMSE", "value": 20.10, "notes": "Test set RMSE in cycles"},
        {"name": "MAE", "value": 14.10, "notes": "Test set MAE in cycles"}
    ]
)

# Add model architecture
model_card.model_overview.set_model_architecture("XGBoost Regressor")
model_card.model_overview.set_algorithm_type("Gradient Boosting")

# Add performance details by RUL phase
model_card.evaluation_details.add_evaluation(
    name="performance_by_rul_phase",
    evaluation_data=pd.DataFrame({
        "rul_phase": ["Healthy", "Degrading", "Degraded", "Critical"],
        "rmse": [5.2, 12.4, 18.1, 22.3],
        "sample_count": [8000, 6000, 4000, 2631]
    })
)

# Add limitations
model_card.model_overview.add_limitation(
    "Only trained on single operating condition (FD001)")
model_card.model_overview.add_limitation(
    "Early-cycle predictions less accurate (limited training data)")

model_card.save_html()
```

#### 14b. **Add Model Risk Assessment**
```python
# NEW: Risk assessment and mitigation strategies
model_risk_assessment = {
    "risks": [
        {
            "risk": "Under-prediction of critical RUL",
            "likelihood": "medium",
            "impact": "engine failure not prevented",
            "mitigation": "Confidence thresholds, manual review for RUL<25"
        },
        {
            "risk": "Model drift on new operating conditions",
            "likelihood": "high",
            "impact": "reduced accuracy over time",
            "mitigation": "Monthly retraining, drift monitoring"
        },
        {
            "risk": "Bias toward healthy engines",
            "likelihood": "high",
            "impact": "poor early-cycle predictions",
            "mitigation": "Weighted loss function, resampling"
        }
    ],
    "monitoring_plan": {
        "monthly_retraining": True,
        "drift_detection": "statistical test on sensor distributions",
        "performance_degradation_threshold": 5.0,  # % RMSE increase
        "audit_frequency": "quarterly"
    }
}

with open('model_risk_assessment.json', 'w') as f:
    json.dump(model_risk_assessment, f, indent=2)
```

#### 14c. **Add Model Approvals Workflow**
```python
# NEW: Structured approval process
approval_checklist = {
    "model_name": "aai540-turbofan-rul-v1",
    "version": 1,
    "approval_criteria": {
        "test_rmse_threshold": {"threshold": 25.0, "actual": 20.10, "passed": True},
        "critical_rul_mae": {"threshold": 30.0, "actual": 22.3, "passed": True},
        "data_quality_score": {"threshold": 0.95, "actual": 0.98, "passed": True},
        "bias_evaluation": {"threshold": 0.1, "actual": 0.08, "passed": True},
        "documentation_complete": True,
        "security_review_approved": True,
        "compliance_check_passed": True
    },
    "approvers": [
        {"name": "Data Science Lead", "status": "pending"},
        {"name": "ML Ops Lead", "status": "pending"},
        {"name": "Business Owner", "status": "pending"}
    ],
    "approval_date": None,
    "deployment_authorized": False
}

def check_approval_readiness(checklist):
    """Verify all criteria met for deployment"""
    criteria_results = checklist['approval_criteria']
    all_passed = all(v.get('passed', v) for v in criteria_results.values())
    
    if all_passed:
        print("✓ Model meets all approval criteria")
        print("  Ready for staging deployment")
    else:
        print("✗ Model does not meet all criteria:")
        for criterion, result in criteria_results.items():
            if not result.get('passed', result):
                print(f"  - {criterion}: FAILED")

check_approval_readiness(approval_checklist)
```

**Expected Impact:** Better governance, risk management, compliance

---

## 15. Batch Transform Deployment

### Current State
- ✓ Batch scoring on test set
- ✓ Downloads predictions
- ✓ Calculates RMSE/MAE

### Improvements to Next Step

#### 15a. **Add Confidence Scores**
```python
# NEW: Quantile regression for prediction intervals
from xgboost import XGBRegressor

# Train quantile models for confidence intervals
quantile_models = {}
for quantile in [0.05, 0.5, 0.95]:
    qrf = XGBRegressor(
        objective=f'reg:quantilehubererror',
        quantile_alpha=quantile,
        random_state=RANDOM_SEED
    )
    qrf.fit(X_train, y_train)
    quantile_models[quantile] = qrf

# Generate predictions with confidence intervals
predictions_lower = np.clip(quantile_models[0.05].predict(X_test), 0, RUL_CAP)
predictions_mean = np.clip(xgb_model.predict(X_test), 0, RUL_CAP)
predictions_upper = np.clip(quantile_models[0.95].predict(X_test), 0, RUL_CAP)

# Output with confidence
results_with_confidence = pd.DataFrame({
    'engine_id': test_results['engine_id'],
    'cycle': test_results['cycle'],
    'actual_rul': test_results['rul'],
    'predicted_rul': predictions_mean,
    'rul_lower_95ci': predictions_lower,
    'rul_upper_95ci': predictions_upper,
    'confidence_interval_width': predictions_upper - predictions_lower,
    'prediction_confidence': 1.0 / (predictions_upper - predictions_lower + 1)
})

print(results_with_confidence.head(10))
```

#### 15b. **Add Batch Processing Monitoring**
```python
# NEW: Track batch job performance
batch_job_stats = {
    "job_name": transformer.latest_transform_job.name,
    "instance_type": "ml.m5.large",
    "total_samples": len(X_test),
    "samples_processed": len(predictions_mean),
    "processing_time_seconds": 240,
    "throughput": len(X_test) / 240,  # samples per second
    "cost_estimate": 0.134 * (240 / 3600),  # $0.134/hr for ml.m5.large
    "prediction_latency_ms": (240 * 1000) / len(X_test)
}

print(f"Batch Transform Job Statistics:")
print(f"  Samples processed: {batch_job_stats['samples_processed']:,}")
print(f"  Throughput: {batch_job_stats['throughput']:.1f} samples/sec")
print(f"  Total cost: ${batch_job_stats['cost_estimate']:.4f}")
print(f"  Avg latency: {batch_job_stats['prediction_latency_ms']:.1f} ms/sample")
```

#### 15c. **Add Prediction Anomaly Detection**
```python
# NEW: Flag unusual predictions
def detect_prediction_anomalies(predictions, actual, threshold_zscore=3):
    """Identify predictions that deviate significantly from expected"""
    errors = np.abs(predictions - actual)
    
    # Z-score based detection
    z_scores = np.abs((errors - errors.mean()) / errors.std())
    anomalies = z_scores > threshold_zscore
    
    if anomalies.any():
        print(f"Found {anomalies.sum()} anomalous predictions:")
        anomaly_idx = np.where(anomalies)[0]
        for idx in anomaly_idx[:10]:  # Show first 10
            print(f"  Sample {idx}: actual={actual[idx]:.1f}, " +
                  f"predicted={predictions[idx]:.1f}, error={errors[idx]:.1f}")
    
    return anomalies

anomalies = detect_prediction_anomalies(predictions_mean, y_test.values)
```

**Expected Impact:** Better prediction interpretability, anomaly detection

---

## 16. Observability & Monitoring Prep

### Current State
- ✓ Creates feature baseline statistics
- ✓ Uploads to S3
- ✓ Ready for monitoring service

### Improvements to Next Step

#### 16a. **Add Automated Drift Detection**
```python
# NEW: Statistical tests for data/prediction drift
from scipy import stats
import numpy as np

def detect_data_drift(baseline_df, current_df, threshold=0.05):
    """Compare current data distribution with training baseline"""
    drift_results = {}
    
    for column in baseline_df.columns:
        if column not in current_df.columns:
            continue
        
        # Kolmogorov-Smirnov test
        statistic, p_value = stats.ks_2samp(
            baseline_df[column], 
            current_df[column]
        )
        
        drift_detected = p_value < threshold
        drift_results[column] = {
            'statistic': statistic,
            'p_value': p_value,
            'drift_detected': drift_detected,
            'baseline_mean': baseline_df[column].mean(),
            'current_mean': current_df[column].mean(),
            'mean_shift_pct': ((current_df[column].mean() - baseline_df[column].mean()) / 
                               baseline_df[column].mean() * 100)
        }
    
    return drift_results

# Test on validation set
drift_report = detect_data_drift(train_features[FEATURE_COLUMNS], 
                                 validation_features[FEATURE_COLUMNS])

print("Data Drift Detection Report:")
print("-" * 70)
for feature, results in list(drift_report.items())[:10]:
    if results['drift_detected']:
        print(f"⚠️  {feature}: DRIFT DETECTED")
        print(f"    Mean shift: {results['mean_shift_pct']:+.1f}%")
    else:
        print(f"✓ {feature}: stable")
```

#### 16b. **Add Real-Time Prediction Monitoring**
```python
# NEW: CloudWatch metrics for production model
def publish_prediction_metrics(predictions, actuals, engine_ids):
    """Publish prediction metrics to CloudWatch"""
    
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    
    # Batch metric publishing (CloudWatch has limits)
    metrics_data = []
    
    # Overall metrics
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    mae = mean_absolute_error(actuals, predictions)
    
    metrics_data.append({
        'MetricName': 'ModelRMSE',
        'Value': rmse,
        'Unit': 'None',
        'Timestamp': datetime.utcnow()
    })
    
    # Per-engine metrics
    for engine_id in engine_ids.unique():
        mask = engine_ids == engine_id
        engine_rmse = np.sqrt(mean_squared_error(
            actuals[mask], predictions[mask]
        ))
        
        metrics_data.append({
            'MetricName': 'EngineRMSE',
            'Value': engine_rmse,
            'Dimensions': [{'Name': 'EngineID', 'Value': str(engine_id)}],
            'Timestamp': datetime.utcnow()
        })
    
    # Publish in batches (max 20 metrics per call)
    for i in range(0, len(metrics_data), 20):
        batch = metrics_data[i:i+20]
        cloudwatch.put_metric_data(
            Namespace='TurbofanRUL',
            MetricData=batch
        )
    
    print(f"✓ Published {len(metrics_data)} metrics to CloudWatch")

publish_prediction_metrics(predictions_mean, y_test.values, test_v1['engine_id'].values)
```

#### 16c. **Add Model Performance Degradation Alert**
```python
# NEW: Alert when model performance drops
def create_performance_degradation_alarm():
    """CloudWatch alarm for model performance drop"""
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    
    cloudwatch.put_metric_alarm(
        AlarmName=f'{PROJECT_PREFIX}-rmse-degradation',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=2,
        MetricName='ModelRMSE',
        Namespace='TurbofanRUL',
        Period=3600,  # 1 hour
        Statistic='Average',
        Threshold=25.0,  # Alert if RMSE > 25 (baseline 20.10 + 25%)
        ActionsEnabled=True,
        AlarmActions=['arn:aws:sns:us-east-1:...'],  # SNS topic
        AlarmDescription='Alert when model RMSE degrades > 25 cycles',
        TreatMissingData='notBreaching'
    )
    
    print("✓ Performance degradation alarm created")

create_performance_degradation_alarm()
```

**Expected Impact:** Production monitoring, rapid issue detection

---

## 17. CI/CD Pipeline (Bonus)

### Current State
- ✓ Documents planned pipeline steps
- ✓ Shows 7-step workflow

### Improvements to Next Step

#### 17a. **Implement Actual SageMaker Pipeline**
```python
# NEW: Build executable SageMaker Pipeline
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.processing import ScriptProcessor

# Step 1: Data Validation
processor = ScriptProcessor(
    role=role,
    image_uri=sagemaker.image_uris.retrieve("scikit-learn", region, version="0.23-1"),
    instance_count=1,
    instance_type="ml.m5.xlarge"
)

step_validate = ProcessingStep(
    name="ValidateData",
    processor=processor,
    code="validate_data.py",
    job_arguments=["--input-data", train_uri]
)

# Step 2: Training (already defined)
step_train = TrainingStep(
    name="TrainXGBoost",
    estimator=xgb_estimator,
    inputs={"training": train_uri}
)

# Step 3: Evaluation
step_eval = ProcessingStep(
    name="EvaluateModel",
    processor=processor,
    code="evaluate_model.py",
    job_arguments=["--model-path", xgb_estimator.model_data]
)

# Combine into pipeline
pipeline = Pipeline(
    name=f"{PROJECT_PREFIX}-pipeline",
    parameters=[],
    steps=[step_validate, step_train, step_eval],
    sagemaker_session=sm_session
)

# Deploy pipeline
pipeline.upsert(role_arn=role)
execution = pipeline.start()
print(f"✓ Pipeline execution started: {execution.arn}")
```

#### 17b. **Add Pipeline Orchestration with Step Functions**
```python
# NEW: Orchestrate pipeline with AWS Step Functions for complex workflows
import json

step_functions_definition = {
    "Comment": "Turbofan RUL ML Pipeline",
    "StartAt": "ValidateData",
    "States": {
        "ValidateData": {
            "Type": "Task",
            "Resource": "arn:aws:states:::sagemaker:createProcessingJob.sync",
            "Next": "CheckValidation"
        },
        "CheckValidation": {
            "Type": "Choice",
            "Choices": [{
                "Variable": "$.ProcessingJobStatus",
                "StringEquals": "Completed",
                "Next": "TrainModel"
            }],
            "Default": "ValidationFailed"
        },
        "TrainModel": {
            "Type": "Task",
            "Resource": "arn:aws:states:::sagemaker:createTrainingJob.sync",
            "Next": "EvaluateModel"
        },
        "EvaluateModel": {
            "Type": "Task",
            "Resource": "arn:aws:states:::sagemaker:createProcessingJob.sync",
            "Next": "CheckPerformance"
        },
        "CheckPerformance": {
            "Type": "Choice",
            "Choices": [{
                "Variable": "$.Metrics.RMSE",
                "NumericLessThan": 25,
                "Next": "RegisterModel"
            }],
            "Default": "PerformanceFailed"
        },
        "RegisterModel": {
            "Type": "Task",
            "Resource": "arn:aws:sagemaker:...",
            "End": True
        },
        "ValidationFailed": {
            "Type": "Fail",
            "Error": "DataValidationFailed"
        },
        "PerformanceFailed": {
            "Type": "Fail",
            "Error": "PerformanceThresholdNotMet"
        }
    }
}
```

**Expected Impact:** Fully automated, reproducible ML workflows

---

## Summary: Priority Ranking

### 🔴 High Priority (Do First)
1. **Section 1:** Resource validation & IAM checks
2. **Section 2:** Cost estimation & budgeting
3. **Section 5:** Data profiling & anomaly detection
4. **Section 7:** Feature selection & importance
5. **Section 12:** Cross-validation & residual analysis

### 🟡 Medium Priority (Do Next)
6. **Section 10:** Parquet optimization for Athena
7. **Section 13:** Hyperparameter optimization
8. **Section 14:** Model Card & risk assessment
9. **Section 16:** Drift detection monitoring

### 🟢 Low Priority (Future Enhancements)
10. **Section 11:** Online Feature Store
11. **Section 17:** Full CI/CD pipeline implementation
12. **Section 15:** Confidence intervals & anomaly detection

---

## Implementation Guide

Each section improvement can be implemented independently. Recommended approach:

1. **Start with data quality** (Sections 1-6)
2. **Enhance modeling** (Sections 7, 12-13)
3. **Add governance** (Sections 2, 14)
4. **Deploy monitoring** (Sections 16-17)

Each enhancement adds 5-15% value to the overall ML operations workflow.
