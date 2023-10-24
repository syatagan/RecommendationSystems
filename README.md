<h1>Business Problem</h1>
The company, which is an online service platform, connects service providers with those seeking services. It enables easy access to services such as cleaning, renovation, and transportation with just a few taps on your computer or smartphone.
We want to create a product recommendation system using Association Rule Learning based on a dataset that includes service users and the services and categories they have received.
<h1>Dataset Story</h1>
The dataset consists of customers' received services and the categories of these services. It also includes the date and time information for each service received.
<h2>Features</h2>
<table>
<tr><td>UserId</td><td>Customer ID</td></tr>
<tr><td>ServiceId</td><td>Each category contains anonymized services. For example, under the "Cleaning" category, there may be services like "Couch Cleaning." A single ServiceId can be found under different categories, and under different categories, it may represent different services. For instance, a service with CategoryId 7 and ServiceId 4 could be "Radiator Cleaning," while a service with CategoryId 2 and ServiceId 4 could be "Furniture Assembly."</td></tr>
<tr><td>CategoryId</td><td>Category ID</td></tr>
<tr><td>CreateDate</td><td>Creation Date</td></tr>
</table>

<h4>Task 1 : Data Preprocessing</h4>
<h4>Task 2 : Create Association Rules and Give Recommendations<h4>

