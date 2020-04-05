# Odoo 13 Small Business Modules

I developed this modules focused on small business retail stores as part of my test for [Bloopark](https://bloopark.de/en_US/)
I was encourage to build something original and mainly focused on Odoo. So maybe you will find some issues on Docker, Nginx or Postgres configurations that could be done better, but as I said it was no the main goal.
My idea was to create a set of tools to allow small stores to be more efficent using odoo.

## Main Goals

- Create another way to start sales and purchase workflows. Starting point: Products.
- Create another way to search products on Sales and Purchases.
- Create Rank Index based on Sales Stats (*)
  Define products rank positions. Bot for Stats and Index Calculations.
- Use Rank Index on Search Assistant. (*)
  Define products Rack Location = Rank Index
  Add Rank on Sales, Purchases and Inventory Views. 
  This means that the store will arrange the inventory following the rank index as a rack position.
  Like JIT methodology. Most Important products closer.
- Purchase Asisstant based on Rank Index  (*)
  Buy just what you really need, based on Ranks.

 (*) Working on it


## Installation Considerations

As a requirement for my case test I needed to built a Docker Ready solution. 
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
Clone this repository

```bash
Development$ git clone https://github.com/awisky/bloopark.git
```
After clone is complete, enter inside the repository folder
```bash
Development$ cd bloopark
```
As this project depends on [OCA](http://odoo-community.org/) product-attributes modules. We must first clone this project inside our project. So inside our bloopark folder enter to addons-oca folder.

```bash
bloopark$ cd addons-oca
```
Now we can clone the Oca Products-Attribute Branch 13.0 repository

```bash
$ git clone -b 13.0 --depth=1 https://github.com/OCA/product-attribute
```
After it finish we go back to our main project folder with:

```bash
bloopark$ cd ..
```

Now we are ready to run our Docker Container. 
```bash
Development$ docker-compose up --build
```
After a couple of minutes you should see every service up and running.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[LGPL version 3 ](http://www.gnu.org/licenses/lgpl-3.0.en.html)