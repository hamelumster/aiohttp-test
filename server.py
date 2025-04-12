from aiohttp import web
from aiohttp.web import HTTPNotFound
import json

from models import init_orm, close_orm, User, Announcement, Session

app = web.Application()

async def orm_context(app: web.Application):
    print("start")
    await init_orm()
    yield
    await close_orm()
    print("finish")


def generate_error(err_cls, message):
    message = json.dumps({"error": message})
    return err_cls(text=message, content_type="application/json")


async def get_user_by_id(user_id: int, session) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise generate_error(HTTPNotFound, "User not found")
    return user


async def get_announcement_by_id(announcement_id: int, session) -> Announcement:
    announcement = await session.get(Announcement, announcement_id)
    if announcement is None:
        raise generate_error(HTTPNotFound, "Announcement not found")
    return announcement


class UserView(web.View):
    async def get(self):
        async with Session() as session:
            user_id = int(self.request.match_info["user_id"])
            user = await get_user_by_id(user_id, session)
            return web.json_response(user.json)

    async def post(self):
        pass


class AnnouncementView(web.View):
    async def get(self):
        async with Session() as session:
            announcement_id = int(self.request.match_info["announcement_id"])
            announcement = await get_announcement_by_id(announcement_id, session)
            return web.json_response(announcement.json)

    async def post(self):
        pass

    async def delete(self):
        pass

    async def patch(self):
        pass

app.cleanup_ctx.append(orm_context)

app.add_routes([
    web.get('/api/v1/users/{user_id:[0-9]+}', UserView),
    web.post('/api/v1/users', UserView),
    web.get('/api/v1/announcement/{announcement_id:[0-9]+}', AnnouncementView),
    web.post('/api/v1/announcement', AnnouncementView),
    web.patch('/api/v1/announcement/{announcement_id:[0-9]+}', AnnouncementView),
    web.delete('/api/v1/announcement/{announcement_id:[0-9]+}', AnnouncementView),
])

web.run_app(app)
