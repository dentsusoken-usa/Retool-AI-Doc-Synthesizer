# Royalty Calculation App Documentation

## Summary
The Royalty Calculation app is a Retool-based financial management tool designed to track sales, calculate royalty adjustments, manage Minimum Guarantee (MG) balances, and generate monthly royalty reports. It provides a workflow for closing monthly royalty periods and managing contract transfers between licensors.

## Main Purpose and Workflow
The application serves as a centralized interface for:
1. **Sales Management:** Viewing, creating, and updating sales records.
2. **Royalty Calculation:** Calculating royalties based on sales and adjustments, including tracking MG balances.
3. **Monthly Closing:** Finalizing monthly royalty data and locking periods to prevent further modifications.
4. **Reporting:** Generating Excel-based royalty reports for specific licensors and contracts.

**Major Data Flows:**
- **Input:** Users provide date ranges and select filters (Licensor, Game Title, GL Account) via UI widgets.
- **Processing:** Queries fetch data from the `NISA_mysql_connection`. JavaScript logic (e.g., `calculateMGBalance`, `exportReport`) processes this data to compute balances and format Excel files.
- **Output:** The app displays data in tables and allows users to export reports or update records in the database.

## Technical Components

### Key SQL Queries
- `get_all_items`: Retrieves transaction data for the selected date range.
- `calc_current_mg_balance`: A complex query using `UNION` to calculate MG balances by comparing `v_all_transactions` and `v_all_royalty_adjustment` against contract terms.
- `create_changed_records` / `create_open_original_records`: Used to generate billing records based on whether the month is closed or open.
- `insert_monthly_royalty`: Performs a bulk insert into the `monthly_royalty` table.

### JavaScript Logic
- `calculateMGBalance`: Orchestrates the calculation of MG balances by triggering multiple sub-queries (`get_royalty_due_from_closed_month`, `get_royalty_due_from_open_month`, etc.) and aggregating the results.
- `exportReport`: Uses the `ExcelJS` library to generate and download multi-sheet Excel reports. It iterates through months, fetches data, applies formatting (borders, number formats), and triggers a file download.
- `transfer_licensors`: A recursive function that handles the transfer of contracts between licensors by updating the `active_contract` table and inserting new records into the `contract` table.

### Key Widgets
- `tabbedContainer1`: The primary navigation component separating the app into functional areas (Sales, Royalty Calculation, Adjustment, Billing, Report, Close Month).
- `royalty_table`: Displays transaction data with conditional row coloring based on unit price changes.
- `delete_modal`: A safety-gated modal for deleting records, which checks if a period is closed before allowing deletion.

## Inferences
*   **Data Integrity:** It is inferred that the `version_id` column in various tables (e.g., `royalty_adjustment`, `sales`) is used for optimistic locking or audit history, as the app frequently increments this value during updates.
*   **Database Schema:** Based on the queries, the database appears to rely on views (e.g., `v_all_transactions`, `v_all_royalty_adjustment`) to abstract complex joins between `licensor`, `contract`, `game_title`, and `sales` tables.

## Appendix: Inventory

### Major Queries
| Query Name | Responsibility |
| :--- | :--- |
| `get_all_items` | Fetches primary transaction data for the main table. |
| `calc_current_mg_balance` | Calculates MG balances for contracts. |
| `insert_monthly_royalty` | Persists calculated royalty data to the database. |
| `get_sales` | Retrieves sales data for the Sales tab. |
| `update_royalty_adjustment` | Updates existing adjustment records. |

### JavaScript Logic Blocks
| Block Name | Role |
| :--- | :--- |
| `calculateMGBalance` | Aggregates royalty and adjustment data to compute MG status. |
| `exportReport` | Generates and downloads Excel reports using `ExcelJS`. |
| `transfer_licensors` | Manages contract migration between licensors. |
| `delete_record_transform` | Validates and executes record deletion. |

### Important Widgets
| Widget Name | Interaction |
| :--- | :--- |
| `tabbedContainer1` | Main navigation between functional modules. |
| `royalty_table` | Main data display; supports row selection and editing. |
| `delete_modal` | Safety gate for record deletion. |
| `start_date` / `end_date` | Global date filters for data retrieval. |

## Risks and Open Questions
*   **Performance:** The `calc_current_mg_balance` query is highly complex with multiple subqueries. As the dataset grows, this may lead to timeouts or performance degradation.
*   **Data Consistency:** The app relies on `isClosedMonthStatus` to determine logic paths. If the status in `monthly_royalty_status` is not updated correctly, the calculation logic may produce incorrect results.
*   **Dependency:** The `exportReport` function relies on an external library (`ExcelJS`). If the CDN link is broken or the library API changes, report generation will fail.
*   **Hardcoded Logic:** Several queries contain hardcoded logic (e.g., `systemStartDate = '2022-07-01'`), which may require manual updates in the future.