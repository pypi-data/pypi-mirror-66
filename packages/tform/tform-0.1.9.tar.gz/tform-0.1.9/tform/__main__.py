import fire
import requests
import json
from pathlib import Path
import os
import yaml
import datetime

__version__ = '0.1.8'

def dict_drop_keys(key,var):
    new = {}
    for k, v in var.items():
        if k == key:
            pass
        elif isinstance(v, dict):
            new[k] = dict_drop_keys(key, v)
        elif isinstance(v, list):
            new[k] = [dict_drop_keys(key, d) for d in v]
        else:
            new[k] = var[k]
    return new



def read_user_config():
    file = Path(os.path.expanduser("~/.tformconfig.json"))
    if not file.exists():
        print(' \
\n \n \
You do not appear to have a tform config. Please see \
https://gitlab.com/jumpingrivers/wiki/wikis/guides/tform \
\n \n \
        ')
        raise FileNotFoundError('No typeform credentials found. Try tform setup')
    d = json.loads(file.read_text())
    if not 'token' in d:
        raise KeyError('You have no key in your typeform credentials. Try tform setup')
    return d['token']#, d['template_workspace']


def create_header(token):
    headers = {
        'Authorization': 'Bearer %s' % (token)
    }
    return headers

def ctor(loader, suffix, node):
    return suffix+node.value

yaml.add_multi_constructor('',ctor)

def read_course_config():
    with open('./questionnaire.yml') as f:
        y = yaml.load(f)
    return y

def prompt_course_config():
    user = input('Please enter your name: ')
    user = user.replace(' ', '-').lower()
    end = input('What is the last date of the course, YYYY-MM-DD: ')
    end = datetime.datetime.strptime(end,'%Y-%m-%d').date()
    while not isinstance(end, datetime.date):
        end = input('Please choose a date of the format YYY-MM-DD.\n \
                    Eg the 3rd \
                    February 2019 would be 2019-02-03')
    client = input('What is the name of the client: ')
    template = input('\n\n Which template would you like to use? The default is the \
standard one or two day course template. \
\n \n \
Press enter to accept the default or provide an\
alternative. \
\n\n \
To see the names of templates, cancel this prompt and run \
tform templates. ')
    if template == '':
        template = '20XX-XX-standardcourse'
    return {
        'user': user,
        'end': end,
        'client': client,
        'template': template
    }



def check_config(config_dict):
    if not isinstance(config_dict['end'], datetime.date):
        raise TypeError('Date should be formatted as YYYY-MM-DD')

class TypeformCLI(object):


    def __init__(self):
        self._base_url = 'https://api.typeform.com/forms'

    def setup(self):
        """
        Will create a ~/.tformconfig.json for storing the key and workspace
        :return: None
        """
        key = input('Please enter your personal access token: ')
        #uname = input('Please enter your default username: ')
        d = {
            'token': key
        #    'uname': uname
        }
        file = Path(os.path.expanduser("~/.tformconfig.json"))
        file.write_text(json.dumps(d))
        return None

    def templates(self):
        """
        List out templates that could be used for cloning
        """
        token= read_user_config()
        template_workspace = self.get_workspace_id('Templates')
        payload = {'workspace_id': template_workspace}
        headers = create_header(token)
        r = requests.get(self._base_url, params=payload, headers = headers)
        response = r.json()
        response = [( x['title'], x['last_updated_at'], x['id']) for x in response['items']]
        print( ('name','last_updated','id') )
        for r in response:
            print(r)
        return None

    def get_template_id(self, name):
        token = read_user_config()
        template_workspace = self.get_workspace_id('Templates')
        payload = {
            'workspace_id': template_workspace,
            'page_size': 50
        }
        headers = create_header(token)
        r = requests.get(self._base_url, params=payload, headers=headers)
        response = r.json()
        response = {
            x['title'] : x['id'] for x in response['items']
        }
        return response[name]


    def create_workspace(self, name):
        url = 'https://api.typeform.com/workspaces'
        token = read_user_config()
        headers = create_header(token)
        headers['Content-Type'] = 'application/json'
        d = {
            'name': name
        }
        r = requests.post(url,data = json.dumps(d), headers=headers)

    def workspace_exists(self, name):
        token = read_user_config()
        headers = create_header(token)
        r = requests.get('https://api.typeform.com/workspaces', headers=headers)
        response = r.json()
        names = [x['name'] for x in response['items']]
        return name in names

    def get_workspace_id(self,name):
        token = read_user_config()
        headers = create_header(token)
        r = requests.get('https://api.typeform.com/workspaces?page_size=50', headers=headers)
        response = r.json()
        response = {
            x['name']: x['id'] for x in response['items']
        }
        return response[name]

    def workspaces(self):
        """
        List out the workspace names and ids
        """
        token = read_user_config()
        headers = create_header(token)
        r = requests.get('https://api.typeform.com/workspaces', headers = headers)
        response = r.json()
        response = [(x['id'], x['name']) for x in response['items']]
        print( ('id    ', 'name') )
        for r in response:
            print(r)
        return None
    
    def get_link(self, name, workspace_name):
        token = read_user_config()
        headers = create_header(token)
        workspace_id = self.get_workspace_id(workspace_name)
        payload = {
            "workspace_id": workspace_id
        }
        r = requests.get(self._base_url, params=payload, headers = headers)
        response = r.json()
        links = {
             x['title'] : x['_links']['display'] for x in response['items']
        }
        return links[name]

    def check_exists(self, name, workspace_name):
        token = read_user_config()
        headers = create_header(token)
        workspace_id = self.get_workspace_id(workspace_name)
        payload = {
            "workspace_id": workspace_id
        }
        r = requests.get(self._base_url, params=payload, headers = headers)
        response = r.json()
        titles = [x['title'] for x in response['items']]
        return name in titles

    def create_from_config(self):
        config = prompt_course_config()
        check_config(config)
        # new typeform name
        client = config['client']
        date = config['end']
        template = config['template']
        user = config['user']
        newname = str(date)+'_'+client+'_'+user
        # workspace name
        workspace_name = 'feedback-' + str(date)[:-3]
        if not self.workspace_exists(workspace_name):
            self.create_workspace(workspace_name)
        if self.check_exists(newname, workspace_name):
            input('A typeform with this name in this workspace already exists')
            new_link = self.get_link(newname, workspace_name)
        else:
            workspace_id = self.get_workspace_id(workspace_name)
            template_id = self.get_template_id(template)
            new_link = self.clone(template_id, workspace_id, newname)
        with open('feedback_link.yaml','w') as f:
            f.write(f'url: {new_link}\n')
            f.write(f'validfrom: {datetime.date.today()}\n')
            f.write(f'validto: {date}\n')

    def create_yaml_template(self):
        uname = input('Please enter your username: ')
        payload = {
            'user': uname,
            'client': 'xyz',
            'start': 'YYYY-MM-DD',
            'end': 'YYYY-MM-DD',
            'template': 'abc'
        }
        with open('questionnaire.yml','w') as f:
            yaml.dump(payload, f, default_flow_style=False)
        return True


    def clone(self,id, workspace_id, name):
        """Clone a typeform questionnaire

        Keyword arguments:
        param: id -- the id of the template to clone, see tform templates
        param: workspace_id -- the workspace to clone to, see tform workspaces
        param: name -- the name of the new questionnaire, should be of format year_month_day_client
        """
        # check the name matches convention
        token = read_user_config()
        headers = create_header(token)
        id = str(id)
        workspace_id = str(workspace_id)
        # clone old typeform
        url = self._base_url + '/' + id
        r = requests.get(url=url, headers = headers)
        questionnaire_dict = r.json()
        # create new copy with dropped ids
        new_dict = dict_drop_keys('id', questionnaire_dict)
        # update other properties that typeform docs don't mention
        new_dict.pop('_links',None)
        new_dict['title'] = name
        new_dict['workspace']['href'] = 'https://api.typeform.com/workspaces/' + workspace_id
        # upload to typeform
        r = requests.post(self._base_url, headers=headers, data=json.dumps(new_dict))
        new_link = r.json()['_links']['display']
        return new_link


    # def update_config(self, link):
    #     """ Update a config.yml file with the link to typeform questionnaire
    #
    #     Keyword arguments:
    #     param: link -- the link which will be entered into the config file
    #     """
    #     file = Path("./config.yml")
    #     if not file.exists():
    #         raise FileNotFoundError('config.yml does not exist in this directory')
    #     lines = file.read_text().splitlines()
    #     # check if questionnaire is in any of the lines
    #     ix = [i for i, x in enumerate(lines) if 'questionnaire' in x]
    #     if len(ix) == 0:
    #         lines.append('  questionnaire: "' + link + '"')
    #     elif len(ix) > 1:
    #         raise ValueError('%d occurences of "questionnaire in config", should only be 1.' % (len(ix)))
    #     else:
    #         lines[ix[0]] = '  questionnaire: "' + link + '"'
    #     # append blank line to stop R config warnings
    #     lines.append('')
    #     text = '\n'.join(lines)
    #     # dump back to file
    #     file.write_text(text)
    #     print('Updated config.yml')
    #     return None



def main():
    fire.Fire(TypeformCLI)

if __name__ == '__main__':
    main()
