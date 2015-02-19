#Images_crawler

This is an exercise that will retrive a list of image links from a list of given URLs.

##Design

Flask is easy to bootstrap and can also be prototyped easily. Flask also comes with SQLAlchemy which becomes the top choice. Instead of having three tables (job, status, result), having two tables can simplify the problem. We can push `in_process` and `completed` status to Job table. In addition, We just need to create a foreign_key in Result table that links back to the primary_key in Job table. We can easily retrieve results for any given job id.

- `Flask`: Bootstraping web framework.

- `SQLAlchemy`: Communication between database and other components.

- `Python`: All the backend stuff.

- `Database`: Two tables - Job and Result where Job is one-to-many relationship with Result. Job table also encapsulates `in_process` and `completed` status.

##Improvement
- Use `Redis` can definitely help in this case. Especailly in the situation where we are constantly updating `in_process` and `complete` status whenever a worker is processing a url or is done with the url. In my solution, whenever I need to update the status, I create a critical section to perfrom atomic update.
- Include multiprocessing lib to take the advantage of multicore machines. This will definitely require major code change to accommodate it.

##Example

#### ```POST /```
```
curl -X POST -F "inputs=@-" http://127.0.0.1:5000/ << EOF
https://www.docker.com/
EOF
```
Return

```
{
  "status": {
      "statusMsg": "OK", 
      "statusDetails": {}, 
      "statusCode": 
      "HTTPOk"
   },
   "result": "job_id: 0"
}
```

#### ```GET /status/<int:id>```
```
curl -X GET http://127.0.0.1:5000/status/0
```

Return

```
{
  "result": {
    "completed": 76,
    "in_process": 0
  },
  "status": {
    "statusCode": "HTTPOk",
    "statusDetails": {},
    "statusMsg": "OK"
  }
}
```

#### ```GET /result/<int:id>```
```
curl -X GET http://127.0.0.1:5000/result/0
```

Return

```
{
  "result": {
    "count": 264,
    "img_links": [
      "https://s3.amazonaws.com/docker-com-static/assets/img/Google/gce@2x.png",
      "https://pbs.twimg.com/profile_images/378800000124779041/fbbb494a7eef5f9278c6967b6072ca3e_400x400.png",
      "https://media.licdn.com/mpr/mpr/shrink_60_60/p/1/000/026/015/0de895e.jpg",
      "https://d207aa93qlcgug.cloudfront.net/1.5.5/img/explore_repos/official_mysql.png",
      "https://pbs.twimg.com/profile_images/517143056345096193/JK2Ta9DV_normal.png",
      "http://www.scoop.it/resources/img/V4/themeActionsBanner/tag.png",
      "https://lh3.googleusercontent.com/-l-2GRUzNZew/AAAAAAAAAAI/AAAAAAAAAWo/yJ4XjYP5yv8/s28-c-k-no/photo.jpg",
      "http://www.scoop.it/resources/img/V4/googleplay_light.png",
      (...)
    ]
  },
  "status": {
    "statusCode": "HTTPOk",
    "statusDetails": {},
    "statusMsg": "OK"
}
```



