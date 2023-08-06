async def load_num_gpus(hub):
    # TODO figure out how to get gpu info
    # get the model and vendor for each GPU
    hub.corn.CORN.gpus = {}
    hub.corn.CORN.num_gpus = len(hub.corn.CORN.gpus)
