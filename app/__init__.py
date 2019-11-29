from app.app import api
from app.handlers import (
    vectors,
    errors,
    manage
)

manage.register(api)
vectors.register(api)
errors.register()
