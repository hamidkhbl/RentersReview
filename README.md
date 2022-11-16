# RentersReview

## What is going on?
This is a platform letting renters share their thoughts about the places that they have rented. This is the capstone project for the [Udacity Full Stack Development Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

### What is covered?
This project will cover the followings:
- Data modeling
- Authentication and Authorization
- APIs
- API unit tests
### What is not covered?
The frontend for this project is minimal and only includes the log in, log out and refresh token functionalities.

## Setup
[Backend settup instruction](https://github.com/hamidkhbl/RentersReview/tree/dev/backend)

[Frontend setup instruction](https://github.com/hamidkhbl/RentersReview/tree/dev/fronend)
## Authentication and Authorization
In this project Auth0 is used as authentication and authorization provider. To call non public routes users need to sign in and get a valid token.

### Permissions
A full set of permissions looks like this.
```json
    "permissions": [
      "bulkdelete:place",
      "delete:comment",
      "delete:place",
      "patch:place",
      "post:comment",
      "post:like",
      "post:place",
    ]
```
### Roles
In this platform we have 4 levels of users.
- *None member users*. This users can only view places and comments.
- *Members users*. Members can do all the actions that a none member user can do plus they can add new places, leave comments and like comments.
Their permission array in the token should look like this:
```json
    "permissions": [
      "post:comment",
      "post:like",
      "post:place"
    ]
```
- *Admin users*. Admins can perform all the actions that member users can plus they can edit and delete all places and comments.
Their permission array in the token should look like this:
```json
    "permissions": [
      "delete:comment",
      "delete:place",
      "patch:place",
      "post:comment",
      "post:like",
      "post:place"
    ]
```
- *Super admin*. super admin users can perform all the actions that admin users can plus they can bulk delete places, import users from Auth0 to the database and view all users' information.
Their permission array in the token should look like this:
```json
    "permissions": [
      "bulkdelete:place",
      "delete:comment",
      "delete:place",
      "patch:place",
      "post:comment",
      "post:like",
      "post:place",

    ]
```
## APIs
Here is a list of all the APIs.

### Place routes
**`GET /places`**

Permission: None (This is a public API)

Response:
```json
{
    "places": [
        {
            "address": "East Broadway",
            "city": "Vancouver",
            "description": "",
            "id": 4,
            "latitude": "0",
            "longtude": null,
            "state": "BC",
            "title": "City Wide Building"
        },
        {
            "address": "East Hornby",
            "city": "Vancouver",
            "description": "",
            "id": 5,
            "latitude": "0",
            "longtude": null,
            "state": "BC",
            "title": "OMG"
        }
    ],
    "success": true
}
```

**`GET /places/<int:place_id>`**

Permission: None (This is a public API)

Response:
```json
{
    "place": {
        "address": "East Broadway",
        "city": "Vancouver",
        "comments": [],
        "description": "",
        "id": 4,
        "latitude": "0",
        "longtude": null,
        "state": "BC",
        "title": "City Wide Building"
    },
    "success": true
}
```


**`POST /places`**

Permission: ```post:place```

Payload:
```json
{
    "title": "New Place",
    "address": "East Hornby",
    "city": "Vancouver",
    "description": "",
    "latitude": "0",
    "longtude": "0",
    "state": "BC"
}
```

Response:
```json
{
    "place": {
        "address": "East Hornby",
        "city": "Vancouver",
        "description": "",
        "id": 5,
        "latitude": "0",
        "longtude": null,
        "state": "BC",
    "title": "New Place",
    },
    "success": true
}
```

**`PATCH /places/<int:place_id>`**

Permission:  ```patch:place```

Payload:
```json
{
    "title": "Wesley_patched",
    "address": "West Broadway",
    "city": "Vancouver",
    "description": "",
    "latitude": "34234",
    "longitude": "234234",
    "state": "BC"
}
```
Response:
```json
{
    "place": {
        "address": "West Broadway",
        "city": "Vancouver",
        "description": "",
        "id": 1,
        "latitude": "34234",
        "longtude": "234234",
        "state": "BC",
        "title": "Wesley_patched"
    },
    "success": true
}
```

**`DELETE /places`**

Permission:  ```delete:place```

Response:
```json
{
    "place": {
        "address": "West Broadway",
        "city": "Vancouver",
        "description": "By Yuacheng",
        "id": 3,
        "latitude": "0",
        "longtude": null,
        "state": "BC",
        "title": "OMG"
    },
    "success": true
}
```

### Comment routes
**`POST /comment`**

Permission: `post:comment`

Payload:
```json
{
    "description": "We lived here for about year",
    "place_id": 8,
    "title": "Nice place to live"
}
```

Response:
```json
{
    "comment": {
        "creation_date": "2022-11-13 20:17:39.938800",
        "description": "Nice place to live",
        "id": 3,
        "likes_count": 0,
        "place_id": 4,
        "title": "Nice place to live",
        "user_id": "636d42aa00f9138b729becf6"
    },
    "success": true
}
```

**`DELETE /comment`**
```json
```

**`PATCH /comment`**
```json
```

### Like routes
**`POST /like`**

If a comment is not liked, this API will add a like to the post. If the comment is already liked by the use it removes the like.

Permission: `post:like`

Payload:
```json
{
    "comment_id": 3
}
```
Response:
```json
{
    "success": true,
    "like": "added" // or "removed"
}
```

