
# # import requests

# data = {
#     "name" : Obj["arg1"],
#     "email" : "vraj.patel4801@gmail.com"
# }

# resp = {
#     "Response" : 200,
#     "Message" : "Hello From Pyhton File:)",
#     "Data" : data
# }

# print(json.dumps(resp))

# sys.stdout.flush()


# from youtube_transcript_api import YouTubeTranscriptApi as yta 
# import re

# vid_id = 'pdYwZhCAeB0' #pdYwZhCAeB0
# data = yta.get_transcript(vid_id)

# transcript = ''
# for value in data:
#     for key,val in value.items():
#         if key == 'text':
#             transcript += val


# l = transcript.splitlines()
# final_tra = " ".join(l)
# file = open("scriptText.txt", 'w')
# file.write(final_tra)
# file.close()


#===============================

# # https://www.youtube.com/watch?v=w82a1FT5o88
# # https://www.youtube.com/watch?v=OIIg5d_WSMc
# # https://www.youtube.com/watch?v=y0aqyspGsdA
# # https://www.youtube.com/watch?v=S7xTBa93TX8
# # https://www.youtube.com/watch?v=Bf-dbS9CcRU      microsoft
# # https://www.youtube.com/watch?v=ebls5x-gb0s      microsoft
# # https://www.youtube.com/watch?v=-glZip6foVk      microsoft
# # vid_id = 'Bf-dbS9CcRU'
# # vid_id2 = 'ebls5x-gb0s'



import sys
import json
from sklearn.feature_extraction.text import CountVectorizer
from youtube_transcript_api import YouTubeTranscriptApi as yta

videos = json.loads(sys.stdin.read())
# print((videos))
# videos = [
#             {
#                 'videoId': 'w82a1FT5o88',
#                 'title': 'Video 1 Title',
#                 'description': 'Video 1 Description'
#             },
#             {
#                 'videoId': '-glZip6foVk',
#                 'title': 'Streamline business processes with Microsoft 365 Copilot',
#                 'description': 'When you lead a sales team, building customer relationships and closing deals are key. Microsoft 365 Copilot can help lighten the load with next-generation AI. Learn how Microsoft 365 Copilot works across Teams, Viva Sales, and Power Automate to streamline business processes.'
#             },
#             {
#                 'videoId': '26Ccd09JoJM',
#                 'title': 'tester code title',
#                 'description': 'description.'
#             },
#             {
#                 'videoId': 'Bf-dbS9CcRU',
#                 'title': 'The Future of Work With AI - Microsoft March 2023 Event',
#                 'description': 'A special event with Satya Nadella and Jared Spataro focused on how AI will power a whole new way of working for everyone. Introducing Microsoft 365 Copilot Copilot in Microsoft 365 Apps20:29 - The Copilot System 23:01 - Copilot in Teams and Business Process28:57 - Introducing Business Chat33:36 - Microsoft\'s Approach to Responsible AI'
#             },
#             {
#                 'videoId': 'ebls5x-gb0s',
#                 'title': 'Introducing Microsoft 365 Copilot with Outlook, PowerPoint, Excel, and OneNote',
#                 'description': 'Planning a grad party? Microsoft 365 Copilot has you covered. Learn how Microsoft 365 Copilot seamlessly integrates into the apps you use every day to turn your words into the most powerful productivity tool on the planet.Check out these highlights from the March, 16 2023 event'
#             },
#             {
#                 'videoId': 'ORyi6tTMNqE',
#                 'title': 'MERN Stack Full Course 2023 | Complete MERN Stack Developer Course | MERN Stack | Simplilearn',
#                 'description': "Full Stack Developer - MEAN Stack Master's Program (Discount Code: YTBE15): ...",
#             },
#         ]


feasible_videos = []
not_captions = []

for video in videos:
    try:
        transcript_data = yta.get_transcript(video['videoId'])
        transcript_text = ' '.join([value['text'] for value in transcript_data])

        # Combine the title and description into a single string
        title_desc = video['title'] + ' ' + video['description']

        # Vectorize the transcript and title+description
        vectorizer = CountVectorizer()
        vectorizer.fit([transcript_text, title_desc])
        transcript_vec = vectorizer.transform([transcript_text])
        title_desc_vec = vectorizer.transform([title_desc])

        # Count the number of matching words
        feature_names = vectorizer.get_feature_names_out()
        count = 0
        for word in feature_names:
            if title_desc_vec[0, vectorizer.vocabulary_.get(word)] > 0:
                count += transcript_vec[0, vectorizer.vocabulary_.get(word)]

        video['count'] = count
        feasible_videos.append(video)

    except:
        video['count'] = 0
        feasible_videos.append(video)
        # not_captions.append(video)

top_counts_indices = sorted(range(len(feasible_videos)), key=lambda i: feasible_videos[i]['count'], reverse=True)[:5]
top_videos =[]

for index in top_counts_indices:
    video = feasible_videos[index]
    video['count'] = str(video['count'])
    top_videos.append(video)

# for vid in not_captions:
#     error = {"videoId" : vid, "error" : "captions not found:)"}
#     top_videos.append(error)


print(json.dumps(top_videos))
