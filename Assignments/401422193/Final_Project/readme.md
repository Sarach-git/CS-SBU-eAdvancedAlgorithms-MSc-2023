# Diet Planning Optimization with Linear Programming

## Introduction

Designing an optimal diet plan is important for maintaining health and nutrition. This project aims to generate personalized diet plans using linear programming optimization. Generated plans are basically for **busy people** that need **minimum time to prepare and cook the foods**.

## What is a diet plan?

A diet plan specifies the types and amounts of food to eat over a set period of time. A good diet plan provides the right balance of calories, macronutrients (carbs, protein, and fat), vitamins and minerals needed for overall health and wellbeing.

### Why it's important?

* Maintain a healthy weight - A balanced diet can help achieve and maintain a healthy body weight.
* Meet nutrient needs - A well-planned diet ensures the intake of all essential nutrients required by the body.
* Improve health - Certain diets can help manage diseases like diabetes, high blood pressure, and high cholesterol.
* Increase energy levels - Nutritious foods fuel the body and improve physical and mental performance.

## Project Phases
**[Video Tutoria of program usage](https://github.com/moligarch/CS-SBU-eAdvancedAlgorithms-MSc-2023/blob/401422193/Assignments/401422193/Final_Project/ODP%20Tutorial-Persian.rar)**

This project aims to optimize diet plans with the following 4 phases:

- [x] **[⛏ Data Gathering/Mining](#⛏Phase-1:-Data-Mining)** - Recipes and nutrition data will be scraped from the BBC Good Food website, focusing on quick and easy recipes that require minimal preparation time.
    - [x] Define what we are looking for
    - [x] Define data scrapping functions
    - [x] Store gathered data into dataset

- [x] **[🧹 Data Cleaning/Selecting](#🧹Phase-2:-Data-Cleaning)** - Missing and erroneous data will be identified and removed. Incomplete recipes will be discarded.
    - [x] Classify foods with category and sub-category
    - [x] Append recipes and their classification into dataset/data frame
    - [x] Remove missing values
    - [x] Convert mismatched data
    - [x] Select data by condition (Preparation time + Cocking time < 30 min)
    - [x] Save modified dataset into file (.csv)

- [x] **[⚖ Data Processing](#⚖Phase-3:-Data-Processing)** - An LP model will be formulated to generate optimized diet plans that maximize nutrition while minimizing preparation time.
    - [x] Make a structure for user prefrences input
    - [x] Find optimized mix of recipes according to `Cleaned Dataset`


- [x] **[📊 GUI](#📊Phase-4:-Interface)** - Build a Graphic User Interface(GUI) will by Tkinter library.
    - [x] Design general wireframe
    - [x] Implement input box to get user prefrences
    - [x] Read data and group food by category.
    - [x] Add popup for more information about food (ingredients, steps, name and etc.)
    - [x] Add popup to show shopping list
     
- [x] **✅ COMPLETED** : This project got successfully COMPLETED! Hooray! 👌😁
