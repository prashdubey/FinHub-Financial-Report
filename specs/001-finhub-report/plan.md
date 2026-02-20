# Implementation Plan: FinHub Financial Summary Report

**Branch**: `001-finhub-report` | **Date**: 2026-02-20 | **Spec**: [specs/001-finhub-report/specification.md](../specification.md)

---

## Summary

Build a financial reporting solution that extracts data from SSAS cube `FinHub_Cube` and delivers Power BI and Excel reports with automated daily refresh (6 AM) and Dev → UAT → Prod promotion workflow. Reports will display TotalRevenue, TotalCost, and ProfitMargin metrics for the Finance department across the last 12 months, with visualizations in corporate brand colors (Dark Blue #1F4E79, Gray #555555). Includes automated data validation at each promotion gate and comprehensive audit logging for governance compliance.

---

## Technical Context

**Language/Version**: 
- Power BI Desktop 2.x with Power Query and DAX
- Excel 365 with Power Query
- PowerShell 5.1+ for automation and refresh scheduling
- SQL-based validation queries against SSAS cube

**Primary Dependencies**: 
- SSAS cube: `FinHub_Cube` (connection: Dev/UAT/Prod servers)
- Power BI Service (Premium or Premium per User for refresh scheduling)
- SQL Server Analysis Services (SSAS) client libraries
- PowerShell: `SqlServer` module, `MSOLAP` provider
- Data refresh: Analysis Services PowerShell cmdlets

**Storage**: 
- Data source: SSAS multidimensional cube (not dimensional model)
- Power BI dataset: Hosted in Power BI Service or on-premises Power BI Report Server
- Excel workbook: Stored in SharePoint with refresh via Power Query connections
- Refresh logs: File-based (.csv or .log) or centralized logging system

**Testing**: 
- Unit tests: DAX formula tests (using external DAX testing framework or manual validation)
- Integration tests: SSAS cube connectivity, measure validation against source queries
- Validation tests: Accuracy reconciliation (Power BI values vs. SSAS direct query)
- Promotion tests: Dev → UAT → Prod flow with data verification

**Target Platform**: 
- Power BI Service (cloud) or on-premises Report Server (if cloud unavailable)
- Excel 365 running on Windows clients with Power Query refresh capability
- PowerShell scheduled tasks on Windows Server for automated refresh

**Project Type**: Multi-artifact (Power BI report + Excel workbook + automation scripts + validation framework)

**Performance Goals**: 
- Power BI report loads: < 3 seconds
- Daily refresh: ≤ 15 minutes
- Data validation: ≤ 5 minutes per environment
- Query response time on SSAS: ≤ 5 seconds for each measure

**Constraints**: 
- SSAS cube must remain read-only for financial data integrity
- Dev/UAT/Prod environments must use separate connection strings (no data mixing)
- Finance department filter must be default but user-removable
- Corporate color palette is mandatory (no deviations without approval)
- All formulas and scripts must reference this specification for traceability

**Scale/Scope**: 
- ~5 key financial metrics (3 measures + 2 composite KPIs)
- 3 main visualizations (line, bar, table) in Power BI
- 100k-500k rows of monthly data per department across 3 regions
- 12-month rolling window (approximately 1,800 rows of detail data per day)
- Estimated 30-50 Finance department users accessing reports

---

## Constitution Check ✓

*GATE: Validates alignment with `.specify/memory/constitution.md` principles before proceeding to Phase 0 research.*

- [x] **Spec-Driven Development**: Complete formal specification (5 user stories, 32 requirements) documented before implementation
- [x] **Environment Alignment**: Dev → UAT → Prod workflow explicit with validation gates (FR-021 through FR-024)
- [x] **Data Accuracy & Validation**: Automated validation framework required (FR-025 through FR-028); metrics must reconcile with SSAS cube before promotion
- [x] **Governance & Security**: Access control (FR-029), audit logging (FR-030), approval gates (FR-031, FR-032) embedded in design
- [x] **AI-Assisted Implementation**: DAX formulas and PowerShell scripts may use Copilot/Claude with manual verification before integration
- [x] **Reporting Standards**: Corporate color palette in use (#1F4E79, #555555); formatting standards defined (FR-009 through FR-011)
- [x] **Documentation & Versioning**: This plan + specification versioned in GitHub; amendments will follow MAJOR.MINOR.PATCH rules

**Gate Status**: ✅ PASSED - All constitution principles satisfied. Proceed to Phase 0 research.

---

## Project Structure

### Documentation (Feature Artifacts)

```
specs/001-finhub-report/
├── specification.md          # ✅ Complete (5 user stories, 32 requirements)
├── plan.md                   # This file (Phase 0 research plan)
├── research.md               # Phase 0 output (SSAS structure, existing reports, tooling evaluation)
├── data-model.md             # Phase 1 output (DAX measures, calculated columns, relationships)
├── architecture.md           # Phase 1 output (Power BI model design, Excel layout, refresh architecture)
├── validation-strategy.md    # Phase 1 output (Data reconciliation approach, automated checks)
├── tasks.md                  # Phase 2 output (/speckit.tasks command output)
└── checklist.md              # Final output (/speckit.checklist command output)
```

### Source Code & Configuration

```
# Project structure: Multi-artifact financial reporting

reports/
├── FinHub_Summary.pbix          # Power BI report file (SSAS connection, visualizations)
├── FinHub_Summary.xlsx          # Excel workbook (Power Query connections, three sheets)
└── configurations/
    ├── connections-dev.json     # Dev SSAS connection string and credentials
    ├── connections-uat.json     # UAT SSAS connection string and credentials
    └── connections-prod.json    # Prod SSAS connection string and credentials

scripts/
├── refresh-schedule.ps1         # PowerShell script to schedule 6 AM daily refresh
├── refresh-execute.ps1          # PowerShell script that executes refresh job
├── validation-runner.ps1        # Automated data accuracy validation script
├── promotion-validator.ps1      # Script to validate before Dev → UAT → Prod promotions
└── audit-logger.ps1             # Script to log all changes and promotions

documentation/
├── deployment-guide.md          # Step-by-step deployment instructions
├── refresh-troubleshooting.md   # Common refresh issues and resolutions
├── validation-baseline.csv      # Expected values for validation (SSAS cube snapshots)
└── approval-matrix.md           # Who approves promotions from each environment

tests/
├── ssas-connectivity-test.ps1   # Verify SSAS cube connections (Dev/UAT/Prod)
├── measure-validation.sql       # Direct SSAS queries to verify measure values
├── promotion-test-checklist.md  # Manual/automated promotion test steps
└── access-control-test.md       # Verify Finance-only access in UAT/Prod
```

**Structure Decision**: Multi-artifact project with centralized configuration, automated refresh/validation scripts, and environment-specific connection management. Power BI handles interactive reporting; Excel serves offline/email distribution; PowerShell automates refresh and validation; SQL validates accuracy.

---

## Phase 0: Research & Discovery

### Research Objectives

1. **SSAS Cube Analysis**
   - [ ] Export SSAS cube schema: measure names, dimensions, hierarchies, caclulated members
   - [ ] Verify measures exist: `TotalRevenue`, `TotalCost`, `ProfitMargin`
   - [ ] Verify dimensions exist: `Month` (date dimension), `Region`, `Department`
   - [ ] Check for existing filters/security roles on Finance department
   - [ ] Query performance baseline: How long does 12-month Finance query take?

2. **Existing Report Review**
   - [ ] Search for existing Power BI reports on `FinHub_Cube` and document patterns
   - [ ] Review existing Excel-based financial reports (naming, formatting, refresh method)
   - [ ] Identify any existing 6 AM refresh jobs to understand current scheduling approach
   - [ ] Document what data validation or reconciliation processes exist today

3. **Technical Tooling & Environment**
   - [ ] Verify Power BI Service is configured and developers have license to Dev/UAT/Prod tenants
   - [ ] Confirm PowerShell v5.1+ is installed on refresh server with SqlServer module
   - [ ] Verify connectivity test to SSAS from Power BI and PowerShell environments
   - [ ] Document SSAS connection strings for each environment (Dev, UAT, Prod)
   - [ ] Confirm Excel 365 with Power Query is available on intended distribution devices

4. **Governance & Approval Setup**
   - [ ] Identify Data Governance team lead for UAT → Prod approvals
   - [ ] Confirm GitHub review/approval workflow is configured in repository
   - [ ] Verify SharePoint or file storage location where Excel reports will be stored
   - [ ] Document current audit logging infrastructure (compliance requirements)

5. **Color Palette & Standards Validation**
   - [ ] Confirm corporate colors: Dark Blue #1F4E79, Gray #555555 are correct
   - [ ] Review any existing FD&E (Finance, Data & Engineering) reporting standards document
   - [ ] Verify Power BI theme/color scheme exists or needs to be created
   - [ ] Confirm Excel header/formatting standards align with specification

### Research Deliverables

- **research.md** document containing findings from all 5 research areas above
- **SSAS cube export** (.cub or schema definition)
- **Environment connectivity validation** confirming all 3 environments reachable
- **Decision log** on any technical alternatives discovered (e.g., DirectQuery vs. Import mode)

---

## Phase 1: Design & Architecture

### Design Activities

1. **Power BI Model Design**
   - Design DAX measures for `TotalRevenue`, `TotalCost`, `ProfitMargin` (if not exists in cube)
   - Design calculated columns for aggregations or derived metrics
   - Specify relationship between Month/Region/Department dimensions
   - Plan data refresh strategy: Incremental vs. Full refresh
   - Design role-based security: Finance department access only

2. **Visualization Design**
   - Create line chart design spec: "Monthly Total Revenue" (X: Month, Y: TotalRevenue, Color: Dark Blue #1F4E79)
   - Create bar chart design spec: "Profit Margin by Region" (X: Region, Y: ProfitMargin, Color: Gray #555555)
   - Create table design spec: Headers dark blue, rows alternating gray, columns sorted by importance
   - Specify filters: "Last 12 Months" (date picker), "Department" (dropdown, default Finance)

3. **Excel Report Architecture**
   - Design three sheets: Summary (all data), by-Region (pivoted), by-Department (pivoted)
   - Specify Power Query connections to SSAS (parameterized for environment)
   - Design formatting: Headers, colors, number formats per corporate standards
   - Plan refresh mechanism: Manual button or background refresh on open

4. **Refresh & Automation Architecture**
   - Design daily 6 AM refresh job using PowerShell scheduled tasks
   - Design Power BI refresh flow (Power Query or Analysis Services connector)
   - Design Excel Power Query refresh trigger
   - Specify logging: Log file location, format, retention

5. **Promotion & Validation Architecture**
   - Design validation queries: Direct SSAS queries to verify measure values
   - Design comparison logic: Power BI values vs. SSAS values (tolerance threshold 0.01%)
   - Design approval workflow: GitHub pull request with review requirements
   - Design rollback procedure if Prod promotion fails validation

### Design Deliverables

- **data-model.md** with DAX formulas, calculated columns, security design
- **architecture.md** with visualization designs, refresh architecture, promotion workflow diagram
- **validation-strategy.md** with reconciliation logic and accuracy checks
- **design-decisions.md** documenting all technical choices and rationale

---

## Phase 2: Task Breakdown & Sequencing

### Implementation Phases (to be detailed in tasks.md)

**Phase 1: Setup & Foundation**
- Create repository structure (specs/, reports/, scripts/, documentation/)
- Initialize Power BI project file and Excel workbook templates
- Setup PowerShell scripts skeleton (refresh, validation, promotion)
- Configure Git branching strategy (dev/uat/prod branches)

**Phase 1.5: Governance & Environment Setup**
- Configure SSAS connections for Dev/UAT/Prod with parameterization
- Setup Power BI dataset refresh configuration
- Configure PowerShell execution policies and scheduler
- Setup audit logging framework

**Phase 2: Power BI Report Development** (US1 - Line chart, bar chart, table)
- Create DAX measures (TotalRevenue, TotalCost, ProfitMargin)
- Build line chart with Monthly TotalRevenue
- Build bar chart with Profit Margin by Region
- Build table with full details by Department
- Apply filters (Last 12 months, Department = Finance)
- Apply corporate color formatting

**Phase 3: Excel Report Development** (US2 - Three sheets, Power Query connections)
- Create Summary sheet with all measures
- Create by-Region pivoted sheet
- Create by-Department pivoted sheet
- Configure Power Query connections (parameterized)
- Apply Excel formatting (Dark Blue headers, gray alternating rows)

**Phase 4: Automated Refresh** (US3 - 6 AM daily, logging, error notifications)
- Create PowerShell refresh script that updates Power BI and Excel
- Configure Windows Task Scheduler for 6 AM daily execution
- Implement error handling and notification (email/Teams if fails)
- Create and test refresh logs

**Phase 5: Promotion Pipeline** (US4 - Dev → UAT → Prod with validation)
- Create promotion validation script (data accuracy checks)
- Configure GitHub approval workflow requirements
- Create change documentation template
- Conduct Dev → UAT promotion test

**Phase 6: Validation Framework** (US5 - Data accuracy reconciliation)
- Create validation queries that directly query SSAS for truth values
- Create reconciliation logic that compares Power BI to SSAS with 0.01% tolerance
- Automate validation at promotion gates
- Automate daily post-refresh validation in Prod

**Phase 7: Security & Governance** (Access control, audit logging)
- Configure Power BI row-level security (Finance department only)
- Configure user review/approval workflow
- Create audit trail logging for all promotions and data exports
- Document access control matrix

**Phase 8: Testing & Documentation**
- Conduct SSAS connectivity tests (all environments)
- Conduct data accuracy validation tests
- Conduct promotion workflow end-to-end test
- Create deployment runbooks and troubleshooting guides

**Phase 9: UAT & Prod Promotion**
- Execute UAT testing with Finance team stakeholders
- Obtain Data Governance approval for Prod promotion
- Deploy to Prod with change log documentation
- Monitor first 7 days for issues

---

## Complexity Tracking

> **No constitutional violations identified** - project aligns fully with all 7 principles

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| SSAS cube unavailable during refresh | High | Implement retry logic; alert on first failure; test failover if backup cube exists |
| Data discrepancies between environments | High | Automated validation at each promotion gate + daily reconciliation in Prod |
| Refresh timeout >15 minutes | Medium | Monitor initial runs; optimize DAX queries if needed; implement incremental refresh |
| Approval delays blocking promotions | Medium | Pre-document approval authority; automate routine approvals via checklist validation |
| Excel Power Query breaks with environment change | Medium | Parameterize all connection strings; test with each environment change |
| Access control bypass (non-Finance views Prod) | High | Implement row-level security in Power BI; conduct access control tests before Prod |

---

## Success Metrics (from Spec)

- Power BI report loads < 3 seconds ✓
- Daily refresh completes in ≤ 15 minutes ✓
- 99%+ refresh success rate ✓
- 0% data discrepancies (dev) / < 0.01% (UAT/Prod) ✓
- All promotions logged with audit trail ✓
- Finance team time to access data reduced 50% ✓
- 90%+ stakeholder satisfaction on visualization clarity ✓

---

## Next Steps

1. **Phase 0 Execution** (1-2 weeks): Research + discoveries documented in research.md
2. **Review & Approval**: Stakeholders review architecture decisions; sign-off from Data Governance
3. **Phase 1 Detail**: Design deliverables (data-model.md, architecture.md, validation-strategy.md)
4. **Task Creation** (`/speckit.tasks`): Break Phase 0-9 into granular, testable tasks
5. **GitHub Issues** (`/speckit.taskstoissues`): Convert tasks to GitHub issues with acceptance criteria
6. **Development** (`/speckit.implement`): Execute tasks in priority order with verification at each step

---

**Plan Status**: READY FOR PHASE 0 RESEARCH

**Version**: 1.0.0 | **Created**: 2026-02-20 | **Last Updated**: 2026-02-20
