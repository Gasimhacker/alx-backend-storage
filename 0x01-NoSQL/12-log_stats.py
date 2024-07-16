#!/usr/bin/env python3
"""A script that provides some stats about Nginx logs stored in MongoDB"""

if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx

    num_docs = nginx.count_documents({})
    methods = {"GET": 0, "POST": 0, "PUT": 0, "PATCH": 0, "DELETE": 0}
    for method in methods:
        methods[method] = nginx.count_documents({"method": method})
    status = nginx.count_documents({"$and":
                                    [{"method": "GET"},
                                     {"path": "/status"}
                                     ]
                                    })

    print(f'{num_docs} logs')
    print('Methods:')
    [print(f"\tmethod {m}: {methods[m]}") for m in methods]
    print(f'{status} status check')
