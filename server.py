from aiohttp import web
from aiohttp.web import HTTPNotFound
import json

from models import init_orm, close_orm, User, Announcement, Session
from sqlalchemy.ext import IntegrityError

app = web.Application()

async def orm_context(app: web.Application):
    print("start")
    await init_orm()
    yield
    await close_orm()
    print("finish")

async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


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

async def add_user(user: User, session) -> User:
    try:
        session.add(user)
        await session.commit()
        return user
    except IntegrityError:
        raise generate_error(web.HTTPConflict, "User already exists")


class UserView(web.View):

    @property
    def session(self):
        return self.request.session

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get_current_user(self):
        user = await get_user_by_id(self.user_id, self.session)
        return user

    async def get(self):
        user = await self.get_current_user()
        return web.json_response(user.json)

    async def post(self):
        json_data = await self.request.json()
        name = json_data["name"]
        password = json_data["password"]
        user = User(name=name, password=password)
        await add_user(user, self.session)
        return web.json_response(user.json_id)


class AnnouncementView(web.View):

    @property
    def session(self):
        return self.request.session

    @property
    def announcement_id(self):
        return int(self.request.match_info["announcement_id"])

    async def get_current_announcement(self):
        announcement = await get_announcement_by_id(self.announcement_id, self.session)
        return announcement

    async def get(self):
        announcement = await self.get_current_announcement()
        return web.json_response(announcement.json)

    async def post(self):
        json_data = await self.request.json()
        title = json_data["title"]
        description = json_data["description"]
        announcement = Announcement(title=title, description=description)
        self.session.add(announcement)
        await self.session.commit()
        return web.json_response(announcement.json)

    async def delete(self):
        announcement = await self.get_current_announcement()
        await self.session.delete(announcement)
        await self.session.commit()
        return web.json_response({"status": "ok"})

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
