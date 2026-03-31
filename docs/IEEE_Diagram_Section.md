# Diagram Section for Final Report (IEEE Style)

## V. SYSTEM DESIGN

### A. Entity Relationship (ER) Diagram

Figure 1 presents the ER design of Global Mart. The model includes ten entities: User (Django authentication), Product, ProductImage, Cart, CartItem, Order, OrderItem, UserAddress, Wishlist, and WishlistItem. One-to-one relations are used for per-user containers (Cart, UserAddress, Wishlist), while one-to-many relations are used for line-item entities (CartItem, OrderItem, WishlistItem, ProductImage).

Figure caption:

Fig. 1. Entity Relationship diagram of the Global Mart e-commerce system.

Source:

- docs/diagrams/ER_Diagram.mmd

### B. Data Flow Diagram (Context Level / Level 0)

Figure 2 models the complete system as a single process interacting with two external entities: Customer/User and Admin. Customer interactions include authentication, browsing, cart actions, wishlist actions, and checkout. Admin interactions include product, image, and order management.

Figure caption:

Fig. 2. Context-level (Level 0) Data Flow Diagram of the proposed system.

Source:

- docs/diagrams/DFD_Level_0.mmd

### C. Data Flow Diagram (Level 1)

Figure 3 decomposes the system into the following processes: user authentication, product browsing, cart management, wishlist management, checkout and order processing, profile/address management, and admin operations. Data stores include Users, Products, Carts/Cart Items, Wishlists/Wishlist Items, Orders/Order Items, and User Addresses.

Figure caption:

Fig. 3. Level 1 Data Flow Diagram showing process decomposition and data stores.

Source:

- docs/diagrams/DFD_Level_1.mmd

### D. Data Flow Diagram (Level 2)

Figure 4 decomposes checkout and order processing into cart validation, address validation, payment authorization, order creation, and cart finalization. It also introduces an external Payment Gateway entity.

Figure caption:

Fig. 4. Level 2 Data Flow Diagram for checkout and order processing decomposition.

Source:

- docs/diagrams/DFD_Level_2.mmd

### E. Data Flow Diagram (Level 3)

Figure 5 decomposes cart management into view cart, add item, update quantity, remove item, and total recalculation operations.

Figure caption:

Fig. 5. Level 3 Data Flow Diagram for cart management decomposition.

Source:

- docs/diagrams/DFD_Level_3.mmd

### F. Data Flow Diagram (Level 4)

Figure 6 decomposes admin operations into category management, product management, image management, order review, and status update operations.

Figure caption:

Fig. 6. Level 4 Data Flow Diagram for admin operations decomposition.

Source:

- docs/diagrams/DFD_Level_4.mmd

### G. Data Flow Diagram (Level 5)

Figure 7 decomposes authentication and account functions into registration, login, session validation, profile update, and address maintenance.

Figure caption:

Fig. 7. Level 5 Data Flow Diagram for authentication and account/profile decomposition.

Source:

- docs/diagrams/DFD_Level_5.mmd

## Deployment Consistency Note

For production reliability, the current deployment flow runs migrations at runtime before starting Gunicorn (`python manage.py migrate && gunicorn myshop.wsgi:application`). This ensures the database schema used by the running app matches the latest code and diagrams.

## How to Export as PNG/SVG

1. Open any .mmd file in VS Code.
2. Use Mermaid preview/export support.
3. Export figures as PNG or SVG for report insertion.
4. Suggested report names:
   - Fig1_ER_Diagram
   - Fig2_DFD_Level0
   - Fig3_DFD_Level1
   - Fig4_DFD_Level2
   - Fig5_DFD_Level3
   - Fig6_DFD_Level4
   - Fig7_DFD_Level5

## Suggested Placement in Report

- Place Fig. 1 under Database Design.
- Place Fig. 2 to Fig. 7 under System Design or Functional Architecture.
- Keep figure numbering and captions consistent with IEEE formatting.
