1. **Docker Engine Starts**: Docker starts with the Docker daemon, which manages Docker
containers.

2. **Container Creation**: Docker uses the `docker run` command to create a new container.

3. **Namespace Creation**: Docker uses the `clone()` system call with specific flags to create
a new process within various Linux namespaces. These namespaces include:
- **PID Namespace**: Isolates process IDs.
- **Network Namespace**: Isolates network interfaces and the network stack.
- **Mount Namespace**: Isolates the filesystem mount points.
- **UTS Namespace**: Isolates hostname and NIS domain name.
- **IPC Namespace**: Isolates System V IPC and POSIX message queues.
- **User Namespace**: Isolates user and group ID number spaces.
- **CGROUP Namespace**: Isolates the view of the cgroup hierarchy.

4. **Resource Isolation**: Each container has its own view of the system resources, providing
isolation from other containers and the host system.

5. **Control Groups (cgroups)**: Docker uses cgroups to limit and isolate the resource usage
of containers.

6. **Union File Systems (UnionFS)**: Docker uses UnionFS to build the file system of the
containers, allowing files and directories of separate file systems to be overlaid.

7. **Networking**: Docker creates a host-private network bridge for all containers to
communicate, and supports software-defined networking.

8. **Images and Registries**: Docker uses Docker images to package and distribute software,
which are stored in Docker registries.

9. **Docker CLI and Docker API**: Docker provides a command-line interface and a REST
API to interact with the Docker daemon.
