# Individual project: Portfolio creation

## Context

In this task, you will use your knowledge in object-oriented programming to create an online presence for yourself as a Data Scientist.

There are three aspects to OOP in the wild. First, OOP is a paradigm as you write a program to structure it. Second, OOP is a perspective with which to approach problems and how to see the world. Third, OOP is a mindset with which you can approach problems and act upon the world.

This project tries to introduce you to OOP in the wild. As you create a website with
github pages, OOP is not necessary the first mode (web rendering is usually based
on static html code that is not a priori OOP. However, to represent complex
websites, you use more complex features and using OOP may help you. You will
not learn html coding or css style sheets but you will use your knowledge of OOP
concepts to instruct github copilot to help you create an interactive, interesting
portfolio.

The second aspect is to show your data prowess, and we do this by embedding a
shiny application server in your website. Github pages cannot execute code.
However, you can use external services like the posit connect cloud to have an
interactive window that executes python code. In this window, you are supposed to
showcase your previous data science projects. You may investigate yourself how
shiny works (and receive a short introduction in the class). Essentially, shiny makes
graphs interactive and allows users to interact with your outcome visualisations. As
a preparation, please revisit your previous work and find one to three projects, that
you would like to highlight. To expand your portfolio, I would recommend you to
add new results from other data science projects throughout your studies to
showcase what you can do.

## Grading

To complete this project, you have to create your online presence and fill it with
content of your choice. You _will not be graded_ for your actual content or the looks of
your website. Instead, you will be graded on how you executed the project and how
well you managed to implement OOP principles in the website.

Please investigate my github example here:
https://github.com/jugdemon/2026_oop_portfolio

And the corresponding github-pages:

https://jugdemon.github.io/2026_oop_portfolio/

You may either fork the repository (create a copy to start with), or start from
scratch. You fill find instructions for both below.

1. Create your github repository called “portfolio”. This will allow us to create
    your portfolio/personal website under https://<user>.github.io/portfolio
    where user is your github user name.
       a. Use the repo link https://github.com/<user>/portfolio.git to setup your
          cloud computing and visual studio in the following steps
2. Create a posit connect cloud account via github integration.
    a. Here you can create data spaces for python to host your shiny app and
       display information interactively.
    b. Select you want to deploy both apps and documents.
    c. Select you prefer python.
3. Install VS Code and activate all AI features via github integration. If you have
    the github student version, you get more advanced features. Activate your
    student version if you haven’t yet.
       a. Go to the market place and install extensions for python, quarto and
          shiny.
4. Start a chat on the right side. Ask the chat to create a project for your
    portfolio that uses quatro as a website and shiny for the visualization. The shiny server should run on posit cloud using the python version. All the code should be synced to your portfolio repository.