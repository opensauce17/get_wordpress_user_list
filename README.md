# GET WORDPRESS USER LIST

I was recently tasked to provide a list of all the wordpress users that are present on all our wordpress servers in all our environments. The requirement was to produce a single csv file with all the required data : 


User Login  
Display Name  
User Email  
Registered Date  
Roles  
Project  
Environment  
Location  

We had 6 Wordpress Servers and each server had over 10 projects with multiple users per project. 

An example of a single output row would look like:

michaelhyland,michaelhyland,michael.hyland@kurtosys.com,2017/11/14 13:30,administrator,as400,production,p21

Each server output is gathered into into it's own csv file and I use the Panda python library to combine all the csv files into a single file. 
