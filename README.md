# Multi-Cloud Healthcare Data Lake & Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GCP](https://img.shields.io/badge/Cloud-GCP-orange.svg)](https://cloud.google.com/)
[![AWS](https://img.shields.io/badge/Cloud-AWS-yellow.svg)](https://aws.amazon.com/)

> **A comprehensive data engineering portfolio project demonstrating multi-cloud healthcare data integration, ETL pipelines, and analytics.**

## 🎯 Project Overview

This project demonstrates real-world data engineering skills by building an end-to-end healthcare analytics platform that spans two cloud providers (GCP and AWS). It simulates a common enterprise scenario: aggregating and analyzing data from two disparate systems - a retail pharmacy system and a hospital EHR system.

### Business Context
Healthcare organizations frequently need to:
- Reconcile medication data across pharmacy and clinical systems
- Analyze patient outcomes and medication adherence
- Track specialty medication (REMS) compliance
- Generate insights for quality improvement and cost optimization

This project showcases how a data engineer would solve these challenges using modern cloud data platforms.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA SOURCES (Synthetic)                    │
├───────────────────────────────┬─────────────────────────────────┤
│    Pharmacy System            │         EHR System              │
│  • Patient Demographics       │  • Patient Demographics         │
│  • Prescriptions              │  • Clinical Notes (SOAP)        │
│  • Insurance Adjudication     │  • Lab Results                  │
│  • Medication Dispensing      │  • Diagnoses (ICD-10)           │
│  • REMS Tracking              │  • Immunizations                │
└───────────────────────────────┴─────────────────────────────────┘
                │                                │
                ▼                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CLOUD STORAGE                            │
├───────────────────────────────┬─────────────────────────────────┤
│     Google Cloud Platform     │     Amazon Web Services         │
│  • BigQuery (Data Warehouse)  │  • S3 (Data Lake)               │
│  • Cloud Storage (Staging)    │  • Athena (Query Engine)        │
│  • 4 Tables, Partitioned      │  • Glue (Data Catalog)          │
│                               │  • 5 Tables, External           │
└───────────────────────────────┴─────────────────────────────────┘
                │                                │
                ▼                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ETL & INTEGRATION                          │
│  • Python-based ETL Pipelines                                   │
│  • Cross-cloud Data Synchronization                             │
│  • Data Quality Validation                                      │
│  • Incremental Load Processing                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYTICS & VISUALIZATION                    │
│  • SQL Analytics (BigQuery + Athena)                            │
│  • Tableau Dashboards                                           │
│  • Medication Reconciliation Reports                            │
│  • Population Health Analytics                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

### Technical Capabilities
- ✅ **Multi-Cloud Architecture**: Demonstrates expertise across GCP and AWS
- ✅ **ETL Pipelines**: Production-quality data transformation and validation
- ✅ **Healthcare Domain Knowledge**: REMS compliance, ICD-10 coding, ACIP guidelines
- ✅ **Data Quality**: Automated validation, error handling, audit logging
- ✅ **Scalable Design**: Partitioned tables, optimized queries, incremental loads
- ✅ **Security Best Practices**: IAM roles, encryption, least privilege access
- ✅ **Cost Optimization**: Free tier usage, efficient query design, budget alerts

### Healthcare-Specific Features
- 📊 **Medication Adherence Tracking**: PDC calculations, gap analysis
- 💊 **REMS Medication Monitoring**: Specialty drug compliance tracking
- 🏥 **Clinical Outcomes Analysis**: Lab trends correlated with medications
- 💰 **Insurance Analytics**: Rejection patterns, formulary impact
- 🔬 **Quality Metrics**: Immunization coverage, chronic disease management

---

## 📊 Data Scale & Complexity

- **Patients**: 250 (with matching identities across systems)
- **Prescriptions**: ~3,000 (including refills and REMS medications)
- **Lab Results**: ~2,000 (with 5-20% aberrant values based on condition burden)
- **Clinical Notes**: ~1,000 (SOAP, progress, consultation notes)
- **Insurance Transactions**: ~3,000 (15% rejection rate)
- **Immunizations**: ~1,500 (following ACIP guidelines)
- **Disease States**: 21 conditions with realistic prevalence
- **Time Period**: 24 months (January 2024 - January 2026)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- GCP account (free tier)
- AWS account (free tier)
- Tableau Public (free) or Tableau Desktop

### Installation

```bash
# Clone repository
git clone https://github.com/John-Poulos/healthcare-data-lake-project.git
cd healthcare-data-lake-project

# Install Python dependencies
cd data_generation
pip install -r requirements.txt

# Generate synthetic data
python generate_pharmacy_data.py
python generate_ehr_data.py
```

### Cloud Setup
1. **GCP Setup**: Follow [PHASE_2A_GCP_SETUP.md](documentation/PHASE_2A_GCP_SETUP.md)
2. **AWS Setup**: Follow [PHASE_2B_AWS_SETUP.md](documentation/PHASE_2B_AWS_SETUP.md)

### Data Upload
3. **Upload to GCP**: Follow [PHASE_3_DATA_UPLOAD.md](documentation/PHASE_3_DATA_UPLOAD.md)
4. **Upload to AWS**: Follow [PHASE_3_DATA_UPLOAD.md](documentation/PHASE_3_DATA_UPLOAD.md)

### Analytics
5. **Run Queries**: See [sql_queries/](sql_queries/) directory
6. **Build Dashboards**: Follow [PHASE_6_VISUALIZATION.md](documentation/PHASE_6_VISUALIZATION.md)

---

## 📁 Project Structure

```
healthcare-data-lake-project/
├── README.md                          # This file
├── PROJECT_OVERVIEW.md                # Detailed project documentation
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
│
├── data_generation/                   # Phase 1: Data Generation
│   ├── generate_pharmacy_data.py      # Pharmacy system data generator
│   ├── generate_ehr_data.py           # EHR system data generator
│   ├── requirements.txt               # Python dependencies
│   ├── README.md                      # Data generation documentation
│   └── *.csv                          # Generated data files (not committed)
│
├── documentation/                     # Comprehensive guides
│   ├── PHASE_2A_GCP_SETUP.md          # Google Cloud Platform setup
│   ├── PHASE_2B_AWS_SETUP.md          # Amazon Web Services setup
│   ├── PHASE_3_DATA_UPLOAD.md         # Data loading procedures
│   ├── PHASE_4_ETL_PIPELINES.md       # ETL development guide
│   ├── PHASE_5_ANALYTICS.md           # SQL analytics guide
│   ├── PHASE_6_VISUALIZATION.md       # Tableau dashboard guide
│   ├── DATA_DICTIONARY.md             # Complete field descriptions
│   └── PORTFOLIO_CASE_STUDY.md        # Portfolio presentation guide
│
├── cloud_configs/                     # Cloud infrastructure code
│   ├── gcp/
│   │   ├── bigquery_tables.sql        # BigQuery DDL
│   │   └── gcp_setup.sh               # GCP setup script
│   └── aws/
│       ├── athena_tables.sql          # Athena DDL
│       ├── cloudformation_template.yaml
│       └── aws_setup.sh               # AWS setup script
│
├── etl_pipelines/                     # Phase 4: ETL Code
│   ├── pharmacy_etl.py                # Pharmacy data ETL
│   ├── ehr_etl.py                     # EHR data ETL
│   ├── cross_cloud_sync.py            # Cross-cloud data integration
│   ├── data_quality.py                # Validation framework
│   └── requirements.txt               # ETL dependencies
│
├── sql_queries/                       # Phase 5: Analytics Queries
│   ├── bigquery/                      # GCP BigQuery queries
│   │   ├── medication_adherence.sql
│   │   ├── rems_compliance.sql
│   │   └── insurance_analytics.sql
│   ├── athena/                        # AWS Athena queries
│   │   ├── clinical_outcomes.sql
│   │   ├── lab_trends.sql
│   │   └── population_health.sql
│   └── cross_cloud/                   # Federated queries
│       └── medication_reconciliation.sql
│
├── visualizations/                    # Phase 6: Tableau Dashboards
│   ├── tableau_workbooks/
│   │   ├── Executive_Dashboard.twbx
│   │   ├── Clinical_Quality.twbx
│   │   ├── Pharmacy_Operations.twbx
│   │   └── Population_Analytics.twbx
│   └── screenshots/                   # Dashboard screenshots
│
└── tests/                             # Data validation tests
    ├── test_data_quality.py
    └── test_etl_pipelines.py
```

---

## 🎓 Skills Demonstrated

### Data Engineering
- Multi-cloud architecture design
- ETL pipeline development
- Data lake vs. data warehouse implementation
- Schema design and optimization
- Data partitioning strategies
- Query optimization
- Data quality validation

### Cloud Technologies
- **GCP**: BigQuery, Cloud Storage, IAM, gcloud CLI
- **AWS**: S3, Athena, Glue, IAM, AWS CLI
- Infrastructure as code (optional: Terraform/CloudFormation)
- Cost optimization and monitoring
- Security best practices

### Healthcare Domain
- Pharmacy operations and workflows
- EHR systems and clinical documentation
- REMS (Risk Evaluation and Mitigation Strategies)
- Insurance adjudication (NCPDP standards)
- ICD-10 coding
- ACIP immunization guidelines
- HIPAA compliance considerations

### Data Analysis
- SQL (BigQuery SQL, Presto/Athena SQL)
- Cross-system data reconciliation
- Medication adherence calculations
- Clinical outcomes analysis
- Population health metrics

### Data Visualization
- Tableau dashboard design
- Interactive filtering and drill-downs
- Healthcare KPI tracking
- Executive-level reporting

### Software Engineering
- Python programming
- Version control (Git/GitHub)
- Documentation best practices
- Code organization
- Error handling and logging

---

## 📈 Project Phases

| Phase | Duration | Description | Status |
|-------|----------|-------------|--------|
| **Phase 1** | 1-2 days | Synthetic data generation | ✅ Complete |
| **Phase 2** | 2-3 days | Cloud infrastructure setup (GCP + AWS) | 🔄 In Progress |
| **Phase 3** | 2 days | Data upload and schema validation | ⏳ Pending |
| **Phase 4** | 3 days | ETL pipeline development | ⏳ Pending |
| **Phase 5** | 3 days | SQL analytics and insights | ⏳ Pending |
| **Phase 6** | 3 days | Tableau dashboard creation | ⏳ Pending |
| **Phase 7** | 2 days | Documentation and GitHub publication | ⏳ Pending |

**Total Estimated Time**: 16-18 days (part-time)

---

## 💡 Sample Analytics Questions

This project can answer questions like:

1. **Medication Adherence**: What percentage of diabetic patients are filling their metformin prescriptions on schedule?
2. **REMS Compliance**: Are patients on isotretinoin (Accutane) getting required monthly pregnancy tests?
3. **Clinical Outcomes**: How do HbA1c levels trend for patients on different diabetes medications?
4. **Insurance Analytics**: What's the average copay difference between brand and generic medications?
5. **Population Health**: What percentage of patients over 65 are up to date on pneumococcal vaccine?
6. **Cost Analysis**: Which insurance carriers have the highest rejection rates?
7. **Medication Reconciliation**: Are there discrepancies between prescribed and dispensed medications?
8. **Quality Metrics**: What's the adherence rate for patients with multiple chronic conditions?

---

## 📊 Sample Queries

### Medication Adherence (BigQuery)
```sql
WITH prescription_fills AS (
  SELECT 
    patient_id,
    medication_name,
    COUNT(*) as fill_count,
    MIN(fill_date) as first_fill,
    MAX(fill_date) as last_fill,
    DATE_DIFF(MAX(fill_date), MIN(fill_date), DAY) as days_between
  FROM `pharmacy_data.prescriptions`
  WHERE condition = 'Type 2 Diabetes'
    AND fill_date BETWEEN '2024-01-01' AND '2025-12-31'
  GROUP BY patient_id, medication_name
)
SELECT 
  medication_name,
  AVG(fill_count) as avg_fills_per_patient,
  AVG(SAFE_DIVIDE(days_between, 365)) * 100 as avg_pdc_percent
FROM prescription_fills
GROUP BY medication_name
ORDER BY avg_pdc_percent DESC;
```

### Lab Trends by Medication (Athena)
```sql
SELECT 
  l.test_component,
  p.medication_name,
  AVG(CASE WHEN l.flag = 'Normal' THEN 1 ELSE 0 END) * 100 as pct_normal,
  COUNT(*) as test_count
FROM ehr_data.lab_results l
JOIN pharmacy_data.prescriptions p 
  ON l.patient_id = p.patient_id
WHERE l.test_name = 'Hemoglobin A1C'
  AND p.condition = 'Type 2 Diabetes'
GROUP BY l.test_component, p.medication_name
HAVING test_count >= 10
ORDER BY pct_normal DESC;
```

---

## 🎨 Tableau Dashboards

### Executive Dashboard
- Total patients and prescriptions
- Revenue by payer mix
- Top medications dispensed
- Monthly prescription volume trends

### Clinical Quality Dashboard
- Medication adherence rates by drug class
- Lab result trends over time
- Immunization coverage by age group
- Chronic disease management metrics

### Pharmacy Operations Dashboard
- Daily/weekly prescription volume
- Insurance rejection rates and top reasons
- Average fill time
- REMS medication tracking

### Population Analytics Dashboard
- Disease prevalence by demographics
- Geographic distribution of patients
- Comorbidity patterns
- Risk stratification

---

## 💰 Cost Estimation

### Free Tier (Recommended for Learning)
- **GCP**: $0/month (within 10GB BigQuery storage, 1TB queries)
- **AWS**: $0/month (within 5GB S3, limited Athena queries)
- **Tableau Public**: $0 (free, public dashboards)
- **Total**: **$0/month** ✅

### Paid Tier (If Scaling Up)
- **GCP**: ~$5-10/month (50GB storage, 5TB queries)
- **AWS**: ~$5-10/month (50GB storage, 100GB scanned)
- **Tableau Desktop**: $70/month or $840/year
- **Total**: **~$10-20/month** (without Tableau Desktop)

### Cost Optimization Tips
- Use table partitioning
- Limit SELECT * queries
- Delete Athena query results periodically
- Use query result caching
- Stay within free tier limits

---

## 🔒 Security & Compliance

- ✅ **Synthetic Data**: All patient data is artificially generated (no real PHI)
- ✅ **Encryption**: Data encrypted at rest and in transit
- ✅ **Access Control**: IAM roles with least privilege
- ✅ **Audit Logging**: CloudTrail (AWS) and Cloud Audit Logs (GCP)
- ✅ **Best Practices**: Service accounts, MFA, no hardcoded credentials

**Note**: This project uses synthetic data for educational purposes. In a real healthcare setting, follow HIPAA regulations and organizational policies.

---

## 📚 Documentation

Comprehensive documentation is provided for each phase:
** IN PROGRESS **
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - High-level project details
- [Data Generation README](data_generation/README.md) - Synthetic data creation
- [GCP Setup Guide](documentation/PHASE_2A_GCP_SETUP.md) - BigQuery configuration
- [AWS Setup Guide](documentation/PHASE_2B_AWS_SETUP.md) - S3/Athena configuration
- [Data Dictionary](documentation/DATA_DICTIONARY.md) - Complete field descriptions
- [Portfolio Case Study](documentation/PORTFOLIO_CASE_STUDY.md) - Presentation tips

---

## 🤝 Contributing

This is a personal portfolio project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**John-Poulos**
- GitHub: [@John-Poulos](https://github.com/John-Poulos)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)
- Portfolio: [Your Portfolio URL](https://your-portfolio.com)

---

## 🙏 Acknowledgments

- **Faker**: Python library for generating realistic fake data
- **FDA**: REMS program documentation and guidelines
- **CDC**: ACIP immunization schedule information
- **NCPDP**: Pharmacy transaction standards
- **Cloud Providers**: GCP and AWS free tier programs

---

## 📞 Questions or Feedback?

Feel free to open an issue or reach out:
- **Issues**: [GitHub Issues](https://github.com/John-Poulos/healthcare-data-lake-project/issues)
- **Discussions**: [GitHub Discussions](https://github.com/John-Poulos/healthcare-data-lake-project/discussions)
- **Email**: your.email@example.com

---

## 🎯 Next Steps for You

1. ⭐ Star this repository
2. 📥 Clone and set up locally
3. ☁️ Complete cloud infrastructure setup (Phases 2A & 2B)
4. 📊 Upload data and run sample queries
5. 📈 Build Tableau dashboards
6. 📝 Document your learnings
7. 💼 Add to your portfolio!

---

**Happy Learning! 🚀**

---

## 📊 Project Stats

![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-5000+-brightgreen)
![SQL Queries](https://img.shields.io/badge/SQL%20Queries-20+-blue)
![Cloud Platforms](https://img.shields.io/badge/Cloud%20Platforms-2-orange)
![Healthcare Standards](https://img.shields.io/badge/Healthcare%20Standards-5+-red)

---

*This README was last updated: January 27, 2026*
