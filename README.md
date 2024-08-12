# Commis
## A Recipe Finder and Uploading Web Application
#### Video Demo: <https://youtu.be/8B0mfFtzcpw>
#### [Link](https://github.com/mmf7992/CS50x-Final-Project-Commis-/blob/main/templates/login.html)

### Overview
Commis is a web application that allows users to discover, rate, and share recipes. It provides an intuitive interface for browsing recipes, viewing details, and engaging with other users through comments and ratings. Users can also upload their own recipes and maintain a history of their interactions with the platform.

#### Description
### 1. User Authentication

**Commis** provides a secure authentication system allowing users to register, log in, and manage their accounts. Using password hashing with Flask’s built-in `werkzeug.security`, the application ensures that user credentials are protected. Users can:

- **Register**: Create a new account by providing a username, password, and password confirmation.
- **Log In**: Access their account using their registered credentials.
- **Log Out**: End their session securely and return to the home page.

### 2. Recipe Management

Users can upload and manage their recipes with ease. The recipe management feature allows users to:

- **Upload Recipes**: Submit new recipes with details such as title, ingredients, instructions, difficulty level, and an image.
- **Edit Recipes**: Modify existing recipes to update details or correct information (feature to be added in future updates).
- **Delete Recipes**: Remove recipes that are no longer needed (feature to be added in future updates).

### 3. Recipe Discovery

The application provides a rich interface for browsing and discovering recipes:

- **Home Page**: Users can view a curated list of recipes with the most popular ones featured prominently.
- **Search Functionality**: Search for recipes by title or ingredient to find exactly what you’re looking for.
- **Recipe Details**: Click on a recipe to view detailed information including ingredients, instructions, and user ratings.

### 4. Rating System

Users can rate recipes to help others make informed decisions:

- **Upvote/Downvote**: Users can express their opinion by upvoting or downvoting recipes. Ratings are handled incrementally, allowing for nuanced feedback.
- **Rating Display**: View the cumulative rating of a recipe based on user interactions.

### 5. Commenting

Add comments to recipes to share feedback, tips, or personal experiences:

- **Add Comments**: Submit text comments on recipes, providing insights or asking questions.
- **View Comments**: Read comments left by other users to gather additional perspectives on a recipe.

### 6. History Tracking

**Commis** tracks the recipes a user has viewed:

- **View History**: Access a list of previously viewed recipes, making it easier to revisit favorites.

## User Interface

**Commis** features a visually appealing and intuitive user interface designed with a modern aesthetic:

- **Background**: The application uses a **marble background**, providing a sleek and sophisticated look that enhances readability and adds a touch of elegance to the user interface.
- **Navigation Bar**: The **navbar is styled in a soft pink color**, offering a pleasant contrast to the marble background and making navigation elements stand out. The navbar is responsive, ensuring that it looks great on both desktop and mobile devices.

### UI Description

- **Homepage**: The homepage features a clean layout with a grid of recipe cards. Each card displays a recipe image, title, difficulty, and a brief description. The use of large, eye-catching images and clear text ensures that users can quickly scan and find interesting recipes.
- **Recipe Details Page**: This page presents detailed information about a selected recipe. The image is prominently displayed, followed by the recipe title, difficulty level, ingredients, and instructions. Comments and rating sections are clearly separated to enhance user interaction.
- **Upload and Profile Pages**: The upload page has a simple form layout, with fields for entering recipe details and uploading an image. Profile and login pages are designed with user accessibility in mind, featuring large input fields and clear instructions.


