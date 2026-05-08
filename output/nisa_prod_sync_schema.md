# NISA Production Sync Database Schema

Schema definition for the NISA production synchronization database.

## Schema Overview

- Database: `nisa_prod_sync`
- Tables documented: 25
- Relationships documented: 27

## ERD

```mermaid
erDiagram
    account {
        INT account_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR account_name
        VARCHAR type
        VARCHAR currency
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    account_history {
        INT account_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR account_name
        VARCHAR type
        VARCHAR currency
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    child_item {
        INT child_item_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR child_item_code
        VARCHAR child_item_name
        INT parent_item_id FK
        VARCHAR royalty_type
        DECIMAL royalty_per_unit
        DECIMAL royalty_percentage
        DECIMAL unit_price
        DECIMAL msrp
        INT sales_account_id FK
        VARCHAR game_type
        INT platform_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    child_item_history {
        INT child_item_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR child_item_code
        VARCHAR child_item_name
        INT parent_item_id FK
        VARCHAR royalty_type
        DECIMAL royalty_per_unit
        DECIMAL royalty_percentage
        DECIMAL unit_price
        DECIMAL msrp
        INT sales_account_id FK
        VARCHAR game_type
        INT platform_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    contract {
        INT contract_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR contract_name
        DECIMAL mg_beginning_balance
        DECIMAL pp_beginning_balance
        DECIMAL mg_original_paid
        INT licensor_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    contract_history {
        INT contract_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR contract_name
        DECIMAL mg_beginning_balance
        DECIMAL pp_beginning_balance
        DECIMAL mg_original_paid
        INT licensor_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    division {
        INT division_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR division_name
        INT debit_account_id FK
        INT credit_account_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    division_history {
        INT division_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR division_name
        INT debit_account_id FK
        INT credit_account_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    game_title {
        INT game_title_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR game_title
        DATE release_date
        INT contract_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    game_title_history {
        INT game_title_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR game_title
        DATE release_date
        INT contract_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    journal_entry_template {
        INT template_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR template_name
        INT debit_account_id FK
        INT credit_account_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    journal_entry_template_history {
        INT template_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR template_name
        INT debit_account_id FK
        INT credit_account_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    licensor {
        INT licensor_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR licensor_name
        VARCHAR mg_balance_calculation_type
        VARCHAR royalty_calculation_type
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    licensor_history {
        INT licensor_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR licensor_name
        VARCHAR mg_balance_calculation_type
        VARCHAR royalty_calculation_type
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    monthly_royalty {
        INT licensor_id
        DATE licensor_effective_start_date
        DATE licensor_effective_end_date
        INT licensor_version_id
        VARCHAR licensor_name
        VARCHAR mg_balance_calculation_type
        VARCHAR royalty_calculation_type
        INT contract_id
        DATE contract_effective_start_date
        DATE contract_effective_end_date
        INT contract_version_id
        VARCHAR contract_name
        DECIMAL mg_beginning_balance
        DECIMAL pp_beginning_balance
        DECIMAL mg_original_paid
        INT game_title_id
        DATE game_title_effective_start_date
        DATE game_title_effective_end_date
        INT game_title_version_id
        VARCHAR game_title
        DATE release_date
        INT parent_item_id
        DATE parent_item_effective_start_date
        DATE parent_item_effective_end_date
        INT parent_item_version_id
        VARCHAR parent_item_code
        VARCHAR parent_item_name
        VARCHAR parent_item_type
        INT division_id
        DATE division_effective_start_date
        DATE division_effective_end_date
        INT division_version_id
        VARCHAR division_name
        INT debit_account_id
        DATE debit_account_effective_start_date
        DATE debit_account_effective_end_date
        INT debit_account_version_id
        VARCHAR debit_account_name
        VARCHAR debit_account_type
        INT credit_account_id
        DATE credit_account_effective_start_date
        DATE credit_account_effective_end_date
        INT credit_account_version_id
        VARCHAR credit_account_name
        VARCHAR credit_account_type
        INT child_item_id PK
        DATE child_item_effective_start_date
        DATE child_item_effective_end_date
        INT child_item_version_id
        VARCHAR child_item_code
        VARCHAR child_item_name
        VARCHAR royalty_type
        DECIMAL royalty_per_unit
        DECIMAL royalty_percentage
        DECIMAL unit_price
        DECIMAL msrp
        INT sales_account_id
        DATE sales_account_effective_start_date
        DATE sales_account_effective_end_date
        INT sales_account_version_id
        VARCHAR sales_account_name
        VARCHAR sales_account_type
        VARCHAR game_type
        INT platform_id
        DATE platform_effective_start_date
        DATE platform_effective_end_date
        INT platform_version_id
        VARCHAR platform_code
        VARCHAR platform_name
        DATE order_date PK
        INT sales_version_id PK
        INT sold_quantity
        DECIMAL sales
        INT manufactured_quantity
        DECIMAL discount
        DECIMAL royalty_due
    }
    monthly_royalty_status {
        INT status_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        TINYINT status
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    monthly_royalty_status_history {
        INT status_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        TINYINT status
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    parent_item {
        INT parent_item_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR parent_item_code
        VARCHAR parent_item_name
        VARCHAR parent_item_type
        INT division_id FK
        INT game_title_id FK
        INT journal_entry_template_id FK
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    parent_item_history {
        INT parent_item_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR parent_item_code
        VARCHAR parent_item_name
        VARCHAR parent_item_type
        INT division_id FK
        INT game_title_id FK
        INT journal_entry_template_id
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    platform {
        INT platform_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR platform_code
        VARCHAR platform_name
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    platform_history {
        INT platform_id PK
        DATE effective_start_date PK
        DATE effective_end_date PK
        INT version_id PK
        VARCHAR platform_code
        VARCHAR platform_name
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    royalty_adjustment {
        INT child_item_id PK FK
        DATE adjustment_date PK
        INT version_id PK
        DECIMAL royalty_adjustment
        VARCHAR adjustment_note
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    royalty_adjustment_history {
        INT child_item_id PK FK
        DATE adjustment_date PK
        INT version_id PK
        DECIMAL royalty_adjustment
        VARCHAR adjustment_note
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    sales {
        INT child_item_id PK FK
        DATE order_date PK
        INT version_id PK
        INT sold_quantity
        DECIMAL sales
        INT manufactured_quantity
        DECIMAL discount
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    sales_history {
        INT child_item_id PK FK
        DATE order_date PK
        INT version_id PK
        INT sold_quantity
        DECIMAL sales
        INT manufactured_quantity
        DECIMAL discount
        TIMESTAMP created_timestamp
        VARCHAR created_by
        TIMESTAMP updated_timestamp
        VARCHAR updated_by
    }
    parent_item ||--o{ child_item : "parent_item_id -> parent_item_id"
    account ||--o{ child_item : "sales_account_id -> account_id"
    platform ||--o{ child_item : "platform_id -> platform_id"
    parent_item ||--o{ child_item_history : "parent_item_id -> parent_item_id"
    account ||--o{ child_item_history : "sales_account_id -> account_id"
    platform ||--o{ child_item_history : "platform_id -> platform_id"
    licensor ||--o{ contract : "licensor_id -> licensor_id"
    licensor ||--o{ contract_history : "licensor_id -> licensor_id"
    account ||--o{ division : "debit_account_id -> account_id"
    account ||--o{ division : "credit_account_id -> account_id"
    account ||--o{ division_history : "debit_account_id -> account_id"
    account ||--o{ division_history : "credit_account_id -> account_id"
    contract ||--o{ game_title : "contract_id -> contract_id"
    contract ||--o{ game_title_history : "contract_id -> contract_id"
    account ||--o{ journal_entry_template : "debit_account_id -> account_id"
    account ||--o{ journal_entry_template : "credit_account_id -> account_id"
    account ||--o{ journal_entry_template_history : "debit_account_id -> account_id"
    account ||--o{ journal_entry_template_history : "credit_account_id -> account_id"
    game_title ||--o{ parent_item : "game_title_id -> game_title_id"
    division ||--o{ parent_item : "division_id -> division_id"
    journal_entry_template ||--o{ parent_item : "journal_entry_template_id -> template_id"
    game_title ||--o{ parent_item_history : "game_title_id -> game_title_id"
    division ||--o{ parent_item_history : "division_id -> division_id"
    child_item ||--o{ royalty_adjustment : "child_item_id -> child_item_id"
    child_item ||--o{ royalty_adjustment_history : "child_item_id -> child_item_id"
    child_item ||--o{ sales : "child_item_id -> child_item_id"
    child_item ||--o{ sales_history : "child_item_id -> child_item_id"
```

## account

**Logical Name:** Account

Stores information about accounts.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | account_id | Account ID | INT | 10 | Y |  | Y |  | Unique identifier for the account. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | account_name | Account Name | VARCHAR | 300 | N |  | N |  | The name of the account. |
| 6 | type | Account Type | VARCHAR | 100 | N |  | N |  | The type of the account (e.g., 'Customer', 'Vendor'). |
| 7 | currency | Currency | VARCHAR | 100 | N |  | N |  | The currency associated with the account. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## account_history

**Logical Name:** Account History

Stores historical versions of account information.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | account_id | Account ID | INT | 10 | Y |  | Y |  | Unique identifier for the account. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | account_name | Account Name | VARCHAR | 300 | N |  | N |  | The name of the account. |
| 6 | type | Account Type | VARCHAR | 100 | N |  | N |  | The type of the account (e.g., 'Customer', 'Vendor'). |
| 7 | currency | Currency | VARCHAR | 100 | N |  | N |  | The currency associated with the account. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## child_item

**Logical Name:** Child Item

Represents individual items or SKUs that are part of a larger parent item.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y |  | Y |  | Unique identifier for the child item. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | child_item_code | Child Item Code | VARCHAR | 100 | N |  | Y |  | Unique code for the child item. |
| 6 | child_item_name | Child Item Name | VARCHAR | 300 | N |  | Y |  | Name of the child item. |
| 7 | parent_item_id | Parent Item ID | INT | 10 | N | parent_item.parent_item_id | Y |  | Foreign key referencing the parent item. |
| 8 | royalty_type | Royalty Type | VARCHAR | 100 | N |  | Y |  | Type of royalty calculation (e.g., 'Percentage', 'Per Unit'). |
| 9 | royalty_per_unit | Royalty Per Unit | DECIMAL | 15,3 | N |  | N |  | The royalty amount per unit sold. |
| 10 | royalty_percentage | Royalty Percentage | DECIMAL | 15,5 | N |  | N |  | The royalty percentage applied to sales. |
| 11 | unit_price | Unit Price | DECIMAL | 15,3 | N |  | N |  | The price of a single unit of the child item. |
| 12 | msrp | MSRP | DECIMAL | 15,3 | N |  | N |  | Manufacturer's Suggested Retail Price. |
| 13 | sales_account_id | Sales Account ID | INT | 10 | N | account.account_id | Y |  | Foreign key referencing the account responsible for sales. |
| 14 | game_type | Game Type | VARCHAR | 100 | N |  | Y |  | The type of game this item belongs to. |
| 15 | platform_id | Platform ID | INT | 10 | N | platform.platform_id | Y |  | Foreign key referencing the platform this item is for. |
| 16 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 17 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 18 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 19 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## child_item_history

**Logical Name:** Child Item History

Stores historical versions of child item information.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y |  | Y |  | Unique identifier for the child item. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | child_item_code | Child Item Code | VARCHAR | 100 | N |  | Y |  | Unique code for the child item. |
| 6 | child_item_name | Child Item Name | VARCHAR | 300 | N |  | Y |  | Name of the child item. |
| 7 | parent_item_id | Parent Item ID | INT | 10 | N | parent_item.parent_item_id | Y |  | Foreign key referencing the parent item. |
| 8 | royalty_type | Royalty Type | VARCHAR | 100 | N |  | Y |  | Type of royalty calculation (e.g., 'Percentage', 'Per Unit'). |
| 9 | royalty_per_unit | Royalty Per Unit | DECIMAL | 15,3 | N |  | N |  | The royalty amount per unit sold. |
| 10 | royalty_percentage | Royalty Percentage | DECIMAL | 15,5 | N |  | N |  | The royalty percentage applied to sales. |
| 11 | unit_price | Unit Price | DECIMAL | 15,3 | N |  | N |  | The price of a single unit of the child item. |
| 12 | msrp | MSRP | DECIMAL | 15,3 | N |  | N |  | Manufacturer's Suggested Retail Price. |
| 13 | sales_account_id | Sales Account ID | INT | 10 | N | account.account_id | Y |  | Foreign key referencing the account responsible for sales. |
| 14 | game_type | Game Type | VARCHAR | 100 | N |  | Y |  | The type of game this item belongs to. |
| 15 | platform_id | Platform ID | INT | 10 | N | platform.platform_id | Y |  | Foreign key referencing the platform this item is for. |
| 16 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 17 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 18 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 19 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## contract

**Logical Name:** Contract

Stores information about contracts with licensors.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | contract_id | Contract ID | INT | 10 | Y |  | Y |  | Unique identifier for the contract. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | contract_name | Contract Name | VARCHAR | 300 | N |  | Y |  | The name of the contract. |
| 6 | mg_beginning_balance | MG Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | Minimum Guarantee beginning balance for the contract. |
| 7 | pp_beginning_balance | PP Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | Per-Product beginning balance for the contract. |
| 8 | mg_original_paid | MG Original Paid | DECIMAL | 15,3 | N |  | Y |  | Original amount paid for the Minimum Guarantee. |
| 9 | licensor_id | Licensor ID | INT | 10 | N | licensor.licensor_id | Y |  | Foreign key referencing the licensor. |
| 10 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 11 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 12 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 13 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## contract_history

**Logical Name:** Contract History

Stores historical versions of contract information.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | contract_id | Contract ID | INT | 10 | Y |  | Y |  | Unique identifier for the contract. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | contract_name | Contract Name | VARCHAR | 300 | N |  | Y |  | The name of the contract. |
| 6 | mg_beginning_balance | MG Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | Minimum Guarantee beginning balance for the contract. |
| 7 | pp_beginning_balance | PP Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | Per-Product beginning balance for the contract. |
| 8 | mg_original_paid | MG Original Paid | DECIMAL | 15,3 | N |  | Y |  | Original amount paid for the Minimum Guarantee. |
| 9 | licensor_id | Licensor ID | INT | 10 | N | licensor.licensor_id | Y |  | Foreign key referencing the licensor. |
| 10 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 11 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 12 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 13 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## division

**Logical Name:** Division

Represents business divisions within the company.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | division_id | Division ID | INT | 10 | Y |  | Y |  | Unique identifier for the division. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | division_name | Division Name | VARCHAR | 100 | N |  | N |  | The name of the division. |
| 6 | debit_account_id | Debit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default debit account for the division. |
| 7 | credit_account_id | Credit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default credit account for the division. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## division_history

**Logical Name:** Division History

Stores historical versions of division information.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | division_id | Division ID | INT | 10 | Y |  | Y |  | Unique identifier for the division. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | division_name | Division Name | VARCHAR | 100 | N |  | N |  | The name of the division. |
| 6 | debit_account_id | Debit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default debit account for the division. |
| 7 | credit_account_id | Credit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default credit account for the division. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## game_title

**Logical Name:** Game Title

Stores information about game titles.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | game_title_id | Game Title ID | INT | 10 | Y |  | Y |  | Unique identifier for the game title. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | game_title | Game Title | VARCHAR | 300 | N |  | Y |  | The name of the game title. |
| 6 | release_date | Release Date | DATE |  | N |  | N |  | The release date of the game title. |
| 7 | contract_id | Contract ID | INT | 10 | N | contract.contract_id | Y |  | Foreign key referencing the contract associated with this game title. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## game_title_history

**Logical Name:** Game Title History

Stores historical versions of game title information.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | game_title_id | Game Title ID | INT | 10 | Y |  | Y |  | Unique identifier for the game title. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | game_title | Game Title | VARCHAR | 300 | N |  | Y |  | The name of the game title. |
| 6 | release_date | Release Date | DATE |  | N |  | N |  | The release date of the game title. |
| 7 | contract_id | Contract ID | INT | 10 | N | contract.contract_id | Y |  | Foreign key referencing the contract associated with this game title. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## journal_entry_template

**Logical Name:** Journal Entry Template

Defines templates for generating journal entries.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | template_id | Template ID | INT | 10 | Y |  | Y |  | Unique identifier for the journal entry template. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | template_name | Template Name | VARCHAR | 300 | N |  | Y |  | The name of the journal entry template. |
| 6 | debit_account_id | Debit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default debit account for this template. |
| 7 | credit_account_id | Credit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default credit account for this template. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## journal_entry_template_history

**Logical Name:** Journal Entry Template History

Stores historical versions of journal entry template information.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | template_id | Template ID | INT | 10 | Y |  | Y |  | Unique identifier for the journal entry template. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | template_name | Template Name | VARCHAR | 300 | N |  | Y |  | The name of the journal entry template. |
| 6 | debit_account_id | Debit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default debit account for this template. |
| 7 | credit_account_id | Credit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default credit account for this template. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## licensor

**Logical Name:** Licensor

Stores information about licensors.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | licensor_id | Licensor ID | INT | 10 | Y |  | Y |  | Unique identifier for the licensor. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | licensor_name | Licensor Name | VARCHAR | 300 | N |  | Y |  | The name of the licensor. |
| 6 | mg_balance_calculation_type | MG Balance Calculation Type | VARCHAR | 100 | N |  | Y |  | Specifies how the Minimum Guarantee balance is calculated. |
| 7 | royalty_calculation_type | Royalty Calculation Type | VARCHAR | 100 | N |  | Y |  | Specifies the method for calculating royalties. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## licensor_history

**Logical Name:** Licensor History

Stores historical versions of licensor information.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | licensor_id | Licensor ID | INT | 10 | Y |  | Y |  | Unique identifier for the licensor. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | licensor_name | Licensor Name | VARCHAR | 300 | N |  | Y |  | The name of the licensor. |
| 6 | mg_balance_calculation_type | MG Balance Calculation Type | VARCHAR | 100 | N |  | Y |  | Specifies how the Minimum Guarantee balance is calculated. |
| 7 | royalty_calculation_type | Royalty Calculation Type | VARCHAR | 100 | N |  | Y |  | Specifies the method for calculating royalties. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## monthly_royalty

**Logical Name:** Monthly Royalty

Aggregated monthly royalty data, linking various entities.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | licensor_id | Licensor ID | INT | 10 | N |  | Y |  | Identifier for the licensor. |
| 2 | licensor_effective_start_date | Licensor Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the licensor record at the time of aggregation. |
| 3 | licensor_effective_end_date | Licensor Effective End Date | DATE |  | N |  | Y |  | The effective end date of the licensor record at the time of aggregation. |
| 4 | licensor_version_id | Licensor Version ID | INT | 10 | N |  | Y |  | The version ID of the licensor record at the time of aggregation. |
| 5 | licensor_name | Licensor Name | VARCHAR | 300 | N |  | Y |  | Name of the licensor. |
| 6 | mg_balance_calculation_type | MG Balance Calculation Type | VARCHAR | 100 | N |  | Y |  | Type of calculation for Minimum Guarantee balance. |
| 7 | royalty_calculation_type | Royalty Calculation Type | VARCHAR | 100 | N |  | Y |  | Type of calculation for royalties. |
| 8 | contract_id | Contract ID | INT | 10 | N |  | Y |  | Identifier for the contract. |
| 9 | contract_effective_start_date | Contract Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the contract record at the time of aggregation. |
| 10 | contract_effective_end_date | Contract Effective End Date | DATE |  | N |  | Y |  | The effective end date of the contract record at the time of aggregation. |
| 11 | contract_version_id | Contract Version ID | INT | 10 | N |  | Y |  | The version ID of the contract record at the time of aggregation. |
| 12 | contract_name | Contract Name | VARCHAR | 300 | N |  | Y |  | Name of the contract. |
| 13 | mg_beginning_balance | MG Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | Minimum Guarantee beginning balance for the contract. |
| 14 | pp_beginning_balance | PP Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | Per-Product beginning balance for the contract. |
| 15 | mg_original_paid | MG Original Paid | DECIMAL | 15,3 | N |  | Y |  | Original amount paid for the Minimum Guarantee. |
| 16 | game_title_id | Game Title ID | INT | 10 | N |  | Y |  | Identifier for the game title. |
| 17 | game_title_effective_start_date | Game Title Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the game title record at the time of aggregation. |
| 18 | game_title_effective_end_date | Game Title Effective End Date | DATE |  | N |  | Y |  | The effective end date of the game title record at the time of aggregation. |
| 19 | game_title_version_id | Game Title Version ID | INT | 10 | N |  | Y |  | The version ID of the game title record at the time of aggregation. |
| 20 | game_title | Game Title | VARCHAR | 300 | N |  | Y |  | Name of the game title. |
| 21 | release_date | Release Date | DATE |  | N |  | N |  | Release date of the game title. |
| 22 | parent_item_id | Parent Item ID | INT | 10 | N |  | Y |  | Identifier for the parent item. |
| 23 | parent_item_effective_start_date | Parent Item Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the parent item record at the time of aggregation. |
| 24 | parent_item_effective_end_date | Parent Item Effective End Date | DATE |  | N |  | Y |  | The effective end date of the parent item record at the time of aggregation. |
| 25 | parent_item_version_id | Parent Item Version ID | INT | 10 | N |  | Y |  | The version ID of the parent item record at the time of aggregation. |
| 26 | parent_item_code | Parent Item Code | VARCHAR | 100 | N |  | Y |  | Code of the parent item. |
| 27 | parent_item_name | Parent Item Name | VARCHAR | 300 | N |  | Y |  | Name of the parent item. |
| 28 | parent_item_type | Parent Item Type | VARCHAR | 100 | N |  | Y |  | Type of the parent item. |
| 29 | division_id | Division ID | INT | 10 | N |  | Y |  | Identifier for the division. |
| 30 | division_effective_start_date | Division Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the division record at the time of aggregation. |
| 31 | division_effective_end_date | Division Effective End Date | DATE |  | N |  | Y |  | The effective end date of the division record at the time of aggregation. |
| 32 | division_version_id | Division Version ID | INT | 10 | N |  | Y |  | The version ID of the division record at the time of aggregation. |
| 33 | division_name | Division Name | VARCHAR | 100 | N |  | N |  | Name of the division. |
| 34 | debit_account_id | Debit Account ID | INT | 10 | N |  | N |  | Identifier for the debit account. |
| 35 | debit_account_effective_start_date | Debit Account Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the debit account record at the time of aggregation. |
| 36 | debit_account_effective_end_date | Debit Account Effective End Date | DATE |  | N |  | Y |  | The effective end date of the debit account record at the time of aggregation. |
| 37 | debit_account_version_id | Debit Account Version ID | INT | 10 | N |  | Y |  | The version ID of the debit account record at the time of aggregation. |
| 38 | debit_account_name | Debit Account Name | VARCHAR | 300 | N |  | N |  | Name of the debit account. |
| 39 | debit_account_type | Debit Account Type | VARCHAR | 100 | N |  | N |  | Type of the debit account. |
| 40 | credit_account_id | Credit Account ID | INT | 10 | N |  | N |  | Identifier for the credit account. |
| 41 | credit_account_effective_start_date | Credit Account Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the credit account record at the time of aggregation. |
| 42 | credit_account_effective_end_date | Credit Account Effective End Date | DATE |  | N |  | Y |  | The effective end date of the credit account record at the time of aggregation. |
| 43 | credit_account_version_id | Credit Account Version ID | INT | 10 | N |  | Y |  | The version ID of the credit account record at the time of aggregation. |
| 44 | credit_account_name | Credit Account Name | VARCHAR | 300 | N |  | N |  | Name of the credit account. |
| 45 | credit_account_type | Credit Account Type | VARCHAR | 100 | N |  | N |  | Type of the credit account. |
| 46 | child_item_id | Child Item ID | INT | 10 | Y |  | Y |  | Identifier for the child item. |
| 47 | child_item_effective_start_date | Child Item Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the child item record at the time of aggregation. |
| 48 | child_item_effective_end_date | Child Item Effective End Date | DATE |  | N |  | Y |  | The effective end date of the child item record at the time of aggregation. |
| 49 | child_item_version_id | Child Item Version ID | INT | 10 | N |  | Y |  | The version ID of the child item record at the time of aggregation. |
| 50 | child_item_code | Child Item Code | VARCHAR | 100 | N |  | Y |  | Code of the child item. |
| 51 | child_item_name | Child Item Name | VARCHAR | 300 | N |  | Y |  | Name of the child item. |
| 52 | royalty_type | Royalty Type | VARCHAR | 100 | N |  | Y |  | Type of royalty calculation. |
| 53 | royalty_per_unit | Royalty Per Unit | DECIMAL | 15,3 | N |  | N |  | Royalty amount per unit. |
| 54 | royalty_percentage | Royalty Percentage | DECIMAL | 15,3 | N |  | N |  | Royalty percentage. |
| 55 | unit_price | Unit Price | DECIMAL | 15,3 | N |  | N |  | Price per unit. |
| 56 | msrp | MSRP | DECIMAL | 15,3 | N |  | N |  | Manufacturer's Suggested Retail Price. |
| 57 | sales_account_id | Sales Account ID | INT | 10 | N |  | Y |  | Identifier for the sales account. |
| 58 | sales_account_effective_start_date | Sales Account Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the sales account record at the time of aggregation. |
| 59 | sales_account_effective_end_date | Sales Account Effective End Date | DATE |  | N |  | Y |  | The effective end date of the sales account record at the time of aggregation. |
| 60 | sales_account_version_id | Sales Account Version ID | INT | 10 | N |  | Y |  | The version ID of the sales account record at the time of aggregation. |
| 61 | sales_account_name | Sales Account Name | VARCHAR | 300 | N |  | N |  | Name of the sales account. |
| 62 | sales_account_type | Sales Account Type | VARCHAR | 100 | N |  | N |  | Type of the sales account. |
| 63 | game_type | Game Type | VARCHAR | 100 | N |  | Y |  | Type of the game. |
| 64 | platform_id | Platform ID | INT | 10 | N |  | Y |  | Identifier for the platform. |
| 65 | platform_effective_start_date | Platform Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the platform record at the time of aggregation. |
| 66 | platform_effective_end_date | Platform Effective End Date | DATE |  | N |  | Y |  | The effective end date of the platform record at the time of aggregation. |
| 67 | platform_version_id | Platform Version ID | INT | 10 | N |  | Y |  | The version ID of the platform record at the time of aggregation. |
| 68 | platform_code | Platform Code | VARCHAR | 100 | N |  | Y |  | Code of the platform. |
| 69 | platform_name | Platform Name | VARCHAR | 100 | N |  | Y |  | Name of the platform. |
| 70 | order_date | Order Date | DATE |  | Y |  | Y |  | The date of the order. |
| 71 | sales_version_id | Sales Version ID | INT | 10 | Y |  | Y |  | The version ID of the sales record at the time of aggregation. |
| 72 | sold_quantity | Sold Quantity | INT | 10 | N |  | Y |  | Quantity of items sold. |
| 73 | sales | Sales | DECIMAL | 15,3 | N |  | Y |  | Total sales amount. |
| 74 | manufactured_quantity | Manufactured Quantity | INT | 10 | N |  | N |  | Quantity of items manufactured. |
| 75 | discount | Discount | DECIMAL | 15,3 | N |  | Y |  | Discount applied to the sales. |
| 76 | royalty_due | Royalty Due | DECIMAL | 15,3 | N |  | N |  | The calculated royalty amount due. |

## monthly_royalty_status

**Logical Name:** Monthly Royalty Status

Tracks the status of monthly royalty calculations.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | status_id | Status ID | INT | 10 | Y |  | Y |  | Unique identifier for the status record. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | status | Status | TINYINT | 3 | N |  | N |  | The status code (e.g., 0 for pending, 1 for processed). |
| 6 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 7 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 8 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 9 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## monthly_royalty_status_history

**Logical Name:** Monthly Royalty Status History

Stores historical versions of monthly royalty status.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | status_id | Status ID | INT | 10 | Y |  | Y |  | Unique identifier for the status record. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | status | Status | TINYINT | 3 | N |  | N |  | The status code (e.g., 0 for pending, 1 for processed). |
| 6 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 7 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 8 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 9 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## parent_item

**Logical Name:** Parent Item

Represents a collection or bundle of child items.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | parent_item_id | Parent Item ID | INT | 10 | Y |  | Y |  | Unique identifier for the parent item. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | parent_item_code | Parent Item Code | VARCHAR | 100 | N |  | Y |  | Unique code for the parent item. |
| 6 | parent_item_name | Parent Item Name | VARCHAR | 300 | N |  | Y |  | Name of the parent item. |
| 7 | parent_item_type | Parent Item Type | VARCHAR | 100 | N |  | Y |  | Type of the parent item (e.g., 'Bundle', 'Collection'). |
| 8 | division_id | Division ID | INT | 10 | N | division.division_id | Y |  | Foreign key referencing the division this parent item belongs to. |
| 9 | game_title_id | Game Title ID | INT | 10 | N | game_title.game_title_id | Y |  | Foreign key referencing the game title associated with this parent item. |
| 10 | journal_entry_template_id | Journal Entry Template ID | INT | 10 | N | journal_entry_template.template_id | Y |  | Foreign key referencing the journal entry template used for this parent item. |
| 11 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 12 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 13 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 14 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## parent_item_history

**Logical Name:** Parent Item History

Stores historical versions of parent item information.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | parent_item_id | Parent Item ID | INT | 10 | Y |  | Y |  | Unique identifier for the parent item. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | parent_item_code | Parent Item Code | VARCHAR | 100 | N |  | Y |  | Unique code for the parent item. |
| 6 | parent_item_name | Parent Item Name | VARCHAR | 300 | N |  | Y |  | Name of the parent item. |
| 7 | parent_item_type | Parent Item Type | VARCHAR | 100 | N |  | Y |  | Type of the parent item (e.g., 'Bundle', 'Collection'). |
| 8 | division_id | Division ID | INT | 10 | N | division.division_id | Y |  | Foreign key referencing the division this parent item belongs to. |
| 9 | game_title_id | Game Title ID | INT | 10 | N | game_title.game_title_id | Y |  | Foreign key referencing the game title associated with this parent item. |
| 10 | journal_entry_template_id | Journal Entry Template ID | INT | 10 | N |  | Y |  | Foreign key referencing the journal entry template used for this parent item. |
| 11 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 12 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 13 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 14 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## platform

**Logical Name:** Platform

Stores information about gaming platforms.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | platform_id | Platform ID | INT | 10 | Y |  | Y |  | Unique identifier for the platform. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | platform_code | Platform Code | VARCHAR | 100 | N |  | Y |  | Unique code for the platform. |
| 6 | platform_name | Platform Name | VARCHAR | 100 | N |  | Y |  | The name of the platform. |
| 7 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 8 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 9 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 10 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## platform_history

**Logical Name:** Platform History

Stores historical versions of platform information.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | platform_id | Platform ID | INT | 10 | Y |  | Y |  | Unique identifier for the platform. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this historical record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this historical record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 5 | platform_code | Platform Code | VARCHAR | 100 | N |  | Y |  | Unique code for the platform. |
| 6 | platform_name | Platform Name | VARCHAR | 100 | N |  | Y |  | The name of the platform. |
| 7 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 8 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 9 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 10 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## royalty_adjustment

**Logical Name:** Royalty Adjustment

Records adjustments made to royalties for a specific child item on a given date.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y | child_item.child_item_id | Y |  | Foreign key referencing the child item to which the adjustment applies. |
| 2 | adjustment_date | Adjustment Date | DATE |  | Y |  | Y |  | The date on which the royalty adjustment was made. |
| 3 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 4 | royalty_adjustment | Royalty Adjustment | DECIMAL | 15,3 | N |  | Y |  | The amount of the royalty adjustment. Can be positive or negative. |
| 5 | adjustment_note | Adjustment Note | VARCHAR | 500 | N |  | N |  | A note explaining the reason for the royalty adjustment. |
| 6 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 7 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 8 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 9 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## royalty_adjustment_history

**Logical Name:** Royalty Adjustment History

Stores historical versions of royalty adjustments.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y | child_item.child_item_id | Y |  | Foreign key referencing the child item to which the adjustment applies. |
| 2 | adjustment_date | Adjustment Date | DATE |  | Y |  | Y |  | The date on which the royalty adjustment was made. |
| 3 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the record. |
| 4 | royalty_adjustment | Royalty Adjustment | DECIMAL | 15,3 | N |  | Y |  | The amount of the royalty adjustment. Can be positive or negative. |
| 5 | adjustment_note | Adjustment Note | VARCHAR | 500 | N |  | N |  | A note explaining the reason for the royalty adjustment. |
| 6 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 7 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 8 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 9 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## sales

**Logical Name:** Sales

Records individual sales transactions for child items.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y | child_item.child_item_id | Y |  | Foreign key referencing the child item sold. |
| 2 | order_date | Order Date | DATE |  | Y |  | Y |  | The date the order was placed. |
| 3 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the sales record. |
| 4 | sold_quantity | Sold Quantity | INT | 10 | N |  | Y |  | The number of units sold in this transaction. |
| 5 | sales | Sales | DECIMAL | 15,3 | N |  | Y |  | The total sales amount for this transaction. |
| 6 | manufactured_quantity | Manufactured Quantity | INT | 10 | N |  | N |  | The quantity manufactured for this sale, if applicable. |
| 7 | discount | Discount | DECIMAL | 15,3 | N |  | Y |  | The discount applied to this sale. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |

## sales_history

**Logical Name:** Sales History

Stores historical versions of sales transactions.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y | child_item.child_item_id | Y |  | Foreign key referencing the child item sold. |
| 2 | order_date | Order Date | DATE |  | Y |  | Y |  | The date the order was placed. |
| 3 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the sales record. |
| 4 | sold_quantity | Sold Quantity | INT | 10 | N |  | Y |  | The number of units sold in this transaction. |
| 5 | sales | Sales | DECIMAL | 15,3 | N |  | Y |  | The total sales amount for this transaction. |
| 6 | manufactured_quantity | Manufactured Quantity | INT | 10 | N |  | N |  | The quantity manufactured for this sale, if applicable. |
| 7 | discount | Discount | DECIMAL | 15,3 | N |  | Y |  | The discount applied to this sale. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the record. |
