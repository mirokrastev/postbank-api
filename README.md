# postbank-api
Postbank API SoftUni Fest project

## Requirements
Python >= 3.9</br>
```pip install -r requirements.txt```</br>
Configure ```.env``` from ```env_example``` template

## Introduction
This document aims to describe the features of this web project.

## App overview
Postbank provides its clients (Traders) with POS terminals, with which they receive payments with debit or credit cards.
Aiming to popularise their business and stimulate card transactions, traders offer discounts to their clients when they
pay via card at a POS terminal. The main goal of this app is to handle these discount offers, which traders will periodically
send to their clients.

## Features
POS Discount app, built with DRF.
It consists of 3 different types of users - trader, bank employee and cardholder.

Traders can have POS terminals and can create discount offers.

Bank employees can see everything from the users, traders, discounts and POS terminals.
They can accept/reject discount offers.

Cardholders can see all available discount offers and can enable/disable
email notifications for new offers.

## API Docs
Check ```/``` for Schema.