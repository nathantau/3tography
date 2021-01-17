## 3tography API

### `GET`

#### Authenticated

`/api/authenticated`

Returns whether or not the current user's access token is valid and thus, whether the user is authenticated.

```
Authorization: Bearer {accessToken}
```

#### Me

`/api/me`

Returns the user's information including username, profile description and image URLs.

```
Authorization: Bearer {accessToken}
```

#### Following

`/api/following`

Returns the list of accounts that the user is following (their image URLs and usernames respectively).

```
Authorization: Bearer {accessToken}
```

#### Search

`/api/search?user={candidate}`

Returns a list of usernames that are similar to the candidate string.

```
Authorization: Bearer {accessToken}
```

### `POST`

#### Register

`/api/register`

Registers a user in the database.

```json
Content-type: application/json

// Sample Request
{
    "user": "nathan",
    "password": "ILoveMikasaAckerman"
}

// Sample Response
{
    "registered": true
}
```

#### Login

`/api/login`

Logs a user in and returns an access token.

```json
Content-type: application/json

// Sample Request
{
    "user": "nathan",
    "password": "ILoveMikasaAckerman"
}

// Sample Response
{
    "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTA4MzkyNjgsImlhdCI6MTYxMDgzMjA2OCwic3ViIjoibmF0ZSJ9.FAY6GzC098aSpky_bdToAxrQ9YBtuGwznAKV_B-F4mc"
}
```

#### Follow

`/api/follow`

Follows a user that is not currently being followed.

```json
Authorization: Bearer {accessToken}
Content-type: application/json

// Sample Request
{
    "user": {userToFollow}
}

// Sample Response
{
    "followed": true
}
```

#### Unfollow

`/api/unfollow`

Unfollows a user that is currently being followed.

```json
Authorization: Bearer {accessToken}
Content-type: application/json

// Sample Request
{
    "user": {userToUnfollow}
}

// Sample Response
{
    "unfollowed": true
}
```

#### Description

`/api/description`

Updates the user's profile description.

```json
Authorization: Bearer {accessToken}
Content-type: application/json

// Sample Request
{
    "description": {newDescription}
}

// Sample Response
{
    "updated": true
}
```

#### Upload

`/api/upload`

Uploads an image to the user's personal repository.

```json
Authorization: Bearer {accessToken}

// Sample Request (Form data)
File: {file}
Pos: {"one"/"two"/"three"}

// Sample Response
{
    "uploaded": true
}
```



