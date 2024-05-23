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
token_credential = TokenCredential(api_host_url=url, user_name=username, password=pw, auto_refresh_token=True)
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

```
from brandcompete.core.classes import Loader

query="Please summarize the following text: "
    
response:dict = client.prompt(
    model_id=1, 
    query=query, 
    loader=Loader.PDF, 
    file_append_to_query="path/to/file.pdf")
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

### Raging with datasources and documents
## Datasource
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
## Documents
Add multiple documents into a datasource (can be url or file)
```
client.add_documents(
    data_source_id=your_ds_id, 
    sources=["path/to_my_data/test.pdf", "https://www.brandcompete.com"] )
```
## Prompt on datasource context
Prompt in conjunction with a datasource id. You have to use the defaultModelTagId instead of the id.
```    
client.prompt_on_datasource(
    datasource_id=datasource_id, 
    model_tag_id=200, 
    query="can you please summarize the content?", 
    prompt_options = None)
```
### Possible loaders

NOTE: Feel free to contact us to enhance our SDK with one of [these](https://llamahub.ai/?tab=loaders) available loader.
Mail to: thorsten.atzeni@brandcompete.com
## Frequently used AI-Models

- [ID: 1] MISTRAL                   - The Mistral 7B model released by Mistral AI
- [ID: 2] LLAMA2                    - The most popular model for general use.
- [ID: 3] OPENCHAT                  - A family of open-source models trained on a wide variety of data, surpassing ChatGPT on various benchmarks.
- [ID: 4] CODELLAMA                 - A large language model that can use text prompts to generate and discuss code.
- [ID: 5] GPT 3.5 TURBO             - Chat GPT 3.5 (NOTE: None confidential, own API-Token required!)
- [ID: 6] VICUNA                    - General use chat model based on Llama and Llama 2 with 2K to 16K context sizes.
- [ID: 7] ORCA-MINI                 - A general-purpose model ranging from 3 billion parameters to 70 billion, suitable for entry-level hardware. 
- [ID: 8] LLAMA2-UNCENSORED         - Uncensored Llama 2 model by George Sung and Jarrad Hope.
- [ID: 9] WIZARD-VICUNA-UNCENSORED  - Wizard Vicuna Uncensored is a 7B, 13B, and 30B parameter model based on Llama 2 uncensored by Eric Hartford. The models were trained against LLaMA-7B.
- [ID: 10] NOUS-HERMES               - General use models based on Llama and Llama 2 from Nous Research.
- [ID: 11] PHIND-CODELLAMA           - Code generation model based on CodeLlama.
- [ID: 12] MISTRAL-OPENORCA          - Mistral OpenOrca is a 7 billion parameter model, fine-tuned on top of the Mistral 7B model using the OpenOrca dataset.
- [ID: 13] WIZARDCODER               - Llama based code generation model focused on Python.
- [ID: 14] WIZARD-MATH               - Model focused on math and logic problems
- [ID: 15] LLAMA2-CHINESE            - Llama 2 based model fine tuned to improve Chinese dialogue ability.
- [ID: 16] STABLE-BELUGA             - Llama 2 based model fine tuned on an Orca-style dataset. Originally called Free Willy.
- [ID: 17] CODEUP                    - Great code generation model based on Llama2.
- [ID: 18] ZEPHYR                    - Zephyr beta is a fine-tuned 7B version of mistral that was trained on on a mix of publicly available, synthetic datasets.
- [ID: 19] EVERYTHINGLM              - Uncensored Llama2 based model with 16k context size.
- [ID: 20] FALCON                    - A large language model built by the Technology Innovation Institute (TII) for use in summarization, text generation, and chat bots.
- [ID: 21] WIZARDLM-UNCENSORED       - Uncensored version of Wizard LM model
- [ID: 22] MEDLLAMA2                 - Fine-tuned Llama 2 model to answer medical questions based on an open source medical dataset.
- [ID: 23] WIZARD-VICUNA             - Wizard Vicuna is a 13B parameter model based on Llama 2 trained by MelodysDreamj.
- [ID: 24] OPEN-ORCA-PLATYPUS2       - Merge of the Open Orca OpenChat model and the Garage-bAInd Platypus 2 model. Designed for chat and code generation.
- [ID: 25] STARCODER                 - StarCoder is a code generation model trained on 80+ programming languages.
- [ID: 26] SAMANTHA-MISTRAL          - A companion assistant trained in philosophy, psychology, and personal relationships. Based on Mistral.
- [ID: 27] OPENHERMES2-MISTRAL       - OpenHermes 2 Mistral is a 7B model fine-tuned on Mistral with 900,000 entries of primarily GPT-4 generated data from open datasets.
- [ID: 28] WIZARDLM                  - General use 70 billion parameter model based on Llama 2.
- [ID: 29] SQLCODER                  - SQLCoder is a code completion model fined-tuned on StarCoder for SQL generation tasks
- [ID: 30] DOLPHIN2.1-MISTRAL        - An instruct-tuned model based on Mistral and trained on a dataset filtered to remove alignment and bias.
- [ID: 31] DOLPHIN2.2-MISTRAL        - An instruct-tuned model based on Mistral. Version 2.2 is fine-tuned for improved conversation and empathy.
- [ID: 32] CODEBOOGA                 - A high-performing code instruct model created by merging two existing code models.
- [ID: 33] YARN-MISTRAL              - An extension of Mistral to support a context of up to 128k tokens.
- [ID: 34] NEXUSRAVEN                - Nexus Raven is a 13 billion parameter model designed for function calling tasks. It is fine-tuned against Meta’s Code Llama 13B instruct model.
- [ID: 35] MISTRALLITE               - MistralLite is a fine-tuned model based on Mistral with enhanced capabilities of processing long contexts.
- [ID: 36] OPENHERMES2.5-MISTRAL     - OpenHermes 2.5 Mistral 7B is a Mistral 7B fine-tune, a continuation of OpenHermes 2 model, which trained on additional code datasets.
- [ID: 37] YARN-LLAMA2               - An extension of Llama 2 that supports a context of up to 128k tokens.
- [ID: 38] XWINLM                    - Conversational model based on Llama 2 that performs competitively on various benchmarks.

