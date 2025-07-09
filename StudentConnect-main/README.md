# StudentConnect

A social platform for students featuring posts (notes, jobs, threads), user profiles, and file sharing.

## Tech Stack

- **Frontend**: React.js with Material-UI
- **Backend**: FastAPI with Python
- **Database**: MongoDB
- **File Storage**: Cloudinary
- **Authentication**: JWT with bcrypt hashing

## Features

### Login Page
- Sign up
- Login 
- Forgot password functionality

### Main Page
- Tab navigation: Posts, Profile
- User authentication with JWT

### Posts Tab
- 3 types of posts:
  1. **Notes**: Document upload (Cloudinary), download option, tags (subjects)
  2. **Jobs**: Job opening links, referrals
  3. **Threads**: Comments and replies
- Filter and search functionality
- Search by title, tags, username, or name
- Filter by category (notes, jobs, threads)

### Profile Tab
- Display picture
- Name, username, bio
- Edit profile options
- View user's posts

### Additional Features
- View other user profiles through posts
- Hashed passwords with JWT authentication
- Responsive Material-UI design

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd "c:/StudentConnect/backend"
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the following variables in `.env`:
  ```
  SECRET_KEY=your-super-secret-key-here
  MONGODB_URL=mongodb://localhost:27017
  DATABASE_NAME=studentconnect_db
  CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
  CLOUDINARY_API_KEY=your-cloudinary-api-key
  CLOUDINARY_API_SECRET=your-cloudinary-api-secret
  ```

5. Install and start MongoDB:
- Download MongoDB Community Server
- Start MongoDB service

6. Set up Cloudinary account:
- Sign up at cloudinary.com
- Get your cloud name, API key, and API secret from dashboard

7. Run the backend server:
```bash
uvicorn main:app --reload
```

The backend will run on http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd "c:/StudentConnect/frontend"
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on http://localhost:3000

## API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `PUT /auth/profile` - Update profile
- `GET /auth/user/{username}` - Get user by username

### Posts
- `POST /posts/` - Create new post
- `GET /posts/` - Get all posts (with search/filter)
- `GET /posts/{post_id}` - Get specific post
- `GET /posts/user/{username}` - Get user's posts

### Comments
- `POST /comments/` - Create new comment
- `GET /comments/{post_id}` - Get post comments

## Project Structure

```
/StudentConnect
  /backend
    main.py              # FastAPI application entry point
    requirements.txt     # Python dependencies
    .env.example        # Environment variables template
    /models
      schemas.py        # Pydantic models
      database.py       # MongoDB operations
    /routes
      auth.py          # Authentication routes
      posts.py         # Posts routes
      comments.py      # Comments routes
    /utils
      auth.py          # Authentication utilities
      cloudinary.py    # Cloudinary utilities
  /frontend
    package.json        # Node.js dependencies
    /public
      index.html       # HTML template
    /src
      App.js           # Main React component
      index.js         # React entry point
      /components
        PostsTab.jsx   # Posts tab component
        ProfileTab.jsx # Profile tab component
      /pages
        LoginPage.jsx  # Login/signup page
        MainPage.jsx   # Main application page
      /contexts
        AuthContext.js # Authentication context
      /api
        api.js         # API client
```

## Development Notes

- The backend uses async/await with MongoDB motor driver
- JWT tokens are stored in localStorage on the frontend
- File uploads are handled via Cloudinary
- Material-UI provides the component library
- React Hook Form handles form validation
- The app is responsive and mobile-friendly

## Next Steps

1. Set up MongoDB database
2. Create Cloudinary account
3. Configure environment variables
4. Install dependencies for both frontend and backend
5. Start both servers
6. Test the application functionality

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Protected routes
- Input validation with Pydantic
- CORS configuration for cross-origin requests
