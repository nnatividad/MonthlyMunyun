# MonthlyMunyun
#### Video Demo:  https://www.youtube.com/watch?v=4MHOY2HkRWk
#### Description: A monthly expense tracker!

Introduction:
Monthly Munyun is a web application built using Flask, HTML/CSS, and SQL that is meant to provide users a platform to keep track of there monthly expenses.

File Overview:
app.py - This file contains all the backend logic written in Flask including user authentication, route logic, and session management.

helpers.py - This file contains the helper functions used in both app.py and in some of the template files.

templates - This folder contains all the frontend html/css and jinja files. I utilize jinja's layout feature to be able to have the navbar accessible in each part of the project and create a uniform style to each page.

tables.sql - This file contains the SQL scripts I wrote to create each of the tables and there relationships. This project right now has three tables to store the users, there budgets, and all activities.


Features:
1. User Dashboard
Each user must make an account or log in to their existing account to be able to begin. The user dashboard will be the home screen that all users will see once making an account. This dashboard shows a pie chart of which categories they are spending the most money on per month. Along with visual progress bars that show both the amount and the percentage of how much in there budget they are spending for the main categories grouped as Income, Needs, Wants, and Savings. This dashboard also shows a table of all of the Users expenses which shows what, when, and where that money was being spent!

2. Income Tracking / Setting a Budget
When the user first makes an account, or in the situation there income is changing per month the user will be able to update and set a budget. This allows them to set how much of each category they would like to allow themselves to spend. Users are able to track there income and update the amount of money they must allocate for there daily lives.

3. Logging and Categorizing Expenses
Users must input and keep track of there own expenses. There are categories which are: Auto, Transportation, Entertainment, Bills, Savings, Debt, and Other. The user can set the amount of money as well as the category to which the expense belongs too. Once submitted they will be sent back to the user dashboard which will show the updated expenses.

Future Improvements:
In the future, the main improvements I want to make would be to be able to connect to the users bank account which will automate getting information such as income and I could then improve the budget to be per check or per month option based on the users choice. I would also like to implement an AI chatbot where the AI can provide financial literacy for the user based on there spending habits.


