# Backend Assignment

As mentioned in the presented [problem set](https://raw.githubusercontent.com/trishantpahwa/webknot_backend_assignment/main/GDNA-Backend-Assignment_v2.pdf).

> As decided, both the microservices were to be designed using Flask.

> Please setup the .env files in projects before starting them up. The format can br referred from the `sample_env' folder.

The flask applications can be boot up in the executing the following commands within the src directory(where app.js is present) of the respective microservice:

`Backend API`: python %path_to_backend_api%/src/app.py
`Cache API`: python %path_to_cache_api%/src/app.py

For example if present in the root directory of the project.
```
cd backend_api/src
python app.py
```

To execute the unittests, navigate to the directory containing the `tests.py` file for the specific api to test, and use the following command:
`python -m unittest tests.py`

