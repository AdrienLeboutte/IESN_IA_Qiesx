### Requirements to run the website
- django channels
    ```
    pip3 install channels
    ```
- django crispy forms
    ```
    pip3 install django-crispy-forms
    ```
- channels_redis
    ```
    pip3 install channels_redis
    ```

You also need to install docker in order to run your own instance of redis
once it's installed run
```
docker run -p 6379:6379 -d redis:2.8
```