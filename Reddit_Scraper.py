import praw
import pandas as pd
import csv, json
import pickle
import os
import random
import numpy as np


# read in csv for post IDs
posts = pd.read_csv('aita_clean.csv')
post_ids = posts.id.values.tolist()

# get ids already processed
processed_posts = os.listdir('comments/')
processed_posts = [i[:6] for i in processed_posts]

# remove processed files from post_ids
post_ids = list(np.setdiff1d(np.array(post_ids),np.array(processed_posts), assume_unique = True))

# shuffle post_ids order
random.shuffle(post_ids)

# fish_the_fred account
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="",
    username="",
)

print(reddit.user.me())

def get_comments(post_id):
    
    # retrieve post submission object
    submission = reddit.submission(id = post_id)
    
    # set comment sort for best
    submission.comment_sort = 'best'

    # Set comment limit to 3
    submission.cmment_limit = 3
    
    # get comment forest object from submission
    comment_forest = submission.comments

    # pull out top 3 comments and append to list
    comment_list = []
    for i, comment in enumerate(comment_forest):
        if i < 3:
            comment_list.append((post_id,comment.body, comment.ups, comment.score))
    
    return comment_list

for post_id in post_ids:
    processed_posts = os.listdir('comments/')
    processed_posts = [i[:6] for i in processed_posts]

    if post_id not in processed_posts:
        # create pkl file for each post id
        with open('comments/{}_data.pkl'.format(post_id), 'wb') as outp:
            # retrieve comments
            data = get_comments(post_id)
            # dump data into a pickle file
            pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)