import sublime, sublime_plugin
import urllib
import json
import subprocess
import os

class Constants:
	name_prefix = '*github-issues*: '
	settings_file = "GithubIssues.sublime-settings"
	help_text = """

# Usage:

	e - edit issue
	v - view issue details
	c - comment issue
	x - close issue
"""
	error_message = """

Sorry! We could not get github settings. 
Please make sure your settings are correct and you are running the command from a git local repository. 

If nothing helps please take your time and submit a ticket here: 

"""


class GithubListIssuesCommand(sublime_plugin.TextCommand):
	username = None
	repository = None
	token = None
	error = ""

	def run(self, edit):
		try:
			# Create / switch to the issues view and initialize
			view = self.activate_view()
			view.erase(edit, sublime.Region(0, view.size()))

			# Load the data
			if self.username and self.repository:
				view.insert(edit, 0, Constants.help_text)
				data_json = self.fetch_issues()
				for ticket in data_json:
					view.insert(edit, 0, str(ticket["number"]) + " - " + ticket["title"] + '\n')
			else:
				view.insert(edit, 0, Constants.error_message)

			# Jump to the begin of the document
			view.show(0)
			sel = view.sel()
			sel.clear()
			sel.add(sublime.Region(0, 0))
		except (IndexError):
			pass

	def fetch_issues(self):
		request = urllib.request.Request('https://api.github.com/repos/' + self.username + '/' + self.repository + '/issues?state=open&per_page=100')
		token = self.token
		if token:
			request.add_header('Authorization', 'token ' + self.token)
		response = urllib.request.urlopen(request)
		str_response = response.readall().decode('utf-8')
		data_json = json.loads(str_response)
		return data_json

	def read_github_info(self, file_name):
		try:
			os.chdir(os.path.dirname(file_name))
			p = subprocess.Popen(["git", "remote", "-v"], stdout=subprocess.PIPE)
			out, err = p.communicate()
			remotes = out.decode('utf-8').split('\n')
			url = remotes[0].split('\t')[1].split(" ")[0]
			path = urllib.parse.urlparse(url)[2].split('/')
			self.username = path[1]
			if path[2].endswith('.git'):
				self.repository = path[2][:-4]
		except (IndexError):
			pass


	def activate_view(self):
		try:
			settings = sublime.load_settings(Constants.settings_file)
			self.username = settings.get('username', None)
			self.repository = settings.get('repository', None)
			self.token = settings.get('token', None)
			if not self.username or not self.repository:
				self.read_github_info(sublime.active_window().active_view().file_name())
		except (IndexError):
			print("ooops something happened")

		window_name = Constants.name_prefix
		if self.repository:
			window_name += self.repository

		open_views = sublime.active_window().views()
		issues_view = None
		for view in open_views:
			if view.name() == window_name:
				issues_view = view
				sublime.active_window().focus_view(issues_view)
				break
		if not issues_view:
			issues_view = sublime.active_window().new_file()
			issues_view.set_name(window_name)
			issues_view.set_scratch(True)
		return issues_view
