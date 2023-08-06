import docker
import pathlib
import os
import argparse
import os.path
import json

prefix = "training_"
out_prefix = "training_output"
in_prefix = "training_input"
default_image = "pytorch/pytorch:1.4-cuda10.1-cudnn7-runtime"


def command_run(args):
    client = docker.from_env()
    path_name = args.task
    task_name = args.task.lower()
    if not os.path.isdir(path_name):
        print("Task directory {} is not found.".format(path_name))
        return
    p = pathlib.Path(path_name)
    image_name = default_image
    if os.path.exists(os.path.join(path_name, "Dockerfile")):
        print("{} is found. Creating Docker image..".format(
            os.path.join(path_name, "Dockerfile")))
        api_client = docker.APIClient(base_url="unix:///var/run/docker.sock")
        b_stream = api_client.build(
            path=path_name,
            tag=task_name,
        )
        for chunk in b_stream:
            j_chunk = json.loads(chunk.decode("UTF-8")) 
            if "stream" in j_chunk and "\r" not in j_chunk["stream"]:
                print(j_chunk["stream"].strip())
        image_name = task_name
    os.makedirs(os.path.join(out_prefix, path_name), exist_ok=True)
    os.makedirs(os.path.join(in_prefix, path_name), exist_ok=True)
    try:
        ec = client.containers.get(prefix+task_name)
    except docker.errors.NotFound:
        print("Task {} is creating".format(task_name))
    else:
        print("Task {} is already exist, recreating...".format(task_name))
        ec.remove(force=True)
    command = args.python_version + " -u /"+path_name+"/main.py"
    if args.options is not None:
        with open(os.path.join(out_prefix, path_name, "options"), "w") as f:
            f.write(",".join(args.options))
        for op in args.options:
            if ":" in op:
                command += " --" + op.replace(":", "=")
            else:
                command += " --" + op
    v_list = {
        p.resolve(): {"bind": '/'+path_name, 'mode': 'rw'},
        pathlib.Path(os.path.join(out_prefix, path_name)).resolve(): {"bind": '/output', 'mode': 'rw'},
        pathlib.Path(os.path.join(in_prefix, path_name)).resolve(): {"bind": '/input', 'mode': 'rw'},
    }
    if args.config is not None:
        v_list[pathlib.Path(args.config).resolve()] = {"bind": '/config.yaml', 'mode': 'ro'}

    c = client.containers.run(
        name=prefix+task_name,
        image=image_name,
        runtime="nvidia",
        #tty=True,
        detach=True,
        # gpus="all",
        command=command,
        volumes=v_list,
    )
    if not args.detach:
        for l in c.logs(stream=True):
            print(l.strip().decode("UTF-8"))


def command_list(args):
    client = docker.from_env()
    c_l = client.containers.list(all=True)
    print("task_name\t| status ")
    for c in c_l:
        if c.name.startswith(prefix):
            print(" {}\t| {}".format(
                c.name[len(prefix):], c.status))


def command_logs(args):
    client = docker.from_env()
    try:
        c = client.containers.get(prefix+args.task)
    except docker.errors.NotFound:
        print("Task {} is not found".format(args.task))
        return

    if args.follow:
        for l in c.logs(stream=True):
            print(l.strip().decode("UTF-8"))
    else:
        log_l = str(c.logs().decode("UTF-8")).split("\n")
        for l in log_l:
            print(l)


def command_rm(args):
    client = docker.from_env()
    try:
        c = client.containers.get(prefix+args.task)
    except docker.errors.NotFound:
        print("Task {} is not found".format(args.task))
        return
    c.remove(force=True)
    print("Task {} is deleted".format(args.task))

def command_clean(args):
    client = docker.from_env()
    print("Cleaning Tasks...")
    client.containers.prune()
    client.images.prune(filters={'dangling': False})
    client.networks.prune()
    client.volumes.prune()

def main():
    parser = argparse.ArgumentParser(description='Fake git command')
    subparsers = parser.add_subparsers()

    parser_run = subparsers.add_parser('run', help='see `run -h`')
    parser_run.add_argument('task', help='task name')
    parser_run.add_argument('-c', '--config', default=None, help='config file')
    parser_run.add_argument('-o', '--options', nargs='*', help='option list')
    parser_run.add_argument('-p', '--python_version', help='python version for task', default="python3")
    parser_run.add_argument(
        '-d', '--detach', action='store_true', help='detach mode')
    parser_run.set_defaults(handler=command_run)

    parser_list = subparsers.add_parser('list', help='see `list -h`')
    parser_list.set_defaults(handler=command_list)

    parser_logs = subparsers.add_parser('logs', help='logs `logs -h`')
    parser_logs.add_argument('task', help='task name')
    parser_logs.add_argument(
        '-f', '--follow', action='store_true', help='follow logs')
    parser_logs.set_defaults(handler=command_logs)

    parser_rm = subparsers.add_parser('rm', help='see `rm -h`')
    parser_rm.add_argument('task', help='task name')
    parser_rm.set_defaults(handler=command_rm)
    
    parser_clean = subparsers.add_parser('clean', help='see `clean -h`')
    parser_clean.set_defaults(handler=command_clean)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        try:
            args.handler(args)
        except KeyboardInterrupt:
            pass
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
