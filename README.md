[![Website](https://img.shields.io/website?up_message=http%3A%2F%2F3tography.nathanau.ca%2F&url=http%3A%2F%2F3tography.nathanau.ca%2F)](http://3tography.nathanau.ca)

# Threetography

A minimalistic photo-sharing platform and potentially one of my dumbest ideas to date. But the tech stack is cool tho so I don't really care lol.

**Features**

- Follow/unfollow friends/influencers
- Upload your own 3 images
- Change your profile description

**What's so special about it**

I'm going to be reaching a little bit here but bear with me. The problem with Instagram is that there is no limit to the amount of media that users can upload. Thus, each profile becomes filled with useless clutter. However, imagine being forced to express yourself with only 3 images - how much more special and significant would each of these uploads be?

---

## Project Summary

### Demo

![Systems Design](assets/demo.gif)

### Tech Stack

For this project I used a `React` frontend and a `Flask` backend supported by a `Postgres` database. Each of these components are deployed as `Docker` containers in a `Compose` cluster. I also used `AWS S3` for cloud storage.

### Architecture

I'm way too lazy to make another one of them system design diagrams online so I drew one instead.

![Systems Design](assets/3tography-systems-design.png)

### How it works

Okay boys and girls this is how it works. When a user uploads their own images onto the platform, it is uploaded into Amazon S3. Then, a presigned URL is generated using temporary AWS credentials (this allows anyone with the URL to view the image) and saved to the user's row in the Postgres database. Because the URLs expire every 8 hours, the URLS are essentially *cached* in the database and do not require regeneration unless they are within an hour of expiry (the backend handles this).

### How to run

To run, simply ensure you have `Docker` installed as well as have an `AWS` account. Then run the following:

**Create AWS credentials file**

```sh
# Create directory
cd src/
mkdir .aws
cd .aws

# Insert AWS credentials
cat > credentials
[default]
aws_access_key_id = {yourAWSKeyId}
aws_secret_access_key = {yourAWSSecretKey}
cd ..
```

**Launch containers**
```sh
# Start containers from root directory (src/)
docker-compose up
```

**Initialize table**
```sh
# Run Postgres table initialization in container
dc exec backend psql -f utils/init_table.sql
```

Hence, the 3 containers should be up and running!

**Deploying**

If this is deployed onto a cloud VM, be sure to modify `app.env` and change the values of `REACT_APP_FLASK_HOST` and `REACT_HOST` accordingly.

- `REACT_APP_FLASK_HOST`: Host of backend, defaulted to `http://localhost:5000`
- `REACT_HOST`: Host of frontend, defaulted to `http://localhost:3000`

For local purposes, the above can be ignored (unless the ports configured in `docker-compose.yml` are modified).

### Reflections

I'm very happy to have used `Docker Compose` from the beginning for development purposes. It really helped with the dependency management and it was really fun using the stuff I learned from my last co-op. Unfortunately, my dumbass got ahead of myself and tried making a `Postgres` engine from scratch so that took out a lot of development time, and I also ended up scrapping it :(.

---

## Backend API

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

```
Authorization: Bearer {accessToken}
Content-type: application/json
```

```json
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

```
Authorization: Bearer {accessToken}
Content-type: application/json
```

```json
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

```
Authorization: Bearer {accessToken}
Content-type: application/json
```

```json
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

```
Authorization: Bearer {accessToken}
```

```json
// Sample Request (Form data)
File: {file}
Pos: {"one/two/three"}

// Sample Response
{
    "uploaded": true
}
```
