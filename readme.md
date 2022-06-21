<br />
<h1 align="center">Python RESTful microservice API</h1>
<br />
<h2>Installation</h2>
<br />
<p><strong>Dependencies</strong></p>
<p>Python 3+, Docker Desktop</p>
<br />
<p><strong>How to install</strong></p>
<p>Run these commands in cmd/powershell, in the main directory of the program:</p>
<p><code>docker-build compose</code></p>
<p><code>docker compose up</code></p>
<br />
<p>Then you can access the API through the front end by a browser on <a>http://127.0.0.1:5000</a>, or by url calls on <a>http://127.0.0.1:5000/api/</a> - read below for more details.</p>
<br />
<h2>Usage through the front end - html website</h2>
<br />
<p>Front end can be accessed on '/' and subdomains '/posts', '/posts/add', '/search/id', '/search/userid', '/posts/edit', '/posts/delete'. For this usage documentation, the route is '/doc'.</p>

    All of this is accessed easily through the navbar at the top of the webpage.
    
    GET, POST, PUT, DELETE requests are handled through input forms which are self-explanatory.
    
    Html code was written with the help of extension Jinja2 to implement basic python expressions from the backend.
<br />
<h2>Usage through URL call</h2>
<br />
<p>All responses will have the form</p>
<p><code>json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of the performed action"
}</code></p>
<p>or</p>
<p><code>json
    {
        "error": "Description of the error occured"
    }</code></p>
<p>in the case of invalid data/errors.</p>
<h3>List all posts</h3>
<p><strong> Definition </strong></p>
<p><code>GET /api/posts</code></p>
<p><strong> Response </strong></p>
<ul>
	<li><code>200 OK</code> on success </li>
</ul>
<p><code>json
{
        "message": "Success",
        "data": [
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
}</code></p>
<h3>Adding a new post</h3>
<p><strong> Definition </strong></p>
<p><code>POST /posts</code></p>
<p><strong> Arguments </strong></p>
<ul>
	<li><code>"userId": integer</code> a globally unique identifier for the user/author of the post, is validated through an external API</li>
	<li><code>"title": string</code> title of the post, requirement for at least 3 characters</li>
	<li><code>"body": string</code> body of the post, requirement for at least 5 characters</li>
</ul>
<p><strong> Response </strong></p>
<ul>
	<li><code>201 Created</code> on success</li>
</ul>
<p><code>json
    {
        "message": "Post successfully added.",
        "data": {
            "id": 103,
            "userId": "1",
            "title": "dolorem dolore est ipsam",
            "body": "dignissimos aperiam dolorem qui eum\nfacilis quibusdam animi sint suscipit qui sint possimus cum\nquaerat magni maiores excepturi\nipsam ut commodi dolor voluptatum modi aut vitae"
        }
    }</code></p>
<h3>Lookup a post by the id of the post</h3>
<p><code>GET /api/posts/&lt;id&gt;</code></p>
<p><strong> Response </strong></p>
<ul>
	<li><code>404 Not Found</code> if the post does not exist</li>
	<li><code>200 OK</code> on success</li>
    <li><code>201 Created</code> on successful restore from external API</li>
</ul>
<p><code>json
    {
        "message": "Post found",
        "data": {
        "userid": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas
        totam\nnostrum rerum est autem sunt rem eveniet architecto"
        }
    }</code></p>
<h3>Lookup a post by the id of the user</h3>
<p><code>GET /api/userposts/&lt;userId&gt;</code></p>
<p><strong> Response </strong></p>
<ul>
	<li><code>404 Not Found</code> if the user does not have any posts</li>
	<li><code>200 OK</code> on success</li>
</ul>
<p><code>json
    {"message": "success", "data": [
    {
        "id": 1,
        "userId": "1",
        "title": "dolorem dolore est ipsam",
        "body": "dignissimos aperiam dolorem qui eum\nfacilis quibusdam animi sint suscipit qui sint possimus cum\nquaerat magni maiores excepturi\nipsam ut commodi dolor voluptatum modi aut vitae"
    },
    {
        "id": 2,
        "userId": "1",
        "title": "voluptatem eligendi optio",
        "body": "fuga et accusamus dolorum perferendis illo voluptas\nnon doloremque neque facere\nad qui dolorum molestiae beatae\nsed aut voluptas totam sit illum"
    ]
    }</code></p>
    <h3>Editing a post</h3>
    <p><strong> Definition </strong></p>
    <p><code>PUT /api/posts/&lt;id&gt;</code></p>
    <p><strong> Arguments </strong></p>
    <ul>
        <li><code>"userId": integer</code> a globally unique identifier for the user/author of the post, must match the post userId, is validated through an external API</li>
        <li><code>"title": string</code> title of the post, requirement for at least 3 characters</li>
        <li><code>"body": string</code> body of the post, requirement for at least 5 characters</li>
    </ul>
    <p><strong> Response </strong></p>
    <ul>
        <li><code>200 OK</code> on success</li>
    </ul>
    <p><code>json
        {
            "message": "Post 1 successfully edited",
            "data": {
            "userId": 1,
            "title": "asd",
            "body": "tsdsfaadsfa"
            }
        }</code></p>
<h3>Delete a post</h3>
<p><code>DELETE /posts/&lt;id&gt;</code></p>
<p><strong> Response </strong></p>
<ul>
	<li><code>404 Not Found</code> if the post does not exist</li>
	<li><code>200 OK</code> on success</li>
</ul>
<p><code>json
    {
        "message": "Post 2 deleted successfully"
    }
</code></p>