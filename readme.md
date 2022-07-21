## FB Messenger Service

## Для установки вам надо
- Переименовать ``.env.example`` в ``.env``
- Запустить ``docker-compose up -d``

## Документация

Документация доступна по роутам
- ``/docs``
- ``/redoc``

#### Авторицация ``/login``
**body**
```
{
  "email": "string",
  "password": "string"
}
```

После авторизации вам выдается JWT token.
Все роуты в ``/contacts`` секьюрные, нужно вставить в заголовки http запроса

Authorization: Bearer <ваш токен>

### OpenAPI

```
{
   "openapi":"3.0.2",
   "info":{
      "title":"FastAPI",
      "version":"0.1.0"
   },
   "paths":{
      "/login":{
         "post":{
            "tags":[
               "login"
            ],
            "summary":"Login",
            "operationId":"login_login_post",
            "requestBody":{
               "content":{
                  "application/json":{
                     "schema":{
                        "$ref":"#/components/schemas/LoginRequst"
                     }
                  }
               },
               "required":true
            },
            "responses":{
               "200":{
                  "description":"Successful Response",
                  "content":{
                     "application/json":{
                        "schema":{
                           "$ref":"#/components/schemas/LoginResponse"
                        }
                     }
                  }
               },
               "401":{
                  "description":"Unauthorized",
                  "detail":{
                     "msg":"Not authorized"
                  }
               },
               "422":{
                  "description":"Validation Error",
                  "content":{
                     "application/json":{
                        "schema":{
                           "$ref":"#/components/schemas/HTTPValidationError"
                        }
                     }
                  }
               }
            }
         }
      },
      "/contacts/send":{
         "post":{
            "tags":[
               "contacts"
            ],
            "summary":"Send",
            "operationId":"send_contacts_send_post",
            "requestBody":{
               "content":{
                  "application/json":{
                     "schema":{
                        "$ref":"#/components/schemas/SendRequest"
                     }
                  }
               },
               "required":true
            },
            "responses":{
               "200":{
                  "description":"Successful Response",
                  "content":{
                     "application/json":{
                        "schema":{
                           
                        }
                     }
                  }
               },
               "422":{
                  "description":"Validation Error",
                  "content":{
                     "application/json":{
                        "schema":{
                           "$ref":"#/components/schemas/HTTPValidationError"
                        }
                     }
                  }
               }
            },
            "security":[
               {
                  "RWAPIKeyHeader":[
                     
                  ]
               }
            ]
         }
      },
      "/contacts/search":{
         "post":{
            "tags":[
               "contacts"
            ],
            "summary":"Search",
            "operationId":"search_contacts_search_post",
            "requestBody":{
               "content":{
                  "application/json":{
                     "schema":{
                        "$ref":"#/components/schemas/SearchRequest"
                     }
                  }
               },
               "required":true
            },
            "responses":{
               "200":{
                  "description":"Successful Response",
                  "content":{
                     "application/json":{
                        "schema":{
                           
                        }
                     }
                  }
               },
               "422":{
                  "description":"Validation Error",
                  "content":{
                     "application/json":{
                        "schema":{
                           "$ref":"#/components/schemas/HTTPValidationError"
                        }
                     }
                  }
               }
            },
            "security":[
               {
                  "RWAPIKeyHeader":[
                     
                  ]
               }
            ]
         }
      },
      "/contacts/messages/{contact}":{
         "get":{
            "tags":[
               "contacts"
            ],
            "summary":"Messages By Contact",
            "operationId":"messages_by_contact_contacts_messages__contact__get",
            "parameters":[
               {
                  "required":true,
                  "schema":{
                     "title":"Contact"
                  },
                  "name":"contact",
                  "in":"path"
               }
            ],
            "responses":{
               "200":{
                  "description":"Successful Response",
                  "content":{
                     "application/json":{
                        "schema":{
                           
                        }
                     }
                  }
               },
               "422":{
                  "description":"Validation Error",
                  "content":{
                     "application/json":{
                        "schema":{
                           "$ref":"#/components/schemas/HTTPValidationError"
                        }
                     }
                  }
               }
            },
            "security":[
               {
                  "RWAPIKeyHeader":[
                     
                  ]
               }
            ]
         }
      }
   },
   "components":{
      "schemas":{
         "HTTPValidationError":{
            "title":"HTTPValidationError",
            "type":"object",
            "properties":{
               "detail":{
                  "title":"Detail",
                  "type":"array",
                  "items":{
                     "$ref":"#/components/schemas/ValidationError"
                  }
               }
            }
         },
         "LoginRequst":{
            "title":"LoginRequst",
            "required":[
               "email",
               "password"
            ],
            "type":"object",
            "properties":{
               "email":{
                  "title":"Email",
                  "type":"string"
               },
               "password":{
                  "title":"Password",
                  "type":"string"
               }
            }
         },
         "LoginResponse":{
            "title":"LoginResponse",
            "required":[
               "uid",
               "token"
            ],
            "type":"object",
            "properties":{
               "uid":{
                  "title":"Uid",
                  "type":"string"
               },
               "token":{
                  "title":"Token",
                  "type":"string"
               }
            }
         },
         "SearchRequest":{
            "title":"SearchRequest",
            "required":[
               "q"
            ],
            "type":"object",
            "properties":{
               "q":{
                  "title":"Q",
                  "type":"string"
               },
               "limit":{
                  "title":"Limit",
                  "type":"integer",
                  "default":10
               }
            }
         },
         "SendRequest":{
            "title":"SendRequest",
            "required":[
               "message",
               "thread_id"
            ],
            "type":"object",
            "properties":{
               "message":{
                  "title":"Message",
                  "type":"string"
               },
               "thread_id":{
                  "title":"Thread Id",
                  "type":"string"
               }
            }
         },
         "ValidationError":{
            "title":"ValidationError",
            "required":[
               "loc",
               "msg",
               "type"
            ],
            "type":"object",
            "properties":{
               "loc":{
                  "title":"Location",
                  "type":"array",
                  "items":{
                     "anyOf":[
                        {
                           "type":"string"
                        },
                        {
                           "type":"integer"
                        }
                     ]
                  }
               },
               "msg":{
                  "title":"Message",
                  "type":"string"
               },
               "type":{
                  "title":"Error Type",
                  "type":"string"
               }
            }
         }
      },
      "securitySchemes":{
         "RWAPIKeyHeader":{
            "type":"apiKey",
            "in":"header",
            "name":"Authorization"
         }
      }
   }
}
```
