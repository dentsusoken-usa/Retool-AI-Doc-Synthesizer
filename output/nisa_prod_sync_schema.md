# NISA Production Sync Database Schema

Schema documentation for the NISA production sync database, detailing tables, columns, and their relationships.

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
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this account record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this account record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the account record. |
| 5 | account_name | Account Name | VARCHAR | 300 | N |  | N |  | The name of the account. |
| 6 | type | Account Type | VARCHAR | 100 | N |  | N |  | The type of the account (e.g., 'Revenue', 'Expense'). |
| 7 | currency | Currency | VARCHAR | 100 | N |  | N |  | The currency associated with the account. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the account record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the account record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the account record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the account record. |

## account_history

**Logical Name:** Account History

Stores historical versions of account records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | account_id | Account ID | INT | 10 | Y |  | Y |  | Unique identifier for the account. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this account record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this account record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the account record. |
| 5 | account_name | Account Name | VARCHAR | 300 | N |  | N |  | The name of the account. |
| 6 | type | Account Type | VARCHAR | 100 | N |  | N |  | The type of the account (e.g., 'Revenue', 'Expense'). |
| 7 | currency | Currency | VARCHAR | 100 | N |  | N |  | The currency associated with the account. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the account record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the account record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the account record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the account record. |

## child_item

**Logical Name:** Child Item

Represents individual items or SKUs that are part of a larger parent item.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y |  | Y |  | Unique identifier for the child item. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this child item record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this child item record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the child item record. |
| 5 | child_item_code | Child Item Code | VARCHAR | 100 | N |  | Y |  | Unique code for the child item. |
| 6 | child_item_name | Child Item Name | VARCHAR | 300 | N |  | Y |  | The name of the child item. |
| 7 | parent_item_id | Parent Item ID | INT | 10 | N | parent_item.parent_item_id | Y |  | Foreign key referencing the parent item this child item belongs to. |
| 8 | royalty_type | Royalty Type | VARCHAR | 100 | N |  | Y |  | The type of royalty calculation (e.g., 'Per Unit', 'Percentage'). |
| 9 | royalty_per_unit | Royalty Per Unit | DECIMAL | 15,3 | N |  | N |  | The royalty amount per unit sold. |
| 10 | royalty_percentage | Royalty Percentage | DECIMAL | 15,5 | N |  | N |  | The royalty percentage applied to sales. |
| 11 | unit_price | Unit Price | DECIMAL | 15,3 | N |  | N |  | The price of a single unit of the child item. |
| 12 | msrp | MSRP | DECIMAL | 15,3 | N |  | N |  | Manufacturer's Suggested Retail Price for the child item. |
| 13 | sales_account_id | Sales Account ID | INT | 10 | N | account.account_id | Y |  | Foreign key referencing the account associated with sales of this child item. |
| 14 | game_type | Game Type | VARCHAR | 100 | N |  | Y |  | The type of game this child item is associated with. |
| 15 | platform_id | Platform ID | INT | 10 | N | platform.platform_id | Y |  | Foreign key referencing the platform on which this child item is available. |
| 16 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the child item record was created. |
| 17 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the child item record. |
| 18 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the child item record was last updated. |
| 19 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the child item record. |

## child_item_history

**Logical Name:** Child Item History

Stores historical versions of child item records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y |  | Y |  | Unique identifier for the child item. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this child item record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this child item record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the child item record. |
| 5 | child_item_code | Child Item Code | VARCHAR | 100 | N |  | Y |  | Unique code for the child item. |
| 6 | child_item_name | Child Item Name | VARCHAR | 300 | N |  | Y |  | The name of the child item. |
| 7 | parent_item_id | Parent Item ID | INT | 10 | N | parent_item.parent_item_id | Y |  | Foreign key referencing the parent item this child item belongs to. |
| 8 | royalty_type | Royalty Type | VARCHAR | 100 | N |  | Y |  | The type of royalty calculation (e.g., 'Per Unit', 'Percentage'). |
| 9 | royalty_per_unit | Royalty Per Unit | DECIMAL | 15,3 | N |  | N |  | The royalty amount per unit sold. |
| 10 | royalty_percentage | Royalty Percentage | DECIMAL | 15,5 | N |  | N |  | The royalty percentage applied to sales. |
| 11 | unit_price | Unit Price | DECIMAL | 15,3 | N |  | N |  | The price of a single unit of the child item. |
| 12 | msrp | MSRP | DECIMAL | 15,3 | N |  | N |  | Manufacturer's Suggested Retail Price for the child item. |
| 13 | sales_account_id | Sales Account ID | INT | 10 | N | account.account_id | Y |  | Foreign key referencing the account associated with sales of this child item. |
| 14 | game_type | Game Type | VARCHAR | 100 | N |  | Y |  | The type of game this child item is associated with. |
| 15 | platform_id | Platform ID | INT | 10 | N | platform.platform_id | Y |  | Foreign key referencing the platform on which this child item is available. |
| 16 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the child item record was created. |
| 17 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the child item record. |
| 18 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the child item record was last updated. |
| 19 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the child item record. |

## contract

**Logical Name:** Contract

Stores information about contracts with licensors.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | contract_id | Contract ID | INT | 10 | Y |  | Y |  | Unique identifier for the contract. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this contract record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this contract record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the contract record. |
| 5 | contract_name | Contract Name | VARCHAR | 300 | N |  | Y |  | The name or title of the contract. |
| 6 | mg_beginning_balance | MG Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | The beginning balance for Minimum Guarantee (MG) royalties. |
| 7 | pp_beginning_balance | PP Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | The beginning balance for Profit Participation (PP) royalties. |
| 8 | mg_original_paid | MG Original Paid | DECIMAL | 15,3 | N |  | Y |  | The original amount paid for Minimum Guarantee (MG) royalties. |
| 9 | licensor_id | Licensor ID | INT | 10 | N | licensor.licensor_id | Y |  | Foreign key referencing the licensor associated with this contract. |
| 10 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the contract record was created. |
| 11 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the contract record. |
| 12 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the contract record was last updated. |
| 13 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the contract record. |

## contract_history

**Logical Name:** Contract History

Stores historical versions of contract records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | contract_id | Contract ID | INT | 10 | Y |  | Y |  | Unique identifier for the contract. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this contract record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this contract record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the contract record. |
| 5 | contract_name | Contract Name | VARCHAR | 300 | N |  | Y |  | The name or title of the contract. |
| 6 | mg_beginning_balance | MG Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | The beginning balance for Minimum Guarantee (MG) royalties. |
| 7 | pp_beginning_balance | PP Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | The beginning balance for Profit Participation (PP) royalties. |
| 8 | mg_original_paid | MG Original Paid | DECIMAL | 15,3 | N |  | Y |  | The original amount paid for Minimum Guarantee (MG) royalties. |
| 9 | licensor_id | Licensor ID | INT | 10 | N | licensor.licensor_id | Y |  | Foreign key referencing the licensor associated with this contract. |
| 10 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the contract record was created. |
| 11 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the contract record. |
| 12 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the contract record was last updated. |
| 13 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the contract record. |

## division

**Logical Name:** Division

Represents business divisions within the company.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | division_id | Division ID | INT | 10 | Y |  | Y |  | Unique identifier for the division. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this division record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this division record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the division record. |
| 5 | division_name | Division Name | VARCHAR | 100 | N |  | N |  | The name of the division. |
| 6 | debit_account_id | Debit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default debit account for this division. |
| 7 | credit_account_id | Credit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default credit account for this division. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the division record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the division record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the division record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the division record. |

## division_history

**Logical Name:** Division History

Stores historical versions of division records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | division_id | Division ID | INT | 10 | Y |  | Y |  | Unique identifier for the division. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this division record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this division record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the division record. |
| 5 | division_name | Division Name | VARCHAR | 100 | N |  | N |  | The name of the division. |
| 6 | debit_account_id | Debit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default debit account for this division. |
| 7 | credit_account_id | Credit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default credit account for this division. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the division record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the division record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the division record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the division record. |

## game_title

**Logical Name:** Game Title

Stores information about game titles.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | game_title_id | Game Title ID | INT | 10 | Y |  | Y |  | Unique identifier for the game title. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this game title record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this game title record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the game title record. |
| 5 | game_title | Game Title | VARCHAR | 300 | N |  | Y |  | The name of the game title. |
| 6 | release_date | Release Date | DATE |  | N |  | N |  | The official release date of the game title. |
| 7 | contract_id | Contract ID | INT | 10 | N | contract.contract_id | Y |  | Foreign key referencing the contract associated with this game title. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the game title record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the game title record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the game title record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the game title record. |

## game_title_history

**Logical Name:** Game Title History

Stores historical versions of game title records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | game_title_id | Game Title ID | INT | 10 | Y |  | Y |  | Unique identifier for the game title. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this game title record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this game title record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the game title record. |
| 5 | game_title | Game Title | VARCHAR | 300 | N |  | Y |  | The name of the game title. |
| 6 | release_date | Release Date | DATE |  | N |  | N |  | The official release date of the game title. |
| 7 | contract_id | Contract ID | INT | 10 | N | contract.contract_id | Y |  | Foreign key referencing the contract associated with this game title. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the game title record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the game title record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the game title record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the game title record. |

## journal_entry_template

**Logical Name:** Journal Entry Template

Defines templates for recurring journal entries.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | template_id | Template ID | INT | 10 | Y |  | Y |  | Unique identifier for the journal entry template. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this template record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this template record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the template record. |
| 5 | template_name | Template Name | VARCHAR | 300 | N |  | Y |  | The name of the journal entry template. |
| 6 | debit_account_id | Debit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default debit account for this template. |
| 7 | credit_account_id | Credit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default credit account for this template. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the template record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the template record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the template record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the template record. |

## journal_entry_template_history

**Logical Name:** Journal Entry Template History

Stores historical versions of journal entry template records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | template_id | Template ID | INT | 10 | Y |  | Y |  | Unique identifier for the journal entry template. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this template record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this template record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the template record. |
| 5 | template_name | Template Name | VARCHAR | 300 | N |  | Y |  | The name of the journal entry template. |
| 6 | debit_account_id | Debit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default debit account for this template. |
| 7 | credit_account_id | Credit Account ID | INT | 10 | N | account.account_id | N |  | Foreign key referencing the default credit account for this template. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the template record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the template record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the template record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the template record. |

## licensor

**Logical Name:** Licensor

Stores information about entities that grant licenses.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | licensor_id | Licensor ID | INT | 10 | Y |  | Y |  | Unique identifier for the licensor. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this licensor record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this licensor record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the licensor record. |
| 5 | licensor_name | Licensor Name | VARCHAR | 300 | N |  | Y |  | The name of the licensor. |
| 6 | mg_balance_calculation_type | MG Balance Calculation Type | VARCHAR | 100 | N |  | Y |  | The method used to calculate Minimum Guarantee (MG) balance. |
| 7 | royalty_calculation_type | Royalty Calculation Type | VARCHAR | 100 | N |  | Y |  | The method used to calculate royalties. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the licensor record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the licensor record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the licensor record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the licensor record. |

## licensor_history

**Logical Name:** Licensor History

Stores historical versions of licensor records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | licensor_id | Licensor ID | INT | 10 | Y |  | Y |  | Unique identifier for the licensor. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this licensor record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this licensor record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the licensor record. |
| 5 | licensor_name | Licensor Name | VARCHAR | 300 | N |  | Y |  | The name of the licensor. |
| 6 | mg_balance_calculation_type | MG Balance Calculation Type | VARCHAR | 100 | N |  | Y |  | The method used to calculate Minimum Guarantee (MG) balance. |
| 7 | royalty_calculation_type | Royalty Calculation Type | VARCHAR | 100 | N |  | Y |  | The method used to calculate royalties. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the licensor record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the licensor record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the licensor record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the licensor record. |

## monthly_royalty

**Logical Name:** Monthly Royalty

Aggregated royalty information for a given month, linking licensor, contract, game title, division, accounts, and child item details.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | licensor_id | Licensor ID | INT | 10 | N |  | Y |  | Identifier for the licensor. |
| 2 | licensor_effective_start_date | Licensor Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the licensor's record at the time of this royalty calculation. |
| 3 | licensor_effective_end_date | Licensor Effective End Date | DATE |  | N |  | Y |  | The effective end date of the licensor's record at the time of this royalty calculation. |
| 4 | licensor_version_id | Licensor Version ID | INT | 10 | N |  | Y |  | The version ID of the licensor's record at the time of this royalty calculation. |
| 5 | licensor_name | Licensor Name | VARCHAR | 300 | N |  | Y |  | The name of the licensor. |
| 6 | mg_balance_calculation_type | MG Balance Calculation Type | VARCHAR | 100 | N |  | Y |  | The method used to calculate Minimum Guarantee (MG) balance for the licensor. |
| 7 | royalty_calculation_type | Royalty Calculation Type | VARCHAR | 100 | N |  | Y |  | The method used to calculate royalties for the licensor. |
| 8 | contract_id | Contract ID | INT | 10 | N |  | Y |  | Identifier for the contract. |
| 9 | contract_effective_start_date | Contract Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the contract's record at the time of this royalty calculation. |
| 10 | contract_effective_end_date | Contract Effective End Date | DATE |  | N |  | Y |  | The effective end date of the contract's record at the time of this royalty calculation. |
| 11 | contract_version_id | Contract Version ID | INT | 10 | N |  | Y |  | The version ID of the contract's record at the time of this royalty calculation. |
| 12 | contract_name | Contract Name | VARCHAR | 300 | N |  | Y |  | The name of the contract. |
| 13 | mg_beginning_balance | MG Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | The beginning balance for Minimum Guarantee (MG) royalties for the contract. |
| 14 | pp_beginning_balance | PP Beginning Balance | DECIMAL | 15,3 | N |  | Y |  | The beginning balance for Profit Participation (PP) royalties for the contract. |
| 15 | mg_original_paid | MG Original Paid | DECIMAL | 15,3 | N |  | Y |  | The original amount paid for Minimum Guarantee (MG) royalties for the contract. |
| 16 | game_title_id | Game Title ID | INT | 10 | N |  | Y |  | Identifier for the game title. |
| 17 | game_title_effective_start_date | Game Title Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the game title's record at the time of this royalty calculation. |
| 18 | game_title_effective_end_date | Game Title Effective End Date | DATE |  | N |  | Y |  | The effective end date of the game title's record at the time of this royalty calculation. |
| 19 | game_title_version_id | Game Title Version ID | INT | 10 | N |  | Y |  | The version ID of the game title's record at the time of this royalty calculation. |
| 20 | game_title | Game Title | VARCHAR | 300 | N |  | Y |  | The name of the game title. |
| 21 | release_date | Release Date | DATE |  | N |  | N |  | The release date of the game title. |
| 22 | parent_item_id | Parent Item ID | INT | 10 | N |  | Y |  | Identifier for the parent item. |
| 23 | parent_item_effective_start_date | Parent Item Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the parent item's record at the time of this royalty calculation. |
| 24 | parent_item_effective_end_date | Parent Item Effective End Date | DATE |  | N |  | Y |  | The effective end date of the parent item's record at the time of this royalty calculation. |
| 25 | parent_item_version_id | Parent Item Version ID | INT | 10 | N |  | Y |  | The version ID of the parent item's record at the time of this royalty calculation. |
| 26 | parent_item_code | Parent Item Code | VARCHAR | 100 | N |  | Y |  | The code of the parent item. |
| 27 | parent_item_name | Parent Item Name | VARCHAR | 300 | N |  | Y |  | The name of the parent item. |
| 28 | parent_item_type | Parent Item Type | VARCHAR | 100 | N |  | Y |  | The type of the parent item. |
| 29 | division_id | Division ID | INT | 10 | N |  | Y |  | Identifier for the division. |
| 30 | division_effective_start_date | Division Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the division's record at the time of this royalty calculation. |
| 31 | division_effective_end_date | Division Effective End Date | DATE |  | N |  | Y |  | The effective end date of the division's record at the time of this royalty calculation. |
| 32 | division_version_id | Division Version ID | INT | 10 | N |  | Y |  | The version ID of the division's record at the time of this royalty calculation. |
| 33 | division_name | Division Name | VARCHAR | 100 | N |  | N |  | The name of the division. |
| 34 | debit_account_id | Debit Account ID | INT | 10 | N |  | N |  | Identifier for the debit account. |
| 35 | debit_account_effective_start_date | Debit Account Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the debit account's record at the time of this royalty calculation. |
| 36 | debit_account_effective_end_date | Debit Account Effective End Date | DATE |  | N |  | Y |  | The effective end date of the debit account's record at the time of this royalty calculation. |
| 37 | debit_account_version_id | Debit Account Version ID | INT | 10 | N |  | Y |  | The version ID of the debit account's record at the time of this royalty calculation. |
| 38 | debit_account_name | Debit Account Name | VARCHAR | 300 | N |  | N |  | The name of the debit account. |
| 39 | debit_account_type | Debit Account Type | VARCHAR | 100 | N |  | N |  | The type of the debit account. |
| 40 | credit_account_id | Credit Account ID | INT | 10 | N |  | N |  | Identifier for the credit account. |
| 41 | credit_account_effective_start_date | Credit Account Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the credit account's record at the time of this royalty calculation. |
| 42 | credit_account_effective_end_date | Credit Account Effective End Date | DATE |  | N |  | Y |  | The effective end date of the credit account's record at the time of this royalty calculation. |
| 43 | credit_account_version_id | Credit Account Version ID | INT | 10 | N |  | Y |  | The version ID of the credit account's record at the time of this royalty calculation. |
| 44 | credit_account_name | Credit Account Name | VARCHAR | 300 | N |  | N |  | The name of the credit account. |
| 45 | credit_account_type | Credit Account Type | VARCHAR | 100 | N |  | N |  | The type of the credit account. |
| 46 | child_item_id | Child Item ID | INT | 10 | Y |  | Y |  | Identifier for the child item. |
| 47 | child_item_effective_start_date | Child Item Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the child item's record at the time of this royalty calculation. |
| 48 | child_item_effective_end_date | Child Item Effective End Date | DATE |  | N |  | Y |  | The effective end date of the child item's record at the time of this royalty calculation. |
| 49 | child_item_version_id | Child Item Version ID | INT | 10 | N |  | Y |  | The version ID of the child item's record at the time of this royalty calculation. |
| 50 | child_item_code | Child Item Code | VARCHAR | 100 | N |  | Y |  | The code of the child item. |
| 51 | child_item_name | Child Item Name | VARCHAR | 300 | N |  | Y |  | The name of the child item. |
| 52 | royalty_type | Royalty Type | VARCHAR | 100 | N |  | Y |  | The type of royalty calculation for the child item. |
| 53 | royalty_per_unit | Royalty Per Unit | DECIMAL | 15,3 | N |  | N |  | The royalty amount per unit for the child item. |
| 54 | royalty_percentage | Royalty Percentage | DECIMAL | 15,3 | N |  | N |  | The royalty percentage for the child item. |
| 55 | unit_price | Unit Price | DECIMAL | 15,3 | N |  | N |  | The unit price of the child item. |
| 56 | msrp | MSRP | DECIMAL | 15,3 | N |  | N |  | Manufacturer's Suggested Retail Price for the child item. |
| 57 | sales_account_id | Sales Account ID | INT | 10 | N |  | Y |  | Identifier for the sales account. |
| 58 | sales_account_effective_start_date | Sales Account Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the sales account's record at the time of this royalty calculation. |
| 59 | sales_account_effective_end_date | Sales Account Effective End Date | DATE |  | N |  | Y |  | The effective end date of the sales account's record at the time of this royalty calculation. |
| 60 | sales_account_version_id | Sales Account Version ID | INT | 10 | N |  | Y |  | The version ID of the sales account's record at the time of this royalty calculation. |
| 61 | sales_account_name | Sales Account Name | VARCHAR | 300 | N |  | N |  | The name of the sales account. |
| 62 | sales_account_type | Sales Account Type | VARCHAR | 100 | N |  | N |  | The type of the sales account. |
| 63 | game_type | Game Type | VARCHAR | 100 | N |  | Y |  | The type of game. |
| 64 | platform_id | Platform ID | INT | 10 | N |  | Y |  | Identifier for the platform. |
| 65 | platform_effective_start_date | Platform Effective Start Date | DATE |  | N |  | Y |  | The effective start date of the platform's record at the time of this royalty calculation. |
| 66 | platform_effective_end_date | Platform Effective End Date | DATE |  | N |  | Y |  | The effective end date of the platform's record at the time of this royalty calculation. |
| 67 | platform_version_id | Platform Version ID | INT | 10 | N |  | Y |  | The version ID of the platform's record at the time of this royalty calculation. |
| 68 | platform_code | Platform Code | VARCHAR | 100 | N |  | Y |  | The code of the platform. |
| 69 | platform_name | Platform Name | VARCHAR | 100 | N |  | Y |  | The name of the platform. |
| 70 | order_date | Order Date | DATE |  | Y |  | Y |  | The date of the order associated with this royalty calculation. |
| 71 | sales_version_id | Sales Version ID | INT | 10 | Y |  | Y |  | The version ID of the sales record at the time of this royalty calculation. |
| 72 | sold_quantity | Sold Quantity | INT | 10 | N |  | Y |  | The quantity of the child item sold. |
| 73 | sales | Sales Amount | DECIMAL | 15,3 | N |  | Y |  | The total sales amount for the child item. |
| 74 | manufactured_quantity | Manufactured Quantity | INT | 10 | N |  | N |  | The quantity of the child item manufactured. |
| 75 | discount | Discount Amount | DECIMAL | 15,3 | N |  | Y |  | The discount applied to the sales. |
| 76 | royalty_due | Royalty Due | DECIMAL | 15,3 | N |  | N |  | The calculated royalty amount due. |

## monthly_royalty_status

**Logical Name:** Monthly Royalty Status

Tracks the processing status of monthly royalty calculations.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | status_id | Status ID | INT | 10 | Y |  | Y |  | Unique identifier for the status record. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this status record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this status record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the status record. |
| 5 | status | Status | TINYINT | 3 | N |  | N |  | The current status of the monthly royalty calculation (e.g., 0=Pending, 1=Processing, 2=Completed). |
| 6 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the status record was created. |
| 7 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the status record. |
| 8 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the status record was last updated. |
| 9 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the status record. |

## monthly_royalty_status_history

**Logical Name:** Monthly Royalty Status History

Stores historical versions of monthly royalty status records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | status_id | Status ID | INT | 10 | Y |  | Y |  | Unique identifier for the status record. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this status record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this status record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the status record. |
| 5 | status | Status | TINYINT | 3 | N |  | N |  | The current status of the monthly royalty calculation (e.g., 0=Pending, 1=Processing, 2=Completed). |
| 6 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the status record was created. |
| 7 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the status record. |
| 8 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the status record was last updated. |
| 9 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the status record. |

## parent_item

**Logical Name:** Parent Item

Represents overarching items or product lines that contain multiple child items.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | parent_item_id | Parent Item ID | INT | 10 | Y |  | Y |  | Unique identifier for the parent item. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this parent item record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this parent item record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the parent item record. |
| 5 | parent_item_code | Parent Item Code | VARCHAR | 100 | N |  | Y |  | Unique code for the parent item. |
| 6 | parent_item_name | Parent Item Name | VARCHAR | 300 | N |  | Y |  | The name of the parent item. |
| 7 | parent_item_type | Parent Item Type | VARCHAR | 100 | N |  | Y |  | The type of the parent item (e.g., 'Game', 'DLC'). |
| 8 | division_id | Division ID | INT | 10 | N | division.division_id | Y |  | Foreign key referencing the division this parent item belongs to. |
| 9 | game_title_id | Game Title ID | INT | 10 | N | game_title.game_title_id | Y |  | Foreign key referencing the game title associated with this parent item. |
| 10 | journal_entry_template_id | Journal Entry Template ID | INT | 10 | N | journal_entry_template.template_id | Y |  | Foreign key referencing the journal entry template used for this parent item. |
| 11 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the parent item record was created. |
| 12 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the parent item record. |
| 13 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the parent item record was last updated. |
| 14 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the parent item record. |

## parent_item_history

**Logical Name:** Parent Item History

Stores historical versions of parent item records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | parent_item_id | Parent Item ID | INT | 10 | Y |  | Y |  | Unique identifier for the parent item. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this parent item record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this parent item record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the parent item record. |
| 5 | parent_item_code | Parent Item Code | VARCHAR | 100 | N |  | Y |  | Unique code for the parent item. |
| 6 | parent_item_name | Parent Item Name | VARCHAR | 300 | N |  | Y |  | The name of the parent item. |
| 7 | parent_item_type | Parent Item Type | VARCHAR | 100 | N |  | Y |  | The type of the parent item (e.g., 'Game', 'DLC'). |
| 8 | division_id | Division ID | INT | 10 | N | division.division_id | Y |  | Foreign key referencing the division this parent item belongs to. |
| 9 | game_title_id | Game Title ID | INT | 10 | N | game_title.game_title_id | Y |  | Foreign key referencing the game title associated with this parent item. |
| 10 | journal_entry_template_id | Journal Entry Template ID | INT | 10 | N |  | Y |  | Foreign key referencing the journal entry template used for this parent item. |
| 11 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the parent item record was created. |
| 12 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the parent item record. |
| 13 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the parent item record was last updated. |
| 14 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the parent item record. |

## platform

**Logical Name:** Platform

Stores information about gaming platforms (e.g., PC, PlayStation, Xbox).

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | platform_id | Platform ID | INT | 10 | Y |  | Y |  | Unique identifier for the platform. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this platform record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this platform record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the platform record. |
| 5 | platform_code | Platform Code | VARCHAR | 100 | N |  | Y |  | A short code representing the platform. |
| 6 | platform_name | Platform Name | VARCHAR | 100 | N |  | Y |  | The full name of the platform. |
| 7 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the platform record was created. |
| 8 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the platform record. |
| 9 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the platform record was last updated. |
| 10 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the platform record. |

## platform_history

**Logical Name:** Platform History

Stores historical versions of platform records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | platform_id | Platform ID | INT | 10 | Y |  | Y |  | Unique identifier for the platform. |
| 2 | effective_start_date | Effective Start Date | DATE |  | Y |  | Y |  | The start date for which this platform record is effective. |
| 3 | effective_end_date | Effective End Date | DATE |  | Y |  | Y |  | The end date for which this platform record is effective. |
| 4 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the platform record. |
| 5 | platform_code | Platform Code | VARCHAR | 100 | N |  | Y |  | A short code representing the platform. |
| 6 | platform_name | Platform Name | VARCHAR | 100 | N |  | Y |  | The full name of the platform. |
| 7 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the platform record was created. |
| 8 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the platform record. |
| 9 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the platform record was last updated. |
| 10 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the platform record. |

## royalty_adjustment

**Logical Name:** Royalty Adjustment

Records manual adjustments made to royalty calculations for a specific child item on a given date.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y | child_item.child_item_id | Y |  | Foreign key referencing the child item to which the adjustment applies. |
| 2 | adjustment_date | Adjustment Date | DATE |  | Y |  | Y |  | The date on which the royalty adjustment was made. |
| 3 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the royalty adjustment record. |
| 4 | royalty_adjustment | Royalty Adjustment | DECIMAL | 15,3 | N |  | Y |  | The amount of the royalty adjustment. Can be positive or negative. |
| 5 | adjustment_note | Adjustment Note | VARCHAR | 500 | N |  | N |  | A description or reason for the royalty adjustment. |
| 6 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the royalty adjustment record was created. |
| 7 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the royalty adjustment record. |
| 8 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the royalty adjustment record was last updated. |
| 9 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the royalty adjustment record. |

## royalty_adjustment_history

**Logical Name:** Royalty Adjustment History

Stores historical versions of royalty adjustment records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y | child_item.child_item_id | Y |  | Foreign key referencing the child item to which the adjustment applies. |
| 2 | adjustment_date | Adjustment Date | DATE |  | Y |  | Y |  | The date on which the royalty adjustment was made. |
| 3 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the royalty adjustment record. |
| 4 | royalty_adjustment | Royalty Adjustment | DECIMAL | 15,3 | N |  | Y |  | The amount of the royalty adjustment. Can be positive or negative. |
| 5 | adjustment_note | Adjustment Note | VARCHAR | 500 | N |  | N |  | A description or reason for the royalty adjustment. |
| 6 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the royalty adjustment record was created. |
| 7 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the royalty adjustment record. |
| 8 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the royalty adjustment record was last updated. |
| 9 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the royalty adjustment record. |

## sales

**Logical Name:** Sales

Records individual sales transactions for child items.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y | child_item.child_item_id | Y |  | Foreign key referencing the child item sold. |
| 2 | order_date | Order Date | DATE |  | Y |  | Y |  | The date the order was placed. |
| 3 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the sales record. |
| 4 | sold_quantity | Sold Quantity | INT | 10 | N |  | Y |  | The number of units sold in this transaction. |
| 5 | sales | Sales Amount | DECIMAL | 15,3 | N |  | Y |  | The total revenue generated from this sale. |
| 6 | manufactured_quantity | Manufactured Quantity | INT | 10 | N |  | N |  | The quantity manufactured for this sale, if applicable. |
| 7 | discount | Discount Amount | DECIMAL | 15,3 | N |  | Y |  | Any discount applied to this sale. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the sales record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the sales record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the sales record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the sales record. |

## sales_history

**Logical Name:** Sales History

Stores historical versions of sales records.

| No | Column Name (Physical) | Column Name (Logical) | Data Type | Length/Precision | PK | FK Reference | Not Null | Default | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | child_item_id | Child Item ID | INT | 10 | Y | child_item.child_item_id | Y |  | Foreign key referencing the child item sold. |
| 2 | order_date | Order Date | DATE |  | Y |  | Y |  | The date the order was placed. |
| 3 | version_id | Version ID | INT | 10 | Y |  | Y |  | Identifier for the version of the sales record. |
| 4 | sold_quantity | Sold Quantity | INT | 10 | N |  | Y |  | The number of units sold in this transaction. |
| 5 | sales | Sales Amount | DECIMAL | 15,3 | N |  | Y |  | The total revenue generated from this sale. |
| 6 | manufactured_quantity | Manufactured Quantity | INT | 10 | N |  | N |  | The quantity manufactured for this sale, if applicable. |
| 7 | discount | Discount Amount | DECIMAL | 15,3 | N |  | Y |  | Any discount applied to this sale. |
| 8 | created_timestamp | Created Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the sales record was created. |
| 9 | created_by | Created By | VARCHAR | 100 | N |  | Y |  | User who created the sales record. |
| 10 | updated_timestamp | Updated Timestamp | TIMESTAMP |  | N |  | N | CURRENT_TIMESTAMP | Timestamp when the sales record was last updated. |
| 11 | updated_by | Updated By | VARCHAR | 100 | N |  | Y |  | User who last updated the sales record. |
