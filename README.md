# FinessePay
A proof-of-concept demo of a P2P payment mobile app.

## Table of Contents
1. [Introduction](#introduction)
2. A GIF or image of the working demo
3. [Getting Started](#getting-started)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)

## Introduction

### Motivation for creating FinessePay
The electronic payment system in Hong Kong is gaining popularity in recent years.  Digital wallets such as Payme, AlipayHK, O!ePay and WeChat PayHK are widely used for making Peer-to-Peer (P2P) payment, online payment and bill payment at stores. Divided bill function is also available in these applications. Although there is payment record in these applications, those records are not categorized and the aggregate amount in different categories of expenditure is not shown.
Several apps such as MoneyPro, AndroMoney and Moze are providing personal budgeting and accounting functions. Users need to manually input their incomes and expenditures and choose the corresponding type.  Data Visualization for income and expenditure is also available for budgeting purposes. 

The electronic payment functions and personal budgeting functions are crucial to people. However, currently there are no applications that integrate these functions together. This creates troubles for people. For example, when Peter uses Payme to transfer money to his friends for the meals, Payme only records the amount of money transfer and the payee. Peter needs to input the data manually in another application AndroMoney for recording and budgeting. This deters people from budgeting.

### Use of FinessePay
Therefore, we are dedicated to integrating electronic payment and budgeting in one single application for users’ convenience. FinessePay enables users to record transactions and budgeting while they are making P2P payments. The target audience is anyone who desires a detailed record of transactions for personal finance management. 

### Functions of the FinessePay
#### Payment
(a) Send Payment
Users can enter this interface
through the drop-down menu in the upper right corner, they need to input the username,
payment amount and the payment category(optional) in this interface (Figure 1a).
If the user has enough balance in his account, the payment is successful (Figure 1b). A reference number is provided for the reference use of the user.

The payment is performed as a transaction in the MySQL database. The transaction consists of 3 queries:
1.	Inserting payment record into the payment table
2.	Debiting the payee’s balance
3.	Crediting the payer’s balance
If any of these queries fails, the transaction is rolled back to avoid inconsistency.
All payment records are kept for archiving purposes.

(b) Receive Payment
Users can receive payment from friends or organizations by giving them usernames. After the payer completes the payment, the payee will get the money and transaction record. For example, figure 2 shows the payment history of the users after receiving payment from Thomas Tsoi.

(c) Scheduled payment
Users can set scheduled payment to another user. Users can choose the types of payment and the date of payment in the calendar (Figure 4a). Those data are also recorded.
This is very similar to the instant payment mentioned before, but it has a timing function, users can make their payment plan. The list of scheduled payments can be viewed and can be deleted with the cross button (Figure 4b). 
Completed scheduled payments in the past 30 days are also shown for records.

A batch script is used to batch process these payments every day at 3 a.m and executed as a cron job. The script checks if the payer has enough funds to perform the transaction, if not, it marks the scheduled payment as “Insufficient fund”, and if yes, it carries out the transaction. The schedule records are kept for archiving purposes even if errors occur.
(d) Payment History
Users can view a list of payment records here.
In this function, users can get all their revenue and expenditure records, and all records will be classified by date (Figure 5). The reference ID is also displayed for reference.
(e) Budgeting
In the ‘overview’, users can view the data analytics for their expenditure/income in a specific period. There will be a pie chart for users to know their expenditure (Figure 6a).
When users press the category in the pie chart, the actual amount and its percentage to the total expenditure is shown (Figure 6b).
In the ‘Set budget’ section, Users can set limits for the total expenditure in a specific period. Users can choose whether to receive notification when the payment exceeds the limit in the setting part (Figure 7a).
Notifications will be sent to users when their expenditure reaches 80% and 100% of the monthly budget respectively (Figure 7b & 7c). This refrains users from overspending.

## Getting Started
These instructions will get you a copy of the project up and running on your local
machine for development and testing purposes.

### Prerequisites
What things you need to install the software and how to install them.

### Installing
A step by step series of examples that tell you how to get a development
environment running.

## Usage
Explain how to use the project. If the project has a UI, provide screenshots or
GIFs showcasing the usage.

## Contributing
Explain how other developers can contribute to the project. You can use
something like the following example:
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/) license.
