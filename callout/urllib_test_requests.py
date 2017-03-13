import urllib.request
import json
import tempfile
import sys

BASE_URL = 'http://127.0.0.1:8000/'
users_file = 'user.txt'
posts_file = 'post.txt'
posts_remarks_file = 'post_remark.txt'
posts_reactions_file = 'post_reaction.txt'

callouts_file = 'callout.txt'
callouts_remarks_file = 'callout_remark.txt'
callouts_reactions_file = 'callout_reaction.txt'

EMAIL = 0, PASSWORD = 1, FNAME = 2, LNAME = 3, DOB = 4, USERID = 5, TOKEN = 6, MEDIAID = 7
MEDIAS = 0, TITLE = 1, CAPTION = 2, POST_TOKEN = 3, POSTID = 4
REMARK = 0, REMARK_TYPE = 1, REMARK_USERID = 2, REMARK_TOKEN = 3, REMARKID = 4

user_headers = ["email", "password", "first_name", "last_name", "date_of_birth"]
post_headers = ["title", "caption", "medias"]
remark_headers = ["remark", "remark_type"]
callout_headers = ["title", "pub_date", "o_posts"]

def response(request):
    return urllib.request.urlopen(request).read()

def json_request_with_data(url, data, token=None):
    if token is None:
        return urllib.request.Request(BASE_URL+url, data=data, headers={'content-type':'application/json'})
    else:
        return urllib.request.Request(BASE_URL+url, data=data, headers={'content-type':'application/json', 'Authorization':'Token %s' % token})

def json_request_without_data(url, token=None):
    if token is None:
        return urllib.request.Request(BASE_URL+url, headers={'content-type':'application/json'})
    else:
        return urllib.request.Request(BASE_URL+url, headers={'content-type':'application/json', 'Authorization':'Token %s' % token})        

def from_json(response):
    return json.loads(response.decode('utf8'))

def register_user():
    temp = tempfile.NamedTemporaryFile(mode='r+')
    file = open(users_file, 'r')
    for line in file:
        data = '{'
        x = 0
        for w in line.split():
            data += '"{0}":"{1}", '.format(user_headers[x], w)
            x+=1

        data=data[:-2]+'}'
        """ form json request """
        request=json_request_with_data('account/register/',data)
        """ send request and get returned response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
        """ write to temporary file """
        temp.write(line.rstrip()+ value['user_id'])

    file.close()
    
    temp.seek(0)

    file = open(filename, "w")

    for line in temp:
        file.write(line)

    temp.close()


def login_user(data):
    temp = tempfile.NamedTemporaryFile(mode='r+')
    file = open(users_file, 'r')
    for line in file:
        data = '{'
        line_arr = line.split()
        data += '"username":"{0}", "passowrd":"{1}"}'.format(line_arr[EMAIL], line_arr[PASSWORD])

        """ form json request """
        request=json_request_with_data('account/login/',data)
        """ send request and get returned response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
        """ write to temporary file """
        temp.write(line.rstrip()+ value['token'])

    file.close()
    
    temp.seek(0)

    file = open(filename, "w")

    for line in temp:
        file.write(line)

    temp.close()

def edit_user(data, token):
    file = open(users_file, 'r')
    for line in file:
        data = '{'
        x = 0
        line_arr = line.split()
        for w in line_arr:
            if x > EMAIL && x < USERID:
                if x == FIRST_NAME:
                    data += '"{0}":"{1}", '.format(header[x], w+"edited" )
                else:
                    data += '"{0}":"{1}", '.format(header[x], "" )
            x+=1

        data=data[:-2]+'}'

        """ form json request """
        request=json_request_with_data('account/user/edit/', data, token)
        """ send request and get returned response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def get_user(user_id, token):
    file = open(users_file, 'r')

    for line in file:
        line_arr=line.split()
        """ form json request """
        request=json_request_without_data('account/user/'+user_id+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def get_extended_user(user_id, token):
    file = open(users_file, 'r')

    for line in file:
        line_arr=line.split()
        """ form json request """
        request=json_request_without_data('account/user/details/'+user_id+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()
        
        
def put_display_picture(media_id, token):
    file = open(users_file, 'r')

    for line in file:
        """ form json request """
        request=json_request_without_data('account/user/details/'+media_id+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def create_post():


def get_list_of_posts(token):
    file = open(users_file, 'r')

    for line in file:
        """ form json request """
        request=json_request_without_data('post/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()

def get_post(post_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(posts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('post/'+post_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()

def edit_post(post_id, data, token):
    file = open(posts_file, 'r')
    for line in file:
        data = '{'
        x = 0
        line_arr = line.split()
        for w in line_arr:
            if x < POSTID:
                if x == CAPTION:
                    data += '"{0}":"{1}", '.format(header[x], w+"edited" )
                else:
                    data += '"{0}":"{1}", '.format(header[x], "" )
            x+=1

        data=data[:-2]+'}'
        """ form json request """
        request=json_request_with_data('post/edit/'+post_id+'/', data, token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def delete_post(post_id, token):
    file = open(posts_file, 'r')

    for line in file:
        line_arr = line.split()
        request=json_request_without_data('post/remove/'+post_id+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def create_post_remark(post_id, data, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(posts_file, 'r')

    for line in file:
        for token in token_arr:
            data = '{"remark":"remark on post", "remark_type":"open"}'
            """ form json request """
            request=json_request_with_data('post/remark/'+post_id+'/', data, token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def get_list_of_post_remarks(post_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(posts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('post/remarks/'+post_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def edit_post_remark(remark_id, data, token):
    file = open(posts_remarks_file, 'r')
    for line in file:
        data = '{'
        x = 0
        line_arr = line.split()
        for w in line_arr:
            if x < REMARK_TYPE:
                if x == REMARK:
                    data += '"{0}":"{1}", '.format(header[x], w+" edited" )
                else:
                    data += '"{0}":"{1}", '.format(header[x], "" )
            x+=1

        data=data[:-2]+'}'
        """ form json request """
        request=json_request_with_data('post/edit/remark/'+remark_id+'/', data, token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def delete_post_remark(remark_id, token):
    file = open(posts_remarks_file, 'r')

    for line in file:
        line_arr = line.split()
        request=json_request_without_data('post/remove/remark/'+remark_id+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def get_number_of_post_remarks(post_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(posts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('post/count/remarks/'+post_d+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def create_post_reaction(post_id, reaction_type, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(posts_file, 'r')

    for line in file:
        for token in token_arr:
            reaction_type = 'fancy'
            """ form json request """
            request=json_request_without_data('post/reaction/'+post_id+'/'+reaction_type+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()        

    file.close()


def get_list_of_post_reactions(post_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(posts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('post/reactions/'+post_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def edit_post_reaction(reaction_id, reaction_type, token):
    file = open(posts_reactions_file, 'r')
    for line in file:
        line_arr = line.split()
        reaction_type = 'disapproval'
        """ form json request """
        request=json_request_without_data('post/edit/reaction/'+reaction_id+'/'+reaction_type+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def delete_post_reaction(reaction_id, token):
    file = open(posts_reactions_file, 'r')

    for line in file:
        line_arr = line.split()
        request=json_request_without_data('post/remove/reaction/'+reaction_id+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def get_number_of_post_reactions(post_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(posts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('post/count/reactions/'+post_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()




def challenge_posts():
    


def get_list_of_callouts(token):
    file = open(users_file, 'r')

    for line in file:
        """ form json request """
        request=json_request_without_data('callout/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()

def get_callout(callout_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(callouts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('callout/'+callout_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()

def edit_callout(callout_id, data, token):
    file = open(callouts_file, 'r')
    for line in file:
        data = '{'
        x = 0
        line_arr = line.split()
        for w in line_arr:
            if x < CALLOUTID:
                if x == CAPTION:
                    data += '"{0}":"{1}", '.format(header[x], w+"edited" )
                else:
                    data += '"{0}":"{1}", '.format(header[x], "" )
            x+=1

        data=data[:-2]+'}'
        """ form json request """
        request=json_request_with_data('callout/edit/'+callout_id+'/', data, token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def delete_callout(callout_id, token):
    file = open(callouts_file, 'r')

    for line in file:
        line_arr = line.split()
        request=json_request_without_data('callout/remove/'+callout_id+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def create_callout_remark(callout_id, data, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(callouts_file, 'r')

    for line in file:
        for token in token_arr:
            data = '{"remark":"remark on callout", "remark_type":"open"}'
            """ form json request """
            request=json_request_with_data('callout/remark/'+callout_id+'/', data, token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def get_list_of_callout_remarks(callout_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(callouts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('callout/remarks/'+callout_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def edit_callout_remark(remark_id, data, token):
    file = open(callouts_remarks_file, 'r')
    for line in file:
        data = '{'
        x = 0
        line_arr = line.split()
        for w in line_arr:
            if x < REMARK_TYPE:
                if x == REMARK:
                    data += '"{0}":"{1}", '.format(header[x], w+" edited" )
                else:
                    data += '"{0}":"{1}", '.format(header[x], "" )
            x+=1

        data=data[:-2]+'}'
        """ form json request """
        request=json_request_with_data('callout/edit/remark/'+remark_id+'/', data, token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def delete_callout_remark(remark_id, token):
    file = open(callouts_remarks_file, 'r')

    for line in file:
        line_arr = line.split()
        request=json_request_without_data('callout/remove/remark/'+remark_id+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def get_number_of_callout_remarks(callout_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(callouts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('callout/count/remarks/'+callout_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def create_callout_reaction(callout_id, reaction_type, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(callouts_file, 'r')

    for line in file:
        for token in token_arr:
            reaction_type = 'fancy'
            """ form json request """
            request=json_request_without_data('callout/reaction/'+callout_id+'/'+reaction_type+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def get_list_of_callout_reactions(callout_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(callouts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('callout/reactions/'+callout_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def edit_callout_reaction(reaction_id, reaction_type, token):
    file = open(callouts_reactions_file, 'r')
    for line in file:
        line_arr = line.split()
        reaction_type = 'disapproval'
        """ form json request """
        request=json_request_without_data('callout/edit/reaction/'+reaction_id+'/'+reaction_type+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def delete_callout_reaction(reaction_id, token):
    file = open(callouts_reaction_file, 'r')

    for line in file:
        line_arr = line.split()
        request=json_request_without_data('callout/remove/reaction/'+reaction_id+'/', token)
        """ send the request and get a response """
        response=response(request)
        """ convert json response to object """
        value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def get_number_of_callout_reactions(callout_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(callouts_file, 'r')

    for line in file:
        for token in token_arr:
            """ form json request """
            request=json_request_without_data('callout/count/reactions/'+callout_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

def respond_to_challenge(status, opost_id, token):
    file = open(users_file, 'r')
    token_arr = []
    for line in file:
        token_arr.add(line.split()[TOKEN])

    file.close()
    
    file = open(challenges_file, 'r')
    
    for line in file:
        status = 'accept'
        for token in token_arr:
            request=json_request_without_data('callout/challenge/'+status+'/'+opost_id+'/', token)
            """ send the request and get a response """
            response=response(request)
            """ convert json response to object """
            value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

def get_list_of_fans(token):
    file = open(users_file, 'r')
    for line in file:

    request=json_request_without_data('fan/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()

def remove_fan_request(request_id, token):
    request=json_request_without_data('fan/remove/request/'+request_id+'/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()


def get_number_of_requests(token):
    file = open(users_file, 'r')
    for line in file:

    request=json_request_without_data('fan/count/requests/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()

def put_follow_request(user_id, token):
    file = open(users_file, 'r')
    for line in file:

    request=json_request_without_data('fan/'+user_id+'/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

    file.close()


def respond_to_follow_request(status, request_id, token):
    request=json_request_without_data('fan/request/'+status+'/'+request_id+'/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

def request_seen(token):
    request=json_request_without_data('fan/seen/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

def fan_seen(user_id, token):
    request=json_request_without_data('fan/seen/'+user_id+'/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

def get_list_of_notifications(token):
    request=json_request_without_data('notification/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

def delete_notification(notification_id, token):
    request=json_request_without_data('notification/remove/'+notification_id+'/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

def get_number_of_notifications(token):
    request=json_request_without_data('notification/count/notifications/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()

def notification_seen(notification_id, token):
    request=json_request_without_data('notification/seen/'+notification_id+'/', token)
    """ send the request and get a response """
    response=response(request)
    """ convert json response to object """
    value=from_json(response)
    """ print the returned object when in debug mode """
    debug_print(value)
    """ return status code """"
    return response.getcode()
