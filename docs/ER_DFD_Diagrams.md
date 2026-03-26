# ER and DFD Diagrams

## 1. ER Diagram (Entity Relationship)

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email
        string password
    }

    PRODUCT {
        int id PK
        string name
        string description
        decimal price
        int stock
        string image_url
    }

    PRODUCT_IMAGE {
        int id PK
        int product_id FK
        string image_url
        boolean is_primary
        int display_order
    }

    CART {
        int id PK
        int user_id FK
        datetime created_at
    }

    CART_ITEM {
        int id PK
        int cart_id FK
        int product_id FK
        int quantity
    }

    ORDERS {
        int id PK
        int user_id FK
        datetime created_at
        decimal total_price
        string status
    }

    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        decimal price
        int quantity
    }

    USER_ADDRESS {
        int id PK
        int user_id FK
        string full_name
        string phone
        string street_address
        string landmark
        string city
        string state
        string pin_code
        string country
    }

    WISHLIST {
        int id PK
        int user_id FK
        datetime created_at
    }

    WISHLIST_ITEM {
        int id PK
        int wishlist_id FK
        int product_id FK
        datetime added_at
    }

    USER ||--|| CART : owns
    CART ||--o{ CART_ITEM : contains
    PRODUCT ||--o{ CART_ITEM : added_in

    USER ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : ordered_as

    USER ||--|| USER_ADDRESS : has

    USER ||--|| WISHLIST : owns
    WISHLIST ||--o{ WISHLIST_ITEM : contains
    PRODUCT ||--o{ WISHLIST_ITEM : saved_as

    PRODUCT ||--o{ PRODUCT_IMAGE : has
```

## 2. DFD Diagram (Level 1)

```mermaid
flowchart LR
    U[Customer/User]
    A[Admin]

    P1((1.0 User Authentication))
    P2((2.0 Product Browsing))
    P3((3.0 Cart Management))
    P4((4.0 Wishlist Management))
    P5((5.0 Checkout and Order Processing))
    P6((6.0 Profile and Address Management))
    P7((7.0 Admin Product and Order Management))

    D1[(D1 Users)]
    D2[(D2 Products)]
    D3[(D3 Cart and Cart Items)]
    D4[(D4 Wishlist and Wishlist Items)]
    D5[(D5 Orders and Order Items)]
    D6[(D6 User Addresses)]

    U -->|signup/login| P1
    P1 <--> D1

    U -->|search/view products| P2
    P2 <--> D2

    U -->|add, remove, update qty| P3
    P3 <--> D3
    P3 -->|reads product info| D2

    U -->|save/remove favorites| P4
    P4 <--> D4
    P4 -->|reads product info| D2

    U -->|place order| P5
    P5 -->|reads cart| D3
    P5 -->|creates order| D5
    P5 -->|validates address| D6
    P5 -->|clears cart items| D3

    U -->|edit profile/address| P6
    P6 <--> D1
    P6 <--> D6

    A -->|manage products, images, orders| P7
    P7 <--> D2
    P7 <--> D5
```

## 3. DFD Diagram (Context / Level 0)

```mermaid
flowchart LR
    U[Customer/User]
    A[Admin]
    S((Global Mart E-Commerce System))

    U -->|signup/login, browse, cart, wishlist, checkout| S
    S -->|product info, cart status, order status| U

    A -->|manage products and orders| S
    S -->|admin data views and updates| A
```

## Notes for Report Submission

- ER diagram is based on your implemented Django models in the store app.
- DFD Level 1 shows major processes and data stores used by your system.
- You can export these Mermaid diagrams to PNG/SVG using VS Code Mermaid preview or online Mermaid tools.
