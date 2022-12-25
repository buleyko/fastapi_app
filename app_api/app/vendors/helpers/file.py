import aiofiles
import shutil 
from pathlib import Path
from fastapi import (
	HTTPException,
	status,
	UploadFile
)
from app.config import cfg



async def aio_write_file(file: UploadFile, path: Path, chunk_size=cfg.chunk_size):
	file_path = path / file.filename
	try:
		async with aiofiles.open(file_path, 'wb') as _fb:
			while True:
				chunk = await file.read(chunk_size)
				if not chunk:
					break
				await _fb.write(chunk)

		return file.filename
	except:
		return None



def write_file(file: UploadFile, path: Path, chunk_size=cfg.chunk_size):
	file_path = path / file.filename
	with open(file_path, 'wb') as _fb:
		shutil.copyfileobj(file.file, _fb, chunk_size)

	return file.filename