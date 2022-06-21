# DRS





## Usage


All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response"
    "message": "Description of the performed action"
}
```


### List all devices


** Definition **

`GET /posts`

** Response**

- `200 OK` on success


```json
[
    {
        "userId": "1",
        "title": "dolorem dolore est ipsam",
	"body": "dignissimos aperiam dolorem qui eum\nfacilis quibusdam animi sint suscipit qui sint possimus cum\nquaerat magni maiores excepturi\nipsam ut commodi dolor voluptatum modi aut vitae"
    },
    {
	"userId": "2",
        "title": "voluptatem eligendi optio",
	"body": "fuga et accusamus dolorum perferendis illo voluptas\nnon doloremque neque facere\nad qui dolorum molestiae beatae\nsed aut voluptas totam sit illum"
    }
]
```


### Adding a new post


** Definition **

`POST /posts`

** Arguments **

- `"userId": integer` a globally unique identifier for the user/author of the post
- `"title": string` title of the post
- `"body": string` body of the post

** Response **

- `201 Created` on success

```json
    {
        "userId": "1",
        "title": "dolorem dolore est ipsam",
	"body": "dignissimos aperiam dolorem qui eum\nfacilis quibusdam animi sint suscipit qui sint possimus cum\nquaerat magni maiores excepturi\nipsam ut commodi dolor voluptatum modi aut vitae"
    }
```


## Lookup a post by the id of the post


`GET /posts/by_id/<id>`

** Response **

- `404 Not Found` if the post does not exist
- `200 OK` on success

```json
    {
        "userId": "1",
        "title": "dolorem dolore est ipsam",
	"body": "dignissimos aperiam dolorem qui eum\nfacilis quibusdam animi sint suscipit qui sint possimus cum\nquaerat magni maiores excepturi\nipsam ut commodi dolor voluptatum modi aut vitae"
    }
```

## Lookup a post by the id of the user


`GET /posts/by_userId/<userId>`

** Response **

- `404 Not Found` if the user does not have any posts
- `200 OK` on success

```json
    {
        "userId": "1",
        "title": "dolorem dolore est ipsam",
	"body": "dignissimos aperiam dolorem qui eum\nfacilis quibusdam animi sint suscipit qui sint possimus cum\nquaerat magni maiores excepturi\nipsam ut commodi dolor voluptatum modi aut vitae"
    },
    {
	"userId": "1",
        "title": "voluptatem eligendi optio",
	"body": "fuga et accusamus dolorum perferendis illo voluptas\nnon doloremque neque facere\nad qui dolorum molestiae beatae\nsed aut voluptas totam sit illum"
    }
```

## Delete a post

`DELETE /posts/<id>`

** Response **

- `404 Not Found` if the post does not exist
- `204 No Content` on success