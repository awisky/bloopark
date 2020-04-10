# Odoo 13 Small Business Modules

I developed this module focusing on small business retail stores as part of my test for [Bloopark](https://bloopark.de/en_US/) I was encouraged to build something original and mainly focused on Odoo. So maybe you will find some issues on Docker, Nginx or Postgres configurations that could be done better, but as I said it was no the main goal. My idea was to create a set of tools that makes the workflow faster.

[Video Demonstration](https://youtu.be/cMHHdh0H7VA)

## Main Goals

- Custom Text Search. This means that you can search using part of the words you remember even if you don't remember the order. Ex. 'De Blac'  or 'D lack' will work to find 'Black Desk' description.
- Multiple product selection. This means that you can add or trim multiple products of your sale or purchase order while they are in draft state.
- Quick Creation. This means that you can create a sale or purchase order from the Search Assistant if you call it from the main menu of each document.
- Stock Calculation. This means that you can see the available stock quantity of each product based on the stock date and warehouse filters. 
- Rank (*) Developing

## Installation Considerations

As a requirement for my case test I needed to build a Docker Ready solution. 
So that is why this is an [Odoo](https://www.odoo.com/es_ES/) 13.0 instance running inside a [Docker](https://www.docker.com) container with [Postgres](https://www.postgresql.org) and [Nginx](https://www.nginx.com). 
Everything is Opensource.

You need Docker installed if you want to run it as I built it.
You can test it without Docker too, just add search_asisstant module inside your Oddo addons path. 
Restart Odoo and update your apps list and should see it. 
I personally use iOs or linux but these instructions are kind of universal commands, so it should work in Windows command terminal too.


## Instructions

Change to your home directory:
```bash
$ cd ~
```
Create a Development folder or just use whatever you want.
```bash
~$ mkdir Development
```
Enter to Development folder
```bash
~$ cd Development
```
Clone this Repository (https://github.com/awisky/bloopark)

```bash
Development$ git clone https://github.com/awisky/bloopark.git
```
After clone is complete, enter inside the repository folder
```bash
Development$ cd bloopark
```
As this project depends on [OCA](http://odoo-community.org/) product-attributes modules. We must first clone this project inside our project. So inside our bloopark folder enter to addons-oca folder.

```bash
bloopark$ cd addons_oca
```
Now we can clone the Oca Products-Attribute Branch 13.0 repository

```bash
$ git clone -b 13.0 --depth=1 https://github.com/OCA/product-attribute
```
After cloning we go back to our main project folder with:

```bash
bloopark$ cd ..
```

Now we are ready to run our Docker Container. 
```bash
Development$ docker-compose up --build
```
After a couple of minutes you should see every service up and running.

## Initial Odoo Setup

After Docker container is running you must do a few step in your new Odoo instance.

- Create a new database with demonstration data
- Install Search Assistant module
- Setup the default partner for sales and purchases on Settings -> Search Assistant
- Grant access to the users on User Settings or Group Settings. Select Search Assitant User checkbox. 
- Reload Odoo web page (F5) to reload the menu. You will see the Search Assistant menu on Sales and Purchase

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[LGPL version 3 ](http://www.gnu.org/licenses/lgpl-3.0.en.html)