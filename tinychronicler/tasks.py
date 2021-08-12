import pickle
from datetime import datetime

from loguru import logger

from . import crud, schemas, generator


async def generate_composition(chronicle_id: int):
    logger.info(
        "Generate new composition based on chronicle {}".format(chronicle_id)
    )
    # Insert pending composition in database
    title = "Composition {}".format(datetime.now().strftime("%d.%m.%Y %H:%M"))
    composition = schemas.CompositionIn(title=title, data=None, is_ready=False)
    last_record_id = await crud.create_composition(composition, chronicle_id)
    # Generate composition, this might take some time ..
    files = await crud.get_files(chronicle_id)
    data = await generator.new_composition(files)
    # Update composition with new data and set it ready
    composition.data = pickle.dumps(data)
    composition.is_ready = True
    await crud.update_composition(last_record_id, composition)
    logger.info(
        "Finished generation of new composition based on chronicle {}".format(
            chronicle_id
        )
    )
