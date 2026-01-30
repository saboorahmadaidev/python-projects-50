from instabot import Bot
bot = Bot()
bot.login(username="your_password", password="your_password")
bot.follow("saboor_ahamd_22")
bot.upload_photo("path_to_your_photo.jpg", caption="Your caption here")
bot.unfollow("user_to_unfollow")
followers = bot.get_user_followers("your_username")
for follower in followers:
    print(bot.get_user_info(follower))
following = bot.get_user_following("your_username")
for Following in following:
    print(bot.get_user_info(Following))