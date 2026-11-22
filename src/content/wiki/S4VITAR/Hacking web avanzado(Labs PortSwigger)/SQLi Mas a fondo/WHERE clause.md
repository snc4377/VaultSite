The application executes an SQL query that searches for products in a specific category that are already published. The goal is to alter this logic to also view unpublished products.

To achieve this, we intercept the request sending the selected category and modify its value by adding an '**OR 1=1**' condition, which forces the query to return all products regardless of their published status. Additionally, a trailing comment is used to ignore the remainder of the original query.

This attack demonstrates how simple user input manipulation can completely alter the backend SQL logic behavior.

**Key takeaway**: A well-placed SQL injection in a WHERE clause allows accessing data that should be hidden. It's one of the most basic yet effective exploitation methods.

---

This lab focuses on an SQLi vulnerability in the product category filter.

When a user selects a product category, the website application executes an SQL query like the following:

`SELECT * FROM products WHERE category ='gifts' AND released = 1`
![[Pasted image 20260414182320.png]]
![[Pasted image 20260414183409.png]]
![[Pasted image 20260414183424.png]]

In this query, our INPUT is the category parameter ("gifts" in this case):
`SELECT * FROM products WHERE category ='gifts' AND released = 1`

We can modify our input to display, for example, unreleased products.

If we add a ' in our URL, the query becomes:
`SELECT * FROM products WHERE category ='gifts'' AND released = 1`
Here the query closes at 'gifts' but leaves another ' open, allowing us to insert our malicious SQLi statement like `or 1=1 -- -` (where -- - comments out everything remaining).
![[Pasted image 20260414184454.png]]
