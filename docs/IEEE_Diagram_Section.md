# Diagram Section for Final Report (IEEE Style)

## V. SYSTEM DESIGN

### A. Entity Relationship (ER) Diagram

The ER diagram of the proposed e-commerce system is shown in Fig. 1. The design consists of ten core entities: Product, ProductImage, Cart, CartItem, Orders, OrderItem, UserAddress, Wishlist, WishlistItem, and User (from the authentication module). One-to-many relationships are used for itemized collections such as cart items, order items, wishlist items, and product images, while one-to-one relationships are used for per-user structures such as Cart, UserAddress, and Wishlist.

Figure caption for report:

Fig. 1. Entity Relationship diagram of the Global Mart e-commerce system.

Source file:

- docs/diagrams/ER_Diagram.mmd

### B. Data Flow Diagram (Context Level / Level 0)

The context-level DFD is shown in Fig. 2. It models the Global Mart E-Commerce System as a single process interacting with two external entities: Customer/User and Admin. The user sends requests for authentication, product browsing, cart operations, wishlist operations, and checkout, while the admin performs product and order management activities.

Figure caption for report:

Fig. 2. Context-level (Level 0) Data Flow Diagram of the proposed system.

Source file:

- docs/diagrams/DFD_Level_0.mmd

### C. Data Flow Diagram (Level 1)

The Level 1 DFD is shown in Fig. 3 and decomposes the main system into seven functional processes: user authentication, product browsing, cart management, wishlist management, checkout and order processing, profile/address management, and admin management operations. Data stores include Users, Products, Cart and Cart Items, Wishlist and Wishlist Items, Orders and Order Items, and User Addresses.

Figure caption for report:

Fig. 3. Level 1 Data Flow Diagram showing process decomposition and data stores.

Source file:

- docs/diagrams/DFD_Level_1.mmd

## How to Export as PNG/SVG

1. Open any .mmd file in VS Code.
2. Use a Mermaid preview extension or Mermaid live preview.
3. Export each figure as PNG for direct report insertion.
4. Suggested filenames for report submission:
   - Fig1_ER_Diagram.png
   - Fig2_DFD_Level0.png
   - Fig3_DFD_Level1.png

## Suggested Placement in Report

- Place Fig. 1 under Database Design.
- Place Fig. 2 and Fig. 3 under System Design or Functional Architecture.
- Keep figure labels centered and use consistent font size throughout the report.
