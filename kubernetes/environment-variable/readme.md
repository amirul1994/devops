imperative approach

kubectl run my-db --image=mysql:latest --env="MYSQL_ROOT_PASSWORD=abc123" --
env="MYSQL_USER=user1" --env="MYSQL_PASSWORD=user1@mydb" 
