# Zeebe Worker for Python

## Usage
### Install
`pip install zeebe-worker`

### Usage
#### Class object
To use the class object

```python
from zeebe_worker import ZeebeWorker
from extensions import zeebe_stub
from config import worker_name

class MyWorker(ZeebeWorker):

    def my_task_type_handler(self, job):
        """Handling my_task_type
        """
        variables = json.loads(job.variables)
        if something_fails:
            # This will trigger a FailJobRequest with the exception
            raise Exception

    def another_task_type_handler(self, job):
        """Handles another task
        """
        pass


# Create your own class instance with your own configuration
my_worker = MyWorker(zeebe_stub, worker_name)

# Subscribe to a task type (uses threading.Thread)
my_worker.subscribe('my_task_type', 'my_task_type_handler')
my_worker.subscribe('my_task_typo', 'my_task_type_handler')
my_worker.subscribe('another_task_type', 'another_task_type_handler')
```

## Publish
- Bump version
- `python setup.py sdist`
- `twine upload dist/zeebe_worker-<version>.tar.gz -u <pypi-username> -p <pypi-password>`
