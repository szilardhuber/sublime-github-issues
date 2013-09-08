import sublime, sublime_plugin
import urllib
import json

class GithubListIssuesCommand(sublime_plugin.TextCommand):
	settings = None
	name_prefix = '*github-issues*: '
	window_name = ''
	settings_file = "GithubIssues.sublime-settings"
	help_text = """

# Usage:

	e - edit issue
	v - view issue details
	c - comment issue
	x - close issue
"""

	def run(self, edit):
		self.settings = sublime.load_settings(self.settings_file)
		self.window_name = self.name_prefix + self.settings.get('repository', '')

		view = self.activate_view()
		view.erase(edit, sublime.Region(0, view.size()))
		self.add_usage_help(view, edit)

		data_json = GithubListIssuesCommand.fetch_issues(self.settings)
		for ticket in data_json:
			view.insert(edit, 0, str(ticket["number"]) + " - " + ticket["title"] + '\n')

		# Jump to begin
		view.show(0)
		sel = view.sel()
		sel.clear()
		sel.add(sublime.Region(0, 0))

	@staticmethod
	def fetch_issues(settings):
		request = urllib.request.Request('https://api.github.com/repos/' + settings.get('username', '') + '/' + settings.get('repository', '') + '/issues?state=open&per_page=100')
		request.add_header('Authorization', 'token ' + settings.get('token', ''))
		response = urllib.request.urlopen(request)
		str_response = response.readall().decode('utf-8')
		data_json = json.loads(str_response)
		return data_json

	def activate_view(self):
		open_views = sublime.active_window().views()
		issues_view = None
		for view in open_views:
			if view.name() == self.window_name:
				issues_view = view
				sublime.active_window().focus_view(issues_view)
				break
		if not issues_view:
			issues_view = sublime.active_window().new_file()
			issues_view.set_name(self.window_name)
			issues_view.set_scratch(True)
		return issues_view

	def add_usage_help(self, view, edit):
		view.insert(edit, 0, self.help_text)
