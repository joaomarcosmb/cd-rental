# ER DIAGRAM
```mermaid
erDiagram
    customer {
        uuid id PK
        string cpf
        string name
        string phone
        string email
    }

    attendant {
        uuid id PK
        string cpf
        string name
        string phone
        string email
        uuid store_id FK
    }

    store {
        uuid id PK
        string cnpj
        string trade_name
    }

    address {
        uuid id PK
        string street
        string number
        string neighborhood
        string city
        string state
        string zip_code
        uuid store_id FK
    }

    cd {
        uuid id PK
        string title
        decimal rental_price
        uuid artist_id FK
        uuid genre_id FK
        uuid status_id FK
        uuid store_id FK
    }

    rental {
        uuid customer_id PK,FK
        uuid cd_id PK,FK
        datetime rental_date
        datetime return_date
        decimal amount_paid
    }

    artist {
        uuid id PK
        string name
    }

    genre {
        uuid id PK
        string description
    }

    cd_status {
        uuid id PK
        string description
    }

    payment {
        uuid id PK
        uuid customer_id FK
        uuid cd_id FK
        decimal amount
        datetime payment_date
        string payment_method
        string status
    }

    store ||--|{ attendant : "employs"
    store ||--|| address : "has"
    store ||--|{ cd : "owns"

    artist ||--|{ cd : "records"
    genre ||--|{ cd : "belongs_to"
    cd_status ||--|{ cd : "has_status"

    customer ||--|{ rental : "makes"
    cd ||--o{ rental : "rented_in"
    
    customer ||--|{ payment : "makes"
    cd ||--o{ payment : "paid_for"
```