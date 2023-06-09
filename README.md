###MyBlogApp
MyBlogApp is a Django-based web application for creating and managing blog posts.

###Features
- User registration and authentication 
- Create, update, and delete blog posts 
- Comment on blog posts 
- Like and dislike blog posts 
- Search functionality to find blog posts by title or content 
- User profile management 
- Installation

###Installation
1. Clone the repository:

```bash
git clone https://github.com/rohinizade27/MyBlogApp.git
```
2. Create a virtual environment: 

```bash
python -m venv myblogenv
```
3. Activate the virtual environment:


- On Windows:

```bash
myblogenv\Scripts\activate
```
- On macOS and Linux:

```bash
source myblogenv/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Apply database migrations:

```bash
python manage.py migrate
````

6. Create a superuser:
```bash
python manage.py createsuperuser
````
7. Start the development server:
```bash
python manage.py runserver
````
8. Access the application at http://localhost:8000 in your web browser.

###Usage
Register a new user account or log in with an existing account.
Create blog posts by clicking on the "Add new Blog" button.
View and manage your blog posts on the dashboard.
Click on a blog post to view its details, comments, and likes.
Search for specific blog posts using the search functionality.
Edit or delete blog posts using the respective buttons.
Leave comments on blog posts.
Like or dislike blog posts by clicking on the thumbs-up or thumbs-down icons.

###Acknowledgements
The project is based on the Django web framework.
The application uses Bootstrap for styling