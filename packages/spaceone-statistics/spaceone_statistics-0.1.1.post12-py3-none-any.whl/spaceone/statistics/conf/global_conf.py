DATABASES = {
    'default': {
        'db': 'statistics',
        'host': 'localhost',
        'port': 27017,
        'username': '',
        'password': ''
    }
}

HANDLERS = {
}

CONNECTORS = {
    'ServiceConnector': {
        'statistics': 'grpc://localhost:50051/v1'
    }
}
