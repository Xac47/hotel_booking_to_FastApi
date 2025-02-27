from app.users.dao import UserDAO


async def test_find_user_by_id():
    user = await UserDAO.find_by_id(1)
    
    print(user)
    