# RentersReview

## What is going on?
This is a platform letting renters share their thoughts about the places thay they have rented. This is the capstone project for the [Udacity Full Stack Development Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## What is covered?
This project will cover the followings:
- Data modeling
- APIs
- Authentication and Authorization
## What is not covered?
The front end is not implemented here, it will be a seperate project.

### Roles
In this platform we have 4 levels of users.
- Unregistered users who can read the content
- Registered users who can add new places, leave comments and like comments
- Admin user who can edit and delete places and comments. Admin users also can lock and unlock users.
### APIs

`GET /places`
```json
```

`GET /places/<int:id>`
```json
```

`POST /places`
```json
```

`DELETE /places`
```json
```

`GET /places/<id:int>/comments`
```json
```

`POST /comment`
```json
```

`DELETE /comment`
```json
```

`PUT /comment`
```json
```

`POST /like`
```json
```

`DELETE /like`
```json
```

`GET /comment/<int:id>/likes`
```json
```

`GET /users`
```json
```

`POST /users`
```json
```

`DELETE /users`
```json
```

`GET /users/<int:user_id>`
```json
```
