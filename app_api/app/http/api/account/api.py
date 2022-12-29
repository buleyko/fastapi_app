from app.vendors.base.router import AppRoute
from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    status,
    Path,
    Query,
    UploadFile,
)
from app.vendors.dependencies.database import (
    get_db,
    DB,
)
from . import services as srv
from . import schemas as sch
from app.config import cfg

account = APIRouter(
    route_class=AppRoute,
    prefix='/account',
    tags=['account'],
)


@account.get('/list/',
             response_model=list[sch.AccountOutItem],
             status_code=status.HTTP_200_OK
             )
async def read_accounts(
        skip: int = 0,
        limit: int = Query(cfg.items_in_list, gt=1),
        db: DB = Depends(get_db)
):
    print(q := 1 / 0)
    return srv.get_accounts(db, skip=skip, limit=limit)


@account.get('/{account_id}/show/',
             response_model=sch.AccountOutItem,
             status_code=status.HTTP_200_OK
             )
async def read_account(account_id: int = Path(..., gt=1), db: DB = Depends(get_db)):
    return srv.get_account(db, account_id=account_id)


# upload video
from app.vendors.helpers.file import (
    write_file, aio_write_file, 
    async_write_file, get_or_create_storage_dir,
)
@account.post('/video-upload/')
async def video_upload(file: UploadFile):
    if file.content_type != 'video/mp4':
        raise HTTPException( # HTTP_422_UNPROCESSABLE_ENTITY or HTTP_406_NOT_ACCEPTABLE
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail='Not valid file extension',
        )
    current_account_name = 'some_user_name'
    ext_video_path = f'video/account/{current_account_name}/mp4'
    storage_path = cfg.root_path / cfg.upload_folder_dir
    dir_path = get_or_create_storage_dir(storage_path, ext_video_path)
    res = await aio_write_file(file, dir_path)
    return {'file': f'{ext_video_path}/{res}'}
    # return {'file': f'{ext_video_path}/{file.filename}'}
    # return srv.video_upload(file)

# streaming video
from typing import Generator
from fastapi.responses import (
    StreamingResponse, 
    HTMLResponse,
)

async def fake_video_streamer(file_path) -> Generator:
    with open(file=file_path, mode='rb') as file_like:
        yield file_like.read()

@account.get('/video-show/{file_name}/')
async def get_video(file_name: str):
    current_account_name = 'some_user_name'
    ext_video_path = f'video/account/{current_account_name}/mp4'
    storage_path = cfg.root_path / cfg.upload_folder_dir
    file_path = storage_path / ext_video_path / file_name
    return StreamingResponse(fake_video_streamer(file_path), media_type='video/mp4')


@account.get('/video-show-page/{file_name}/')
async def show_video_page(file_name: str):
    html_content = f'''
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Some HTML in here</title>
            <link href="https://vjs.zencdn.net/7.10.2/video-js.css" rel="stylesheet" />
        </head>
        <body>
            <h1>Look ma! HTML!</h1>

            <video
                id="my-video"
                class="video-js"
                controls
                preload="auto"
                width="400"
                height="300"
                data-setup="{{}}"
            >
                <source src="http://127.0.0.1:4040/account/video-show/{file_name}" type="video/mp4" />
                <source src="http://127.0.0.1:4040/account/video-show/{file_name}" type="video/webm" />
            </video>

            <script src="https://vjs.zencdn.net/7.10.2/video.min.js"></script>
        </body>
    </html>
    '''
    return HTMLResponse(content=html_content, status_code=200)


# @account.post('/image-upload/')
# async def image_upload(files: list[UploadFile]):
#     res = await srv.image_upload(files)
#     return {'q': 'Q'}