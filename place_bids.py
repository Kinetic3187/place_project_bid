from locale import currency
from freelancersdk.resources.projects import place_project_bid
from freelancersdk.session import Session
from freelancersdk.resources.users \
    import get_self_user_id
from freelancersdk.resources.projects.projects import (
    get_projects, get_project_by_id
)
from freelancersdk.resources.projects.helpers import (
    create_get_projects_object, create_get_projects_project_details_object,
    create_get_projects_user_details_object
)
from freelancersdk.exceptions import BidNotPlacedException
from freelancersdk.resources.projects.exceptions import \
    ProjectsNotFoundException
from freelancersdk.resources.projects.helpers import (
    create_search_projects_filter,
    create_get_projects_user_details_object,
    create_get_projects_project_details_object,
)
from freelancersdk.resources.projects.projects import search_projects
from freelancersdk.resources.projects.exceptions import \
    ProjectsNotFoundException

from freelancersdk.resources.users.users import get_self
from freelancersdk.resources.users.exceptions import \
    SelfNotRetrievedException
from freelancersdk.resources.users.helpers import (
    create_get_users_details_object
)

from freelancersdk.resources.projects.projects import get_bids
from freelancersdk.resources.projects.exceptions import \
    BidsNotFoundException

import os
import json

import time
import requests

freelancer_oauth_token = "b3Zw1MbRtiUyJFyU4FAbrzNy3sv7iz"
chat_id = "-664070387"

BOT_TOKEN = "5317996229:AAFFNPKde5Bi5iQsJlD8cAWZSG2CuTN3Bb4"
base_url = "https://api.telegram.org/bot" + BOT_TOKEN
offset = 0

time_interval = 60  # (in seconds) Specify the frequency of code execution

url = os.environ.get('https://www.freelancer.com/dashboard')
bid_description = '''
Dear Prospective Client,
The project you posted caught my attention because it is similar to the work I have done in the past for other clients.
I have 4 years of experience in website designing and programming, as I have worked on several projects that involves both design and programming. Some of them are;
http://tindog-co-uk.stackstaging.com/
A tindog template

http://orange-com-ng.stackstaging.com/
A Ecommerce website (still working on the backend as at the time of bidding)

http://lonirry-com-ng.stackstaging.com/
a wristwatch design

I created all those, this gives me the right experience and know-all that you're looking for.
I give all these in the completion of my clients’ project by following the steps below:
✓ Fully hand code
✓ Highly professional html template and responsive design on all devices
✓ All browsers compatible
✓ Customized design

Why choose me?
✓ Unlimited revision until satisfaction.
✓ 100% Money back Guarantee.
✓ 4+ years’ experience in Web Design and development.
✓ Fluent in English and Project Understanding
✓ Always Available
✓ Fully code html template
✓ 100% copyright safe content.


 Habeeb Bello

'''


def sample_search_projects():
    session = Session(oauth_token=freelancer_oauth_token, url=url)

    query = 'Html Css Php javascript mysql'
    search_filter = create_search_projects_filter(
        sort_field='time_updated',
        min_avg_price=100,
        project_types='fixed',
        or_search_query=True,
    )

    try:
        p = search_projects(
            session,
            query=query,
            search_filter=search_filter
        )

    except ProjectsNotFoundException as e:
        print('Error message: {}'.format(e.message))
        print('Server response: {}'.format(e.error_code))
        return None
    else:
        return p


while True:
    p = sample_search_projects()
    time.sleep(time_interval)

    if p:

        for x in p.get('projects'):
            title = x.get('title')

            project_id = x.get('id')

            session = Session(oauth_token=freelancer_oauth_token, url=url)
            my_user_id = get_self_user_id(session)

            get_bids_data = {
                'project_ids': [project_id],
                'limit': 25,
                'offset': 0,
            }

            # bid amount = (Project MAX Budget - Avergage Bid AMount)/2 + Avergage Bid Amount
            # You can write your own formula
            amount = int((x.get('budget').get('maximum') - x.get('bid_stats').get('bid_avg')) / 2) + x.get(
                'bid_stats').get('bid_avg')

            try:
                bid = get_bids(session, **get_bids_data)
                if bid and x.get('status') == 'active' and (
                        x.get('currency').get('code') == 'USD' or x.get('currency').get('code') == 'AUD'):
                    print('Found bids: {}'.format(len(bid['bids'])))
                    if len(bid['bids']) < 20:
                        bid_data = {
                            'project_id': int(project_id),
                            'bidder_id': my_user_id,
                            'amount': amount - 75,
                            'period': 7,
                            'milestone_percentage': 20,
                            'description': bid_description,
                        }

                        print(bid_data)
                        print('https://www.freelancer.com/projects/' + x.get('seo_url'))
                        message = 'https://www.freelancer.com/projects/' + x.get('seo_url')
                        b = place_project_bid(session, **bid_data)
                        if b:
                            print('*********************')
                            print(("Bid placed: %s" % b))
                            parameters = {
                                "chat_id": chat_id,
                                "text": message,
                            }
                            resp = requests.get(base_url + "/sendMessage", data=parameters)



            except BidsNotFoundException as e:
                print('Error message: {}'.format(e.message))
                print('Server response: {}'.format(e.error_code))
                continue
            except:
                continue






