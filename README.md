# qmobi_task

There was some problems with docker-compose, so I had to use only docker.

**To build and start this container you need to:**
1. Clone this repository
1. Install docker
1. Run command: "docker build -f Dockerfile -t qmobi_task ." in Dockerfile dir
1. Run: "docker run -p 8000:8000 -t qmobi_task:latest"

**If you have troubles with access, then:**
1. Run command: "docker container ls"
1. Run: ""docker inspect <contaner_id> | grep '"IPAddress"' | head -n 1
1. Edit line in Dockerfile "172.17.0.2" to "<ip of your container>"
1. Rebuild container

*Task for Qmobi made by Eugene Bazarov.*
