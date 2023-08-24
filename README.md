# Net Worth Calculator/Tracker Desktop App

## Background

This project is a result of my desire to build a foundation in desktop app development using Python. I plan to build personal desktop apps similar to this one, using the same stack. I wanted to gain some experience working on a smaller project that could be completed in a weekend before moving on to something larger. Additionally, I am a huge fan of all the financial assistance tools and calculators that one can find on the [Smart Assets Website](https://smartasset.com/), o recreating some of these but personalizing them and allowing them the ability to retain my information would be ideal.l.

## Problem Statement

I have used online net worth tracking apps that have done everything that I need, but are missing key pieces that I wanted. Additionally, I really just wanted to make my first desktop app that was small in scope and could be a foundation for projects that I want to work on in the future.

Online net worth calculators that I have used often look like this:

- Calculate Net Worth, and on exit all the data is lost and need to re-enter the next time you want to calculate
- Calculate AND Track Net Worth, but save the information to a database/server that I do not own/operate where my "senstive" information is out of my control.

So I thought a good solution would do calculate networth, track the information, retain the data locally.

## Current Solution

My solution to this problem was to create a desktop application that would allow me to calculate and store the information needed to calculate net worth and display data visualization on that information as well. I chose this approach to making the application for desktop so that the instance remained local (not running on a cloud server). This means that the UI, Backend, and Database are all within my machine and nothing needs to go over the network also allowing for use offline. Using PyInstaller I was able to package my Python application that was comprised of the following components into a single executable:

- Front End: [NiceGUI](https://nicegui.io/)
- Back End: [SQLModel](https://sqlmodel.tiangolo.com/)
- Database: SQLite

Additionally, the installer for the execuatable is available for download in the repository (for anyone that wants to check it out for themselves)!

### Front End: NiceGUI

I went with NiceGUI because I wanted to iterate quickly and NiceGUI does all the heavy lifting required for creating a beautiful web UI. Additionally, it allows you to change a flag in the `ui.run()` command where you can enter `native=True` and your web app will display as an electron-like app on your desktop. Also, NiceGUI has a wonderful community where new programmers to the library like myself can come and ask questions and many of the founders and contributors will gladly support your efforts by answering questions. You can join their [Discord](https://discord.gg/AjjD2EeR) and participate!

### Back End: SQLModel

Again, for the sake of speed, I chose SQLModel which is a great python library that allows you to create and interact with SQL databases/tables extremely efficiently as well as intuitively using python code. Also, SQLModel integrated well with the NiceGUI user interface and allowed me to connect the user input to be saved to the database and fetch that information as well.

## Future Work/Improvement Ideas

So I learned a lot during this project as it was my first foray into making a desktop application. And while I think it came put great there are some ideas that I think would make it better:

- API: I went without making an actual API for the app since it was small enough. But if it was to expand that I would using the native FastAPI integration within NiceGUI to do that
- Modularize Frontend: Again, it was a smaller app so I created the entire front end in the `main.py`, if it is to grow I would want to break it up
- Database in App Local: Currently the database is created in the same directory (in Program Files) as the application. I wasn't aware that the app would need admin permissions in order to interact with the sqlite file in the directory. So as a improvement I would create the DB in a directory that needed lower permissions to interact with like App Local.
