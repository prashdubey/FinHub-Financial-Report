# Tasks: FinHub Financial Summary Report

**Input**: Spec documents from `/specs/001-finhub-report/`  
**Prerequisites**: specification.md ✅, plan.md ✅

**Organization**: Tasks are grouped by user story and implementation phase to enable independent testing and parallel execution where possible.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different systems, no dependencies)
- **[Story]**: Which user story or phase this task belongs to (US1-5, Phase)
- Paths reference Power BI reports/, scripts/, specs/

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Repository and project initialization

- [ ] T001 Create repository folder structure: specs/001-finhub-report/, reports/, scripts/, tests/, documentation/
- [ ] T002 [P] Initialize Power BI Desktop project file `reports/FinHub_Summary.pbix` (blank dataset)
- [ ] T003 [P] Create Excel template `reports/FinHub_Summary.xlsx` with three blank sheets (Summary, by-Region, by-Department)
- [ ] T004 [P] Initialize PowerShell script files in scripts/: refresh-schedule.ps1, refresh-execute.ps1, validation-runner.ps1, promotion-validator.ps1, audit-logger.ps1
- [ ] T005 Configure Git branching: main (prod-ready), uat (staging), dev (development)
- [ ] T006 [P] Create documentation templates: deployment-guide.md, troubleshooting.md, approval-matrix.md

---

## Phase 1.5: Governance & Environment Setup

**Purpose**: Security, configuration management, and audit infrastructure per Constitution

- [ ] T007 [P] Create environment configuration files: configurations/connections-dev.json, connections-uat.json, connections-prod.json (parameterized SSAS connection strings)
- [ ] T008 [P] Document SSAS connection strings for Dev, UAT, Prod with Windows authentication details in configs
- [ ] T009 Setup PowerShell execution policy on refresh server: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned`
- [ ] T010 [P] Create audit logging framework: scripts/audit-logger.ps1 with standardized log format (timestamp, user, action, environment, status)
- [ ] T011 [P] Setup error notification mechanism (email/Teams webhook) for failed refresh jobs in scripts/refresh-execute.ps1
- [ ] T012 Configure GitHub branch protection rules: main requires 1 Data Governance review; uat requires 1 technical review
- [ ] T013 Create validation baseline CSV: tests/validation-baseline.csv with expected measure values from SSAS (TotalRevenue, TotalCost, ProfitMargin by region/department)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core SSAS connectivity and model setup before any report development

⚠️ **CRITICAL**: Tasks T014-T019 must be complete before Phase 3+ work can begin

- [ ] T014 Validate SSAS cube connectivity from Power BI Desktop to all three environments (Dev, UAT, Prod)
  - **Acceptance**: Can connect and query `FinHub_Cube` in all three environments without authentication errors
- [ ] T015 [P] Export SSAS cube schema: Document measure names, dimension names, hierarchies in tests/ssas-schema.txt
  - **Acceptance**: Schema shows TotalRevenue, TotalCost, ProfitMargin measures; Month, Region, Department dimensions
- [ ] T016 Test SSAS measure data: Query `TotalRevenue`, `TotalCost`, `ProfitMargin` directly in SSAS; document sample values for baseline
  - **Acceptance**: All three measures return data; values are numeric (currency/percentage as appropriate)
- [ ] T017 [P] Verify Last 12 Months date range logic: Define which 12 calendar months to include; confirm date dimension exists
  - **Acceptance**: Can write DAX or MDX formula that filters to last 12 months dynamically
- [ ] T018 Verify Finance Department filter: Test that Department = Finance filter reduces data appropriately
  - **Acceptance**: Query with Department filter returns only Finance department rows; row count is significantly smaller than unfiltered
- [ ] T019 [P] Setup Power BI Import vs DirectQuery decision: Test query performance on SSAS cube with 12-month Finance department filter
  - **Acceptance**: Query completes in < 5 seconds; document decision in architecture.md

**Checkpoint**: All SSAS connectivity and foundational data validated. User story development can now begin in parallel.

---

## Phase 3: User Story 1 - Power BI Dashboard (Priority: P1) 🎯 MVP

**Goal**: Build Line chart (Monthly Revenue), Bar chart (Profit by Region), Table (Summary) with filters

**Independent Test**: Power BI opens, all measures appear, filters work, visualizations render correctly

### Tests for User Story 1 (Automated & Manual)

- [ ] T020 [P] [US1] Contract test: Create DAX query in tests/measure-validation.sql to verify TotalRevenue measure returns data for last 12 months, Finance department
- [ ] T021 [P] [US1] Create test data snapshot: tests/us1-expected-values.csv with sample revenue values by month for verification
- [ ] T022 [US1] Integration test: Open FinHub_Summary.pbix in Power BI Desktop, load SSAS data, verify no errors in Power Query
  - **Independent Test Result**: Report loads without errors; data/queries appear in Power Query Editor

### DAX Measures (if not in SSAS cube)

- [ ] T023 [US1] Create DAX measure `TotalRevenue` if missing: `SUM(FinanceTable[Revenue])`
- [ ] T024 [US1] Create DAX measure `TotalCost` if missing: `SUM(FinanceTable[Cost])`
- [ ] T025 [US1] Create DAX measure `ProfitMargin` if missing: `[TotalRevenue] - [TotalCost]` or as percentage `([TotalRevenue] - [TotalCost]) / [TotalRevenue]`

### Visualizations for User Story 1

#### Line Chart - Monthly Revenue

- [ ] T026 [US1] Create line chart visualization titled "Monthly Total Revenue" in FinHub_Summary.pbix
  - X-axis: Month (Date)
  - Y-axis: TotalRevenue
  - Color: Dark Blue (#1F4E79)
  - **Acceptance**: Chart displays monthly trend correctly; hovering shows exact values

#### Bar Chart - Profit Margin by Region

- [ ] T027 [US1] Create bar chart visualization titled "Profit Margin by Region" in FinHub_Summary.pbix
  - X-axis: Region
  - Y-axis: ProfitMargin
  - Color: Gray (#555555)
  - **Acceptance**: Chart shows one bar per region; values are correct; colors match corporate standard

#### Table - Summary by Department

- [ ] T028 [US1] Create table visualization with columns: Month, Department, TotalRevenue, TotalCost, ProfitMargin
  - Formatting: 
    - Header row: Dark Blue (#1F4E79) background, white text, bold
    - Data rows: Alternating light gray (#F2F2F2) shading for readability
    - Number format: Revenue/Cost as currency ($), ProfitMargin as percentage (%)
  - **Acceptance**: Table displays with correct formatting; all columns visible and properly sized

### Filters for User Story 1

- [ ] T029 [P] [US1] Create filter: "Last 12 Months" date range slicer
  - Behavior: Filters all visualizations to selected date range
  - Default: Auto-calculated to last 12 calendar months from today
  - **Acceptance**: Changing date filter updates line chart, bar chart, and table in real-time (< 1 second)

- [ ] T030 [P] [US1] Create filter: "Department" multi-select slicer, default to "Finance"
  - Behavior: Filters all visualizations to selected departments
  - Default: Finance department pre-selected
  - **Acceptance**: Toggling department filter updates visualizations; Finance default is applied on report open

### Data Validation for User Story 1

- [ ] T031 [US1] Run validation: Compare Power BI table values against direct SSAS queries using tests/measure-validation.sql
  - Acceptance criteria: All values match to 2 decimal places (0% discrepancy for dev)

**Checkpoint**: User Story 1 complete. Power BI dashboard is fully functional with all three visualizations and filters working correctly.

---

## Phase 4: User Story 2 - Excel Financial Report (Priority: P2)

**Goal**: Create three Excel sheets (Summary, by-Region, by-Department) with Power Query connections and corporate formatting

**Independent Test**: Excel opens, data loads from SSAS, sheet tabs display correct data, formatting matches standards

### Excel Sheets - Structure

- [ ] T032 [P] [US2] Create "Summary" sheet in FinHub_Summary.xlsx
  - Columns: Month, Department, TotalRevenue, TotalCost, ProfitMargin
  - Data: All Finance department data for last 12 months
  - Formatting: Headers in Dark Blue (#1F4E79) with white text; data rows alternating light gray

- [ ] T033 [P] [US2] Create "by-Region" sheet in FinHub_Summary.xlsx
  - Pivoted data: Regions as rows, Months as columns, values as TotalRevenue and ProfitMargin
  - Formatting: Same corporate standards (headers, alternating rows)

- [ ] T034 [P] [US2] Create "by-Department" sheet in FinHub_Summary.xlsx
  - Pivoted data: Departments as rows, Months as columns, values as TotalRevenue and ProfitMargin
  - Filtering: Finance department only (per specification)
  - Formatting: Same corporate standards

### Power Query Connections

- [ ] T035 [US2] Create Power Query connection in Excel to SSAS cube `FinHub_Cube` (use configurations/connections-dev.json for connection string)
  - **Acceptance**: Excel can connect to SSAS without errors; credentials work for Windows authentication

- [ ] T036 [P] [US2] Parameterize connection string: Create Excel parameter for environment (Dev/UAT/Prod)
  - **Acceptance**: Switching environment parameter in Excel updates all sheet data queries

- [ ] T037 [US2] Write Power Query logic to:
  - Filter to Last 12 Months dynamically
  - Filter to Finance Department only (default)
  - Group/aggregate data for by-Region and by-Department pivots

### Excel Refresh & Data Updates

- [ ] T038 [US2] Create "Refresh Data" button in Excel using Data > Queries > Refresh feature
  - **Acceptance**: Clicking button refreshes all three sheets from SSAS; takes < 2 minutes to complete

- [ ] T039 [US2] Configure Excel to refresh on open (optional, subject to user preference in deployment guide)

### Data Validation for User Story 2

- [ ] T040 [US2] Validate Excel data matches source SSAS and Power BI values
  - Spot-check 5-10 key values (TotalRevenue by Region, ProfitMargin by Month)
  - **Acceptance**: Excel values match Power BI values match SSAS query results within 0% (dev)

**Checkpoint**: User Story 2 complete. Excel workbook is fully populated with three sheets and can refresh from SSAS.

---

## Phase 5: User Story 3 - Automated Daily Refresh (Priority: P1)

**Goal**: Schedule 6 AM daily refresh of both Power BI and Excel datasets with logging and error notifications

**Independent Test**: Refresh job runs at 6 AM, completes in < 15 minutes, logs success/failure, emails on error

### Refresh Scheduling

- [ ] T041 [US3] Implement PowerShell refresh script in scripts/refresh-execute.ps1 with:
  - Power BI dataset refresh call using `Invoke-PowerBIRestApiCall` or REST API
  - Excel Power Query refresh (remotely via Excel Automation or via Excel add-in)
  - Logging to file: scripts/logs/refresh-[date].log
  - Error handling: Retry on failure; alert if retry limit exceeded

- [ ] T042 [US3] Configure Windows Task Scheduler to run scripts/refresh-schedule.ps1 at 6 AM daily
  - Schedule status: Active (confirmed by `schtasks /query`)
  - Service account: Sufficient permissions to access SSAS cube and Power BI (validate with IT)
  - **Acceptance**: Scheduled task runs at 6 AM; task completion logged in Windows Task Scheduler

### Refresh Logging

- [ ] T043 [P] [US3] Create logging framework in scripts/audit-logger.ps1 with format:
  - [TIMESTAMP] | [STATUS] | [ENVIRONMENT] | [MEASURE_COUNT] | [DURATION_SECONDS] | [ERROR_MSG]
  - Example: `2026-02-20 06:05:12 | SUCCESS | DEV | 3 measures refreshed | 180 | N/A`

- [ ] T044 [P] [US3] Store logs in scripts/logs/ directory with one file per day: refresh-2026-02-20.log

- [ ] T045 [US3] Create log retention policy: Archive logs older than 90 days to archive/ folder

### Error Notification

- [ ] T046 [US3] Configure email notification: On refresh failure, send alert to Data Admin team with:
  - Failure time and duration
  - Error message and stack trace
  - Suggestion for troubleshooting (e.g., "SSAS cube connection timeout - verify network connectivity")

- [ ] T047 [P] [US3] Configure Teams webhook notification as alternative to email (subject to organizational preference)

### Refresh Performance Validation

- [ ] T048 [US3] Test refresh timing: Run refresh manually; verify completion in < 15 minutes (acceptance criteria)
  - If > 15 minutes: Investigate query optimization (FR-018 requirement)

- [ ] T049 [US3] Test refresh on weekends and holidays: Verify 6 AM refresh operates consistently
  - Acceptance: No environment-specific issues (e.g., holiday shutdowns affecting SSAS)

**Checkpoint**: User Story 3 complete. Daily 6 AM refresh is scheduled and operational with proper logging and error handling.

---

## Phase 6: User Story 4 - Environment Promotion Pipeline (Priority: P1)

**Goal**: Define and validate Dev → UAT → Prod promotion workflow with checklist and approval gates

**Independent Test**: Complete one promotion cycle (Dev → UAT → Prod) with all validations passing and approvals obtained

### Dev → UAT Promotion

- [ ] T050 [US4] Create promotion checklist in documentation/promotion-checklist.md:
  - [ ] Data accuracy validation: TotalRevenue, TotalCost, ProfitMargin match SSAS (0% discrepancy)
  - [ ] Measure count matches: 3 measures present and queryable
  - [ ] Dimension integrity: Month, Region, Department hierarchies present
  - [ ] Filter validation: Last 12 months, Finance department filters functional
  - [ ] Visualization validation: Line chart, bar chart, table render without errors
  - [ ] Color accuracy: Dark Blue #1F4E79, Gray #555555 verified in Power BI
  - [ ] Excel refresh: Power Query connections functional; refresh completes in < 2 minutes

- [ ] T051 [US4] Create GitHub pull request template documentation/promotion-pr-template.md with:
  - Branch destination: main (for prod) or uat (for uat)
  - Checklist: All items from T050 marked as complete
  - Change notes: What changed since last promotion (e.g., "Added ProfitMargin visualization")
  - Rollback plan: How to revert if promotion causes issues

- [ ] T052 [US4] Implement automated validation on PR: GitHub Actions workflow that:
  - Runs scripts/promotion-validator.ps1 on PR open
  - Validates all checklist items programmatically where possible
  - Reports pass/fail status as PR check (blocks merge if validation fails)

### UAT → Prod Promotion

- [ ] T053 [US4] Add approval requirement to documentation/approval-matrix.md:
  - UAT → Prod requires approval from: Data Governance team lead (1 review required)
  - Technical review: At least 1 developer approval on PR
  - Documented reason: Release notes explaining business value

- [ ] T054 [US4] Configure GitHub branch protection rule: `main` branch (Prod-ready) requires status checks pass + 1 review before merge
  - Status checks: GitHub Actions validation (T052)
  - Required reviewers: Data Governance team lead (automatic assignment)

### Promotion Documentation

- [ ] T055 [P] [US4] Create change log template: documentation/release-notes-[VERSION].md with:
  - Version: [MAJOR.MINOR.PATCH]
  - Deployment date/time
  - Promoted by: [Name]
  - Approved by: [Name] (for UAT → Prod)
  - Changes: Bullet list of what changed
  - Impact: What end users will see/experience
  - Rollback procedure: Steps to revert if critical issue found

- [ ] T056 [P] [US4] Create deployment runbook: documentation/deployment-guide.md with numbered steps:
  1. Create feature branch from dev or uat
  2. Make changes, test in Dev
  3. Create PR against uat (for UAT promotion)
  4. Run checklist; wait for validation
  5. Get technical review approval
  6. Merge PR to uat
  7. (For Prod) Create PR uat → main
  8. Wait for Data Governance approval
  9. Merge PR to main
  10. Monitor logs post-deployment for 24 hours

### Promotion Testing

- [ ] T057 [US4] Execute test promotion Dev → UAT:
  - Create feature branch with trial changes
  - Follow runbook steps T056; validate each step
  - Confirm data flows correctly from Dev to UAT environment
  - Document any issues in release-notes

- [ ] T058 [US4] Execute test promotion UAT → Prod:
  - Following T057 completion, promote to Prod with full approval workflow
  - Verify Prod environment accessible and data current
  - Confirm Finance team can access Prod reports

**Checkpoint**: User Story 4 complete. Promotion pipeline is documented, tested, and operational from Dev through Prod.

---

## Phase 7: User Story 5 - Data Accuracy Validation (Priority: P1)

**Goal**: Implement automated framework that validates reported metrics match source SSAS cube before promotions

**Independent Test**: Run validation queries; confirm Power BI values match SSAS values within 0.01% tolerance; validation blocks promotion if threshold exceeded

### Validation Query Creation

- [ ] T059 [P] [US5] Create direct SSAS validation query in tests/measure-validation.sql:
  ```sql
  SELECT 
    Month, Region, Department,
    SUM(Revenue) as TotalRevenue,
    SUM(Cost) as TotalCost,
    (SUM(Revenue) - SUM(Cost)) as ProfitMargin
  FROM FinHub_Cube
  WHERE Month >= EOMONTH(TODAY(), -12) AND Department = 'Finance'
  GROUP BY Month, Region, Department
  ```
  - This query represents the "source of truth" for validation

- [ ] T060 [P] [US5] Create Power BI query extractor: Script that exports Power BI table data to CSV for comparison
  - Exports: Results of Power BI table visualization (with same filters applied)
  - Format: CSV with columns matching validation query (Month, Region, Department, TotalRevenue, TotalCost, ProfitMargin)

### Validation Logic

- [ ] T061 [US5] Implement validation script in scripts/validation-runner.ps1 with:
  - Step 1: Execute SSAS query (T059) → Store results in ssas-results.csv
  - Step 2: Extract Power BI data (T060) → Store in powerbi-results.csv
  - Step 3: Compare line-by-line; calculate variance for each measure
  - Step 4: Flag discrepancies > 0.01% as FAIL
  - Step 5: Generate validation-report.html with detailed comparison table

- [ ] T062 [US5] Define tolerance thresholds in scripts/validation-runner.ps1:
  - Currency fields (TotalRevenue, TotalCost): Tolerance 0.01 (one cent) for absolute difference OR 0.01% for relative difference
  - Percentage fields (ProfitMargin): Tolerance 0.01% relative difference
  - Acceptable variance reason: SSAS aggregation may differ slightly from Power BI aggregation in rare cases

- [ ] T063 [US5] Create tolerance baseline: tests/validation-baseline.csv with known good values
  - Periodically updated (quarterly) from SSAS direct query
  - Used as reference for year-over-year validation

### Automated Validation at Promotion Gates

- [ ] T064 [US5] Integrate validation into Dev → UAT promotion:
  - scripts/promotion-validator.ps1 calls scripts/validation-runner.ps1 before approval
  - If validation FAILS: PR check fails; promotion blocked with error details
  - If validation PASSES: PR check passes; promotion can proceed

- [ ] T065 [US5] Integrate validation into UAT → Prod promotion:
  - Same logic as T064 at UAT → Prod boundary
  - Data Governance review includes validation-report.html as supporting evidence

### Daily Post-Refresh Validation (Prod Only)

- [ ] T066 [US5] Schedule daily validation in Prod environment post-refresh:
  - Time: 6:30 AM (30 minutes after refresh completes at 6 AM)
  - Trigger: scripts/validation-runner.ps1 executes automatically after refresh
  - Output: Logged to scripts/logs/validation-[date].log

- [ ] T067 [US5] Configure alert on validation failure:
  - If Prod validation FAILS: Send email/Teams to Data Admin team with:
    - Discrepancy details (which measures, which rows, magnitude of variance)
    - Estimated impact (e.g., "Profit Margin overstated by 0.5%")
    - Recommended action (investigate query; check SSAS cube health)

### Validation Testing

- [ ] T068 [P] [US5] Test validation with intentional error:
  - Modify one Power BI measure value (in Dev)
  - Run validation; confirm it detects the discrepancy and FAILS
  - Verify error message is clear and actionable

- [ ] T069 [US5] Test validation passes with good data:
  - Restore correct measure value
  - Run validation; confirm it PASSES
  - Verify promotion can proceed

**Checkpoint**: User Story 5 complete. Data accuracy validation is automated and integrated into promotion gates.

---

## Phase 8: Security & Governance (US4 Components)

**Purpose**: Implement access control, audit logging, and compliance tracking

- [ ] T070 [P] [Phase8] Configure Power BI row-level security (RLS):
  - Create security role "Finance_Only": User can only see Department = 'Finance'
  - Test RLS: Non-Finance users try to view Prod reports; confirm access denied or filtered

- [ ] T071 [P] [Phase8] Configure Excel access control:
  - Excel file stored in SharePoint with Finance team as only readers
  - Document procedure: Users request access via ticketing system; Data Admin approves/denies

- [ ] T072 [Phase8] Create audit logging trigger on all Power BI report views:
  - Log: [TIMESTAMP] | [USERNAME] | [REPORT_NAME] | [ACTION] (View/Export/Refresh)
  - Store in: Azure Table Storage or centralized logging system (configure based on org infrastructure)

- [ ] T073 [Phase8] Create audit logging trigger on Excel exports/downloads:
  - Log: [TIMESTAMP] | [USERNAME] | [FILENAME] | [ACTION] (Download/Modify/Export)

- [ ] T074 [Phase8] Create approval workflow trace:
  - Every promotion event logged with: Promoted-by, Approved-by, Date, Reason, Changes
  - Store in: GitHub pull request history (automatically captured) + audit-log.csv (redundant backup)

---

## Phase 9: Testing & Validation

**Purpose**: Comprehensive testing of all components and promotion workflow

- [ ] T075 [SSAS] Test SSAS connectivity from all three environments (Dev, UAT, Prod):
  - [ ] Test from Power BI Desktop: Can connect without error
  - [ ] Test from Excel Power Query: Can connect and query without error
  - [ ] Test from PowerShell: Can execute DAX/MDX query using OLEDB provider
  - **Result**: All three connectivity tests PASS; connection strings documented in configurations/

- [ ] T076 [Measures] Test all three measures in all three environments:
  - [ ] TotalRevenue: Returns currency values; sum is reasonable (e.g., in millions for finance org)
  - [ ] TotalCost: Returns currency values; sum is reasonable; less than TotalRevenue
  - [ ] ProfitMargin: Returns percentage or currency values; calculated correctly (Revenue - Cost)
  - **Result**: All measures return expected data ranges

- [ ] T077 [Filters] Test Last 12 Months and Finance filters:
  - [ ] Last 12 Months: Filter reduces data to approximately 1/12 of full dataset (varies by department)
  - [ ] Department = Finance: Filter applied, only Finance rows visible
  - [ ] Both filters combined: Further reduction to Finance-only, Last 12 months
  - **Result**: Filters work individually and in combination

- [ ] T078 [Power BI] Test Power BI visualizations:
  - [ ] Line chart: Shows monthly trend; clicking legend toggles series visibility
  - [ ] Bar chart: Shows one bar per region; bars have correct heights; colors are correct (#555555)
  - [ ] Table: Shows all rows; columns sortable; formatting matches corporate standards
  - **Result**: All visualizations render correctly; user interactions work

- [ ] T079 [Excel] Test Excel workbook:
  - [ ] Sheets tab: All three sheets present (Summary, by-Region, by-Department)
  - [ ] Data: Each sheet populated with correct data; counts match Power BI
  - [ ] Refresh: "Refresh Data" button works; queries execute; data updates
  - [ ] Formatting: Headers are Dark Blue, alternating row shading applied
  - **Result**: Excel workbook is fully functional

- [ ] T080 [Refresh] Test daily refresh schedule:
  - [ ] Manual trigger: Run scripts/refresh-execute.ps1 manually; completes successfully
  - [ ] Scheduled trigger: Verify task scheduler runs at 6 AM; check task history
  - [ ] Logging: Verify refresh logs written to scripts/logs/refresh-[date].log
  - [ ] Performance: Measure refresh duration; verify < 15 minutes
  - **Result**: Refresh pipeline works end-to-end; performance is acceptable

- [ ] T081 [Promotion] Test promotion workflow:
  - [ ] Dev → UAT: Follow promotion-guide.md; create PR, validate checklist, merge to uat branch
  - [ ] Verify data in UAT matches Dev
  - [ ] UAT → Prod: Create PR, get approval, merge to main branch
  - [ ] Verify data in Prod matches UAT (post-promotion)
  - **Result**: Promotion workflow tested end-to-end; all gates function correctly

- [ ] T082 [Validation] Test data accuracy validation:
  - [ ] Run validation script in each environment
  - [ ] Compare Power BI values to direct SSAS queries
  - [ ] Verify all values match within tolerance (0% variance in Dev)
  - [ ] **Result**: Validation passes; no discrepancies found

- [ ] T083 [Security] Test access control:
  - [ ] Prod Power BI: Finance user accesses report - SUCCESS
  - [ ] Prod Power BI: Non-Finance user accesses report - DENIED (RLS enforced)
  - [ ] Prod Excel: Finance user can download - SUCCESS
  - [ ] Prod Excel: Non-Finance user tries to access SharePoint - DENIED
  - **Result**: Access control working; only Finance team can view reports in Prod

---

## Phase 10: Documentation & Deployment Guides

- [ ] T084 [P] [Docs] Create deployment-guide.md with step-by-step promotion instructions (referenced in T056)
- [ ] T085 [P] [Docs] Create troubleshooting guide: documentation/troubleshooting.md with common issues:
  - SSAS connection timeout → check network connectivity, firewall rules
  - Refresh fails → check SSAS cube availability, Power BI service status
  - Data discrepancies → run validation script, compare to baseline
  - Excel Power Query connection fails → verify parameterized connection strings

- [ ] T086 [P] [Docs] Create user guide for Finance team: documentation/user-guide.md
  - How to access Power BI reports
  - How to use filters and visualizations
  - How to export to Excel
  - How to request access or report issues

- [ ] T087 [Docs] Create admin runbook: documentation/admin-runbook.md for Data Admin team
  - Monitoring dashboard for refresh status
  - Handling refresh failures
  - Promoting changes and approving promotions
  - Reviewing audit logs for compliance

---

## Phase 11: UAT & Stakeholder Sign-Off

- [ ] T088 [UAT] Conduct Finance team UAT testing:
  - Finance team accesses Power BI reports in UAT
  - Validates visualizations show expected financial summary
  - Confirms data accuracy against prior month reports
  - Tests filter functionality and export to Excel

- [ ] T089 [UAT] Get stakeholder sign-off:
  - Finance Manager: Approves dashboard for Prod deployment
  - Data Governance Lead: Approves promotion procedure, security controls, audit logging
  - IT Security: Approves access control implementation (RLS, SharePoint permissions)

- [ ] T090 [Prod] Deploy to Production:
  - Create final promotion PR from uat → main
  - Obtain all required approvals (T089)
  - Merge to main branch; trigger release workflow
  - Monitor logs and dashboards for 24-hour post-deployment window

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1-2**: Setup + Foundation (no dependencies) → Execute first (weeks 1-2)
- **Phase 3-5**: User Stories 1-2-3 (depend on foundational) → Can run in parallel (weeks 3-5)
- **Phase 6-7**: User Stories 4-5 (depend on Phase 5) → Execute after (weeks 5-6)
- **Phase 8-9**: Security + Testing (depend on all user stories complete) → Execute after (weeks 6-7)
- **Phase 10-11**: Documentation + UAT + Prod Deployment (after testing) → Execute last (weeks 7-8)

### User Story Parallelization

After Foundational phase (T014-T019 complete):
- **US1** (Power BI) and **US2** (Excel): Can run in parallel; different file formats
- **US3** (Refresh): Can start independently; depends only on foundation
- **US4-5** (Promotion + Validation): Must run after US1-2-3 complete for end-to-end testing

### Critical Path

```
T001-T006 (Setup) → T007-T019 (Foundation)
                 ├→ T026-T030 (US1 - Power BI)
                 ├→ T032-T039 (US2 - Excel) → In parallel
                 └→ T041-T049 (US3 - Refresh)
                              ↓
                    T050-T058 (US4 - Promotion) → Sequential
                              ↓
                    T059-T069 (US5 - Validation)
                              ↓
                    T070-T074 (Security)
                              ↓
                    T075-T083 (Testing)
                              ↓
                    T084-T087 (Documentation)
                              ↓
                    T088-T090 (UAT + Prod Release)
```

---

## Parallel Execution Opportunities

- All T002-T006 marked [P] can run in parallel in Phase 1
- All T007-T012 marked [P] can run in parallel in Phase 1.5
- All T020-T021 marked [P] testing can run in parallel in Phase 3
- User Stories 1, 2, 3 can run in parallel after foundation (different roles/systems)
- All Phase 10 documentation tasks marked [P] can run in parallel

**Estimated Timeline**: 8 weeks (6 weeks development + 1 week UAT + 1 week Prod stabilization)

---

**Tasks Status**: READY FOR TEAM ASSIGNMENT

**Version**: 1.0.0 | **Created**: 2026-02-20
