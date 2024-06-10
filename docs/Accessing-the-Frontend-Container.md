# Accessing the Frontend Container

To work directly with the frontend in development, you can access its container similarly:

```bash
# Accessing the frontend container's shell
docker exec -it graduation-project-frontend-1 /bin/bash

# Inside the container, you might start the development server or run other npm scripts:
npm run serve
```
