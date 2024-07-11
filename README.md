# brandcompete AI-Manager-Python-SDK

## Preconditions

Python version: >=3.8.1,<3.12

## Example
We have created an example (demo) project to demonstrate the use of the SDK within a project.
The repository can found [here](https://github.com/brandcompete/AI-Manager-Usage-Example)

## How to install

Inside your project folder (or python environment) you can install the SDK via pip
```
pip install -e git+https://github.com/brandcompete/AI-Manager-Python-SDK.git#egg=AI-Manager-Python-SDK
```

Or add this into your requirements.txt
```
AI-Manager-Python-SDK @ git+https://github.com/brandcompete/AI-Manager-Python-SDK.git
```
and install via pip like
```
pip install -r requirements.txt
```


## Usage

### Instantiate the service client

The client authenticates itself for all requests via a JWT token. 
To obtain a token, the client must log in to the corresponding API host via username and password.

```
IMPORTANT NOTE: Use only the base url (without slash at the end and without /api/v1/ etc.)
```

```
from brandcompete.core.credentials import TokenCredential
from brandcompete.client import AI_ManServiceClient

url = "https://aiman-api-test.brandcompete.com" (<-- base url only!)
username = "john@doe.com"
pw = "top_secret"

token_credential = TokenCredential(api_host_url=url, user_name=username, password=pw)
client = AI_ManServiceClient(credential=token_credential)
```

The client takes care of updating the token during the client's runtime if it has expired.
The automatic refresh can be controlled via optional parameter ```auto_refresh_token=True or False``` of the TokenCredential.

Example:
```
token_credential = TokenCredential(
    api_host_url=url, 
    user_name=username, 
    password=pw, 
    auto_refresh_token=True)
```

### Fetching available AI-Models

This method returns a list of type: AI_Model (```List[AI_Model]```)

```
models = client.get_models()
```

### Prompting a simple query to a specific model

In order to submit a query, the model must be passed as a parameter via id
```
response:str = client.prompt(
    model_id=10,
    query="my question to AI-Model")
```

### Prompting a query with appended file content

You can pass a specific file content to your prompt.
Current available loaders are:
- loader.PDF
- loader.EXCEL
- loader.DOCX
- loader.CSV
- loader.IMAGE

#### PDF example
```
from brandcompete.core.classes import Loader

query="Please summarize the following text: "  
response:dict = client.prompt(
    model_id=1, 
    query=query, 
    loader=Loader.PDF, 
    file_append_to_query="path/to/file.pdf")
```

#### Image example
```
from brandcompete.core.classes import Loader

query="describe what you see on the picture."  
response:dict = client.prompt(
    model_id=21, 
    query=query, 
    loader=Loader.IMAGE, 
    file_append_to_query="path/to/file.png")
```

### Prompting a query with appended file content and raging files

```
query="your question or order..."
    
response:dict = client.prompt(
    model_id=1, 
    query=query, 
    loader=Loader.PDF, 
    file_append_to_query="path/to/file.pdf",
    files_to_rag=["file/path/1.pdf", "file/path/2.pdf"]
    )
   
```

### Prompting a query with raging files only

```
query="your question or order..."
    
response:dict = client.prompt(
    model_id=1, 
    query=query, 
    loader=Loader.PDF, 
    files_to_rag=["file/path/1.pdf", "file/path/2.pdf"]
    )
   
```

## Raging with datasources and documents
### Datasource
Init a new datasource (minimum requirements - name and summary)
```
datasource_id = client.init_new_datasource(
    name="Test datasource", 
    summary="New datasource for uploading some documents")
```
Or init a new datasource with a list of tags and categories
```
datasource_id = client.init_new_datasource(
    name="Test datasource", 
    summary="New datasource for uploading documents", 
    tags=["tagA","tagB", "etc"], 
    categories=["catA","catB","etc"])
```
Fetch all datasources (associated to my account).
Possible status: 
- (2)ready
- (1)indexing
- (0)pending

```
datasources = client.fetch_all_datasources()
for source in datasources:
    print(f"{source.id}")
    print(f"{source.name}")
    print(f"{source.status}")
```
### Documents
Add multiple documents into a datasource (can be url or file)
```
client.add_documents(
    data_source_id=your_ds_id, 
    sources=["path/to_my_data/test.pdf", "https://www.brandcompete.com"] )
```
### Prompt on datasource context
Prompt in conjunction with a datasource id. You have to use the defaultModelTagId instead of the id.
```    
client.prompt_on_datasource(
    datasource_id=datasource_id, 
    model_tag_id=200, 
    query="can you please summarize the content?", 
    prompt_options = None)
```