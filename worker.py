from rq import Worker as Base


class Worker(Base):
    def __init__(self, queues=None, *args, **kwargs):
        super().__init__(queues, *args, **kwargs)
        print("LOADING WORKER")
