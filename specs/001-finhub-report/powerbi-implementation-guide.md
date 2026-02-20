# Power BI Implementation Guide: FinHub Financial Summary Report

**Project**: FinHub Financial Summary Report  
**Specification Reference**: [specs/001-finhub-report/specification.md](./specification.md)  
**Phase**: Detailed Power BI Architecture & Implementation  
**Version**: 1.0.0 | **Date**: 2026-02-20

---

## Overview

This guide provides step-by-step instructions for building the FinHub Financial Summary Report in Power BI Desktop. It covers:

1. **SSAS Cube Connection** — Connecting to the `FinHub_Cube` data source
2. **Data Model Design** — Measures, calculated columns, and relationships
3. **Visualizations** — Line chart, bar chart, and summary table
4. **Filters & Interactivity** — Date range and department slicers
5. **Formatting & Branding** — Corporate color palette and FD&E standards
6. **Validation Strategy** — Data accuracy reconciliation
7. **Refresh & Promotion** — Dev → UAT → Prod workflow

---

## Part 1: SSAS Cube Connection Setup

### Step 1.1: Prepare Connection Credentials

**Objective**: Gather connection information for all three environments (Dev, UAT, Prod)

**Action Items**:
- [ ] Obtain SSAS server names and ports for Dev, UAT, Prod environments
- [ ] Example format: `Dev: analysis-dev.company.com:2383`, `UAT: analysis-uat.company.com:2383`, `Prod: analysis-prod.company.com:2383`
- [ ] Confirm Windows authentication will be used (no separate username/password)
- [ ] Verify firewall rules allow Power BI Desktop → SSAS connectivity
- [ ] Test connectivity using SQL Server Management Studio or Excel Power Query beforehand

**Result**: Connection credentials documented in `configurations/connections-[environment].json`

```json
{
  "environment": "dev",
  "ssas_server": "analysis-dev.company.com",
  "ssas_port": 2383,
  "ssas_database": "FinHub_Cube",
  "authentication": "windows",
  "data_source_name": "SSAS_FinHub_Dev"
}
```

---

### Step 1.2: Create Power BI Project & Connect to SSAS

**Objective**: Open Power BI Desktop and establish SSAS data connection

**Action Items**:

1. **Open Power BI Desktop**
   - [ ] Launch Power BI Desktop application
   - [ ] Click **New report** or start with blank report

2. **Create SSAS Connection**
   - [ ] Go to **Home** → **Get Data** → **Other** → **Analysis Services**
   - [ ] Server field: Enter `analysis-dev.company.com:2383` (or UAT/Prod as appropriate)
   - [ ] Database field: Leave blank initially (will be populated with available databases)
   - [ ] Click **OK** or **Connect**

3. **Select Database**
   - [ ] Find and select `FinHub_Cube` from the list of available databases
   - [ ] Click **OK** to confirm
   - [ ] Wait for metadata to load

4. **Verify Connection**
   - [ ] In Power BI Desktop, you should see the **Data** pane on the right
   - [ ] Expand `FinHub_Cube` node; verify measures and dimensions appear
   - [ ] Expected measures: `TotalRevenue`, `TotalCost`, `ProfitMargin`
   - [ ] Expected dimensions: `Month`, `Region`, `Department`

**Troubleshooting**:
- Connection failed? Check firewall rules; test connectivity from command line: `Test-NetConnection analysis-dev.company.com -Port 2383`
- Measures/dimensions not visible? Verify SSAS cube permissions; may need to grant "Read" access

**Result**: Power BI Desktop connected to Dev SSAS cube with all measures and dimensions visible

---

### Step 1.3: Create Data Model (Import vs DirectQuery Decision)

**Objective**: Decide whether to Import data into Power BI or use DirectQuery to SSAS

**Decision Matrix**:

| Factor | Import Mode | DirectQuery Mode |
|--------|-------------|------------------|
| **Refresh Performance** | Slower (imports all data) | Faster (queries live) |
| **Query Response Time** | Fast (data in memory) | Depends on SSAS performance |
| **Real-time Data** | Updates on schedule | Real-time (each query goes to SSAS) |
| **File Size** | Larger (.pbix file) | Smaller |
| **Recommended For** | Dev/UAT testing | Prod large datasets |

**Recommendation for FinHub**: Use **Import mode** for Dev/UAT (better performance for development), consider **DirectQuery** for Prod if SSAS can handle concurrent queries.

**Action Items** (Import Mode):

1. **Load Data into Power BI**
   - [ ] In Power BI Desktop, click **Home** → **Transform data** to open Power Query Editor
   - [ ] In the left pane, you'll see the SSAS cube name
   - [ ] Select `FinHub_Cube` table; click **Load** to import into Power BI model
   - [ ] Wait for data to load (may take 1-2 minutes depending on data volume)

2. **Verify Data Load**
   - [ ] In the **Data** pane, confirm a table appears with all measures and dimensions
   - [ ] Refresh status should show: Row count ≈ 1,800 for 12-month Finance department data

3. **Create Relationships** (if not auto-detected)
   - [ ] Open **Model** view (button in left ribbon)
   - [ ] Verify relationships between Month, Region, Department dimensions
   - [ ] Relationships should be: `FinHub_Cube[Month] → Month[Month]`, etc.
   - [ ] If missing, drag dimension fields to create relationships (typically 1-to-many)

**Result**: Data imported into Power BI model with 1,800+ rows; relationships established

---

## Part 2: Data Model & Measure Creation

### Step 2.1: Verify Measures from SSAS Cube

**Objective**: Confirm that TotalRevenue, TotalCost, ProfitMargin measures exist in SSAS and are properly recognized by Power BI

**Action Items**:

1. **Check Measure Visibility**
   - [ ] Open **Data** pane (if closed: **View** → **Data**)
   - [ ] Expand `FinHub_Cube` table
   - [ ] Look for three measures: `TotalRevenue`, `TotalCost`, `ProfitMargin`
   - [ ] Measure icons: Should show Σ (summation) symbol indicating they're measures

2. **Sample Query Results**
   - [ ] Create a blank table visualization (temporary for testing)
   - [ ] Drag `TotalRevenue` to the table
   - [ ] Verify values appear (should show sum of revenue; likely millions for finance org)
   - [ ] Sample value: $25,450,000 (example)

3. **Verify Measure Definitions**
   - [ ] If measures not visible or values incorrect, check SSAS cube:
     - [ ] Open SQL Server Management Studio
     - [ ] Connect to SSAS
     - [ ] Right-click `FinHub_Cube` → **Script Cube as** → **Alter to New Query Window**
     - [ ] Search for MEASURE definitions; verify names and calculations match specification
   - [ ] If SSAS defines measures differently (e.g., single-currency conversion), document discrepancies

**Result**: All three measures confirmed in Power BI with correct values

---

### Step 2.2: Create Calculated Columns (if needed)

**Objective**: Add any derived calculations (e.g., ProfitMargin percentage if only stored as absolute value)

**Action Items**:

1. **Check if ProfitMargin is Already Calculated**
   - [ ] In SSAS, verify ProfitMargin definition:
     - [ ] If ProfitMargin = `[TotalRevenue] - [TotalCost]` (absolute), it's a simple difference
     - [ ] If ProfitMargin = `([TotalRevenue] - [TotalCost]) / [TotalRevenue]` (percentage), it's already calculated
   - [ ] Document which approach SSAS uses

2. **Create Percentage Measure (if needed)**
   - [ ] If SSAS only provides absolute profit, create percentage in Power BI:
   - [ ] **Modeling** → **New Column** (or **Model** view → **New Measure**)
   - [ ] Name: `ProfitMargin %`
   - [ ] Formula: `[ProfitMargin] / [TotalRevenue]`
   - [ ] Format: Percentage (right-click column → **Format** → **Percentage**)

3. **Add Profit Margin Absolute Value** (if only percentage exists)
   - [ ] If SSAS provides percentage, create absolute profit in Power BI:
   - [ ] Name: `Profit (Absolute)`
   - [ ] Formula: `[TotalRevenue] - [TotalCost]`
   - [ ] Format: Currency

**Result**: All required measures available; calculated columns added if needed

---

### Step 2.3: Create Date Dimension Calculated Columns (for filtering)

**Objective**: Add helper columns for "Last 12 Months" filtering

**Action Items**:

1. **Add Month Name Column** (if not in SSAS)
   - [ ] **Model** view → Select Month dimension table
   - [ ] **New Column** → Name: `Month Name`
   - [ ] Formula: `FORMAT([Date], "MMM YYYY")` (format as "Jan 2026")

2. **Add Year-Month Number**
   - [ ] **New Column** → Name: `Year-Month Number`
   - [ ] Formula: `YEAR([Date]) * 100 + MONTH([Date])`
   - [ ] Purpose: Useful for sorting or programmatic filtering

3. **Add "Last 12 Months" Flag** (Advanced option)
   - [ ] **New Column** → Name: `Is Last 12 Months`
   - [ ] Formula: `IF([Date] >= TODAY()-365, "Yes", "No")`
   - [ ] This enables quick filtering

**Result**: Date dimension enhanced with helper columns for filtering

---

## Part 3: Visualizations

### Step 3.1: Build Line Chart - "Monthly Total Revenue"

**Objective**: Create visualization showing revenue trend over 12 months

**Action Items**:

1. **Insert Line Chart**
   - [ ] **Home** → **Insert** → **Line chart** → Select **Line chart** (first option)
   - [ ] Place chart on canvas

2. **Configure Chart Data**
   - [ ] **Data** pane → Drag `Month` dimension to **Axis** field
     - Position: X-axis should show months in chronological order
   - [ ] Drag `TotalRevenue` measure to **Values** field
     - Power BI auto-aggregates using SUM (correct for this measure)
   - [ ] Drag `Region` to **Legend** field (optional: shows revenue by region with different line colors)

3. **Format Chart - Colors & Appearance**
   - [ ] Right-click chart → **Format visual**
   - [ ] Navigate to **Visual** → **Data colors**
   - [ ] Change line color to Dark Blue (#1F4E79)
   - [ ] Set line thickness to 2.5 pt for visibility

4. **Add Chart Title**
   - [ ] **Format visual** → **Title** → Toggle ON
   - [ ] Title text: "Monthly Total Revenue"
   - [ ] Font size: 16 pt
   - [ ] Font weight: Bold

5. **Format Axis Labels**
   - [ ] **Format visual** → **X-axis**
   - [ ] Format: Specify month format (e.g., "Jan", "Feb")
   - [ ] **Y-axis**
   - [ ] Format: Currency ($) with 0 decimal places for cleaner look

6. **Enable Interactive Features**
   - [ ] **Format visual** → **General** → **Advanced**
   - [ ] Ensure tooltips show exact values on hover
   - [ ] Expected tooltip: "Month: Jan 2026, Revenue: $2,450,000"

**Acceptance Criteria**:
- ✅ Chart renders with 12 months on X-axis
- ✅ Revenue values correct (match SSAS query)
- ✅ Line color is Dark Blue (#1F4E79)
- ✅ Title reads "Monthly Total Revenue"
- ✅ Hovering shows exact values

**Result**: Line chart displays monthly revenue trend

---

### Step 3.2: Build Bar Chart - "Profit Margin by Region"

**Objective**: Create visualization showing profit margin across regions (one bar per region)

**Action Items**:

1. **Insert Bar Chart**
   - [ ] **Home** → **Insert** → **Bar chart** → Select **Clustered bar chart**
   - [ ] Place chart on canvas below line chart

2. **Configure Chart Data**
   - [ ] Drag `Region` dimension to **Axis** field (Y-axis)
     - Regions appear as horizontal bars
   - [ ] Drag `ProfitMargin` measure to **Values** field
     - Power BI aggregates (SUM or AVG depending on measure type)

3. **Format Chart - Colors**
   - [ ] Right-click chart → **Format visual**
   - [ ] **Visual** → **Data colors**
   - [ ] Change bar color to Gray (#555555)
   - [ ] Font color: Black for labels

4. **Add Chart Title**
   - [ ] **Format visual** → **Title**
   - [ ] Title text: "Profit Margin by Region"
   - [ ] Font: 16 pt, Bold

5. **Format Axis Labels**
   - [ ] **X-axis**: Format as currency (if profit margin is absolute) or percentage (if ratio)
   - [ ] **Y-axis**: Region names (typically 3-5 regions)

6. **Sort Bars**
   - [ ] **Format visual** → **Visual** → **Sort axis**
   - [ ] Sort by: `ProfitMargin` Descending (highest profit first)

**Acceptance Criteria**:
- ✅ One bar per region
- ✅ Bar color is Gray (#555555)
- ✅ Title: "Profit Margin by Region"
- ✅ Values sorted (highest profit at top)
- ✅ Exact values visible on hover

**Result**: Bar chart displays profit margin by region

---

### Step 3.3: Build Table - "Summary by Department"

**Objective**: Create tabular view showing all measures and dimensions for detailed review

**Action Items**:

1. **Insert Table Visualization**
   - [ ] **Home** → **Insert** → **Table**
   - [ ] Place on canvas

2. **Add Columns to Table**
   - [ ] Drag `Month` dimension to **Columns**
   - [ ] Drag `Department` dimension to **Columns**
   - [ ] Drag `TotalRevenue` measure to **Values**
   - [ ] Drag `TotalCost` measure to **Values**
   - [ ] Drag `ProfitMargin` measure to **Values**
   - [ ] Result: 5-column table (Month, Department, Revenue, Cost, Profit)

3. **Format Table - Appearance**
   - [ ] Right-click table → **Format visual**
   - [ ] **Visual** → **Style** → Select a built-in table style
   - [ ] Or customize manually:
     - [ ] **Header** → Background color: Dark Blue (#1F4E79), Font color: White, Bold
     - [ ] **Values** → Apply alternating row colors (light gray #F2F2F2)

4. **Format Number Columns**
   - [ ] Right-click `TotalRevenue` column → **Format**
   - [ ] Format: Currency ($) with 2 decimals
   - [ ] Right-click `TotalCost` → Apply same format
   - [ ] Right-click `ProfitMargin` → Format: Percentage (if applicable) or Currency

5. **Enable Row Sorting**
   - [ ] Click column header to sort by that column
   - [ ] Default sort: By Month (chronological)

6. **Width Adjustment**
   - [ ] Adjust column widths for readability
   - [ ] Month: 100px, Department: 120px, Revenue: 140px, Cost: 140px, Profit: 140px

**Acceptance Criteria**:
- ✅ Table shows 5 columns (Month, Department, Revenue, Cost, Profit)
- ✅ Header row: Dark Blue (#1F4E79) background, white text
- ✅ Alternating row shading (light gray) for readability
- ✅ Rows sortable by column
- ✅ Numbers formatted correctly ($ and %)
- ✅ Expected row count: ~1,800 (12 months × departments in Finance)

**Result**: Summary table displays all detailed data

---

## Part 4: Filters & Interactivity

### Step 4.1: Create "Last 12 Months" Date Range Slicer

**Objective**: Add interactive filter allowing users to change date range (default: last 12 months)

**Action Items**:

1. **Insert Date Slicer**
   - [ ] **Home** → **Insert** → **Slicer** → **Date slicer**
   - [ ] Place top-left of report (above visualizations)

2. **Connect Slicer to Data**
   - [ ] After inserting slicer, **Data** pane appears
   - [ ] Drag `Month` or `Date` dimension to slicer
   - [ ] Slicer displays calendar or date range selector

3. **Set Default Filter (Last 12 Months)**
   - [ ] Click slicer → Look for filter options
   - [ ] Configure to show last 12 calendar months by default:
     - [ ] Example: If today is Feb 20, 2026, show Mar 2025 through Feb 2026
   - [ ] **Format visual** → **General** → Set **Filter type** to "Relative date" if available
   - [ ] Or manually select: Click last 12 months in calendar

4. **Format Slicer**
   - [ ] **Format visual** → **Title** → Add title "Date Range" or "Month"
   - [ ] Font: 12 pt, bold
   - [ ] Display style: Dropdown or calendar (your choice; both work)

5. **Test Slicer Interaction**
   - [ ] Click different months in slicer
   - [ ] Verify all three visualizations (line chart, bar chart, table) update instantly
   - [ ] Change back to "Last 12 months" - all values should recalculate

**Acceptance Criteria**:
- ✅ Slicer visible at top of report
- ✅ Default: Last 12 months selected
- ✅ Changing slicer updates all visualizations in < 1 second
- ✅ Title displayed

**Result**: Date slicer functional; users can customize date range

---

### Step 4.2: Create "Department" Multi-Select Slicer

**Objective**: Add filter for department selection (default: Finance only)

**Action Items**:

1. **Insert Department Slicer**
   - [ ] **Home** → **Insert** → **Slicer** → **Slicer**
   - [ ] Place next to date slicer (top-center of report)

2. **Connect Slicer to Department Dimension**
   - [ ] **Data** pane → Drag `Department` dimension to slicer
   - [ ] Slicer displays list of all departments (e.g., Finance, Operations, Sales, Marketing)

3. **Enable Multi-Select**
   - [ ] Right-click slicer → **Format visual**
   - [ ] **Visual** → **Slicer settings** → Toggle **Multi-select with Ctrl** ON
   - [ ] This allows users to hold Ctrl and click multiple departments

4. **Set Default (Finance Only)**
   - [ ] Click "Finance" in slicer
   - [ ] Other departments become dimmed/inactive
   - [ ] Expected: Only Finance department data shown in all visualizations

5. **Format Slicer**
   - [ ] **Format visual** → **Title**: "Department"
   - [ ] Display style: "Dropdown" or "List" (list is recommended for visibility)
   - [ ] Font: 12 pt, bold

6. **Test Slicer Interaction**
   - [ ] Click "Sales" department (while holding Ctrl)
   - [ ] Verify table now shows both Finance & Sales data
   - [ ] Notice: Bar chart may only show regions with selected department data
   - [ ] Click "Finance" only to return to default

**Acceptance Criteria**:
- ✅ Department slicer visible; Finance selected by default
- ✅ Multi-select works: Ctrl+click adds/removes departments
- ✅ Changing department updates all visualizations
- ✅ Title displayed

**Result**: Department slicer functional; users can view multiple departments if desired

---

### Step 4.3: Add "Reset Filters" Button (Optional Enhancement)

**Objective**: Provide one-click reset to default filters (Last 12 months + Finance only)

**Action Items**:

1. **Create Bookmark for Default State**
   - [ ] With filters set to default (Last 12 months + Finance):
   - [ ] **View** → **Bookmarks pane**
   - [ ] Click **Add** → Name: "Reset Filters" or "Default View"
   - [ ] This bookmark captures current filter state

2. **Insert Button**
   - [ ] **Insert** → **Button** → **Blank button**
   - [ ] Size and position bottom-left of report

3. **Add Button Action**
   - [ ] Right-click button → **Button action**
   - [ ] Action type: **Bookmark**
   - [ ] Select: "Reset Filters" bookmark created in Step 4.3.1
   - [ ] Button text: "Reset Filters"

4. **Format Button**
   - [ ] Font: 12 pt, dark color
   - [ ] Background: Light gray or white, border

**Result**: Users can click "Reset Filters" button to return to default view (optional feature)

---

## Part 5: Formatting & Branding

### Step 5.1: Apply Corporate Theme & Color Palette

**Objective**: Ensure all visualizations follow FinHub corporate brand standards

**Specifications**:
- Primary color: Dark Blue (#1F4E79)
- Secondary color: Gray (#555555)
- Background: White
- Font: Arial or Calibri (standard)

**Action Items**:

1. **Create/Apply Custom Theme**
   - [ ] **View** → **Themes** → **Browse themes** (if custom theme exists)
   - [ ] Or manually apply colors:
     - [ ] Select each visualization
     - [ ] **Format visual** → **Appearance** → Set colors

2. **Report Page Background**
   - [ ] **Page background** (right-click white area) → Format
   - [ ] Color: White (#FFFFFF)
   - [ ] No image

3. **Report Title Formatting**
   - [ ] Insert text box at top: "FinHub Financial Summary Report"
   - [ ] Font: Arial 18pt, Bold, Dark Blue (#1F4E79)

4. **Chart Title Formatting** (applied in prior steps)
   - [ ] Line chart: "Monthly Total Revenue" - Dark Blue
   - [ ] Bar chart: "Profit Margin by Region" - Gray
   - [ ] Table header: Dark Blue with white text

5. **Consistency Check**
   - [ ] All headers: Dark Blue (#1F4E79)
   - [ ] All secondary elements: Gray (#555555)
   - [ ] Background: White
   - [ ] Fonts: Readable and consistent

**Result**: Report branded with corporate colors and consistent formatting

---

### Step 5.2: Number Formatting Standards

**Objective**: Ensure all currency and percentage values display correctly

**Action Items**:

1. **Currency Fields** (TotalRevenue, TotalCost, ProfitMargin Absolute)
   - [ ] Format: $#,##0 (e.g., $2,450,000)
   - [ ] Decimals: 0 for large numbers like millions; 2 decimals for detail tables
   - [ ] Negative numbers: Show in parentheses (red color) if needed

2. **Percentage Fields** (ProfitMargin %)
   - [ ] Format: 0.00% (e.g., 23.45%)
   - [ ] Decimals: 2

3. **Apply to All Measures**
   - [ ] Right-click each measure in **Data** pane
   - [ ] **Data type** → Format Number
   - [ ] Global setting applies to all visualizations using that measure

**Result**: All numbers display in standard corporate format

---

## Part 6: Data Validation Strategy

### Step 6.1: Create Validation Query (SSAS Truth Source)

**Objective**: Establish baseline for data accuracy validation

**Action Items**:

1. **Write Direct SSAS Query**
   - [ ] Open SQL Server Management Studio (SSAS connection required)
   - [ ] Create validation query:

```sql
SELECT 
  [Measures].[TotalRevenue],
  [Measures].[TotalCost],
  [Measures].[ProfitMargin],
  [Month].[Month].CurrentMember.Name AS MonthName,
  [Region].[Region].CurrentMember.Name AS RegionName,
  [Department].[Department].CurrentMember.Name AS DepartmentName
FROM [FinHub_Cube]
WHERE [Department].[Department].&[Finance]
AND [Month].[Month] >= [Last 12 Months]
ORDER BY [Month].[Month] DESC
```

2. **Export Results to CSV**
   - [ ] Execute query in SSAS
   - [ ] Export results to `tests/ssas-validation-baseline.csv`
   - [ ] This becomes the "source of truth" for validation

3. **Document Expected Values**
   - [ ] Example row in baseline:
     - [ ] Jan 2026, Finance, North Region, Revenue: $2,450,000, Cost: $1,800,000, Profit: $650,000

**Result**: Validation baseline created; serves as truth source

---

### Step 6.2: Create Power BI Validation Export

**Objective**: Extract Power BI data (from our report table) for comparison

**Action Items**:

1. **Export Table Data from Power BI**
   - [ ] In Power BI Desktop report, right-click summary table
   - [ ] **Export data** or copy table to clipboard
   - [ ] Paste into Excel
   - [ ] Save as `tests/powerbi-validation-results.csv`

2. **Ensure Columns Match Baseline**
   - [ ] Columns: Month, Department, Region, TotalRevenue, TotalCost, ProfitMargin
   - [ ] Row count: Should match baseline

3. **Sample Data Comparison**
   - [ ] Pick 5-10 random rows
   - [ ] Compare values to baseline:
     - [ ] Jan 2026, Finance, North: Revenue in Power BI = $2,450,000 ✅
     - [ ] If discrepancy: Investigate measure definition in SSAS vs Power BI

**Result**: Power BI data exported; ready for validation comparison

---

### Step 6.3: Run Validation (Accuracy Reconciliation)

**Objective**: Confirm Power BI values match SSAS within acceptable tolerance

**Action Items**:

1. **Compare Baseline to Power BI Export**
   - [ ] Create Excel workbook: `tests/validation-comparison.xlsx`
   - [ ] Sheet 1: Baseline (SSAS data)
   - [ ] Sheet 2: Power BI export
   - [ ] Sheet 3: Comparison
     - [ ] Formula: `=IF(ABS(Sheet2!Revenue - Sheet1!Revenue) <= $1, "PASS", "FAIL")`
     - [ ] Tolerance: ±$1 for currency (0.01 variance acceptance)

2. **Identify Discrepancies** (if any)
   - [ ] Flag rows where Power BI value differs from SSAS by > tolerance
   - [ ] Investigate cause:
     - [ ] Measure definition mismatch?
     - [ ] Filter not applied correctly (Finance filter missing)?
     - [ ] Rounding difference in aggregation?

3. **Document Validation Result**
   - [ ] Create `tests/validation-report.txt`:
     - [ ] Total rows compared: 1,800
     - [ ] Rows passed: 1,800 (✅ 100%)
     - [ ] Rows failed: 0
     - [ ] Status: PASS

**Result**: Validation passed; Power BI data confirmed accurate

---

### Step 6.4: Automate Validation (PowerShell Script)

**Objective**: Create script to validate power BI data automatically before promotions

**Action Items**:

1. **Create PowerShell Script: `scripts/validate-powerbi-accuracy.ps1`**

```powershell
# FinHub Power BI Validation Script
# Purpose: Compare Power BI exported data to SSAS baseline
# Usage: .\validate-powerbi-accuracy.ps1 -Environment "dev" -BaselineCSV "tests/baseline.csv" -PowerBICSV "tests/powerbi-export.csv"

param(
    [string]$Environment = "dev",
    [string]$BaselineCSV,
    [string]$PowerBICSV,
    [decimal]$TolerancePercent = 0.01  # 0.01% tolerance
)

# Load data
$baseline = Import-Csv $BaselineCSV
$powerbi = Import-Csv $PowerBICSV

# Initialize counters
$passCount = 0
$failCount = 0
$discrepancies = @()

# Compare row-by-row
foreach ($row in $baseline) {
    $pbRow = $powerbi | Where-Object { $_.Month -eq $row.Month -and $_.Department -eq $row.Department }
    
    if ($null -eq $pbRow) {
        $discrepancies += "Row missing in Power BI: $($row.Month), $($row.Department)"
        $failCount++
        continue
    }
    
    # Compare Revenue
    $revVariance = [math]::Abs([decimal]$pbRow.TotalRevenue - [decimal]$row.TotalRevenue) / [decimal]$row.TotalRevenue * 100
    if ($revVariance -gt $TolerancePercent) {
        $discrepancies += "Revenue mismatch $($row.Month): SSAS=$($row.TotalRevenue), PBI=$($pbRow.TotalRevenue), Variance=$($revVariance)%"
        $failCount++
    } else {
        $passCount++
    }
}

# Output report
Write-Host "========== Power BI Validation Report =========="
Write-Host "Environment: $Environment"
Write-Host "Baseline: $BaselineCSV"
Write-Host "Power BI Export: $PowerBICSV"
Write-Host "Tolerance: $TolerancePercent%"
Write-Host ""
Write-Host "Results:"
Write-Host "  Passed: $passCount"
Write-Host "  Failed: $failCount"
Write-Host "  Total: $($passCount + $failCount)"
Write-Host ""

if ($failCount -gt 0) {
    Write-Host "Discrepancies Found (validation FAILED):"
    $discrepancies | ForEach-Object { Write-Host "  $_" }
    exit 1
} else {
    Write-Host "Status: PASS - All values accurate"
    exit 0
}
```

2. **Test Script**
   - [ ] Run: `.\scripts\validate-powerbi-accuracy.ps1 -Environment "dev" -BaselineCSV "tests/baseline.csv" -PowerBICSV "tests/powerbi-export.csv"`
   - [ ] Expected output: "Status: PASS - All values accurate"

**Result**: Validation automation ready; can integrate into promotion gates

---

## Part 7: Refresh & Promotion Workflow

### Step 7.1: Configure Power BI Refresh Schedule

**Objective**: Set up daily 6 AM refresh of Power BI dataset

**Action Items**:

1. **Publish Report to Power BI Service**
   - [ ] In Power BI Desktop: **File** → **Publish**
   - [ ] Select workspace: Dev (or appropriate workspace)
   - [ ] Report name: "FinHub Financial Summary Report"
   - [ ] Click **Select** to confirm

2. **Configure Refresh Schedule in Power BI Service**
   - [ ] After publishing, go to **Power BI Service** (web portal: app.powerbi.com)
   - [ ] Find the dataset "FinHub Financial Summary Report"
   - [ ] Click dataset → **Settings** (⚙icon)
   - [ ] **Data source credentials** → Update with SSAS connection details:
     - [ ] Username: [Windows account]
     - [ ] Password: [Account password]
     - [ ] Gateway: [On-premises data gateway, if using]
   - [ ] **Refresh schedule** → Enable
   - [ ] Refresh frequency: Daily
   - [ ] Time: 06:00 (6 AM)
   - [ ] Timezone: [Your timezone, e.g., Central Time]
   - [ ] Click **Apply**

3. **Verify Refresh Scheduled**
   - [ ] Check dataset settings; confirm refresh shows "Daily at 06:00"
   - [ ] Wait for first refresh cycle (or trigger manual refresh to test)
   - [ ] Check refresh history: **Dataset** → **Refresh history**
   - [ ] Expected: Last refresh timestamp should be recent

**Troubleshooting**:
- Refresh failed? Check credentials; verify Power BI service can reach SSAS server
- Gateway required if SSAS is on-premises

**Result**: Power BI dataset configured to refresh daily at 6 AM

---

### Step 7.2: Create Validation Checkpoint Before Promotion

**Objective**: Implement validation gate before promoting Dev → UAT

**Workflow**:
1. Dev environment report built ✅
2. Run validation script: `validate-powerbi-accuracy.ps1` → PASS ✅
3. Create GitHub PR (dev → uat branch)
4. Attach validation report to PR
5. Dev Lead approves → Merge to uat

**Action Items**:

1. **Create Validation Test Report**
   - [ ] File: `tests/promotion-checklist-dev-to-uat.md`
   - [ ] Checklist items:
     - [ ] Power BI connects to SSAS without errors
     - [ ] All measures populate (TotalRevenue, TotalCost, ProfitMargin)
     - [ ] Filters work (Last 12 months, Finance department)
     - [ ] Visualizations render correctly
     - [ ] Data validation: PASS (< 0.01% discrepancy)
     - [ ] Performance: Report loads < 3 seconds
     - [ ] Colors match corporate standards

2. **Document Promotion Steps**
   - [ ] File: `documentation/promotion-dev-to-uat.md`
   - [ ] Steps:
     1. Run validation script in Dev
     2. Export Power BI data
     3. Compare to SSAS baseline
     4. Document results in PR
     5. Request Dev Lead approval
     6. Merge to uat branch
     7. Update Power BI Service connection string to point to UAT SSAS
     8. Publish updated report to UAT workspace
     9. Verify UAT report shows UAT data (data should be different from Dev)

**Result**: Validation checkpoint established; ready for Dev → UAT promotion

---

### Step 7.3: Environment Configuration for UAT & Prod

**Objective**: Update Power BI report to work with different SSAS servers in each environment

**Action Items**:

1. **Create Connection Parameters in Power BI**
   - [ ] **Transform data** → **Manage Parameters**
   - [ ] New parameter: Name "Environment"
   - [ ] Type: Text
   - [ ] Allowed values: "dev", "uat", "prod"
   - [ ] Current value: "dev"

2. **Create Connection String Based on Environment**
   - [ ] In Power Query Editor:
   - [ ] New query: `ConnectionString`
   - [ ] Formula: `if [Environment]="dev" then "analysis-dev.company.com:2383" else if [Environment]="uat" then "analysis-uat.company.com:2383" else "analysis-prod.company.com:2383"`
   - [ ] This query returns the appropriate SSAS server based on Environment parameter

3. **Update SSAS Connection to Use Parameter**
   - [ ] In Power Query, edit the SSAS connection query
   - [ ] Replace hardcoded server name with `[ConnectionString]` parameter reference
   - [ ] This makes the report re-point to different SSAS when Environment parameter changes

4. **Test Connection Switching**
   - [ ] Change Environment parameter to "uat"
   - [ ] Publish report to Power BI Service (UAT workspace)
   - [ ] Verify it connects to UAT SSAS cube
   - [ ] Check that data is different from Dev (UAT data should reflect UAT values)

**Result**: Report works across Dev, UAT, Prod environments; connection switches automatically

---

## Part 8: Testing & Validation

### Step 8.1: User Acceptance Testing (UAT)

**Objective**: Validate report meets specification with Finance team

**Action Items**:

1. **Schedule UAT Session**
   - [ ] Date/Time: [Schedule with Finance team]
   - [ ] Participants: Finance Manager, Finance Analysts (2-3 users)
   - [ ] Duration: 1-2 hours

2. **UAT Test Scenarios**
   - [ ] **Scenario 1: Data Accuracy**
     - [ ] Compare Power BI values to Finance team's manual calculations or prior reports
     - [ ] Result: Finance Manager confirms "Values match our expected financials" ✅

   - [ ] **Scenario 2: Filters**
     - [ ] Test Last 12 Months filter
     - [ ] Test Department filter (select Finance, then add Sales)
     - [ ] Result: Visualizations update correctly per filter selection ✅

   - [ ] **Scenario 3: Visualizations**
     - [ ] Revenue trend looks reasonable (should show seasonal patterns if any)
     - [ ] Profit margin by region shows top/bottom performers
     - [ ] Table is sortable and readable
     - [ ] Result: Finance team says "Visualizations are clear and actionable" ✅

   - [ ] **Scenario 4: Export & Sharing**
     - [ ] Export line chart to PowerPoint
     - [ ] Export table to Excel
     - [ ] Share report link with colleague
     - [ ] Result: Exports preserve formatting; sharing works ✅

3. **Collect Feedback**
   - [ ] Ask: "Are there any adjustments needed?"
   - [ ] Document feedback in UAT report
   - [ ] Prioritize: Must-fix vs. nice-to-have

4. **Sign-Off**
   - [ ] Finance Manager signs: "UAT approved for production deployment"

**Result**: Finance team confirms report meets requirements

---

### Step 8.2: Performance Testing

**Objective**: Verify report meets performance targets

**Targets** (from specification):
- Report load time: < 3 seconds
- Filter refresh: < 1 second
- Daily refresh completion: < 15 minutes

**Action Items**:

1. **Report Load Time**
   - [ ] Clock load time from Power BI Service web portal
   - [ ] Load 5 times; record each: [2.8s, 2.9s, 2.7s, 3.1s, 2.8s]
   - [ ] Average: 2.9s ✅ (< 3s target)

2. **Filter Interaction Time**
   - [ ] Click Date slicer; clock update time for visualizations
   - [ ] Record: 0.8s ✅ (< 1s target)
   - [ ] Click Department slicer; record: 0.6s ✅

3. **Refresh Duration**
   - [ ] Trigger manual refresh in Power BI Service
   - [ ] Start: 10:00 AM, End: 10:12:30 AM
   - [ ] Duration: 12.5 minutes ✅ (< 15 min target)

**Result**: All performance targets met; report is performant

---

## Part 9: Deployment to Production

### Step 9.1: Final Promotion Checklist

**Objective**: Verify all gates are passed before Prod deployment

**Checklist** (from specification):

- [ ] Constitution Compliance: All 7 principles verified ✅
- [ ] Data Accuracy: Validation passed (< 0.01% discrepancy) ✅  
- [ ] Performance: Load time < 3s, Refresh < 15 min, Filter < 1s ✅
- [ ] UAT Approval: Finance team signed off ✅
- [ ] Security: RLS configured for Finance-only access ✅
- [ ] Refresh Schedule: 6 AM daily confirmed ✅
- [ ] Documentation: All runbooks and guides completed ✅
- [ ] Data Governance: Approval from Data Governance lead ✅

**Result**: All gates passed; ready for Prod deployment

---

### Step 9.2: Deploy to Production

**Action Items**:

1. **Copy .pbix to Prod**
   - [ ] Save current Power BI Desktop file as "FinHub_FinancialSummary_v1.0.0.pbix"
   - [ ] Store in: `reports/FinHub_FinancialSummary_v1.0.0.pbix`
   - [ ] Commit to GitHub (main branch, tagged v1.0.0)

2. **Publish to Prod Power BI Service**
   - [ ] In Power BI Desktop: **File** → **Publish**
   - [ ] Workspace: Production Analytics (or Prod workspace)
   - [ ] Dataset name: "FinHub Financial Summary Report"
   - [ ] Report name: "FinHub Financial Summary Report - Production"

3. **Configure Prod Refresh Schedule**
   - [ ] Follow Step 7.1 (configure daily 6 AM refresh)
   - [ ] Update connection to point to Prod SSAS server

4. **Set Prod Security (RLS)**
   - [ ] In Power BI Service Prod dataset:
     - [ ] **Security** → Create role "Finance_Only"
     - [ ] DAX rule: `[Department] = "Finance"`
     - [ ] Assign Finance team users to this role
   - [ ] Non-Finance users cannot access report (or see empty dataset)

5. **Monitor Post-Deployment**
   - [ ] First 24 hours: Check for errors
   - [ ] Verify first 6 AM refresh completes successfully
   - [ ] Check access logs: Finance team accessing report ✅
   - [ ] Validation passing: No data discrepancies ✅

**Result**: Report deployed to Production; monitoring confirmed ✅

---

## Summary: Implementation Path

```
Phase 1: Connect SSAS Cube (Step 1.1 - 1.3)
    ↓
Phase 2: Create Data Model (Step 2.1 - 2.3)
    ↓
Phase 3: Build Visualizations (Step 3.1 - 3.3)
    ↓
Phase 4: Add Interactivity (Step 4.1 - 4.3)
    ↓
Phase 5: Format & Brand (Step 5.1 - 5.2)
    ↓
Phase 6: Validation (Step 6.1 - 6.4)
    ↓
Phase 7: Refresh Setup (Step 7.1 - 7.3)
    ↓
Phase 8: Testing (Step 8.1 - 8.2)
    ↓
Phase 9: Prod Deployment (Step 9.1 - 9.2)
```

**Total Estimated Time**: 2-3 weeks (depending on team size and SSAS complexity)

---

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| **Can't connect to SSAS** | Firewall/network | Verify connectivity: `Test-NetConnection server:port`; check firewall rules |
| **Measures not visible** | Permissions | Check SSAS security; verify user has Read permission on cube |
| **Data doesn't update on filter** | Relationship missing | Create relationships between dimensions; verify Month linked to facts |
| **Report loads slowly** | Too many rows in data | Limit dataset to last 12 months + Finance; consider DirectQuery for Prod |
| **Refresh fails** | Credentials expired | Update credentials in Power BI Service; re-enter SSAS password |
| **Colors not matching** | Hex code mismatch | Verify hex codes: Dark Blue #1F4E79 (not 1F4E78), Gray #555555 |
| **Table rows missing** | Filter applied | Check filters; ensure Last 12 Months and Finance filters inclusive |

---

**Guide Version**: 1.0.0  
**Created**: 2026-02-20  
**Last Updated**: 2026-02-20  
**Status**: READY FOR IMPLEMENTATION
