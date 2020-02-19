# GET WORDPRESS USER LIST

I was recently tasked to provide a list of all the WordPress users that are present on all our WordPress servers in all our environments. The requirement was to produce a single csv file with all the required data : 


User Login  
Display Name  
User Email  
Registered Date  
Roles  
Project  
Environment  
Location  

We had 6 Wordpress Servers, in 6 different environment and each server had over 10 projects with multiple users per project. 

An example of a single output row would look like:

michaelhyland,michaelhyland,michael.hyland@emailaddress.com,2017/11/14 13:30,administrator,as400,production,p21

I use the [Paramiko](https://www.paramiko.org/) Python module to connect to each server. To get the user detail, I use the [WordPress CLI](https://wp-cli.org/) and converted the user output details to comma delimited output with the additional requirements. Each server output is gathered into it's own csv file and I use the [Pandas](https://pandas.pydata.org/) python library to combine all the csv files into a single file.

In the end I was able to gather over 7000 rows of user details from all our WordPress servers into a single file.
