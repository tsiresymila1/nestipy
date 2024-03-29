# Blank Application with Nestipy

## Introduction

This documentation introduces a creation of the simplest Nestipy Application.

### Requirements

- Python 3.10+
- Nestipy (latest version)

## Setting Up

### Installation and Setup

All you need to getting started is to install only nestipy, you can achieve this by running the following command using
pip

```bash
pip install nestipy
```

## Start with cli

#### Create a new project

```bash
nestipy new my_app
```

This command will create a new project with the following structure:

```text
├── app_module.py
├── app_controller.py
├── app_service.py
├── main.py
|── requirements.txt
|── README.md
├── src
│    ├── __init__.py
```

After creating the project, to start serve, run the following command inside the project directory:

```bash
python main.py
```
Now you can access the application at [http://localhost:8000/schema/swagger](http://localhost:8000/schema/swagger)
for <b>Litestar</b>, [http://localhost:8000/docs](http://localhost:8000/docs) for <b>Fastapi</b> and test the endpoints.

Let's go over the boilerplate code that generated by the cli:

`app_module.py`

```python
from nestipy.common.decorator import Module
from .app_controller import AppController
from .app_service import AppService


@Module(
    controllers=[AppController],
    providers=[AppService]
)
class AppModule:
    pass

```

`app_controller.py`

```python
from nestipy.common.decorator import Controller, Get, Inject, Post, Put, Delete
from .app_service import AppService


@Controller()
class AppController:
    service: AppService = Inject(AppService)

    @Get()
    async def get(self) -> str:
        return await self.service.get()

    @Post()
    async def post(self, data: str) -> str:
        return await self.service.post(data=data)

    @Put('/{user_id}')
    async def put(self, user_id: int, data: str) -> str:
        return await self.service.put(id_=user_id, data=data)

    @Delete('/{user_id}')
    async def delete(self, user_id: int) -> None:
        await self.service.delete(id_=user_id)

```

`app_service.py`

```python
from nestipy.common.decorator import Injectable


@Injectable()
class AppService:

    @classmethod
    async def get(cls):
        return "test"

    @classmethod
    async def post(cls, data: str):
        return "test"

    @classmethod
    async def put(cls, id_: int, data: str):
        return "test"

    @classmethod
    async def delete(cls, id_: int):
        return "test"

```

`main.py`

```python
import uvicorn

from .app_module import AppModule
from nestipy.core.factory import NestipyFactory
# from nestipy.core.platform import PlatformFastAPI

from nestipy.core.platform import PlatformLitestar

# app = NestipyFactory[PlatformFastAPI].create(AppModule, title="My FastAPI App")
app = NestipyFactory[PlatformLitestar].create(AppModule, title="My App")

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)


```

### Creating new resource
After creating the project, let's create a new resource:

```bash
pynest g resource user
-> api
-> graphql
```

By choosing <b>api</b>, we have generated new folder inside <b>src</b>

```text
├── user
│    ├── __init__.py
│    ├── user_controller.py
│    ├── user_service.py
│    ├── user_dto.py
│    ├── user_module.py
```

By choosing <b>graphql</b>, we have resolver instead of controller, like the following

```text
├── user
│    ├── __init__.py
│    ├── user_resolver.py
│    ├── user_service.py
│    ├── user_input.py
│    ├── user_module.py
```

By using graphql, dont forget to register strawberry module from nestipy plugin inside app_module imports.

```python
...
from nestipy.plugins.strawberry_module.strawberry_module import StrawberryModule, StrawberryOption

...


@Module(
    imports=[
        ...
        StrawberryModule.for_root(
            resolvers=[UserModule],
            option=StrawberryOption(graphql_ide='graphiql')
        ),
        ...
    ],
)
class AppModule:
    pass
```

### Creating new module

With nestipy we can create a module by running the following command

```bash
nestipy g module exemple
```

This command will create a new directory <b>exemple</b> inside <b>src</b> and update app_module imports to import this
new module.

```text
├── exemple
│    ├── __init__.py
│    ├── exemple_module.py
```

So inside, we got,

`exemple_module.py`

```python
from nestipy.common.decorator import Module
from nestipy.common.decorator import Module


@Module()
class ExempleModule:
    pass
```
### Creating new controller

Create a controller to handle the requests and responses.

```bash
nestipy g controller exemple
```

`examples_controller.py`

```python

from nestipy.common.decorator import Controller, Get


@Controller('exemples')
class ExempleController:

    @Get()
    async def get(self) -> str:
        return "test"

```
### Creating new resolver
Or for graphql , create a resolver.

```bash
nestipy g resolver exemple
```

`examples_resolver.py`

```python

from strawberry.types import Info
from nestipy.plugins.strawberry_module.decorator import Resolver, Query, Mutation


@Resolver()
class ExempleResolver:

    @Query()
    def exemple_test_query(self, root: Info) -> str:
        return "test"

    @Mutation()
    def exemple_test_mutation(self, root: Info, test: str) -> str:
        return test


```

### Creating new service
Implement services to handle business logic.

```bash
nestipy g service exemple
```

`examples_service.py`

```python
from nestipy.common.decorator import Injectable


@Injectable()
class ExempleService:

    async def test(self):
        pass

```

Service is injectable inside a controller, resolver or other service by using <b>Inject</b> to inject it as a property of them. 

```python
service: ExempleService = Inject(ExempleService)
```