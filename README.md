# Give Hope Hub

Give Hope Hub is a versatile module designed to empower the creation of searches for various entities within the Give Hope Hub donation website. This module serves as a fundamental building block for administrators and developers, facilitating an efficient and flexible search experience.

This is a final project for [CS50] 
#### Video Demo: https://youtu.be/pNJqGqhJiVE

[CS50]: https://cs50.harvard.edu/x/2023/

![miniHome Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/miniHome.png)

Developers, on the other hand, will be impressed by the large flexibility and
numerous ways of extension the module provides. Hence, the growing number of
additional contribution modules provides additional functionality or helps users
customize some aspects of the search process.

#### Description:
## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Features](#features)
  - [Home Page](#home-page)
  - [About Page](#about-page)
  - [Registration and Login](#registration-and-login)
    - [Registration](#registration)
    - [Login](#login) 
  - [User Dashboard](#user-dashboard)
  - [Adding a Charity](#adding-a-charity)
  - [Adding Funds](#adding-funds)
  - [Making Donations](#making-donations)
  - [Viewing Transactions](#viewing-transactions)
- [Contributing](#contributing)


## Getting Started

## Prerequisites
Before you begin, ensure you have the following prerequisites installed on your system:

- [Python](https://www.python.org/) (version 3.6 or higher)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/)


## Installation
1. Clone the repository:
   ```bash
   git clone (https://github.com/RehabHesham/Donation-System.git)
   cd donation-platform

2. Create a virtual environment:
   ```bash
    python -m venv venv
   
3. Activate the virtual environment:
  - On Windows:
      ```bash
        .\venv\Scripts\activate
  - On macOS/Linux:
      ```bash
      source venv/bin/activate
      
4. Install dependencies:
    ```bash
        pip install -r requirements.txt
    
5. Run the application:

    ```bash
      flask run
Open your web browser and navigate to http://localhost:5000.

## Features
### Home Page
  - Welcome Section:
      Display a warm welcome message and brief introduction to the donation platform.
      Highlight the platform's mission and goals.
    ![Homepage Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/HomePage.png)
  
### About Page
  - Platform Overview:
      Provide detailed information about the donation platform's history, mission, and values.
      Include testimonials or success stories from donors and charities.
  - Team Members:
      Introduce the core team members and their roles.
      Include brief profiles and images to humanize the platform.
    ![AboutUs Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/AboutUs.png)

### Registration and Login
  ### Registration:
    - Allow users to create an account by providing necessary information (name, email, password).
      Implement email verification for account security.
  ![Register Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/Register.png)
  ### Login:
    - Provide a secure login system with email/password authentication.
    Offer options for password recovery.
  ![Login Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/login.png)
### User Dashboard
  - Overview:
      Display a personalized dashboard upon login.
      Highlight key metrics such as the user's total donations and available balance.
      ![UserHome Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/AddCharity.png)

    
### Adding a Charity:
  - Allow users to add new charities to the platform for consideration.
    Include fields for charity name, description, and contact information.
    ![AddCharity Screenshot]()
  - When add a charity you will be redirected to see this charity's details
    ![CharityDetails Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/CharityDetails.png)


### Adding Funds:
  Enable users to add funds to their platform balance securely.
  Display the current balance and transaction history.
    ![AddFund Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/AddFund.png)


### Viewing Transactions:
  Provide a section to view a detailed history of past donations.
  Include information such as date, charity name, and donation amount.
    ![Transactions Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/UserTransactions.png)

  
### Making Donations:
  Implement a simple and secure donation process for users to contribute to specific charities.
  Allow users to set custom donation amounts.
    ![Donate Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/Donate.png)


### Transaction Page
  - Transaction History:
    Offer a page where users can view a complete history of their financial transactions.
    Include details such as date, transaction type (donation or fund addition), and amount.
      ![Login Screenshot](https://github.com/RehabHesham/Donation-System/blob/main/screenshots/login.png)


## Contributing
  We welcome contributions! If you have ideas for improvements or find issues, please open an issue or submit a pull request.
