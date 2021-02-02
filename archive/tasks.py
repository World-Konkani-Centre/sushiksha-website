
# @shared_task
# def get_team_file_weekly():
#     date = timezone.now()
#     print("team file weekly")
#     print("weekly end date " + str(date))
#     date_7 = date - datetime.timedelta(days=7)
#     date_7 = date_7.date()
#     print("weekly start date " + str(date_7))
#     filename = 'Sushiksha-Team-Points-Weekly-' + str(date.date()) + '.csv'
#     filepath = os.path.join(FILE_PATH_FIELD_DIRECTORY, filename)
#     if not os.path.exists(FILE_PATH_FIELD_DIRECTORY):
#         os.makedirs(FILE_PATH_FIELD_DIRECTORY)
#     with open(filepath, 'w+', newline='') as response:
#         writer = csv.writer(response)
#         headers = ['Team Name', 'Total Points']
#         badge_category_start = 2
#         category_points = []
#         categories = BadgeCategory.objects.all().order_by('name')
#         for category in categories:
#             headers.append(category.name)
#             category_points.append(0)
#         headers.append('Points This Week')
#         writer.writerow(headers)
#
#         teams = Teams.objects.all().order_by('name')
#
#         for team in teams:
#             members = team.members.all()
#             points = 0
#             for i in range(0, len(category_points)):
#                 category_points[i] = 0
#             for member in members:
#                 badges_received = Reward.objects.filter(user=member.user, timestamp__lt=date, timestamp__gte=date_7)
#                 for _badge in badges_received:
#                     index = headers.index(_badge.badges.category.name)
#                     category_points[index - badge_category_start] = category_points[
#                                                                         index - badge_category_start] + _badge.badges.points
#                     points = points + _badge.badges.points
#             row_of_team = [team.name, team.points] + category_points + [points]
#             writer.writerow(row_of_team)
#     AnalyticsReport.objects.create(title='Team-Weekly-Report-' + str(date.date()),
#                                    file=filepath)
#     return True
#
#
# @shared_task
# def get_team_file_monthly():
#     date = timezone.now()
#     year = date.year
#     last_month = date.month - 1 if date.month > 1 else 12
#     last_year = date.year - 1
#     if last_month == 12:
#         year = last_year
#     (start_day, end_day) = calendar.monthrange(year, last_month)
#     naive_start_time = DT(year, last_month, start_day, 0, 0)
#     print("team file monthly")
#     print("monthly start date " + str(naive_start_time))
#     naive_end_time = DT(year, last_month, end_day, 0, 0)
#     print("Montly end date " + str(naive_end_time))
#     filename = 'Sushiksha-Team-Points-Monthly-' + str(datetime.date.today()) + '.csv'
#     filepath = os.path.join(FILE_PATH_FIELD_DIRECTORY, filename)
#     if not os.path.exists(FILE_PATH_FIELD_DIRECTORY):
#         os.makedirs(FILE_PATH_FIELD_DIRECTORY)
#     with open(filepath, 'w+', newline='') as response:
#         writer = csv.writer(response)
#         headers = ['Team Name', 'Total Points']
#         badge_category_start = 2
#         category_points = []
#         categories = BadgeCategory.objects.all().order_by('name')
#         for category in categories:
#             headers.append(category.name)
#             category_points.append(0)
#         headers.append('Points of ' + str(last_month) + '-' + str(year))
#         writer.writerow(headers)
#
#         teams = Teams.objects.all().order_by('name')
#
#         for team in teams:
#             members = team.members.all()
#             points = 0
#             for i in range(0, len(category_points)):
#                 category_points[i] = 0
#             for member in members:
#                 badges_received = Reward.objects.filter(user=member.user, timestamp__lte=naive_end_time,
#                                                         timestamp__gte=naive_start_time)
#                 for _badge in badges_received:
#                     index = headers.index(_badge.badges.category.name)
#                     category_points[index - badge_category_start] = category_points[
#                                                                         index - badge_category_start] + _badge.badges.points
#                     points = points + _badge.badges.points
#             row_of_team = [team.name, team.points] + category_points + [points]
#             writer.writerow(row_of_team)
#     AnalyticsReport.objects.create(title='Team-Monthly-Report-' + str(last_month) + '-' + str(year), file=filepath)
#     return True
#
#
# @shared_task
# def get_user_file_weekly():
#     date = timezone.now()
#     print("member file weekly")
#     print("weekly end date " + str(date))
#     date_7 = date - datetime.timedelta(days=7)
#     date_7 = date_7.date()
#     print("weekly start date " + str(date_7))
#     filename = 'Sushiksha-Member-Points-Weekly' + str(datetime.date.today()) + '.csv'
#     filepath = os.path.join(FILE_PATH_FIELD_DIRECTORY, filename)
#     if not os.path.exists(FILE_PATH_FIELD_DIRECTORY):
#         os.makedirs(FILE_PATH_FIELD_DIRECTORY)
#     with open(filepath, 'w+', newline='') as response:
#         writer = csv.writer(response)
#         headers = ['Username', 'Name', 'Email', 'Batch', 'Total Points', 'Stars']
#         badge_category_start = 6
#         category_points = []
#         categories = BadgeCategory.objects.all().order_by('name')
#         for category in categories:
#             headers.append(category.name)
#             category_points.append(0)
#         headers.append('Points This Week')
#         writer.writerow(headers)
#
#         users = User.objects.all().order_by('profile__name')
#
#         for user in users:
#             points = 0
#             badges_received = Reward.objects.filter(user=user, timestamp__lt=date, timestamp__gte=date_7)
#             for i in range(0, len(category_points)):
#                 category_points[i] = 0
#             for _badge in badges_received:
#                 index = headers.index(_badge.badges.category.name)
#                 category_points[index - badge_category_start] = category_points[
#                                                                     index - badge_category_start] + _badge.badges.points
#                 points = points + _badge.badges.points
#             row_of_user = [user.username, user.profile.name, user.email, user.profile.batch, user.profile.points,
#                            user.profile.stars] + category_points + [points]
#             writer.writerow(row_of_user)
#
#         AnalyticsReport.objects.create(
#             title='Members-Weekly-Report-' + str(date.date()), file=filepath)
#         return True
#
#
# @shared_task
# def get_user_file_monthly():
#     print("member file monthly")
#     date = datetime.datetime.now()
#     year = date.year
#     last_month = date.month - 1 if date.month > 1 else 12
#     last_year = date.year - 1
#     if last_month == 12:
#         year = last_year
#     (start_day, end_day) = calendar.monthrange(year, last_month)
#     naive_start_time = DT(year, last_month, start_day, 0, 0)
#     print("monthly start date " + str(naive_start_time))
#     naive_end_time = DT(year, last_month, end_day, 0, 0)
#     print("Montly end date " + str(naive_end_time))
#     filename = 'Sushiksha-Member-Points-Monthly-' + str(datetime.date.today()) + '.csv'
#     filepath = os.path.join(FILE_PATH_FIELD_DIRECTORY, filename)
#     if not os.path.exists(FILE_PATH_FIELD_DIRECTORY):
#         os.makedirs(FILE_PATH_FIELD_DIRECTORY)
#     with open(filepath, 'w+', newline='') as response:
#         writer = csv.writer(response)
#         headers = ['Username', 'Name', 'Email', 'Batch', 'Total Points', 'Stars']
#         badge_category_start = 6
#         category_points = []
#         categories = BadgeCategory.objects.all().order_by('name')
#         for category in categories:
#             headers.append(category.name)
#             category_points.append(0)
#         headers.append('Points of ' + str(last_month) + '-' + str(year))
#         writer.writerow(headers)
#
#         users = User.objects.all().order_by('profile__name')
#
#         for user in users:
#             points = 0
#             badges_received = Reward.objects.filter(user=user, timestamp__lte=naive_start_time,
#                                                     timestamp__gte=naive_end_time)
#             for i in range(0, len(category_points)):
#                 category_points[i] = 0
#             for _badge in badges_received:
#                 index = headers.index(_badge.badges.category.name)
#                 category_points[index - badge_category_start] = category_points[
#                                                                     index - badge_category_start] + _badge.badges.points
#                 points = points + _badge.badges.points
#             row_of_user = [user.username, user.profile.name, user.email, user.profile.batch, user.profile.points,
#                            user.profile.stars] + category_points + [points]
#             writer.writerow(row_of_user)
#
#         AnalyticsReport.objects.create(title='Members-Monthly-Report-' + str(last_month) + '-' + str(year),
#                                        file=filepath)
#         return True
