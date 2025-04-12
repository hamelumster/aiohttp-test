from aiohttp import web

from models import init_orm, close_orm, User, Announcement

app = web.Application()

async def orm_context(app: web.Application):
    print("start")
    await init_orm()
    yield
    await close_orm()
    print("finish")

async def get_user_by_id(user_id: int, session) -> User:
    user = await session.get(User, user_id)
    return user

async def get_announcement_by_id(announcement_id: int, session) -> Announcement:
    announcement = await session.get(Announcement, announcement_id)
    return announcement


class UserView(web.View):
    async def get(self):
        pass

    async def post(self):
        pass


class AnnouncementView(web.View):
    async def get(self):
        pass

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
