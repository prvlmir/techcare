# 🛠️ TechCare — ITSM Helpdesk & Inventory System

**TechCare** is a comprehensive web-based ITSM (Information Technology Service Management) solution designed to automate internal IT support processes. It combines a ticketing system with hardware inventory management, providing a unified platform for IT staff and employees.


## 🚀 Key Features

### 👤 For Employees (End-Users)
* **Secure Authentication:** Easy login using Email and Password.
* **Ticket Submission:** Intuitive interface to report issues, select categories (Hardware, Software, Network), and assign priority.
* **Real-time Tracking:** Monitor ticket status (New, In Progress, Closed) and view technician comments.
* **History:** Access to personal ticket history.

### 👨‍💻 For IT Staff (Admins)
* **Staff Dashboard:** Centralized hub with live statistics (Total tickets, Critical issues, SLA monitoring).
* **Ticket Management:** Workflow for processing requests, changing statuses, and assigning internal notes.
* **Asset Management (CMDB):** Full inventory control for hardware (Laptops, PCs, Printers).
    * Add new assets.
    * Track assignment to specific users.
    * Monitor equipment status (Active, In Repair, Decommissioned).
* **Advanced Filtering:** Filter tickets by status and urgency.

## 🛠️ Technology Stack

* **Backend:** Python 3.12, Django 5.0
* **Frontend:** HTML5, CSS3, Bootstrap 5 (Custom Dark Mode UI)
* **Database:** SQLite (Dev), PostgreSQL compatible
* **Authentication:** Custom EmailBackend

## ⚙️ Installation & Setup

To run this project locally, follow these steps:

### 1. Clone the repository
```bash
git clone [https://github.com/prvlmir/techcare.git](https://github.com/prvlmir/techcare.git)
cd techcare
