## CSS 348 - Advanced Database Management Systems

# **influence**

Influence is a community publishing platform, willfully blurring the lines between blogging and social networking. This is a web application.
It is home to a wide array of creative individuals looking to share common interests, meet new friends, and express themselves.
Our product will empower people to share ideas, offer support and make a difference.
We want to help them learn, work, communicate and have fun.

Influence encourages communal interaction and personal expression by offering a user-friendly interface and a deeply customizable blog system.
The service's individuality stems from the way highly dedicated users utilize our simple tools, along with the instinct for individual expression, to create new venues for online socializing.

With topics like politics, entertainment, fashion, literature and design, some key similarities emerge: the overall culture is distinctly open source-not only from a product perspective-but from a cultural one. The spirit of volunteerism pervades Influence, crossing all boundaries and propagated via insanely passionate individuals. At Influence creativity, diversity and tolerance are the mainstream.

***

### Our Principles:

#### Self-Expression
Our tools allow our user community to communicate with each other in immediate and creative ways. We believe in letting our users create their own content, to choose how they express themselves, their thoughts, and their feelings.

#### Diversity
We welcome and respect different opinions, different cultures, and different perspectives, and are committed to helping our users share their diversity with others. LiveJournal brings people of various backgrounds together, and strongly supports freedom of expression.

#### Creativity
We encourage our user community to use Influence to share the process of creating their content with friends. We believe that everyone has something to offer, whatever form it may take, and want to make it easy for our users to share that with the world.

#### Community
Influence thrives because of loyal users and active community volunteers. We're committed to collaborating with the community in order to improve the service for everyone, so we work to incorporate member feedback into our product and technical decisions. The Influence community enjoys an unprecedented amount of inspiration and input into product and policy decisions.

#### Privacy
We make sure to safeguard our users' private blog entries but also provide tools that allow them to choose with whom to share the content they want to share, be it with just a small group of friends, or with a larger user-created community. We respect the decisions our users make, and let them decide how to protect the content they create. We continue to maintain the service that the Influence community trusts.

***

<h2 id="functions-and-features">Functions and Features</h2>

- Reader-friendly interface

- Authorization / Registration

- Categories

- Views

- Likes

- Comments

- Search

- Post

- Follow

***

## Technologies

### **User interface**

We are going to build a full web application.

Advantages:
Reaching a Wider Audience <br>
The first and perhaps most obvious advantage of a website is the potential for reaching a wider audience. The internet is used by literally millions of people, all of them are looking for something and some of them might be looking for you!

Anyone, Anywhere & Anytime <br>
An advantage of having a website is your valuable information and details about your products and services can be accessed by anyone, no matter where they are on the planet or what time of day it is.

Easy Access To Information <br>
With a website, users can easily access information about your business. They can see what products or services you sell, your prices, your location and much more. Whatever you decide to tell them, they can find it with a few clicks of a mouse.

<br>

### Programming language: **Python**

### **♕ Django**

Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source. 

**Why Django?**

With Django, you can take Web applications from concept to launch in a matter of hours. Django takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

**Ridiculously fast.**

Django was designed to help developers take applications from concept to completion as quickly as possible.

**Fully loaded.**

Django includes dozens of extras you can use to handle common Web development tasks. Django takes care of user authentication, content administration, site maps, RSS feeds, and many more tasks — right out of the box.

**Reassuringly secure.**

Django takes security seriously and helps developers avoid many common security mistakes, such as SQL injection, cross-site scripting, cross-site request forgery and clickjacking. Its user authentication system provides a secure way to manage user accounts and passwords.

**Exceedingly scalable.**

Some of the busiest sites on the planet use Django’s ability to quickly and flexibly scale to meet the heaviest traffic demands.

**Incredibly versatile.**

Companies, organizations and governments have used Django to build all sorts of things — from content management systems to social networks to scientific computing platforms.

<br>

### Database: SQL

### **♔ SQLite**

**What Is SQLite?**

SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. SQLite is the most used database engine in the world. SQLite is built into all mobile phones and most computers and comes bundled inside countless other applications that people use every day.

The SQLite file format is stable, cross-platform, and backwards compatible. SQLite database files are commonly used as containers to transfer rich content between systems and as a long-term archival format for data. There are over 1 trillion SQLite databases in active use.

SQLite source code is in the public-domain and is free to everyone to use for any purpose.

SQLite emphasizes economy, efficiency, reliability, independence, and simplicity.

Situations Where SQLite Works Well:

- Server-side database

- Websites

- File archive and/or data container

- Cache

- Data analysis

- Embedded devices and the IOT

***

## Questions

1. How does commenting on a post-work?

The comment table associated with the post and account tables by their IDs. When an account comments on someone's post, the text comment will be inserted in the “comment_text” column with the automatically incrementing “comment_id” and “post_id”, ”account-id”.


2. What if an account wants to register on the site, but his email address is already registered?

First, the account can use a password to log in to their account. If it doesn't remember, the account can log into their account using the "forgot password" feature. Then a message about account recovery is sent to the client's email address. After confirming the ownership of the mail, the account can change the password and other data on the site.

3. How does an account log in to the site?

The account enters their email address and password to form and with POST method and server searches from the database the input email and checks the input password with an active password. If they are equal then the account logs in.

4. How images are arranged in publications?

“post” table joins with tables like “image”, “image_post” by post_id and image_id. Out of here, the post searches for all images that belong to it and shows them in the post container.

5. How does a follow action works?

The account can follow other accounts, by the “follow” feature. It works like, the account’s(follower) id and selected account’s(leader) id inserts into the “follow” table.

6. Can the author see the owner of the like?

Yes, their can. Each post joins with “like” and “accounts” tables. If some account puts like to post, the account’s “account_id” and the post’s “post_id” save in the “like” table. Thus, giving access to maintain the ownership of the like.

7. How do categories switch?

Every category has its own id, and every category name in the navigation bar in its own links have something like id. Every time, when the account selects a category, the feed changes the category id, and of course, posts. Because the “post” table joins with the “category” table by “category_id”.

8. Why is there information about the date in the comments, but not in the likes?

Comments may help an account with some useful information, and information can change tomorrow. Maybe after adding a comment to the post, this information is already outdated. That's why, every account should see the date of the comment, so as not to get confused. Like does not carry such an important role.

9. If I have an unwanted subscriber, how can I get rid of it?

To do this operation, you must be logged in, then in the subscriber's department delete the account that you selected, if everything is successful, this account will be removed from your subscribers.

10. Find the total number of subscribers of authors, whose name length is between 3-5. Search it only in posts, which category names length is less than 6.

First, join “follow”, “account”, “category”, “post” tables. Find posts with a category name length is less than 6, after, take an account_name from it and check the length by 3,5 letter limit. Finally, output count of subscribers of the accounts.

11. Find min length name of the account, who liked a post, with a category name, which length is more than 4, and followed by more than 10 accounts?

Join “post”, “category”, “follow”, “accounts” tables. Then, find posts, which are with category name, which length is more than 4, after by “follow” table columns count followers of the account, if followers are more than 10, then output the min length name from the accounts.

12. How works the rendering of the post?

First things first, when a post renders on the site, it requires some pieces of information from “account”, “like”, “comment”, “image”, “image_post” and also, “category” tables. A server takes the account name, avatar and category name, date, title, content, like’s amount, amount of view and finally, comments of the post and puts them together.

13. How many likes does the post have, with categories name’s length is more than 4, and who are its owners?

To do this, we will join the "like" table with “post” and “account”, “category”. Find posts with categories name’s length more than 4, and in order to see the number of likes, we can check the “post.like_count” value. Then, output “post.like_count” value,  the column “like.account_id” value.
 
14. Is the commentator of the post, which is called "Golden Park", and has a couple of pictures, liked the post and is he the follower of the author? If yes output the name of the commentator.

We will join tables “comments”, “post”, “account”, “follow” and “postImage”. Then, If the value of “post.title” is “Golden Park” and If the commentator id exists in the “like.account_id” column, and If the commentator id exists in the “follow_id” output name of the commentator.

15. Is the subscriber the author of a post that has more than 30 likes, and the category name length is more than 4, and the number of images of the post is more than one? If yes, output subscriber name.

For this question, we must join the “follow”, “post”, “category”, “postImage” tables. After that, if in the table "follow" the account's id exists and in the "post" table if its id exists in "post.account_id" and the value of "post.like_counter" is more than 30, If the length of "category.name" is more than 4 and finally, count the rows in the table "postImage", if the count is more than one, output the name of the subscriber.

16. Find the name of the account that left comments in November last year on the publication called "Player of the Year", which is among those who put a like, there is a user named "Ivan"

To solve this problem, we need to join the tables "account", "comment", "post", "like". After, find comments that left the account in November last year by checking the value of “comment.date” column. Then, find if exists a post named “Player of the Year” and via “like” table, a check is there an owner named "Ivan", output the account name.

***

## Link to a dataset for the project:
https://drive.google.com/drive/folders/1JFoSSLcWD-iCh6jkggGZKUH9WsSo9pL4?usp=sharing

***

## Table structures

<pre>
account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password TEXT NOT NULL,
    image_id INT
);

post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INT NOT NULL,
    category_id INT,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_date DATETIME DEFAULT current_timestamp,
    like_count INT DEFAULT 0,
    view_count INT DEFAULT 0
);

comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INT NOT NULL,
    account_id INT NOT NULL,
    content TEXT NOT NULL,
    added_date DATETIME DEFAULT current_timestamp
);

category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

image (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL
);

likes (
    post_id INT NOT NULL,
    account_id INT NOT NULL
);

subscriptions (
    account_id INT NOT NULL,
    following_id INT NOT NULL
);

postimages (
    post_id INT NOT NULL,
    image_id INT NOT NULL
);
</pre>

***

## Use-case diagram

![influence-UseCase-UML](./influence-UseCase-UML.png "influence-UseCase-UML")
