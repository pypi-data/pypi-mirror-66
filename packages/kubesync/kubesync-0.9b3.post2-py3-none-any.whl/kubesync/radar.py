# Standard Library
import time
from typing import Dict, List
from pathlib import Path

# Third Party
import docker
from watchdog.events import FileMovedEvent, FileDeletedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

# First Party
from kubesync.dock import DockerSync
from kubesync.kube import KubeManager
from kubesync.colors import print_red, print_green, print_yellow
from kubesync.models import Sync, WatcherStatus


class Watcher:
    def __init__(self) -> None:
        self.docker_client = docker.from_env()
        self.kube = KubeManager()
        self.observer_list: Dict[str, Observer] = {}

        WatcherStatus.objects.update(status=True)
        Sync.objects.update(connected=False, synced=False)

    def run(self) -> None:
        while True:
            for sync in Sync.objects.all():
                container = self.kube.get_container(sync.selector, sync.container_name)

                if sync.connected == 0 and container:
                    print_green(f"{sync.selector}::{sync.container_name} container found.")
                    if not Path(sync.source_path).exists():
                        print_red(f"{sync.source_path} path not found.")
                        continue

                    sync.container_id = container.container_id
                    sync.connected = True
                    sync.save()

                    sync_list = Sync.objects.filter(connected=True, source_path=sync.source_path)
                    old_observer = self.observer_list.get(sync.source_path, None)
                    if old_observer:
                        old_observer.stop()
                        old_observer.join()
                        sync_list = Sync.objects.filter(connected=True, source_path=sync.source_path)
                        print_green(f"Creating handler again for {sync.source_path}")

                    event_handler = Handler(self.docker_client, sync_list)
                    observer = Observer()
                    observer.schedule(event_handler, sync.source_path, recursive=True)
                    observer.start()

                    self.observer_list[sync.source_path] = observer

                if sync.connected == 1 and not container:
                    print_yellow(f"{sync.selector}::{sync.container_name} container down.")

                    sync.connected = False
                    sync.save()

                    observer = self.observer_list.pop(sync.source_path)
                    observer.stop()
                    observer.join()

                    sync_list = Sync.objects.filter(connected=True, source_path=sync.source_path)
                    if sync_list:
                        event_handler = Handler(self.docker_client, sync_list)
                        observer = Observer()
                        observer.schedule(event_handler, sync.source_path, recursive=True)
                        observer.start()
                        self.observer_list[sync.source_path] = observer
                        print_green(f"Creating handler again for {sync.source_path}")
                    else:
                        print_yellow(f"Stop handler for {sync.source_path}")

            time.sleep(1)

    def stop(self) -> None:
        print_yellow("Stop watching.")

        WatcherStatus.objects.update(status=False)
        Sync.objects.update(connected=False, synced=False)

        for observer in self.observer_list.values():
            observer.stop()
            observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, docker_client: docker.DockerClient, sync_list: List[Sync]):
        self.docker_sync_list: List[DockerSync] = [
            DockerSync(docker_client=docker_client, sync=sync) for sync in sync_list
        ]
        self.sync_list = sync_list

        print_green(f"Handling {self.sync_list[0].source_path} directory.")

    def reloading(self) -> None:
        for sync in self.sync_list:
            print_green(f"Reloading {sync.selector}::{sync.container_name}{sync.destination_path}")
            sync.synced = False
            sync.save()

    def done(self) -> None:
        for sync in self.sync_list:
            print_green(f"Reloaded {sync.selector}::{sync.container_name}{sync.destination_path}")
            sync.synced = True
            sync.save()

    def on_modified(self, event: FileModifiedEvent):
        print_red("Modified: %s" % event.src_path)
        self.reloading()
        for docker_sync in self.docker_sync_list:
            docker_sync.move_object(event.src_path)
        self.done()

    def on_moved(self, event: FileMovedEvent):
        print_red("Moved: %s - %s" % (event.src_path, event.dest_path))
        self.reloading()
        for docker_sync in self.docker_sync_list:
            docker_sync.delete_object(event.src_path, event.is_directory)
        self.done()

    def on_deleted(self, event: FileDeletedEvent):
        print_red("Deleted: %s" % event.src_path)
        self.reloading()
        for docker_sync in self.docker_sync_list:
            docker_sync.delete_object(event.src_path, event.is_directory)
        self.done()
