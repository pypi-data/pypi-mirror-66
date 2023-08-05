#!/usr/bin/env python
import requests
import json
import hashlib
import time

class MailchimpService():
    def __init__(self, api_key, region='us'):
        self.baseurl = 'https://{}.api.mailchimp.com/3.0'.format(region)
        self.headers = {
            'content-type': 'application/json'
        }
        self.api_key = api_key
        self.username = "mocherry-client"

    def subscribe_to_mailing_list(self, list_id, params):
        member_id = str(hashlib.md5(params['email'].lower().encode('utf-8')).hexdigest())
        endpoint = "{}/lists/{}/members/{}".format(self.baseurl, list_id, member_id)
        payload = json.dumps({
            'status': 'subscribed',
            'email_address': params['email'],
            'merge_fields': {
                'FNAME': params['firstname'],
                'LNAME': params['lastname']
            },
        })
        resp = requests.put(endpoint, auth=(self.username, self.api_key), data=payload)
        return resp.json()

    def unsubscribe_from_mailing_list(self, list_id, email):
        member_id = str(hashlib.md5(email.lower().encode('utf-8')).hexdigest())
        endpoint = '{}/lists/{}/members/{}'.format(self.baseurl, list_id, member_id)

        payload = json.dumps({
            'status': 'unsubscribed'
        })
        resp = requests.put(endpoint, auth=(self.username, self.api_key), data=payload)
        return resp.json()




