Deployment of a Fullstack app in docker containers. The frontend of the
application is developed using React.js, while the backend is implemented with the
Django framework. Docker Compose is utilized to orchestrate the deployment of these
components as individual containers.
To make the docker containers accessible in the local network, I have used the docker host's ip address.
To use only inside the localhost, use the load balancer's ip address in the frontend (App.js) and 
backend server 1 and backend server 2 ip addresses in the load balancer's configuration(nginx.conf). 
