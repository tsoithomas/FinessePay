# FinessePay
This is a proof-of-concept demo of a P2P payment mobile app which I completed as a project for the course COMP7300 Financial Technology of the program MSc in Data Analytics and Artificial Intelligence at Hong Kong Baptist University.

The app is implemented with Flask, Python and MySQL.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Contributing](#contributing)
4. [License](#license)

## Introduction
FinessePay enables users to record transactions and budgeting while they are making P2P payments. The target audience is anyone who desires a detailed record of transactions for personal finance management. 

![FinessePay](https://github.com/tsoithomas/FinessePay/blob/master/FinessePay1.png?raw=true)
![FinessePay](https://github.com/tsoithomas/FinessePay/blob/master/FinessePay2.png?raw=true)
![FinessePay](https://github.com/tsoithomas/FinessePay/blob/master/FinessePay3.png?raw=true)
![FinessePay](https://github.com/tsoithomas/FinessePay/blob/master/FinessePay4.png?raw=true)
![FinessePay](https://github.com/tsoithomas/FinessePay/blob/master/FinessePay5.png?raw=true)
![FinessePay](https://github.com/tsoithomas/FinessePay/blob/master/FinessePay6.png?raw=true)
![FinessePay](https://github.com/tsoithomas/FinessePay/blob/master/FinessePay7.png?raw=true)

## Features
### Payment
#### Send Payment
Users can enter this interface through the drop-down menu in the upper right corner, they need to input the username, payment amount and the payment category(optional) in this interface.
If the user has enough balance in his account, the payment is successful (Figure 1b). A reference number is provided for the reference use of the user.

#### Receive Payment
Users can receive payment from friends or organizations by giving them usernames. After the payer completes the payment, the payee will get the money and transaction record. 

#### Scheduled payment
Users can set scheduled payment to another user. Users can choose the types of payment and the date of payment in the calendar. Those data are also recorded.
This is very similar to the instant payment mentioned before, but it has a timing function, users can make their payment plan. The list of scheduled payments can be viewed and can be deleted with the cross button (Figure 4b). 
Completed scheduled payments in the past 30 days are also shown for records.

### Payment History
Users can view a list of payment records here.
In this function, users can get all their revenue and expenditure records, and all records will be classified by date. The reference ID is also displayed for reference.

### Budgeting
In the ‘overview’, users can view the data analytics for their expenditure/income in a specific period. There will be a pie chart for users to know their expenditure.
When users press the category in the pie chart, the actual amount and its percentage to the total expenditure is shown.

In the ‘Set budget’ section, Users can set limits for the total expenditure in a specific period. Users can choose whether to receive notification when the payment exceeds the limit in the setting part (Figure 7a).
Notifications will be sent to users when their expenditure reaches 80% and 100% of the monthly budget respectively. This refrains users from overspending.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

## License
MIT License

Copyright (c) 2022 Thomas Tsoi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
