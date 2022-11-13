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
- None member users. This users can only view places and comments.
- Members users. Members can do all the actions that a none member user can do plus they can add new places, leave comments and like comments
- Admin users. Admins can perform all the actions that member users can plus they can edit and delete all places and comments.
- Super admin. super admin users can perform all the actions that admin users can plus they can bulk delete places and view other users information.
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
