# ER and DFD Diagrams

This file documents the current design represented by the Mermaid files inside docs/diagrams.

## Current Diagram Files

- docs/diagrams/ER_Diagram.mmd
- docs/diagrams/DFD_Level_0.mmd
- docs/diagrams/DFD_Level_1.mmd

Exported assets for report usage are also available as SVG and HD PNG in the same folder.

## 1) ER Diagram Summary

The ER model reflects the current Django store app.

### Entities

- USER (Django auth user)
- PRODUCT
- PRODUCT_IMAGE
- CART
- CART_ITEM
- ORDER
- ORDER_ITEM
- USER_ADDRESS
- WISHLIST
- WISHLIST_ITEM

### Relationship Highlights

- USER 1:1 CART
- USER 1:1 USER_ADDRESS
- USER 1:1 WISHLIST
- USER 1:N ORDER
- PRODUCT 1:N PRODUCT_IMAGE
- CART 1:N CART_ITEM
- ORDER 1:N ORDER_ITEM
- WISHLIST 1:N WISHLIST_ITEM

## 2) DFD Level 0 (Context)

External entities:

- Customer/User
- Admin

Main system process:

- Global Mart E-Commerce System

Level 0 captures top-level data movement between these actors and the system.

## 3) DFD Level 1

Level 1 decomposes system flow into these functional processes:

- User authentication
- Product browsing
- Cart management
- Wishlist management
- Checkout and order processing
- Profile/address management
- Admin operations (products, images, orders)

Data stores represented:

- Users
- Products
- Cart/Cart Items
- Wishlist/Wishlist Items
- Orders/Order Items
- User Addresses

## Notes

- Diagram content matches the current codebase after latest model and deployment updates.
- For report submission, use the pre-exported images in docs/diagrams or re-export from .mmd.
